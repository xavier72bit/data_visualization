from loguru import logger
import matplotlib.pyplot as plt


# -----------------------------------------------------
# 绘图功能函数
# -----------------------------------------------------


def draw_pie(ax: plt.Axes, data_list_x: list, data_list_y: list, **kwargs) -> bool:
    """
    绘制饼状图

    :param ax: 绘图坐标系
    :param data_list_x: 种类数据列表
    :param data_list_y: 数字数据列表
    :param kwargs: 其他绘图选项(关键字参数)
    :return: 绘图操作是否成功

    其他的绘图选项：
        暂无
    """
    # 绘图过程
    try:
        # 绘图
        ax.pie(data_list_y, labels=data_list_x)
    except Exception as plot_err:
        logger.error("draw_pie绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
