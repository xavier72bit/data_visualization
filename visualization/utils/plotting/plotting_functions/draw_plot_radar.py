import numpy as np
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

def draw_radar(ax: plt.PolarAxes, data_list_x: list, data_list_y: list, **kwargs) -> bool:
    """
    绘制雷达图

    :param ax: 绘图坐标系(极坐标系)
    :param data_list_x: 种类数据列表
    :param data_list_y: 数字数据列表
    :param kwargs: 其他绘图选项(关键字参数)
    :return: 绘图操作是否成功

    其他的绘图选项：
        暂无其他绘图选项
    """
    try:
        # 设置雷达图的角度，用于平分切开一个圆面
        angles = np.linspace(0, 2 * np.pi, len(data_list_x), endpoint=False)

        # 为了使雷达图一圈封闭起来，需要下面的步骤
        values = np.concatenate((data_list_y, [data_list_y[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        catalog_list = np.concatenate((data_list_x, [data_list_x[0]]))

        # 绘制图形
        ax.plot(angles, values, 'o-', linewidth=2)

        # 填充颜色
        ax.fill(angles, values, alpha=0.25)

        # 添加每个特征的标签
        ax.set_thetagrids(angles * 180/np.pi, labels=catalog_list)

        # 添加网格线
        ax.grid(True)
    except Exception as plot_err:
        print("draw_radar绘图失败，错误原因: {0}".format(plot_err))
        return False
    else:
        return True
