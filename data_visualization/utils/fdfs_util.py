import os.path
import platform

from project_common import CURRENT_CONFIG_PATH
from data_visualization.utils import logging_util

from fdfs_client.client import get_tracker_conf, Fdfs_client

# -----------------------------------------------------
# 初始化模块日志
# -----------------------------------------------------

fdfs_util_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))

# -----------------------------------------------------
# 初始化fdfs_client
# -----------------------------------------------------

fdfs_config_file = os.path.join(CURRENT_CONFIG_PATH, 'fdfs_client.conf')

try:
    tracker_conf = get_tracker_conf(fdfs_config_file)
    client = Fdfs_client(tracker_conf)
except Exception as e:
    fdfs_util_logger.error("初始化fdfs_client失败，错误原因: {0}".format(e))
else:
    fdfs_util_logger.info("初始化fdfs_client成功，配置内容: {0}".format(tracker_conf))


def upload_file(file_path):
    """
    上传文件到FastDFS，返回文件ID
    """
    try:
        if platform.system() == 'Linux':
            upload_result = client.upload_by_file(file_path)
        else:
            with open(file_path, 'rb') as data:
                upload_result = client.upload_by_buffer(data.read(), file_ext_name='png')
    except Exception as err:
        fdfs_util_logger.error("上传文件操作失败，错误原因：{0}".format(err))
        return None
    else:
        fdfs_util_logger.info("上传文件操作成功，详情：{0}".format(upload_result))

    if upload_result.get('Status') == 'Upload successed.':
        fdfs_util_logger.info("上传状态正常")
        return upload_result.get('Remote file_id').decode('utf-8')
    else:
        fdfs_util_logger.error("上传状态异常: {0}".format(upload_result.get('Status')))
        return None
