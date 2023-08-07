import json
from flask import Blueprint, request, jsonify

sysinfo_api = Blueprint('sysinfo_api', __name__)


@sysinfo_api.route('/ip_access_count', methods=['GET'])
def count_access_times_by_ip():
    pass