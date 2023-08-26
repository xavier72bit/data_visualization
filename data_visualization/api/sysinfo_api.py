from flask import Blueprint


# -----------------------------------------------------
# 定义蓝图
# -----------------------------------------------------

sysinfo_api = Blueprint('sysinfo_api', __name__)


# -----------------------------------------------------
# API
# -----------------------------------------------------


@sysinfo_api.route('/test', methods=['GET'])
def test():
    return 'hello, world'
