import os.path
import platform
from loguru import logger

from project_common import CURRENT_CONFIG_PATH
from fdfs_client.client import get_tracker_conf, Fdfs_client


# -----------------------------------------------------
# 初始化FastDFS Client
# -----------------------------------------------------

fdfs_config_file = os.path.join(CURRENT_CONFIG_PATH, 'fdfs_client.conf')

try:
    tracker_conf = get_tracker_conf(fdfs_config_file)
    fdfs_client = Fdfs_client(tracker_conf)
except Exception as e:
    logger.error("初始化fdfs_client失败，错误原因: {0}".format(e))
else:
    logger.info("初始化fdfs_client成功，配置内容: {0}".format(tracker_conf))


# -----------------------------------------------------
# 工具函数
# -----------------------------------------------------

def upload_file(file_path):
    """
    上传文件到FastDFS，返回文件ID
    """
    try:
        if platform.system() == 'Linux':
            upload_result = fdfs_client.upload_by_file(file_path)
        else:
            with open(file_path, 'rb') as data:
                upload_result = fdfs_client.upload_by_buffer(data.read(), file_ext_name='png')
    except Exception as err:
        logger.error("上传文件操作失败，错误原因：{0}".format(err))
        return None
    else:
        logger.info("上传文件操作成功，详情：{0}".format(upload_result))

    if upload_result.get('Status') == 'Upload successed.':
        logger.info("上传状态正常")
        return upload_result.get('Remote file_id').decode('utf-8')
    else:
        logger.error("上传状态异常: {0}".format(upload_result.get('Status')))
        return None
