import json
from flask import Blueprint, request, jsonify

from visualization.stream import plot_stream
from project_common import CONST_PLOT_TASK_SUPPORT_FLAG_DICT, CONST_PLOT_REQUIREMENT_ERROR_MSG
from visualization.utils.do.data_object import AccessLog, PlotTask
from visualization.service import access_log_service, plot_task_service

# -----------------------------------------------------
# 定义flask蓝图
# -----------------------------------------------------

plot_api = Blueprint('plot_api', __name__)


# -----------------------------------------------------
# 业务API
# -----------------------------------------------------


@plot_api.route('2d/data/submit', methods=['POST'])
def commit_data_source():
    """
    获取数据，创建绘图任务，返回绘图任务ID
    """
    # 接收json数据
    get_json_data: dict = request.get_json()

    # 记录请求
    access_log = access_log_service.create(
        AccessLog(
            access_ip=request.remote_addr,
            access_url=request.url,
            access_param=json.dumps(get_json_data)
        )
    )

    # 创建任务单
    plot_task = plot_task_service.create(
        PlotTask(
            access_log_id=access_log.access_log_id
        )
    )

    # 过滤json数据，留下"data_source"，作为绘图任务单数据
    plot_task_data: dict = get_json_data["data_source"]

    # 更新任务单绘图数据并判断绘图种类
    plot_task.plot_task_data = json.dumps(plot_task_data)
    result_plot_task = plot_stream.check_plot_type(plot_task)

    res_data = {
        'code': result_plot_task.plot_task_support_flag,
        'msg': (
            result_plot_task.plot_task_id
            if result_plot_task.plot_task_support_flag == 0
            else CONST_PLOT_TASK_SUPPORT_FLAG_DICT[result_plot_task.plot_task_support_flag]
        ),
        'data': (
            json.loads(result_plot_task.plot_task_support_type)
            if result_plot_task.plot_task_support_flag == 0
            else None
        )
    }

    return jsonify(res_data)


@plot_api.route('2d/chart/plotting', methods=['POST'])
def data_source_plot():
    # 接收json数据
    json_data: dict = request.get_json()

    # 记录请求
    access_log_service.create(
        AccessLog(
            access_ip=request.remote_addr,
            access_url=request.url,
            access_param=json.dumps(json_data)
        )
    )

    # 校验json数据完整性
    if not ('plot_key' in json_data.keys() and 'plot_requirement' in json_data.keys()):
        res_data = {
            'code': 500,
            'msg': '请求体结构错误',
            'data': None
        }
        return jsonify(res_data)

    # 获取请求数据
    plot_task_id = json_data['plot_key']
    plot_requirement_dict = json_data['plot_requirement']

    # 根据plot_key获取plot_task
    plot_task = plot_task_service.read_one(
        PlotTask(
            plot_task_id=plot_task_id
        )
    )

    if plot_task is None:
        res_data = {
            'code': 500,
            'msg': 'plot_key无效',
            'data': None
        }
        return jsonify(res_data)

    # 绘图
    exec_result: dict | int = plot_stream.plot_and_upload_picture(plot_task, plot_requirement_dict)

    # 返回绘图结果
    if type(exec_result) is dict:
        res_data = {
            'code': 200,
            'msg': '绘图需求校验通过，绘图结果请查看data',
            'data': exec_result
        }
    else:
        res_data = {
            'code': exec_result,
            'msg': CONST_PLOT_REQUIREMENT_ERROR_MSG[exec_result],
            'data': None
        }

    return jsonify(res_data)
