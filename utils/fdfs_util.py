import os
from fdfs_client.client import get_tracker_conf, Fdfs_client

"""
上传文件到fdfs服务工具类
"""


def upload_file(full_file_path):
    # 获得tracker配置文件目录
    conf_dir = os.path.join(get_parent_path(__file__, 5), 'conf')

    tracker_conf_file_path = os.path.join(conf_dir, 'client.conf')

    print(tracker_conf_file_path)
    # 加载tracker配置
    if os.path.exists(tracker_conf_file_path):
        tracker_conf = get_tracker_conf(tracker_conf_file_path)

        # 获取fastdfs client
        client = Fdfs_client(tracker_conf)

        # 判断上传文件是否存在
        if os.path.exists(full_file_path):
            # 只有linux系统才能使用下面这一行的
            # upload_result = client.upload_by_file(full_file_path)

            with open(full_file_path, 'rb') as data:
                upload_result = client.upload_by_buffer(data.read(), file_ext_name='jpg')

                # 处理返回结果
                if upload_result.get('Status') == 'Upload successed.':
                    return upload_result.get('Remote file_id').decode('utf-8')