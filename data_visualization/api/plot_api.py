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
    1: '绘图失败',
    2: '图片保存失败',
    3: '图片上传失败'
}

# 数据校验状态
data_state_dict = {
    0: '数据正常',
    1: '数据源结构无效',
    2: '两个数据序列长度不一致',
    3: '数据类型无效',
    4: '缺少数据源'
}


# -----------------------------------------------------
# 业务API
# -----------------------------------------------------


@plot_api.route('/data/source', methods=['POST'])
def commit_data_source():
    # 接收json数据
    json_data: dict = request.get_json()

    # 记录请求
    access_log = access_log_service.create(AccessLog(access_ip=request.remote_addr,
                                                     access_url=request.url,
                                                     access_param=json.dumps(json_data)))

    # 校验json数据
    if not ('data_source_1' in json_data.keys() and 'data_source_2' in json_data.keys()):
        access_log.access_plot_flag = 4
        access_log_service.update(access_log)
        res_data = {
            'code': access_log.access_plot_flag,
            'msg': data_state_dict[access_log.access_plot_flag],
            'data': None
        }
        return jsonify(res_data)

    # 提取绘图数据源
    data_source_1 = json_data['data_source_1']
    data_source_2 = json_data['data_source_2']

    # 判断绘图种类
    result_access_log = plot_stream.check_plot_type(access_log, data_source_1, data_source_2)

    res_data = {
        'code': result_access_log.access_plot_flag,
        'msg': result_access_log.access_plot_type if result_access_log.access_plot_flag == 0 else data_state_dict[result_access_log.access_plot_flag],
        'data': result_access_log.access_log_id if result_access_log.access_plot_flag == 0 else None
    }

    return jsonify(res_data)


@plot_api.route('/plotting/id', methods=['POST'])
def data_source_plot():
    # 接收json数据
    json_data: dict = request.get_json()

    # 记录请求
    access_log_service.create(AccessLog(access_ip=request.remote_addr,
                                        access_url=request.url,
                                        access_param=json.dumps(json_data)))

    # 校验json数据完整性
    if not ('plot_key' in json_data.keys() and 'plot_requirement_list' in json_data.keys()):
        res_data = {
            'code': 500,
            'msg': '请求体结构错误',
            'data': None
        }
        return jsonify(res_data)

    # 获取请求数据
    plotting_access_log_id = json_data['plot_key']
    plotting_require_list = json_data['plot_requirement_list']

    # 根据plot_key获取access_log
    access_log = access_log_service.read_one(access_log=AccessLog(access_log_id=plotting_access_log_id))

    if access_log is None:
        res_data = {
            'code': 500,
            'msg': 'plot_key无效',
            'data': None
        }
        return jsonify(res_data)

    # 绘图
    plot_result = plot_stream.data_source_plot_upload_picture(access_log=access_log,
                                                              plotting_require_list=plotting_require_list)

    # 判断绘图结果
    if plot_result is None:
        res_data = {
            'code': 500,
            'msg': '请求数据无效',
            'data': None
        }
        return jsonify(res_data)
    else:
        res_data = {
            'code': plot_result.plot_result_state,
            'msg': plot_state_dict[plot_result.plot_result_state],
            'data': plot_result.plot_result_url if plot_result.plot_result_state == 0 else None
        }
        return jsonify(res_data)
