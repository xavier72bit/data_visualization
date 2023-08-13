from flask import Blueprint, request, jsonify

from data_visualization.service import plot_result_service

plot_api = Blueprint('plot_api', __name__)


@plot_api.route('/source', method=['POST'])
def plot_with_source():
    pass


@plot_api.route('/object', method=['POST'])
def plot_with_object():
    pass
