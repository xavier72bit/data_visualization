import numpy as np
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

def draw_catalog_num_radar(catalog_data_list, num_data_list, plot_title) -> plt.Figure:
    """
    绘制 类别-数字 雷达图
    """
    # 设置雷达图的角度，用于平分切开一个圆面
    angles=np.linspace(0, 2*np.pi, len(catalog_data_list), endpoint=False)

    # 为了使雷达图一圈封闭起来，需要下面的步骤
    values=np.concatenate((num_data_list,[num_data_list[0]]))
    angles=np.concatenate((angles,[angles[0]]))
    catalog_list=np.concatenate((catalog_data_list,[catalog_data_list[0]]))

    # 绘图
    fig = plt.figure()
    # 极坐标格式的Axe
    ax = fig.add_subplot(polar=True)
    # 绘制折线图
    ax.plot(angles, values, 'o-', linewidth=2)
    # 填充颜色
    ax.fill(angles, values, alpha=0.25)
    # 添加每个特征的标签
    ax.set_thetagrids(angles * 180/np.pi, labels=catalog_list)
    # 添加网格线，标题
    ax.grid(True)
    ax.set_title(plot_title)

    return fig
