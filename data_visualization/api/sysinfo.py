from flask import Blueprint, request, jsonify

from data_visualization.service import access_log_service

__all__ = ['sysinfo_api']

# -----------------------------------------------------
# 定义蓝图
# -----------------------------------------------------

sysinfo_api = Blueprint('sysinfo_api', __name__)


# -----------------------------------------------------
# API
# -----------------------------------------------------


@sysinfo_api.route('/ip_access_count', methods=['GET'])
def count_access_times_by_ip():
    ip_addr = request.args.get('ip_address', '')

    access_count = access_log_service.read_access_count_by_ip(ip_addr)

    data = {
        "code": "200",
        "msg": "请求成功",
        "data": access_count
    }

    return jsonify(data)
