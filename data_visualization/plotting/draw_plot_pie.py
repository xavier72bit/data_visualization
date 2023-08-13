import matplotlib.pyplot as plt

font = {'family': 'SimSun',
        'size': '12'}

plt.rc('font', **font)


def draw_catalog_num_pie(catalog_data_list, num_data_list, plot_title) -> plt.Figure:
    fig, ax = plt.subplots()

    ax.set_title(plot_title)
    ax.pie(num_data_list, labels=catalog_data_list)

    return fig
