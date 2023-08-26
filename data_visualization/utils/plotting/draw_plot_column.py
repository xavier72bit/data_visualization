import matplotlib.pyplot as plt
import numpy as np

# -----------------------------------------------------
# 定义字体
# -----------------------------------------------------

font_rc = {'family': 'SimSun',
           'size': '12'}

plt.rc('font', **font_rc)


# -----------------------------------------------------
# 绘图功能函数
# -----------------------------------------------------

def draw_time_num_column(time_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 时间-数字 柱状图
    """
    # 设置每个“柱”的宽度
    width = 0.3

    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.bar(time_data_list, num_data_list, width)

    return fig


def draw_catalog_num_column(catalog_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 类别-数字 柱状图
    """
    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.bar(catalog_data_list, num_data_list)

    return fig


def draw_time_catalog_num_column(time_data_list, catalog_num_dict, plot_title) -> plt.Figure:
    """
    绘制 时间-类别-数字 并列柱状图
    """
    # 设定x轴
    x = np.arange(len(time_data_list))
    # 每个“柱”的宽度
    width = 0.2
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for catalog, num in catalog_num_dict.items():
        # 绘制偏移量
        offset = width * multiplier
        # 绘制数据
        rects = ax.bar(x + offset, num, width, label=catalog)
        ax.bar_label(rects, padding=3)
        multiplier += 1

    # 设置绘图标题
    ax.set_title(plot_title)
    # 设置横坐标刻度值
    ax.set_xticks(x + width, time_data_list)
    # 设置图例
    ax.legend(loc='upper left', ncols=len(catalog_num_dict.keys()))

    return fig
