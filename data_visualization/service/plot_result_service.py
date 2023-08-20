import uuid
from project_common import DATE_TIME_NOW, FDFS_SERVER_ADDRESS
from data_visualization.utils import fdfs_util, minio_util, logging_util

from data_visualization.domain.plot_result import PlotResult
from data_visualization.dao.plot_result_dao import PlotResultDao

from data_visualization.plotting import plot_storage
from data_visualization.plotting import draw_plot_line, draw_plot_radar, draw_plot_column, draw_plot_bar, draw_plot_pie

"""
plot_result_finish_state 绘图结果状态：

=========== =============================
 状态码        意义
----------- -----------------------------
    '0'       '绘图成功'
    '1'       '数据序列长度不一致'
    '2'       '绘图失败'
    '3'       '图片保存失败'
    '4'       '图片上传失败'
=========== =============================
"""

# -----------------------------------------------------
# 初始化模块日志
# -----------------------------------------------------

plot_result_service_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))


# -----------------------------------------------------
# 功能函数
# -----------------------------------------------------


def create_a_new_plot_result(access_log_id):
    """
    创建一个新的plot_result，返回plot_result_id
    """
    plot_result = PlotResult(plot_result_id=str(uuid.uuid4()),
                             access_log_id=access_log_id)

    with PlotResultDao() as prd:
        prd.insert_one_exc(plot_result)

    return plot_result.plot_result_id


def read_url_by_id(plot_result_id):
    """
    根据plot_result_id读取plot_result_url
    """
    plot_result = PlotResult(plot_result_id=plot_result_id)

    with PlotResultDao() as prd:
        plot_result = prd.select_one_exc_by_pk(plot_result)

    return plot_result.plot_result_url


def read_state_by_id(plot_result_id):
    """
    根据plot_result_id读取plot_result_state
    """
    plot_result = PlotResult(plot_result_id=plot_result_id)

    with PlotResultDao() as prd:
        plot_result = prd.select_one_exc_by_pk(plot_result)

    return plot_result.plot_result_state


def plot_time_num(plot_result_id, time_data_list, num_data_list, plot_title):
    """
    绘制 时间-数字 类型的图表
    """
    # 根据传入的plot_result_id，从数据库中查询这条plot_result记录
    with PlotResultDao() as prd:
        plot_result = prd.select_one_exc_by_pk(PlotResult(plot_result_id=plot_result_id))

    # 第一步，判断传入的两个列表长度是否一致
    if len(time_data_list) != len(num_data_list):
        plot_result.plot_result_state = 1

        # 第一步判断失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id

    # 第二步，根据time_data_list长度，选择图表，调用相应函数绘图
    try:
        if len(time_data_list) <= 7:
            fig = draw_plot_column.draw_time_num_column(time_data_list, num_data_list, plot_title)
            plot_result.plot_result_type = 'column'
        else:
            fig = draw_plot_line.draw_time_num_line(time_data_list, num_data_list, plot_title)
            plot_result.plot_result_type = 'line'
    except Exception as err:
        plot_result_service_logger.error("绘图失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 2

        # 第二步执行失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id
    else:
        plot_result_service_logger.info("绘图成功，fig对象: {0}".format(fig))

    # 第三步，存储图表
    try:
        plot_picture_path = plot_storage(fig, plot_result_id)
    except Exception as err:
        plot_result_service_logger.error("图片保存失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 3

        # 第三步执行失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id
    else:
        plot_result_service_logger.info("图片保存成功")
        plot_result.plot_result_finish_date_time = DATE_TIME_NOW
        plot_result.plot_result_local_path = plot_picture_path

    # 第四步，上传图表
    plot_remote_id = fdfs_util.upload_file(plot_picture_path)
    if plot_remote_id:
        plot_result_service_logger.info("图片上传成功，remote id: {0}".format(plot_remote_id))
        plot_result.plot_result_upload_date_time = DATE_TIME_NOW
        plot_result.plot_result_url = FDFS_SERVER_ADDRESS + plot_remote_id
    else:
        plot_result_service_logger.error("图片上传失败")
        plot_result.plot_result_state = 4

        # 第四步失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id

    # 最后，全部步骤执行通过，更新记录，返回plot_result_id
    plot_result.plot_result_state = 0
    with PlotResultDao() as prd:
        prd.update_one_exc(plot_result)

    return plot_result.plot_result_id


def plot_catalog_time_num(plot_result_id, time_data_list, catalog_num_data_dict, plot_title):
    """
    绘制 类别-时间-数字 类型的图表

    `time_data_list`:
    [time1, time2, time3, time4]
    `catalog_num_data_dict`:
    {
        catalog1: [num1, num2, num3, num4],
        catalog2: [num1, num2, num3, num4],
        catalog3: [num1, num2, num3, num4]
    }
    """
    # 根据传入的plot_result_id，从数据库中查询这条plot_result记录
    with PlotResultDao() as prd:
        plot_result = prd.select_one_exc_by_pk(PlotResult(plot_result_id=plot_result_id))

    # 第一步，循环判断每个catalog对应的num_data_list
    for catalog in catalog_num_data_dict.keys():
        if len(time_data_list) != len(catalog_num_data_dict[catalog]):
            plot_result.plot_result_state = 1

            # 第一步判断失败，更新记录，返回plot_result_id
            with PlotResultDao() as prd:
                prd.update_one_exc(plot_result)

            return plot_result.plot_result_id

    # 第二步，根据catalog_num的数量，选择图表，调用相应函数绘图
    try:
        if len(catalog_num_data_dict) <= 3:
            fig = draw_plot_column.draw_time_catalog_num_column(time_data_list, catalog_num_data_dict, plot_title)
            plot_result.plot_result_type = 'column'
        else:
            fig = draw_plot_line.draw_time_catalog_num_line(time_data_list, catalog_num_data_dict, plot_title)
            plot_result.plot_result_type = 'line'
    except Exception as err:
        plot_result_service_logger.error("绘图失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 2

        # 第二步执行失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id
    else:
        plot_result_service_logger.info("绘图成功，fig对象: {0}".format(fig))

    # 第三步，存储图表
    try:
        plot_picture_path = plot_storage(fig, plot_result_id)
    except Exception as err:
        plot_result_service_logger.error("图片保存失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 3

        # 第三步执行失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id
    else:
        plot_result_service_logger.info("图片保存成功")
        plot_result.plot_result_finish_date_time = DATE_TIME_NOW
        plot_result.plot_result_local_path = plot_picture_path

    # 第四步，上传图表
    plot_remote_id = fdfs_util.upload_file(plot_picture_path)
    if plot_remote_id:
        plot_result_service_logger.info("图片上传成功，remote id: {0}".format(plot_remote_id))
        plot_result.plot_result_upload_date_time = DATE_TIME_NOW
        plot_result.plot_result_url = FDFS_SERVER_ADDRESS + plot_remote_id
    else:
        plot_result_service_logger.error("图片上传失败")
        plot_result.plot_result_state = 4

        # 第四步失败，更新记录，返回plot_result_id
        with PlotResultDao() as prd:
            prd.update_one_exc(plot_result)

        return plot_result.plot_result_id

    # 最后，全部步骤执行通过，更新记录，返回plot_result_id
    plot_result.plot_result_state = 0
    with PlotResultDao() as prd:
        prd.update_one_exc(plot_result)

    return plot_result.plot_result_id
