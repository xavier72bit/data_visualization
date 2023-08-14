import uuid

from project_common import DATE_TIME_NOW
from data_visualization.utils import logging_util
from data_visualization.domain.access_log import AccessLog
from data_visualization.dao.access_log_dao import AccessLogDao

__all__ = ["creat_a_new_access_log"]

# -----------------------------------------------------
# 初始化模块日志
# -----------------------------------------------------

access_log_service_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))

# -----------------------------------------------------
# 功能函数
# -----------------------------------------------------


def creat_a_new_access_log(access_ip: str, access_token: str, access_log_message: str) -> str:
    """
    新建一条access_log，返回access_log_id

    :return: access_log_id
    :rtype: str
    """
    new_access_log = AccessLog(access_log_id=str(uuid.uuid4()),
                               access_date_time=DATE_TIME_NOW,
                               access_token=access_token,
                               access_log_message=access_log_message,
                               access_ip=access_ip)

    with AccessLogDao() as ald:
        ald.insert_one_exc(new_access_log)

    access_log_service_logger.info("新建access_log，access_log_id={0}".format(new_access_log.access_log_id))
    return new_access_log.access_log_id


def read_access_count_by_ip(access_ip_address):
    """
    根据ip地址统计访问量
    """
    access_log = AccessLog(access_ip=access_ip_address)

    with AccessLogDao() as ald:
        access_log_list = ald.select_list_exc_by_column_name(access_log, 'access_ip')

    if access_log_list:
        access_count = len(access_log_list)
        access_log_service_logger.info("根据ip: {0}，查询到{1}次访问记录".format(access_ip_address, access_count))
        return access_count
    else:
        access_log_service_logger.info("根据ip: {0}，未查询到访问记录".format(access_ip_address))
        return 0
