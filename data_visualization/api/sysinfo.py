from flask import Blueprint, request, jsonify

from data_visualization.service import access_log_service

sysinfo_api = Blueprint('sysinfo_api', __name__)


@sysinfo_api.route('/ip_access_count', methods=['GET'])
def count_access_times_by_ip():
    ip_addr = request.args.get('ip_address', '')

    if ip_addr:
        access_count = access_log_service.read_access_count_by_ip(ip_addr)

        data = {
            "code": "200",
            "msg": "请求成功",
            "data": access_count
        }
    else:
        data = {
            "code": "10003",
            "msg": "参数错误",
            "data": None
        }

    return jsonify(data)
