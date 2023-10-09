import os.path
import datetime


# -----------------------------------------------------
# 通用常量
# -----------------------------------------------------

# 工作目录
CURRENT_WORKSPACE = os.path.split(os.path.abspath(__file__))[0]
CURRENT_CONFIG_PATH = os.path.join(CURRENT_WORKSPACE, 'config')
CURRENT_LOG_PATH = os.path.join(CURRENT_WORKSPACE, 'logs')
CURRENT_PLOT_PATH = os.path.join(CURRENT_WORKSPACE, 'plot_output')

# 当前时间
DATE_TIME_NOW = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# -----------------------------------------------------
# visualization.util.storage.minio_util 模块常量
# -----------------------------------------------------

# 文件后缀名与content_type对照字典
CONST_FILE_CONTENT_TYPE_DICT = {
    "jpg": "image/jpeg",
    "png": "image/png"
}

# -----------------------------------------------------
# visualization.api.plot_api 模块常量
# -----------------------------------------------------

# 绘图类型与序号对照字典
CONST_PLOT_TYPE_DICT = {
    1: '折线图',
    2: '柱状图',
    3: '条形图',
    4: '饼状图',
    5: '雷达图'
}


# 绘图任务状态常量
CONST_PLOT_TASK_SUPPORT_FLAG_DICT = {
    0: '数据正常',
    1: '数据源结构无效',
    2: '数据源个数小于2',
    3: '数据源无法组合绘图'
}


# 绘图结果状态常量
CONST_PLOT_RESULT_STATE_DICT = {
    0: '绘图成功',
    1: '绘图失败',
    2: '图片保存失败',
    3: '图片上传失败',
    4: '图表类型组合无法绘图',
    5: '图表数据长度不一致',
    6: '数据源组合没有共享X轴'
}


# 绘图需求校验错误信息
CONST_PLOT_REQUIREMENT_ERROR_MSG = {
    1: "绘图需求为空",
    2: "绘图需求无法被满足"
}
