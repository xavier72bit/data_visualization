from api.domain.access_log import AccessLog
from utils.pymysql_util import db_util_logger


__all__ = ["AccessLogDao"]


class AccessLogDao:
    """
    access_log表的操作
    """
    def __init__(self, cursor):
        self._execute_cursor = cursor

    def insert_exc(self, access_log: AccessLog):
        insert_sql = 'INSERT INTO access_log (access_log_id, access_date_time, access_token, access_state, delete_flag, access_log_message) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (access_log.access_log_id,
                  access_log.access_date_time,
                  access_log.access_token,
                  access_log.access_state,
                  access_log.delete_flag,
                  access_log.access_log_message)

        return self._execute_cursor.execute(insert_sql, params)

    def delete_exc(self, access_log: AccessLog):
        delete_sql = 'DELETE FROM access_log WHERE access_log_id = %s'
        params = (access_log.access_log_id,)

        return self._execute_cursor.execute(delete_sql, params)

    def update_exc(self, access_log: AccessLog):
        update_sql = 'UPDATE access_log SET access_date_time = %s, access_token = %s, access_state = %s, delete_flag = %s, access_log_message = %s WHERE access_log_id = %s'
        params = (access_log.access_date_time,
                  access_log.access_token,
                  access_log.access_state,
                  access_log.delete_flag,
                  access_log.access_log_message,
                  access_log.access_log_id)

        return self._execute_cursor.execute(update_sql, params)

    def select_one_exc_by_id(self, access_log: AccessLog):
        select_one_by_id_sql = 'SELECT access_log_id, access_date_time, access_token, access_state, delete_flag, access_log_message FROM access_log WHERE access_log_id = %s LIMIT 0, 1'
        params = (access_log.access_log_id,)

        exc_result = self._execute_cursor.execute(select_one_by_id_sql, params)

        if exc_result:
            try:
                db_util_logger.info("select_one_exc_by_id查询到{0}条结果".format(exc_result))
                select_result = self._execute_cursor.fetchone()
                access_log_result = AccessLog(select_result['access_log_id'],
                                              select_result['access_date_time'],
                                              select_result['access_token'],
                                              select_result['access_state'],
                                              select_result['delete_flag'],
                                              select_result['access_log_message'])
            except Exception as select_exc_err:
                db_util_logger.warning("row转换为数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return access_log_result
        else:
            db_util_logger.info("select_one_exc_by_id未查到任何结果")
            return None

    def select_list_exc_by_access_token(self, access_log: AccessLog):
        select_list_by_access_token_sql = 'SELECT access_log_id, access_date_time, access_token, access_state, delete_flag, access_log_message FROM access_log WHERE access_token LIKE %s'
        params = (access_log.access_token,)

        exc_result = self._execute_cursor.execute(select_list_by_access_token_sql, params)
        access_log_result_list = []

        if exc_result:
            try:
                db_util_logger.info("select_list_exc_by_access_token查询到{0}条结果".format(exc_result))
                # 遍历查询到的所有row
                for select_result in self._execute_cursor:
                    access_log_result = AccessLog(select_result['access_log_id'],
                                                  select_result['access_date_time'],
                                                  select_result['access_token'],
                                                  select_result['access_state'],
                                                  select_result['delete_flag'],
                                                  select_result['access_log_message'])

                    access_log_result_list.append(access_log_result)
            except Exception as select_exc_err:
                db_util_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return access_log_result_list
        else:
            db_util_logger.info("select_list_exc_by_access_token未查到任何结果")
            return None