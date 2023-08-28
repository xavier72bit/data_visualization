from data_visualization.dao import access_log_dao
from data_visualization.utils.do.data_object import AccessLog
from data_visualization.utils.do.data_object_util import general_primary_key


def create(access_log: AccessLog) -> AccessLog | None:
    """
    创建一个新的access_log并插入数据库。

    :return: 成功access_log，失败None
    """
    # 验证access_log_id为空
    if access_log.access_log_id is not None:
        return None

    # 设置主键ID
    access_log.access_log_id = general_primary_key()

    # 插入操作
    insert_result = access_log_dao.insert(access_log)

    # 根据影响行数判断是否插入成功
    if insert_result:
        return access_log
    else:
        return None
