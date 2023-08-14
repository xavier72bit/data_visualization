import matplotlib.pyplot as plt

# -----------------------------------------------------
# 定义字体
# -----------------------------------------------------

font_rc = {'family': 'SimSun',
           'size': '12'}

plt.rc('font', **font_rc)


# -----------------------------------------------------
# 绘图功能函数
# -----------------------------------------------------

def draw_time_num_line(time_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 时间-数字 折线图
    """
    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.plot(time_data_list, num_data_list)

    return fig


def draw_catalog_num_line(catalog_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 类别-数字 折线图
    """
    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.plot(catalog_data_list, num_data_list)

    return fig


def draw_time_catalog_num_line(time_data_list, catalog_num_dict, plot_title) -> plt.Figure:
    """
    绘制 时间-类别-数字 多条折线图
    """
    fig, ax = plt.subplots()

    for catalog in catalog_num_dict.keys():
        ax.plot(time_data_list, catalog_num_dict[catalog], label=catalog)

    # 设置图例
    ax.legend(loc='upper left', ncols=3)
    # 设置标题
    ax.set_title(plot_title)

    return fig
