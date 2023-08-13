import matplotlib.pyplot as plt

font_rc = {'family': 'SimSun',
           'size': '12'}

plt.rc('font', **font_rc)


def draw_catalog_num_bar(catalog_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 类别-数字 条形图
    """
    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.barh(catalog_data_list, num_data_list)

    return fig
