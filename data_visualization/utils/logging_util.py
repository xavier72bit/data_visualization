import os.path
import logging

from project_common import CURRENT_LOG_PATH
from flask.logging import default_handler as flask_default_handler


__all__ = ["create_file_handler", "std_init_module_logging"]

# -----------------------------------------------------
# 常量定义
# -----------------------------------------------------

# 项目日志 Format 常量
FLASK_DEFAULT_LOG_FORMAT = '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
# 项目日志 Formatter
default_formatter = logging.Formatter(FLASK_DEFAULT_LOG_FORMAT)

# -----------------------------------------------------
# 模块初始化
# -----------------------------------------------------

# 创建日志目录
if not os.path.exists(CURRENT_LOG_PATH):
    os.mkdir(CURRENT_LOG_PATH)


# -----------------------------------------------------
# 日志模块的工具函数
# -----------------------------------------------------

def create_file_handler(file_name: str, level: str) -> logging.Handler:
    """
    创建文件handler，并将其 Formatter 设置为 FLASK_DEFAULT_LOG_FORMAT

    :param file_name: 日志文件名
    :param level: Handler的级别
    :return: logging.Handler
    """
    file_path = os.path.join(CURRENT_LOG_PATH, file_name)

    if os.path.exists(file_path):
        file_handler = logging.FileHandler(filename=file_path, mode='a', encoding='utf-8')
    else:
        file_handler = logging.FileHandler(filename=file_path, mode='x', encoding='utf-8')

    file_handler.setLevel(level)
    file_handler.setFormatter(default_formatter)

    return file_handler


def std_init_module_logging(logger_name, logger_level, log_file_name) -> logging.Logger:
    """
    本项目标准的日志功能初始化流程

    如果没有特殊需要，直接调用此函数即可完成初始化，初始化流程为：
    1. 创建 Logger，并设定级别
    2. 创建 File Handler，并设定其 Formatter 为 FLASK_DEFAULT_LOG_FORMAT，Level设定为DEBUG
    3. 为 Logger 绑定 File Handler 和 Flask 的 Stream Handler
    4. 返回一个模块可调用的 Logger

    :param logger_name: Logger 的名称
    :param logger_level: Logger 的级别
    :param log_file_name: 日志文件名
    :return: logging.Logger
    """

    created_logger = logging.getLogger(logger_name)
    created_logger.setLevel(logger_level)

    created_file_handler = create_file_handler(log_file_name, 'DEBUG')
    created_file_handler.setFormatter(default_formatter)

    created_logger.addHandler(created_file_handler)
    created_logger.addHandler(flask_default_handler)

    return created_logger
