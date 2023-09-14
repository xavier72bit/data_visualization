import os
import os.path
from loguru import logger
import matplotlib.pyplot as plt
from project_common import CURRENT_PLOT_PATH


# -----------------------------------------------------
# 绘图工具函数
# -----------------------------------------------------


def plot_storage(figure: plt.Figure, file_name: str) -> str | None:
    """
    绘图结果存储

    :return: 成功：图片路径，失败：None
    """
    if not os.path.exists(CURRENT_PLOT_PATH):
        os.mkdir(CURRENT_PLOT_PATH)

    file_path = os.path.join(CURRENT_PLOT_PATH, file_name)

    try:
        figure.savefig(file_path)
    except Exception as err:
        logger.error('图片存储出错，错误原因: {0}'.format(err))
        return None
    else:
        return file_path + '.png'
