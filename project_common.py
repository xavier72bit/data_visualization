import os.path
import datetime

__all__ = ["CURRENT_WORKSPACE", "CURRENT_CONFIG_PATH", "CURRENT_LOG_PATH", "CURRENT_PLOT_PATH",
           "DATE_TIME_NOW"]

# 工作目录
CURRENT_WORKSPACE = os.path.split(os.path.abspath(__file__))[0]
CURRENT_CONFIG_PATH = os.path.join(CURRENT_WORKSPACE, 'config')
CURRENT_LOG_PATH = os.path.join(CURRENT_WORKSPACE, 'logs')
CURRENT_PLOT_PATH = os.path.join(CURRENT_WORKSPACE, 'plot_output')

# 当前时间
DATE_TIME_NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
