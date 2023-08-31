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

def draw_catalog_num_pie(catalog_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 类别-数字 饼状图
    """
    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.pie(num_data_list, labels=catalog_data_list)

    return fig
