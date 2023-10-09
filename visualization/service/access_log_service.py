from project_common import DATE_TIME_NOW
from visualization.dao import access_log_dao
from visualization.utils.do.data_object import AccessLog
from visualization.utils.do.data_object_util import general_primary_key


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

    # 设置访问时间
    access_log.access_date_time = DATE_TIME_NOW

    # 插入操作
    insert_result = access_log_dao.insert(access_log)

    # 根据影响行数判断是否插入成功
    if insert_result:
        return access_log
    else:
        return None


def update(access_log: AccessLog) -> bool:
    """
    更新access_log信息

    :return: 成功True，失败False。
    """
    # 验证主键值非空
    if access_log.access_log_id is None:
        return False

    # 验证传入的access_log在数据库中是否有记录
    old_access_log = access_log_dao.select_one(access_log)
    if old_access_log is None:
        return False

    # 更新操作
    update_result = access_log_dao.update(access_log)

    if update_result:
        return True
    else:
        return False


def read_one(access_log: AccessLog) -> AccessLog | None:
    """
    读取一条access_log信息

    :return: 成功AccessLog，失败None
    """
    # 验证主键值非空
    if access_log.access_log_id is None:
        return None

    return access_log_dao.select_one(access_log)
