import matplotlib as mpl
from loguru import logger
import matplotlib.pyplot as plt


# -----------------------------------------------------
# 绘图功能函数
# -----------------------------------------------------


def draw_one_line(ax: plt.Axes, data_list_x: list, data_list_y: list, **kwargs) -> bool:
    """
    绘制折线图

    :param ax: 绘图坐标系
    :param data_list_x: x轴数据列表
    :param data_list_y: y轴数据列表
    :param kwargs: 其他绘图选项(关键字参数)
    :return: 绘图操作是否成功

    其他的绘图选项：
        1. is_xa_time: bool: 横轴是否为datetime类型
        2. label: str | None: 图例标题
        3. color: str | None: 线条颜色
    """
    # 分析is_xa_time绘图选项
    try:
        is_xa_time = kwargs['is_xa_time']
    except KeyError:
        is_xa_time = False

    # 分析label绘图选项
    try:
        label = kwargs['label']
    except KeyError:
        label = None

    # 分析color绘图选项
    try:
        line_color = kwargs['color']
    except KeyError:
        line_color = None

    # 绘图过程
    try:
        # 绘图
        ax.plot(data_list_x, data_list_y, marker='.', label=label, color=line_color)

        # 加图例
        ax.legend(loc='upper left')

        # 加标签
        for (x, y) in zip(data_list_x,  data_list_y):
            ax.text(x, y, y)

        # 判断横轴是不是datetime类型
        if is_xa_time:
            # 使用针对Date类型优化的特殊Formatter
            cdf = mpl.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
            ax.xaxis.set_major_formatter(cdf)
    except Exception as plot_err:
        logger.error("draw_one_line绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
