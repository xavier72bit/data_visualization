import os.path
import loguru
from flask import Flask
from werkzeug.utils import cached_property
from flask.json.provider import DefaultJSONProvider

from project_common import CURRENT_LOG_PATH
from visualization.api import plot_api
from visualization.api import sysinfo_api
from visualization.utils import config_util

# -----------------------------------------------------
# 初始化项目日志
# -----------------------------------------------------

if not os.path.exists(CURRENT_LOG_PATH):
    os.mkdir(CURRENT_LOG_PATH)

log_file_name = "data_visualization_{time}.log"
log_file_path = os.path.join(CURRENT_LOG_PATH, log_file_name)

loguru.logger.add(log_file_path, encoding='utf-8', rotation='00:00')

# -----------------------------------------------------
# 读取配置
# -----------------------------------------------------

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
    1. 重新指定Flask app的json_provider_class
    2. 将app的默认logger从 logging.logger 改为 loguru.logger
    """
    json_provider_class = NoAsciiJSONProvider

    @cached_property
    def logger(self):
        return loguru.logger


app = CurrentFlask(__name__)

app.config.from_mapping(app_config_dict)
app.logger.info("app配置：{0}".format(app.config))

# -----------------------------------------------------
# 注册flask蓝图
# -----------------------------------------------------

app.register_blueprint(sysinfo_api.sysinfo_api, url_prefix='/sysinfo')
app.register_blueprint(plot_api.plot_api, url_prefix='/plot')

# -----------------------------------------------------
# 程序入口
# -----------------------------------------------------

if __name__ == '__main__':
    app.run(app_server_config_dict['host'],
            app_server_config_dict['port'])
