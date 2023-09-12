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

def draw_bar(ax: plt.Axes,
             data_list_x: list,
             data_list_y: list,
             plot_title: str,
             is_xa_time: bool) -> bool:
    """
    绘制条形图

    `plotting_engine.plot_index_dict[3]`
    """
    try:
        ax.set_title(plot_title)
        ax.barh(data_list_x, data_list_y)

        # 判断横轴是不是datetime类型
        if is_xa_time:
            # 使用针对Date类型优化的特殊Formatter
            cdf = mpl.dates.ConciseDateFormatter(ax.xaxis.get_major_locator())
            ax.xaxis.set_major_formatter(cdf)
    except Exception as plot_err:
        logger.error("draw_bar绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
