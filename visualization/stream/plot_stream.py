import json
import itertools
from loguru import logger

from visualization.utils.plotting import plotting_engine
from visualization.utils.storage.minio_util import MinioUtil
from visualization.utils.do.data_object import PlotTask, PlotResult
from project_common import DATE_TIME_NOW, CONST_PLOT_RESULT_STATE_DICT
from visualization.service import plot_task_service, plot_result_service

# -----------------------------------------------------
# 初始化minio_util
# -----------------------------------------------------

minio_util = MinioUtil()

# -----------------------------------------------------
# 本模块内部使用的工具函数
# -----------------------------------------------------


def _convert_plot_task_data_2_data_source_object_name_dict(plot_task_data: dict) -> dict:
    """
    将绘图任务中的绘图数据转换为 “数据源名称(str): 数据源对象(plotting_engine.PlotDataSource)” 的字典
    """
    return {key: plotting_engine.PlotDataSource(**plot_task_data[key]) for key in plot_task_data.keys()}


def _check_the_plot_type(plot_data_source_1_object: plotting_engine.PlotDataSource,
                         plot_data_source_2_object: plotting_engine.PlotDataSource) -> list | None:
    """
    分析两个数据源是否能绘制图表，能绘制哪些图表

    :return: 成功，绘图类型list，失败，None
    """
    # 分析两个数据源的数据类型
    two_data_type_set = {plot_data_source_1_object.data_type, plot_data_source_2_object.data_type}

    # 判断两个数据源长度是否一致
    if plot_data_source_1_object.data_source_length != plot_data_source_2_object.data_source_length:
        logger.error("两个数据源长度不一致")
        return None

    # 判断绘图类型
    if two_data_type_set == {'datetime', 'number'}:  # 时间-数字类型
        return [1, 2]
    elif two_data_type_set == {'catalog', 'number'}:  # 类别-数字类型
        return [1, 2, 3, 4, 5]
    else:  # 其他类型
        logger.error("{0}类型数据无法绘图".format(two_data_type_set))
        return None


def _convert_plot_chart_requirement_str_2_plot_chart(plot_task: PlotTask, plot_requirement_list: list) -> list | None:
    """
    将绘图需求列表转换为PlotChart对象列表

    例：["A1", "B2"] -> [plot_chart(A1), plot_chart(B2)]
    """
    # 读取plot_task中的绘图数据(plot_task_data)
    plot_task_data: dict = json.loads(plot_task.plot_task_data)
    plot_task_data_dict = _convert_plot_task_data_2_data_source_object_name_dict(plot_task_data)
    # 读取plot_task中的绘图支持列表(plot_task_support_type)
    plot_task_support_type = json.loads(plot_task.plot_task_support_type)

    plot_chart_list = list()
    for plot_requirement in plot_requirement_list:
        # 获取图表绘图数据
        two_plot_data_group_name = plot_requirement[0]
        data_source_combination = plot_task_support_type[two_plot_data_group_name]['data_source_combination']
        plot_data_source_object_list = [plot_task_data_dict[key] for key in data_source_combination]

        # 获取图表类型
        plot_type = int(plot_requirement[1])

        # 生成绘图图表类
        plot_chart = plotting_engine.PlotChart(plot_data_source_object_list, plot_type)

        plot_chart_list.append(plot_chart)

    return plot_chart_list


def _check_plot_type_set(plot_type_set: set) -> bool:
    """
    校验图表是否能画到同一个图片中
    """
    if len(plot_type_set) == 1:  # 只有一种绘图类型
        return True
    elif plot_type_set == {1, 2}:  # 柱状图和折线图可以一起绘制
        return True
    else:
        return False


def _check_plot_requirement(plot_task_support_type: dict, plot_requirement: dict) -> bool:
    """
    校验plot_requirement是否有效
    """
    # 获取plot_task中的数据源组合(dsg)-绘图类型(pt)的集合
    all_support_set = set()
    for pt_dsg in plot_task_support_type.keys():
        for pt_pt in plot_task_support_type[pt_dsg]["support_plot_type"]:
            item = "".join([pt_dsg, str(pt_pt)])
            all_support_set.add(item)

    # 获取plot_requirement中所有图片(fn)的数据源组合(dsg)-绘图类型(pt)的集合
    plot_requirement_set = set()
    for fn in plot_requirement.keys():
        for dsg_pt in plot_requirement[fn]["type"]:
            plot_requirement_set.add(dsg_pt)

    return True if plot_requirement_set <= all_support_set else False


def _check_figure_is_plotted(plot_task: PlotTask, plot_figure_info: dict) -> str | None:
    """
    检查图片需求是否已经被绘制过
    # TODO: 为什么画一张图就得查一次数据库？暂时这样操作可以避免在一个请求中重复画两张一样的图

    :return: 存在，返回URL；不存在，返回None
    """
    plot_result = plot_result_service.read_one_by_plot_task_id_and_plot_result_type(
        PlotResult(
            plot_task_id=plot_task.plot_task_id,
            plot_result_type=json.dumps(plot_figure_info["type"])
        )
    )

    if plot_result is None:
        return None
    else:
        if plot_figure_info["plot_title"] == plot_result.plot_result_title:
            return plot_result.plot_result_url
        else:
            return None


# -----------------------------------------------------
# 业务函数
# -----------------------------------------------------


def check_plot_type(plot_task: PlotTask) -> PlotTask:
    """
    分析数据源可以绘制哪些图表
    """
    # 读取绘图任务数据字典
    plot_data = json.loads(plot_task.plot_task_data)

    # 数据源个数校验，必须有两个以上数据源
    if len(plot_data) < 2:
        logger.error("数据源个数小于2，无法绘图")
        plot_task.plot_task_support_flag = 2
        plot_task_service.update(plot_task)
        return plot_task

    # 校验通过后，进行字典转换
    plot_task_data_dict = _convert_plot_task_data_2_data_source_object_name_dict(plot_data)

    # 循环判断所有数据源是否有效
    for key in plot_task_data_dict.keys():
        if not plot_task_data_dict[key].is_data_valid:
            logger.error("{0}数据源无效，无法绘图".format(key))
            plot_task.plot_task_support_flag = 1
            plot_task_service.update(plot_task)
            return plot_task
        else:
            continue

    # 生成plot_task.plot_task_support_type
    plot_task_support_type_dict = dict()
    group_id_ascii_int = 65  # 标记每一种数据源组合，从'A'开始

    # 分析数据源绘图组合
    for two_data_source_combination in itertools.combinations(plot_task_data_dict.keys(), 2):
        logger.info("分析数据源组合:{0}".format(two_data_source_combination))
        two_data_source_object: list = [plot_task_data_dict[key] for key in two_data_source_combination]

        # 按照x-y轴的顺序进行两两排序
        if (two_data_source_object[0].data_type == 'number'
                and two_data_source_object[1].data_type in ('catalog', 'datetime')):
            two_data_source_combination = two_data_source_combination[::-1]
            two_data_source_object.reverse()

        check_result = _check_the_plot_type(*two_data_source_object)

        if type(check_result) is list:
            plot_task_support_type_dict[chr(group_id_ascii_int)] = {
                'support_plot_type': check_result,
                'data_source_combination': two_data_source_combination,
                'comment': "-".join([dso.data_source_comment for dso in two_data_source_object])
            }
            group_id_ascii_int += 1

    # 判断plot_task_support_type_dict
    if plot_task_support_type_dict:  # 非空
        plot_task.plot_task_support_type = json.dumps(plot_task_support_type_dict)
        plot_task.plot_task_support_flag = 0
        plot_task_service.update(plot_task)
        return plot_task
    else:
        logger.error("数据源无法组合绘图")
        plot_task.plot_task_support_flag = 3
        plot_task_service.update(plot_task)
        return plot_task


def plot_and_upload_picture(plot_task: PlotTask, plot_requirement_dict: dict) -> dict | int:
    """
    根据绘图要求列表进行绘图，并将绘图结果上传到MinIO，返回绘图类型与其执行结果
    plot_requirement_dict示例：
    {
        "figure1": {
            "type": ["A1", "B2"],
            "plot_title": "test figure"
        },
        "figure2": {
            "type": ["A1", "B5"],
            "plot_title": "test figure"
        }
    }

    :return: 绘图需求校验通过，绘图类型与其执行结果的字典(示例：{"figure1": URL1, "figure2": None})；绘图需求校验不通过，返回错误码。
    """
    # 先判定plot_requirement_dict是否为空
    if not plot_requirement_dict:
        logger.error("绘图需求为空")
        return 1

    # 检查绘图需求能否被满足
    if not _check_plot_requirement(json.loads(plot_task.plot_task_support_type), plot_requirement_dict):
        logger.error("绘图要求无法被满足")
        return 2

    # 创建结果字典
    result_dict = dict()

    # 循环处理每一张figure图片
    for figure_key in plot_requirement_dict.keys():
        logger.info("当前处理{0}figure".format(figure_key))
        # 获取绘图需求信息
        plot_figure_info_dict: dict = plot_requirement_dict[figure_key]

        # 校验这张图是否被画过，被画过直接向结果字典中添加
        plotted_check_result = _check_figure_is_plotted(plot_task, plot_figure_info_dict)
        if plotted_check_result is not None:
            logger.info("{0}已经被绘制过了".format(figure_key))
            result_dict[figure_key] = plotted_check_result
            continue

        # 获取图片标题
        try:
            plot_title = plot_figure_info_dict["plot_title"]
        except KeyError:
            plot_title = None

        # 新建绘图结果
        plot_result = plot_result_service.create(
            PlotResult(
                plot_task_id=plot_task.plot_task_id,
                plot_result_title=plot_title
            )
        )

        # 获取当前图片的绘图需求，示例：['A1', 'B1']
        plot_requirement_type_list = plot_figure_info_dict["type"]

        # 校验绘图需求是否为空
        if not plot_requirement_type_list:
            plot_result.plot_result_state = 4

        # 将当前图片的绘图需求列表转换为PlotChart类列表
        plot_chart_list = _convert_plot_chart_requirement_str_2_plot_chart(plot_task, plot_requirement_type_list)

        # 获取绘图类型校验数据(cs: check set，校验用的集合)
        xd_cs = {pco.plot_data_source_object_list[0] for pco in plot_chart_list}  # 所有图表数据源组合的X轴数据(x_data)
        pt_cs = {pco.plot_type for pco in plot_chart_list}  # 所有图表的类型(plot_type)
        pdsl_cs = {pco.plot_data_source_length for pco in plot_chart_list}  # 所有图表的数据源长度(plot_data_source_length)

        # 绘图类型校验
        if not _check_plot_type_set(pt_cs):  # 进行图表类型校验
            logger.error("图表类型组合无法绘图")
            plot_result.plot_result_state = 4
        elif len(pdsl_cs) != 1:  # 进行绘图数据长度校验
            logger.error("图表数据长度不一致")
            plot_result.plot_result_state = 5
        elif len(xd_cs) != 1:  # 进行图表组合共享X轴校验
            logger.error("数据源组合没有共享X轴")
            plot_result.plot_result_state = 6
        else:
            plot_result.plot_result_state = 0

        # 获取绘图流程校验数据(ci: check int，校验用的整数)
        ctcc_ci = [pco.plot_type for pco in plot_chart_list].count(2)  # 柱状图类型图表的个数(column_type_chart_count)

        # 绘图流程
        if plot_result.plot_result_state == 0:
            # 生成画布
            plot_figure = plotting_engine.PlotFigure(plot_chart_list[0].is_polar_ax, plot_title)

            # 绘图
            if ctcc_ci >= 2:  # 有两个以上柱状图
                pcof_result = plotting_engine.plot_multi_column_charts_on_figure(plot_figure, plot_chart_list)
            else:
                pcof_result = plotting_engine.plot_charts_on_figure(plot_figure, plot_chart_list)

            if not pcof_result:
                plot_result.plot_result_state = 1

            # 绘图成功后，保存绘图结果
            plot_figure.figure_save(plot_result.plot_result_id)

            if plot_figure.fig_local_path is None:  # 图片保存失败
                plot_result.plot_result_state = 2
            else:
                plot_result.plot_result_state = 0
                plot_result.plot_result_finish_date_time = DATE_TIME_NOW
                plot_result.plot_result_local_path = plot_figure.fig_local_path
                plot_result.plot_result_type = json.dumps(plot_requirement_type_list)

            # 保存成功后，上传图片
            if plot_result.plot_result_state == 0:
                upload_result = minio_util.upload_file(plot_result.plot_result_local_path)

                if upload_result is None:  # 上传失败
                    logger.error("图片{0}上传失败！".format(plot_result.plot_result_id))
                    plot_result.plot_result_state = 3
                else:
                    logger.info("图片{0}上传成功！".format(plot_result.plot_result_id))
                    plot_result.plot_result_upload_date_time = DATE_TIME_NOW
                    plot_result.plot_result_url = upload_result

        # 更新绘图结果
        plot_result_service.update(plot_result)

        # 向操作结果列表添加操作结果
        result_dict[figure_key] = (
            plot_result.plot_result_url  # 图片URL
            if plot_result.plot_result_state == 0
            else CONST_PLOT_RESULT_STATE_DICT[plot_result.plot_result_state]  # 错误原因
        )

    return result_dict
