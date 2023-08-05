from flask import Blueprint

sysinfo_api = Blueprint('sysinfo_api', __name__)


@sysinfo_api.route('/', methods=['GET'])
def token():
    pass