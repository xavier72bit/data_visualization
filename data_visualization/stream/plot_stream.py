import typing
from loguru import logger

from data_visualization.service import plot_result_service
from data_visualization.utils.do.data_object import PlotResult
from project_common import DATE_TIME_NOW, MINIO_SERVER_ADDRESS
from data_visualization.utils.storage.minio_util import MinioUtil
from data_visualization.utils.plotting import plotting_util, draw_plot_line, draw_plot_column


def plot_time_num(access_log_id: str,
                  time_data_list: typing.List,
                  num_data_list: typing.List,
                  plot_title: str) -> PlotResult | None:
    """
    绘制 时间-数字 类型的图表

    :return: PlotResult | None
    """
    # 1. 创建plot_result
    plot_result = plot_result_service.create(PlotResult(access_log_id=access_log_id))

    if plot_result is None:
        return None

    # 2. 绘图步骤
    # 第一步，判断传入的两个列表长度是否一致
    if len(time_data_list) != len(num_data_list):
        plot_result.plot_result_state = 1

        # 第一步判断失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

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
        logger.error("绘图失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 2

        # 第二步执行失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

        return plot_result.plot_result_id
    else:
        logger.info("绘图成功，fig对象: {0}".format(fig))

    # 第三步，存储图表
    try:
        plot_picture_path = plotting_util.plot_storage(fig, plot_result.plot_result_id)
    except Exception as err:
        logger.error("图片保存失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 3

        # 第三步执行失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

        return plot_result
    else:
        logger.info("图片保存成功")
        plot_result.plot_result_finish_date_time = DATE_TIME_NOW
        plot_result.plot_result_local_path = plot_picture_path

    # 第四步，上传图表
    minio_util = MinioUtil()
    plot_remote_url = minio_util.upload_file(plot_picture_path)
    if plot_remote_url:
        logger.info("图片上传成功，remote url: {0}".format(plot_remote_url))
        plot_result.plot_result_upload_date_time = DATE_TIME_NOW
        plot_result.plot_result_url = MINIO_SERVER_ADDRESS + plot_remote_url
    else:
        logger.error("图片上传失败")
        plot_result.plot_result_state = 4

        # 第四步失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

        return plot_result

    # 最后，全部步骤执行通过，更新记录，返回plot_result
    plot_result.plot_result_state = 0
    plot_result_service.update(plot_result)

    return plot_result


def plot_catalog_time_num(access_log_id: str,
                          time_data_list: typing.List,
                          catalog_num_data_dict: dict,
                          plot_title: str) -> PlotResult | None:
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

    :return: plot_result | None
    """
    # 1. 创建plot_result
    plot_result = plot_result_service.create(PlotResult(access_log_id=access_log_id))

    if plot_result is None:
        return None

    # 2. 绘图步骤
    # 第一步，循环判断每个catalog对应的num_data_list
    for catalog in catalog_num_data_dict.keys():
        if len(time_data_list) != len(catalog_num_data_dict[catalog]):
            plot_result.plot_result_state = 1

            # 第一步判断失败，更新记录，返回plot_result
            plot_result_service.update(plot_result)

            return plot_result

    # 第二步，根据catalog_num的数量，选择图表，调用相应函数绘图
    try:
        if len(catalog_num_data_dict) <= 3:
            fig = draw_plot_column.draw_time_catalog_num_column(time_data_list, catalog_num_data_dict, plot_title)
            plot_result.plot_result_type = 'column'
        else:
            fig = draw_plot_line.draw_time_catalog_num_line(time_data_list, catalog_num_data_dict, plot_title)
            plot_result.plot_result_type = 'line'
    except Exception as err:
        logger.error("绘图失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 2

        # 第二步执行失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

        return plot_result
    else:
        logger.info("绘图成功，fig对象: {0}".format(fig))

    # 第三步，存储图表
    try:
        plot_picture_path = plotting_util.plot_storage(fig, plot_result.plot_result_id)
    except Exception as err:
        logger.error("图片保存失败，错误原因: {0}".format(err))
        plot_result.plot_result_state = 3

        # 第三步执行失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

        return plot_result
    else:
        logger.info("图片保存成功")
        plot_result.plot_result_finish_date_time = DATE_TIME_NOW
        plot_result.plot_result_local_path = plot_picture_path

    # 第四步，上传图表
    minio_util = MinioUtil()
    plot_remote_url = minio_util.upload_file(plot_picture_path)
    if plot_remote_url:
        logger.info("图片上传成功，remote url: {0}".format(plot_remote_url))
        plot_result.plot_result_upload_date_time = DATE_TIME_NOW
        plot_result.plot_result_url = MINIO_SERVER_ADDRESS + plot_remote_url
    else:
        logger.error("图片上传失败")
        plot_result.plot_result_state = 4

        # 第四步失败，更新记录，返回plot_result
        plot_result_service.update(plot_result)

        return plot_result

    # 最后，全部步骤执行通过，更新记录，返回plot_result
    plot_result.plot_result_state = 0
    plot_result_service.update(plot_result)

    return plot_result
