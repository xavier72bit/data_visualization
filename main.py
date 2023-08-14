from flask import Flask
from flask.json.provider import DefaultJSONProvider

from data_visualization.api import sysinfo
from data_visualization.api import plot
from data_visualization.utils import config_util, logging_util

# -----------------------------------------------------
# 初始化模块日志Logger，读取配置
# -----------------------------------------------------

main_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))
property_config_dict = config_util.read_yaml("properties.yaml")
app_config_dict = property_config_dict['app']
app_server_config_dict = property_config_dict['app_server']


# -----------------------------------------------------
# 初始化Flask app
# -----------------------------------------------------

class NoAsciiJSONProvider(DefaultJSONProvider):
    """
    关闭flask.json模块的ascii编码
    """
    ensure_ascii = False


class CurrentFlask(Flask):
    """
    重新指定Flask app的json_provider_class
    """
    json_provider_class = NoAsciiJSONProvider


app = CurrentFlask(__name__)

# app的日志初始化
# 这一步只是给 Flask app 的 logger 添加一个 FileHandler
web_app_file_handler = logging_util.create_file_handler('flask_web_api.log', 'DEBUG')
app.logger.addHandler(web_app_file_handler)

# 重新配置werkzeug的日志，覆盖默认配置
werkzeug_logger = logging_util.std_init_module_logging('werkzeug', 'DEBUG', 'wsgi_request.log')

app.config.from_mapping(app_config_dict)
main_logger.info("app配置：{0}".format(app.config))

# -----------------------------------------------------
# 注册flask蓝图
# -----------------------------------------------------

app.register_blueprint(sysinfo.sysinfo_api, url_prefix='/sysinfo')
app.register_blueprint(plot.plot_api, url_prefix='/plot')

# -----------------------------------------------------
# 程序入口
# -----------------------------------------------------

if __name__ == '__main__':
    app.run(app_server_config_dict['host'],
            app_server_config_dict['port'])
