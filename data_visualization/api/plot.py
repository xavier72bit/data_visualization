from flask import Blueprint, request, jsonify

from data_visualization.service import access_log_service
from data_visualization.service import plot_result_service

__all__ = ['plot_api']

# -----------------------------------------------------
# 定义蓝图
# -----------------------------------------------------

plot_api = Blueprint('plot_api', __name__)

# -----------------------------------------------------
# 绘图状态定义
# -----------------------------------------------------

plot_state_dict = {
    0: '绘图成功',
    1: '数据序列长度不一致',
    2: '绘图失败',
    3: '图片保存失败',
    4: '图片上传失败'
}


# -----------------------------------------------------
# API
# -----------------------------------------------------

@plot_api.route('/source', methods=['POST'])
def plot_time_num_with_source():
    # 记录请求
    access_log_id = access_log_service.creat_a_new_access_log(access_ip=request.remote_addr,
                                                              access_token='zanshimeiyoutoken',
                                                              access_log_message='zanshibuzhidaotiansha')

    # 新建plot_result
    new_plot_result_id = plot_result_service.create_a_new_plot_result(access_log_id)

    # 接收json数据
    json_data = request.get_json()
    time_data_list = json_data['time_data_list']
    print(time_data_list)
    num_data_list = json_data['num_data_list']
    print(num_data_list)
    plot_title = json_data['plot_title']
    print(plot_title)

    # 绘图
    plot_result_id = plot_result_service.plot_time_num(plot_result_id=new_plot_result_id,
                                                       time_data_list=time_data_list,
                                                       num_data_list=num_data_list,
                                                       plot_title=plot_title)

    # 获取绘图状态
    state_code = plot_result_service.read_state_by_id(plot_result_id)

    # 获取状态描述
    state_message = plot_state_dict[state_code]

    if state_code:
        # 绘图状态不正常
        res_data = {
            'code': state_code,
            'msg': state_message,
            'data': None
        }
    else:
        # 绘图状态正常

        # 获取url
        plot_picture_url = plot_result_service.read_url_by_id(plot_result_id)

        res_data = {
            'code': state_code,
            'msg': state_message,
            'data': plot_picture_url
        }

    return jsonify(res_data)


@plot_api.route('/object', methods=['POST'])
def plot_with_object():
    pass
