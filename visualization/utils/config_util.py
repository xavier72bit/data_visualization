import json
import yaml
import os.path

from project_common import CURRENT_CONFIG_PATH


# -----------------------------------------------------
# 工具函数
# -----------------------------------------------------

def read_yaml(yaml_file_name: str) -> dict:
    """
    读取yaml文件并将其转换为字典
    """
    # 拼接yaml文件的绝对路径
    yaml_file_abs_path = os.path.join(CURRENT_CONFIG_PATH, yaml_file_name)

    with open(yaml_file_abs_path, 'rb') as yf:
        config_dict = yaml.safe_load(yf.read())

    return config_dict


def read_json(json_file_name: str) -> dict:
    """
    读取json文件并转换为字典
    """
    # 拼接json文件的绝对路径
    json_file_abs_path = os.path.join(CURRENT_CONFIG_PATH, json_file_name)

    with open(json_file_abs_path, 'rb') as jf:
        json_data = json.load(jf)

    return json_data
