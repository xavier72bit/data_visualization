import flask
import config_util
import logging_util
from flask import Flask
from pymysql_toolkit import MysqlConnection


# -----------------------------------------------------
# 模块工具函数
# -----------------------------------------------------


def create_app(app_name: str, config_dict: dict) -> flask.Flask:
    """
    配置并创建 Flask_app

    :param app_name: app的名称
    :param config_dict: app的配置字典
    :return: Flask app 实例
    """
    new_app = Flask(app_name)

    # app的日志初始化
    # 这一步只是给 Flask app 的 logger 添加一个 FileHandler
    # TODO: 可以考虑使用MemoryHandler日志缓存
    web_app_file_handler = logging_util.create_file_handler('flask_web_api.log', 'DEBUG')
    new_app.logger.addHandler(web_app_file_handler)

    # 重新配置werkzeug的日志，覆盖默认配置
    # TODO: 可以考虑使用MemoryHandler日志缓存
    werkzeug_logger = logging_util.std_init_module_logging('werkzeug', 'DEBUG', 'wsgi_request.log')

    # 更新app实例的配置
    new_app.config.update(config_dict)

    return new_app


# -----------------------------------------------------
# 模块初始化，加载模块配置，创建app
# -----------------------------------------------------

# 加载模块的配置
properties_dict = config_util.read_yaml("properties.yaml")
app_config = properties_dict['flask_app']
app_server_config = properties_dict['app_server']

# 创建app
app = create_app(__name__, app_config)


# -----------------------------------------------------
# 视图函数
# -----------------------------------------------------

@app.route('/hello')
def hello():
    return 'hello, world!'


@app.route('/pymysql_test')
def pymysql_test():
    with MysqlConnection() as connection1:
        connection1_cursor = connection1.get_cursor()
        pass

    with MysqlConnection(transaction=True) as connection2:
        connection2_cursor = connection2.get_cursor()
        pass

    return 'pymysql_test'


# -----------------------------------------------------
# 程序入口
# -----------------------------------------------------

if __name__ == '__main__':
    app.run(host=app_server_config['host'],
            port=app_server_config['port'])
