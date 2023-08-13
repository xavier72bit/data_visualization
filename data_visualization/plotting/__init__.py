import os
import os.path
from project_common import CURRENT_PLOT_PATH


def choose_plot_data_source():
    """
    数据源模式下，选择绘图类型
    """
    pass


def choose_plot_data_object():
    """
    数据对象模式下，选择绘图类型
    """
    pass


# TODO: 注解类型表达式
def plot_storage(figure, file_name: str):
    """
    绘图结果存储
    """
    if not os.path.exists(CURRENT_PLOT_PATH):
        os.mkdir(CURRENT_PLOT_PATH)

    file_path = os.path.join(CURRENT_PLOT_PATH, file_name)

    figure.savefig(file_path)


