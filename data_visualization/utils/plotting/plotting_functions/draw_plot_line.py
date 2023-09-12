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

def draw_one_line(ax,
                  data_list_x: list,
                  data_list_y: list,
                  plot_title: str,
                  is_xa_time: bool) -> bool:
    """
    绘制折线图

    `plotting_engine.plot_index_dict[1]`
    """
    try:
        ax.set_title(plot_title)
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


def draw_multi_line(ax,
                    data_list_x: list,
                    data_dict_y: dict,
                    plot_title: str,
                    is_xa_time: bool) -> bool:
    """
    绘制多条折线图

    `plotting_engine.plot_index_dict[6]`
    """
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

        # 设置标题
        ax.set_title(plot_title)
    except Exception as plot_err:
        logger.error("draw_multi_line绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
