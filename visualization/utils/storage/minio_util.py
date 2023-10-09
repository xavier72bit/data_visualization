import json
import os.path
from minio import Minio
from loguru import logger

from visualization.utils import config_util
from project_common import FILE_CONTENT_TYPE_DICT


# -----------------------------------------------------
# MinIO工具类
# -----------------------------------------------------


class MinioUtil:
    minio_bucket_name = "py-data-visualization"
    minio_bucket_policy_dict = config_util.read_json('minio_bucket_policy_anyone_readonly.json')
    minio_client_config = config_util.read_yaml('properties.yaml')['minio']

    def __init__(self):
        # 1. 初始化Minio Client对象
        self.minio_client = Minio(endpoint=self.minio_client_config["endpoint"],
                                  access_key=self.minio_client_config["user"],
                                  secret_key=self.minio_client_config["password"],
                                  secure=self.minio_client_config["enable_https"])

        logger.info('Minio Client初始化成功，配置内容：{0}'.format(self.minio_client_config))

        # 2. 创建存储桶，配置匿名用户只能读取对象，禁止遍历桶内文件
        is_bucket_exist = self.minio_client.bucket_exists(self.minio_bucket_name)

        if is_bucket_exist:
            logger.info("{0}存储桶已存在".format(self.minio_bucket_name))
        else:
            logger.info("{0}存储桶不存在，创建存储桶".format(self.minio_bucket_name))

            # 创建存储桶
            try:
                self.minio_client.make_bucket(self.minio_bucket_name)
            except Exception as err:
                logger.error("创建存储桶失败，错误原因：{0}".format(err))
            else:
                logger.info("创建存储桶成功")

            # 修改存储桶的权限
            try:
                logger.info("修改存储桶权限为匿名用户只读")
                self.minio_client.set_bucket_policy(self.minio_bucket_name, json.dumps(self.minio_bucket_policy_dict))
            except Exception as err:
                logger.error("存储桶权限修改失败，错误原因：{0}".format(err))
            else:
                logger.info("修改存储桶权限成功，权限：{0}"
                            .format(self.minio_client.get_bucket_policy(self.minio_bucket_name)))

    def upload_file(self, file_path: str) -> str | None:
        """
        上传文件到minio，返回文件URL
        """
        object_name = os.path.split(file_path)[-1]
        object_content_type = FILE_CONTENT_TYPE_DICT[os.path.split(file_path)[-1].split(".")[-1]]

        try:
            with open(file_path, 'rb') as data:
                # 上传图片的大小未知，part_size设置为最小的5MB
                upload_result = self.minio_client.put_object(bucket_name=self.minio_bucket_name,
                                                             object_name=object_name,
                                                             data=data,
                                                             part_size=5 * 1024 * 1024,
                                                             length=-1,
                                                             content_type=object_content_type)
        except Exception as upload_err:
            logger.error("上传文件失败，错误原因：{0}".format(upload_err))
            return None
        else:
            logger.info("上传文件成功，已创建{0}对象，etag：{1}，content-type：{2}"
                        .format(upload_result.object_name, upload_result.etag, object_content_type))

            return '/'.join([self.minio_client_config["endpoint"], self.minio_bucket_name, object_name])
