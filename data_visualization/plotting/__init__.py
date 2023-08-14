import os
import os.path
from project_common import CURRENT_PLOT_PATH

from data_visualization.utils import logging_util

# -----------------------------------------------------
# 初始化模块日志
# -----------------------------------------------------

plotting_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))


# -----------------------------------------------------
# 工具函数
# -----------------------------------------------------

def plot_storage(figure, file_name: str) -> str | int:
    """
    绘图结果存储
    """
    if not os.path.exists(CURRENT_PLOT_PATH):
        os.mkdir(CURRENT_PLOT_PATH)

    file_path = os.path.join(CURRENT_PLOT_PATH, file_name)

    try:
        figure.savefig(file_path)
    except Exception as err:
        plotting_logger.error('图片存储出错，错误原因: {0}'.format(err))
        return 2
    else:
        return file_path + '.png'
