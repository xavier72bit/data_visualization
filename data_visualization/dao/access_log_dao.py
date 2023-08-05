from typing import List
from pymysql.cursors import DictCursor

from data_visualization.utils import logging_util
from data_visualization.domain.access_log import AccessLog
from data_visualization.utils.pymysql_util import connection_pool

__all__ = ["AccessLogDao"]

# 初始化模块日志
access_log_dao_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))


class AccessLogDao:
    """
    access_log表的操作
    """

    def __init__(self):
        access_log_dao_logger.info("初始化access_log_dao对象")
        access_log_dao_logger.info(self)

    def __enter__(self):
        """
        自动获取mysql连接与光标

        :return: AccessLogDao
        """
        access_log_dao_logger.info("获取MySQL连接")
        try:
            self._mysql_connection = connection_pool.connection()
        except Exception as e:
            access_log_dao_logger.error("获取MySQL连接失败，错误原因: {0}".format(e))
        else:
            access_log_dao_logger.info("获取MySQL连接成功")

        access_log_dao_logger.info("获取MySQL操作光标")
        try:
            self._execute_cursor = self._mysql_connection.cursor(DictCursor)
        except Exception as e:
            access_log_dao_logger.error("MySQL光标获取失败，错误原因: {0}".format(e))
        else:
            access_log_dao_logger.info("MySQL光标获取成功")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出时自动关闭mysql连接与光标
        """
        access_log_dao_logger.info("关闭MySQL光标: {0}".format(self._execute_cursor))
        self._execute_cursor.close()

        access_log_dao_logger.info("关闭MySQL连接: {0}".format(self._mysql_connection))
        self._mysql_connection.close()

    def insert_one_exc(self, access_log: AccessLog) -> int:
        """
        单条INSERT操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        insert_sql = 'INSERT INTO access_log (access_log_id, access_date_time, access_token, access_state, access_log_message) VALUES (%s, %s, %s, %s, %s)'
        params = (access_log.access_log_id,
                  access_log.access_date_time,
                  access_log.access_token,
                  access_log.access_state,
                  access_log.access_log_message)

        try:
            result = self._execute_cursor.execute(insert_sql, params)
        except Exception as err:
            access_log_dao_logger.error("单条INSERT操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            access_log_dao_logger.info("单条INSERT操作已执行，受影响行数: {0}".format(result))

        return result

    def delete_one_exc_by_id(self, access_log: AccessLog) -> int:
        """
        根据access_log_id，单条DELETE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        delete_sql = 'DELETE FROM access_log WHERE access_log_id = %s'
        params = (access_log.access_log_id,)

        try:
            result = self._execute_cursor.execute(delete_sql, params)
        except Exception as err:
            access_log_dao_logger.error("根据access_log_id单条DELETE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            access_log_dao_logger.info("根据access_log_id单条DELETE操作已执行，受影响行数: {0}".format(result))

        return result

    def update_one_exc_by_id(self, access_log: AccessLog) -> int:
        """
        根据access_log_id，单条UPDATE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        update_sql = 'UPDATE access_log SET access_date_time = %s, access_token = %s, access_state = %s, access_log_message = %s WHERE access_log_id = %s'
        params = (access_log.access_date_time,
                  access_log.access_token,
                  access_log.access_state,
                  access_log.access_log_message,
                  access_log.access_log_id)

        try:
            result = self._execute_cursor.execute(update_sql, params)
        except Exception as err:
            access_log_dao_logger.error("根据access_log_id单条UPDATE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            access_log_dao_logger.info("根据access_log_id单条UPDATE操作已执行，受影响行数: {0}".format(result))

        return result

    def select_one_exc_by_id(self, access_log: AccessLog) -> AccessLog | None:
        """
        根据access_log_id，单条SELECT操作
        """
        select_one_by_id_sql = 'SELECT access_log_id, access_date_time, access_token, access_state, access_log_message FROM access_log WHERE access_log_id = %s LIMIT 0, 1'
        params = (access_log.access_log_id,)

        result = self._execute_cursor.execute(select_one_by_id_sql, params)

        if result:
            access_log_dao_logger.info("根据access_log_id，单条SELECT操作，查询到{0}条结果".format(result))

            try:
                select_result = self._execute_cursor.fetchone()
                access_log_result = AccessLog(select_result['access_log_id'],
                                              select_result['access_date_time'],
                                              select_result['access_token'],
                                              select_result['access_state'],
                                              select_result['access_log_message'])
            except Exception as select_exc_err:
                access_log_dao_logger.warning("row转换为数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return access_log_result

        else:
            access_log_dao_logger.info("根据access_log_id，单条SELECT操作，未查到任何结果")
            return None

    def select_list_exc_by_access_token(self, access_log: AccessLog) -> List[AccessLog] | None:
        """
        根据access_token，批量SELECT操作
        """
        select_list_by_access_token_sql = 'SELECT access_log_id, access_date_time, access_token, access_state, access_log_message FROM access_log WHERE access_token LIKE %s'
        params = (access_log.access_token,)

        result = self._execute_cursor.execute(select_list_by_access_token_sql, params)

        if result:
            access_log_dao_logger.info("根据access_token，批量SELECT操作，查询到{0}条结果".format(result))
            access_log_result_list = []

            try:
                # 遍历查询到的所有row
                for select_result in self._execute_cursor:
                    access_log_result = AccessLog(select_result['access_log_id'],
                                                  select_result['access_date_time'],
                                                  select_result['access_token'],
                                                  select_result['access_state'],
                                                  select_result['access_log_message'])

                    access_log_result_list.append(access_log_result)
            except Exception as select_exc_err:
                access_log_dao_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return access_log_result_list

        else:
            access_log_dao_logger.info("根据access_token，批量SELECT操作，未查到任何结果")
            return None
