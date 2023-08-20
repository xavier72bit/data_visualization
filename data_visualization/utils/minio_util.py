import json
import os.path
from minio import Minio

from project_common import FILE_CONTENT_TYPE_DICT
from data_visualization.utils import config_util, logging_util

__all__ = ['upload_file']

# -----------------------------------------------------
# 模块初始化
# -----------------------------------------------------

# 初始化本模块日志
minio_util_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))

# -----------------------------------------------------
# 初始化MinIO Client
# -----------------------------------------------------

minio_connection_config = config_util.read_yaml('properties.yaml')['minio']

try:
    minio_util_logger.info('开始初始化Minio Client')
    minio_client = Minio(endpoint=minio_connection_config["endpoint"],
                         access_key=minio_connection_config["user"],
                         secret_key=minio_connection_config["password"],
                         secure=minio_connection_config["enable_https"])
except Exception as err:
    minio_util_logger.critical('初始化Minio Client失败，错误: {0}'.format(err))
    minio_client = None
else:
    minio_util_logger.info('Minio Client初始化成功，配置内容：{0}'.format(minio_connection_config))

# -----------------------------------------------------
# 创建存储桶，配置匿名用户只能读取对象，禁止遍历桶内文件
# -----------------------------------------------------

minio_bucket_name = "py-data-visualization"
minio_bucket_policy_dict = config_util.read_json('minio_bucket_policy_anyone_readonly.json')

if minio_client:
    if minio_client.bucket_exists(minio_bucket_name):
        minio_util_logger.info("{0}存储桶已存在".format(minio_bucket_name))
    else:
        minio_util_logger.info("{0}存储桶不存在，创建存储桶".format(minio_bucket_name))

        # 创建存储桶
        try:
            minio_client.make_bucket(minio_bucket_name)
        except Exception as err:
            minio_util_logger.error("创建存储桶失败，错误原因：{0}".format(err))
        else:
            minio_util_logger.info("创建存储桶成功")

        # 修改存储桶的权限
        try:
            minio_util_logger.info("修改存储桶权限为匿名用户只读")
            minio_client.set_bucket_policy(minio_bucket_name, json.dumps(minio_bucket_policy_dict))
        except Exception as err:
            minio_util_logger.error("存储桶权限修改失败，错误原因：{0}".format(err))
        else:
            minio_util_logger.info("修改存储桶权限成功，权限：{0}".format(minio_client.get_bucket_policy(minio_bucket_name)))
else:
    minio_util_logger.error("Minio Client不存在，无法检查存储桶信息！")


# -----------------------------------------------------
# 工具函数
# -----------------------------------------------------


def upload_file(file_path: str) -> None | str:
    """
    上传png图片到minio，返回文件URL后缀
    """

    object_name = os.path.split(file_path)[-1]
    object_content_type = FILE_CONTENT_TYPE_DICT[os.path.split(file_path)[-1].split(".")[-1]]

    try:
        with open(file_path, 'rb') as data:
            # 上传图片的大小未知，part_size设置为最小的5MB
            upload_result = minio_client.put_object(bucket_name=minio_bucket_name,
                                                    object_name=object_name,
                                                    data=data,
                                                    part_size=5 * 1024 * 1024,
                                                    length=-1,
                                                    content_type=object_content_type)
    except Exception as upload_err:
        minio_util_logger.error("上传文件失败，错误原因：{0}".format(upload_err))
        return None
    else:
        minio_util_logger.info("上传文件成功，已创建{0}对象，etag：{1}，content-type：{2}"
                               .format(upload_result.object_name, upload_result.etag, object_content_type))

        return '/'.join([minio_bucket_name, object_name])
