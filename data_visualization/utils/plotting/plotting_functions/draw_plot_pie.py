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

def draw_pie(ax,
             data_list_x: list,
             data_list_y: list,
             plot_title: str) -> bool:
    """
    绘制饼状图

    `plotting_engine.plot_index_dict[4]`
    """
    try:
        ax.pie(data_list_y, labels=data_list_x)
        ax.set_title(plot_title)
    except Exception as plot_err:
        logger.error("draw_pie绘图失败，错误原因：{0}".format(plot_err))
        return False
    else:
        return True
