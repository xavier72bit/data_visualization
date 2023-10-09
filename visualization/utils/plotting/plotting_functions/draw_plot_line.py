import matplotlib as mpl
from loguru import logger
import matplotlib.pyplot as plt

# -----------------------------------------------------
# 定义字体
# -----------------------------------------------------

font_rc = {
    'family': 'SimSun',
    'size': '12'
}

plt.rc('font', **font_rc)


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
    """
    # 先分析其他绘图选项
    try:
        is_xa_time = kwargs['is_xa_time']
    except KeyError:
        is_xa_time = False

    # 绘图
    try:
        ax.plot(data_list_x, data_list_y)

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


def draw_multi_line(ax: plt.Axes, data_list_x: list, data_dict_y: dict, **kwargs) -> bool:
    """
    绘制多条折线图

    :param ax: 绘图坐标系
    :param data_list_x: x轴数据列表
    :param data_dict_y: 多个y轴数据列表组成的字典
    :param kwargs: 其他绘图选项(关键字参数)
    :return: 绘图操作是否成功

    其他的绘图选项：
        1. is_xa_time: bool: 横轴是否为datetime类型
    """
    # 先分析其他绘图选项
    try:
        is_xa_time = kwargs['is_xa_time']
    except KeyError:
        is_xa_time = False

    try:
        # 依次绘制折线
        for catalog in data_dict_y.keys():
            ax.plot(data_list_x, data_dict_y[catalog], label=catalog)

        # 判断横轴是不是datetime类型
        if is_xa_time:
            # 使用针对Date类型优化的特殊Formatter
            cdf = mpl.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
            ax.xaxis.set_major_formatter(cdf)

        # 设置图例
        ax.legend(loc='upper left', ncols=3)

    except Exception as plot_err:
        logger.error("draw_multi_line绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
