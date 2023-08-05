import yaml
import os.path

from project_common import CURRENT_CONFIG_PATH

__all__ = ['read_yaml']


# -----------------------------------------------------
# 配置模块的工具函数
# -----------------------------------------------------

def read_yaml(yaml_file_name: str) -> dict:
    """
    读取yaml文件并将其转换为字典

    :param yaml_file_name: yaml文件名称（只需要文件名）
    :return: 配置字典
    """
    # 拼接yaml文件的绝对路径
    yaml_file_abs_path = os.path.join(CURRENT_CONFIG_PATH, yaml_file_name)

    with open(yaml_file_abs_path, 'rb') as yf:
        config_dict = yaml.safe_load(yf.read())

    return config_dict
