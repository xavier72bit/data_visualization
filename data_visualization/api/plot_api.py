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

plot_state_dict = {
    0: '绘图成功',
    1: '数据序列长度不一致',
    2: '绘图失败',
    3: '图片保存失败',
    4: '图片上传失败'
}

# -----------------------------------------------------
# 业务API
# -----------------------------------------------------

@plot_api.route('/data/source', methods=['POST'])
def get_user_plot_data_source():
    """
    获取用户的绘图数据

    """


# -----------------------------------------------------
# 示例API （开始）
# 等待业务API基本开发完毕后，删除以下这些
# -----------------------------------------------------

@plot_api.route('/source/two', methods=['POST'])
def plot_time_num_with_source():
    # 记录请求
    access_log = access_log_service.create(AccessLog(access_ip=request.remote_addr,
                                                     access_token='zanshimeiyoutoken',
                                                     access_log_message='zanshibuzhidaotiansha'))

    # 接收json数据
    json_data = request.get_json()

    time_data_list = json_data['time_data_list']
    num_data_list = json_data['num_data_list']
    plot_title = json_data['plot_title']

    # 绘图
    plot_result = plot_stream.plot_time_num(access_log_id=access_log.access_log_id,
                                            time_data_list=time_data_list,
                                            num_data_list=num_data_list,
                                            plot_title=plot_title)

    # 判断绘图是否成功
    if plot_result is None:
        res_data = {
            'code': 10000,
            'msg': 'plot_result创建失败',
            'data': None
        }
    else:
        res_data = {
            'code': plot_result.plot_result_state,
            'msg': plot_state_dict[plot_result.plot_result_state],
            'data': None if plot_result.plot_result_state else plot_result.plot_result_url
        }

    return jsonify(res_data)


@plot_api.route('/source/three', methods=['POST'])
def plot_catalog_time_num_with_source():
    # 记录请求
    access_log = access_log_service.create(AccessLog(access_ip=request.remote_addr,
                                                     access_token='zanshimeiyoutoken',
                                                     access_log_message='zanshibuzhidaotiansha'))

    # 接收json数据
    json_data = request.get_json()

    time_data_list = json_data['time_data_list']
    catalog_num_data_dict = json_data['catalog_num_data_dict']
    plot_title = json_data['plot_title']

    # 绘图
    plot_result = plot_stream.plot_catalog_time_num(access_log_id=access_log.access_log_id,
                                                    time_data_list=time_data_list,
                                                    catalog_num_data_dict=catalog_num_data_dict,
                                                    plot_title=plot_title)

    # 判断绘图是否成功
    if plot_result is None:
        res_data = {
            'code': 10000,
            'msg': 'plot_result创建失败',
            'data': None
        }
    else:
        res_data = {
            'code': plot_result.plot_result_state,
            'msg': plot_state_dict[plot_result.plot_result_state],
            'data': None if plot_result.plot_result_state else plot_result.plot_result_url
        }

    return jsonify(res_data)

# -----------------------------------------------------
# 示例API （结束）
# 等待业务API基本开发完毕后，删除以上这些
# -----------------------------------------------------
