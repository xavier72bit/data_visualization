import os.path
import datetime

__all__ = ["CURRENT_WORKSPACE", "CURRENT_CONFIG_PATH", "CURRENT_LOG_PATH", "CURRENT_PLOT_PATH",
           "DATE_TIME_NOW", "FDFS_SERVER_ADDRESS"]

# 工作目录
CURRENT_WORKSPACE = os.path.split(os.path.abspath(__file__))[0]
CURRENT_CONFIG_PATH = os.path.join(CURRENT_WORKSPACE, 'config')
CURRENT_LOG_PATH = os.path.join(CURRENT_WORKSPACE, 'logs')
CURRENT_PLOT_PATH = os.path.join(CURRENT_WORKSPACE, 'plot_output')

# 当前时间
DATE_TIME_NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# FastDFS文件预览地址
FDFS_SERVER_ADDRESS = 'https://fs.zhulin.xin/'
