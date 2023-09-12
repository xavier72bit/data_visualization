import os.path
import datetime


# 工作目录
CURRENT_WORKSPACE = os.path.split(os.path.abspath(__file__))[0]
CURRENT_CONFIG_PATH = os.path.join(CURRENT_WORKSPACE, 'config')
CURRENT_LOG_PATH = os.path.join(CURRENT_WORKSPACE, 'logs')
CURRENT_PLOT_PATH = os.path.join(CURRENT_WORKSPACE, 'plot_output')

# 当前时间
DATE_TIME_NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# TODO: FastDFS 和 MinIO的地址通过配置文件读取，不放在project_common中，应当放在实现“绘图存储”功能的模块中
"""
FastDFS文件预览地址
FDFS_SERVER_ADDRESS = 'https://fs.zhulin.xin/'

MinIO文件预览地址
MINIO_SERVER_ADDRESS = 'http://192.168.64.17:9001/'
"""

# 文件后缀名与content_type对照字典
FILE_CONTENT_TYPE_DICT = {
    "jpg": "image/jpeg",
    "png": "image/png"
}

# 绘图类型与序号对照字典
PLOT_INDEX_TYPE_DICT = {
    '1': '折线图',
    '2': '柱状图',
    '3': '条形图',
    '4': '饼状图',
    '5': '雷达图',
    '6': '多条折线图',
    '7': '并列柱状图'
}
