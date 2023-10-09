from visualization.utils.do.data_object import AccessLog
from visualization.utils.db.pymysql_util import MysqlUtil


def insert(access_log: AccessLog) -> int:
    """
    INSERT

    :return: 操作影响行数
    :rtype: int
    """
    sql = 'INSERT INTO access_log (access_log_id, access_date_time, access_ip, access_url, access_param) VALUES (%s, %s, %s, %s, %s);'
    args = (
        access_log.access_log_id,
        access_log.access_date_time,
        access_log.access_ip,
        access_log.access_url,
        access_log.access_param
    )

    with MysqlUtil() as mu:
        result = mu.insert(sql, args)

    return result


def delete(access_log: AccessLog) -> int:
    """
    DELETE

    :return: 操作影响行数
    :rtype: int
    """
    sql = 'DELETE FROM access_log WHERE access_log_id = %s;'
    args = (
        access_log.access_log_id,
    )

    with MysqlUtil() as mu:
        result = mu.delete(sql, args)

    return result


def update(access_log: AccessLog) -> int:
    """
    UPDATE

    :return: 操作影响行数
    :rtype: int
    """
    sql = 'UPDATE access_log SET access_log_id = %s, access_date_time = %s, access_ip = %s, access_url = %s, access_param = %s WHERE access_log_id = %s;'
    args = (
        access_log.access_log_id,
        access_log.access_date_time,
        access_log.access_ip,
        access_log.access_url,
        access_log.access_param,
        access_log.access_log_id
    )

    with MysqlUtil() as mu:
        result = mu.update(sql, args)

    return result


def select_one(access_log: AccessLog) -> AccessLog | None:
    """
    SELECT

    :return: AccessLog对象
    :rtype: dict | None
    """
    sql = 'SELECT access_log_id, access_date_time, access_ip, access_url, access_param FROM access_log WHERE access_log_id = %s LIMIT 0, 1;'
    args = (
        access_log.access_log_id,
    )

    with MysqlUtil() as mu:
        result = mu.select_one(sql, args)

    if result is not None:
        access_log_result = AccessLog(**result)
    else:
        access_log_result = None

    return access_log_result


def select_list_by_access_ip(access_log: AccessLog) -> list[AccessLog] | None:
    """
    SELECT

    :return: 包含多个AccessLog数据对象的列表
    :rtype: list[AccessLog] | None
    """
    sql = 'SELECT access_log_id, access_date_time, access_ip, access_url, access_param FROM access_log WHERE access_ip LIKE %s;'
    args = (
        access_log.access_ip,
    )

    with MysqlUtil() as mu:
        result = mu.select_list(sql, args)

    # 这一步是判断result是否为空列表或None
    if result:
        access_log_result_list = [AccessLog(**row) for row in result]
    else:
        access_log_result_list = None

    return access_log_result_list
