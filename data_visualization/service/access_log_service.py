import uuid
from typing import List

from project_common import DATE_TIME_NOW
from data_visualization.domain.access_log import AccessLog
from data_visualization.dao.access_log_dao import AccessLogDao

__all__ = ["creat_a_new_access_log", "read_a_access_log_by_id", "read_access_list_by_token"]


def creat_a_new_access_log(access_token: str, access_log_message: str) -> str:
    """
    新建一条access_log，返回access_log_id

    :return: access_log_id
    :rtype: str
    """
    new_access_log = AccessLog(access_log_id=uuid.uuid4(),
                               access_date_time=DATE_TIME_NOW,
                               access_token=access_token,
                               access_log_message=access_log_message)

    with AccessLogDao() as ald:
        ald.insert_one_exc(new_access_log)

    return new_access_log.access_log_id


def read_a_access_log_by_id(access_log_id: str) -> AccessLog:
    """
    根据access_log_id，读取一条access_log

    :return: access_log
    :rtype: AccessLog
    """
    access_log = AccessLog(access_log_id=access_log_id)

    with AccessLogDao() as ald:
        access_log = ald.select_one_exc_by_pk(access_log)

    return access_log


def read_access_list_by_token(access_token: str) -> List[AccessLog]:
    """
    根据access_token，读取access_log列表

    :return: access_log_list
    :rtype: List[AccessLog]
    """
    access_log = AccessLog(access_token=access_token)

    with AccessLogDao() as ald:
        access_log_list = ald.select_list_exc_by_column_name(access_log)

    return access_log_list
