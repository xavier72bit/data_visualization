import numpy as np
import matplotlib as mpl
from loguru import logger
import matplotlib.pyplot as plt


# -----------------------------------------------------
# 绘图功能函数
# -----------------------------------------------------


def draw_one_column(ax: plt.Axes, data_list_x: list, data_list_y: list, **kwargs) -> bool:
    """
    绘制柱状图

    :param ax: 绘图坐标系
    :param data_list_x: x轴数据列表
    :param data_list_y: y轴数据列表
    :param kwargs: 其他绘图选项(关键字参数)
    :return: 绘图操作是否成功

    其他的绘图选项：
        1. is_xa_time: bool: 横轴是否为datetime类型
        2. color: str | None: 柱的颜色
    """
    # 分析is_xa_time绘图选项
    try:
        is_xa_time = kwargs['is_xa_time']
    except KeyError:
        is_xa_time = False

    # 分析color绘图选项
    try:
        column_color = kwargs['color']
    except KeyError:
        column_color = None

    # 设置每个“柱”的宽度
    width = 0.3

    # 绘图过程
    try:
        # 绘图
        bar_container = ax.bar(data_list_x, data_list_y, width, color=column_color)

        # 加数据标注
        ax.bar_label(bar_container, labels=data_list_y, padding=3)

        # 判断横轴是不是datetime类型
        if is_xa_time:
            # 使用针对Date类型优化的特殊Formatter
            cdf = mpl.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
            ax.xaxis.set_major_formatter(cdf)
    except Exception as plot_err:
        logger.error("draw_one_column绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True


def draw_multi_column(ax: plt.Axes, data_list_x: list, data_dict_y: dict, **kwargs) -> bool:
    """
    绘制并列柱状图

    :param ax: 绘图坐标系
    :param data_list_x: x轴数据列表
    :param data_dict_y: 多个y轴数据列表组成的字典
    :param kwargs: 其他绘图选项(关键字参数)
    :return: 绘图操作是否成功

    其他的绘图选项：
        暂无
    """
    # 设定x轴
    x_aix = np.arange(len(data_list_x))

    # 每个“柱”的宽度
    width = 0.2
    # 绘制偏移量参数
    multiplier = -0.5 * (len(data_dict_y) - 1)

    # 绘图过程
    try:
        # 绘制并列柱状图
        for catalog, num in data_dict_y.items():
            # 绘制偏移量
            offset = width * multiplier
            # 绘制数据
            rects = ax.bar(x_aix + offset, num, width, label=catalog)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # 设置横坐标刻度值
        ax.set_xticks(x_aix, data_list_x)

        # 设置图例
        ax.legend(loc='upper left', ncols=len(data_dict_y.keys()))

    except Exception as plot_err:
        logger.error("draw_multi_column绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
