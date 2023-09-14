import json
from loguru import logger

from data_visualization.utils.plotting import plotting_engine
from project_common import PLOT_INDEX_TYPE_DICT, DATE_TIME_NOW
from data_visualization.utils.storage.minio_util import MinioUtil
from data_visualization.utils.do.data_object import AccessLog, PlotResult
from data_visualization.service import access_log_service, plot_result_service


# -----------------------------------------------------
# 本模块内部使用的工具函数
# -----------------------------------------------------


def _convert_plotting_type_list_2_str(plotting_type_list: list) -> str:
    """
    ['1', '2', '3', '4', '5'] -> '1:折线图,2:柱状图,3:条形图,4:饼状图,5:雷达图'
    """
    convert_string_list = ['{0}:{1}'.format(item, PLOT_INDEX_TYPE_DICT[item]) for item in plotting_type_list]
    return ','.join(convert_string_list)


def _convert_plotting_type_str_2_list(plotting_type_str: str) -> list:
    """
    '1:折线图,2:柱状图,3:条形图,4:饼状图,5:雷达图' -> ['1', '2', '3', '4', '5']
    """
    return [item.split(':')[0] for item in plotting_type_str.split(',')]


# -----------------------------------------------------
# 业务函数
# -----------------------------------------------------


def check_plot_type(access_log: AccessLog,
                    data_source_1: list | dict,
                    data_source_2: list | dict) -> AccessLog:
    """
    分析两个数据源可以绘制哪些图表
    """

    # 生成两个数据源对象
    plot_data_source_1_object = plotting_engine.PlotDataSource(data_source_1)
    plot_data_source_2_object = plotting_engine.PlotDataSource(data_source_2)

    # 判断数据源是否有效
    if not plot_data_source_1_object.is_data_valid or not plot_data_source_2_object.is_data_valid:
        logger.error("数据源结构无效，无法绘图")
        access_log.access_plot_flag = 1
        access_log_service.update(access_log)
        return access_log

    # 判断两个数据源的长度是否一致，不一致则无法绘图
    if plot_data_source_1_object.data_source_length != plot_data_source_2_object.data_source_length:
        logger.error("两个数据源长度不一致，无法绘图")
        access_log.access_plot_flag = 2
        access_log_service.update(access_log)
        return access_log

    # 分析两个数据源的类型
    two_data_source_type_set = {plot_data_source_1_object.data_source_type, plot_data_source_2_object.data_source_type}
    # 分析两个数据源的数据类型
    two_data_type_set = {plot_data_source_1_object.data_type, plot_data_source_2_object.data_type}

    # 以下是 判断数据源类型 的逻辑
    if two_data_source_type_set == {'list'}:  # 当数据源是两个列表
        # 判断数据类型
        if two_data_type_set == {'datetime', 'number'}:  # 时间-数字类型
            access_log.access_plot_flag = 0
            access_log.access_plot_type = _convert_plotting_type_list_2_str(['1', '2'])
            access_log_service.update(access_log)
            return access_log
        elif two_data_type_set == {'catalog', 'number'}:  # 类别-数字类型
            access_log.access_plot_flag = 0
            access_log.access_plot_type = _convert_plotting_type_list_2_str(['1', '2', '3', '4', '5'])
            access_log_service.update(access_log)
            return access_log
        else:  # 其他类型
            logger.error("{0}类型数据无法绘图".format(two_data_type_set))
            access_log.access_plot_flag = 3
            access_log_service.update(access_log)
            return access_log
    elif two_data_source_type_set == {'list', 'dict'}:  # 当数据源是一个列表一个字典
        dict_data_source = data_source_1 if plot_data_source_1_object.data_source_type == 'dict' else plot_data_source_2_object

        # 判断字典数据源的长度
        if dict_data_source.dict_data_source_key_length <= 3:  # 字典数据源长度小于3
            access_log.access_plot_flag = 0
            access_log.access_plot_type = _convert_plotting_type_list_2_str(['7'])
            access_log_service.update(access_log)
            return access_log
        else:  # 字典数据源长度大于3
            access_log.access_plot_flag = 0
            access_log.access_plot_type = _convert_plotting_type_list_2_str(['6'])
            access_log_service.update(access_log)
            return access_log
    else:  # 其他数据源
        logger.error("{0}类型数据源无法绘图".format(two_data_source_type_set))
        access_log.access_plot_flag = 1
        access_log_service.update(access_log)
        return access_log


def data_source_plot_upload_picture(access_log: AccessLog, plotting_require_list: list) -> PlotResult | None:
    """
    根据绘图要求列表进行绘图，并将绘图结果上传
    """
    # 检验access_log是否存在
    read_access_log = access_log_service.read_one(access_log)

    if read_access_log is None:
        logger.error("access_log不存在")
        return None

    # 新建绘图结果
    plot_result = plot_result_service.create(PlotResult(access_log_id=access_log.access_log_id))

    if plot_result is None:
        logger.error("新建plot_result失败")
        return None

    # 校验绘图需求
    if not plotting_require_list:
        logger.error("plot_require_list为空")
        return None
    elif not (set(plotting_require_list) <= set(_convert_plotting_type_str_2_list(access_log.access_plot_type))):
        logger.error("绘图要求：{0}无法满足".format(plotting_require_list))
        return None
    else:
        # 绘图需求能满足，记录绘图需求
        plot_result.plot_result_type = _convert_plotting_type_list_2_str(plotting_require_list)

    # 获取绘图数据
    access_param_dict = json.loads(access_log.access_param)

    # 执行绘图
    plotting_engine_exec_result = plotting_engine.plotting_picture(access_param_dict['data_source_1'],
                                                                   access_param_dict['data_source_2'],
                                                                   plotting_require_list,
                                                                   plot_result.plot_result_id)

    if type(plotting_engine_exec_result) is int:  # 执行结果为整数，说明是错误码
        plot_result.plot_result_state = plotting_engine_exec_result
        plot_result_service.update(plot_result)
        return plot_result
    else:  # 执行结果为字符串，说明绘图成功，返回的是图片本地路径
        plot_result.plot_result_state = 0
        plot_result.plot_result_finish_date_time = DATE_TIME_NOW
        plot_result.plot_result_local_path = plotting_engine_exec_result
        plot_result_service.update(plot_result)

    # 绘图结果上传
    picture_upload_minio_util = MinioUtil()
    picture_upload_result = picture_upload_minio_util.upload_file(plotting_engine_exec_result)

    if picture_upload_result is None:  # 上传失败
        plot_result.plot_result_state = 3
        plot_result_service.update(plot_result)
        return plot_result
    else:
        plot_result.plot_result_upload_date_time = DATE_TIME_NOW
        plot_result.plot_result_url = picture_upload_result
        plot_result_service.update(plot_result)
        return plot_result
