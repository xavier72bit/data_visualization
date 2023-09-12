import json
from flask import Blueprint, request, jsonify

from data_visualization.stream import plot_stream
from data_visualization.service import access_log_service
from data_visualization.utils.do.data_object import AccessLog

# -----------------------------------------------------
# 定义flask蓝图
# -----------------------------------------------------

plot_api = Blueprint('plot_api', __name__)

# -----------------------------------------------------
# 绘图状态定义
# -----------------------------------------------------

# 绘图状态
plot_state_dict = {
    0: '绘图成功',
    1: '数据序列长度不一致',
    2: '绘图失败',
    3: '图片保存失败',
    4: '图片上传失败'
}

# 数据校验状态
data_state_dict = {
    0: '数据正常',
    1: '数据源结构无效',
    2: '两个数据序列长度不一致',
    3: '数据类型无效'
}


# -----------------------------------------------------
# 业务API
# -----------------------------------------------------


@plot_api.route('/data/source', methods=['POST'])
def commit_data_source():
    # 接收json数据
    json_data = request.get_json()

    # TODO: 校验一下json的key是否符合要求

    # 记录请求
    access_log = access_log_service.create(AccessLog(access_ip=request.remote_addr,
                                                     access_url=request.url,
                                                     access_param=json.dumps(json_data)))

    # 提取绘图数据源
    data_source_1 = json_data['data_source_1']
    data_source_2 = json_data['data_source_2']

    # 校验数据
    result_access_log = plot_stream.check_plot_type(access_log, data_source_1, data_source_2)

    if result_access_log.access_plot_flag == 0:  # 检查通过，可以绘图
        res_data = {
            'code': result_access_log.access_plot_flag,
            'msg': result_access_log.access_plot_type,
            'data': result_access_log.access_log_id
        }
    else:
        res_data = {
            'code': result_access_log.access_plot_flag,
            'msg': data_state_dict[result_access_log.access_plot_flag],
            'data': None
        }

    return jsonify(res_data)
