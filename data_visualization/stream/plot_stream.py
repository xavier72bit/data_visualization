from loguru import logger

from project_common import PLOT_INDEX_TYPE_DICT
from data_visualization.utils.plotting import plotting_engine
from data_visualization.utils.do.data_object import AccessLog, PlotResult
from data_visualization.service import access_log_service, plot_result_service


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
        return access_log

    # 判断两个数据源的长度是否一致，不一致则无法绘图
    if plot_data_source_1_object.data_source_length != plot_data_source_2_object.data_source_length:
        logger.error("两个数据源长度不一致，无法绘图")
        access_log.access_plot_flag = 2
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
