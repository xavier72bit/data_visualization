import numpy as np
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

def draw_one_column(ax,
                    data_list_x: list,
                    data_list_y: list,
                    plot_title: str,
                    is_xa_time: bool) -> bool:
    """
    绘制柱状图

    `plotting_engine.plot_index_dict[2]`
    """
    # 设置每个“柱”的宽度
    width = 0.3
    try:
        ax.set_title(plot_title)
        ax.bar(data_list_x, data_list_y, width)

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


def draw_multi_column(ax,
                      data_list_x: list,
                      data_dict_y: dict,
                      plot_title: str,
                      is_xa_time: bool) -> bool:
    """
    绘制并列柱状图

    `plotting_engine.plot_index_dict[7]`
    """
    # 设定x轴
    x_aix = np.arange(len(data_list_x))
    # 每个“柱”的宽度
    width = 0.2
    multiplier = 0

    try:
        # 绘制并列柱状图
        for catalog, num in data_dict_y.items():
            # 绘制偏移量
            offset = width * multiplier
            # 绘制数据
            rects = ax.bar(x_aix + offset, num, width, label=catalog)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        # 设置绘图标题
        ax.set_title(plot_title)

        # 设置横坐标刻度值
        ax.set_xticks(x_aix + width, data_list_x)

        # 设置图例
        ax.legend(loc='upper left', ncols=len(data_dict_y.keys()))

        # 判断横轴是不是datetime类型
        if is_xa_time:
            # 使用针对Date类型优化的特殊Formatter
            cdf = mpl.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
            ax.xaxis.set_major_formatter(cdf)
    except Exception as plot_err:
        logger.error("draw_multi_column绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
