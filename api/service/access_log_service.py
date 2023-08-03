import uuid
import datetime

from api.domain.access_log import AccessLog
from api.dao.access_log_dao import AccessLogDao

__all__ = ["creat_a_new_access_log"]

date_time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def creat_a_new_access_log(access_token, access_log_message) -> str:
    """
    新建一条access_log，返回access_log_id

    :return: access_log_id
    """
    new_access_log = AccessLog(access_log_id=uuid.uuid4(),
                               access_date_time=date_time_now,
                               access_token=access_token,
                               access_log_message=access_log_message)

    # 将条目插入数据库
    with AccessLogDao() as ald:
        ald.insert_exc(new_access_log)

    return new_access_log.access_log_id


if __name__ == '__main__':
    for i in range(1000):
        print(creat_a_new_access_log("test_token", "test_message"))