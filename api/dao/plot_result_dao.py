from typing import List
from utils import logging_util
from pymysql.cursors import DictCursor
from api.domain.plot_result import PlotResult
from utils.pymysql_util import connection_pool

__all__ = ["PlotResultDao"]

# 初始化模块日志
plot_result_dao_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))


# TODO: 将dao抽象出一个类，PlotResultDao和AccessLogDao均继承自这个类
class PlotResultDao:
    """
    plot_result表的操作
    """

    def __init__(self):
        plot_result_dao_logger.info("初始化plot_result_dao对象")
        plot_result_dao_logger.info(self)

    def __enter__(self):
        """
        自动获取mysql连接与光标

        :return: PlotResultDao
        """
        plot_result_dao_logger.info("获取MySQL连接")
        try:
            self._mysql_connection = connection_pool.connection()
        except Exception as e:
            plot_result_dao_logger.error("获取MySQL连接失败，错误原因: {0}".format(e))
        else:
            plot_result_dao_logger.info("获取MySQL连接成功")

        plot_result_dao_logger.info("获取MySQL操作光标")
        try:
            self._execute_cursor = self._mysql_connection.cursor(DictCursor)
        except Exception as e:
            plot_result_dao_logger.error("MySQL光标获取失败，错误原因: {0}".format(e))
        else:
            plot_result_dao_logger.info("MySQL光标获取成功")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出时自动关闭mysql连接与光标
        """
        plot_result_dao_logger.info("关闭MySQL光标: {0}".format(self._execute_cursor))
        self._execute_cursor.close()

        plot_result_dao_logger.info("关闭MySQL连接: {0}".format(self._mysql_connection))
        self._mysql_connection.close()

    def insert_one_exc(self, plot_result: PlotResult) -> int:
        """
        单条INSERT操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        insert_sql = 'INSERT INTO plot_result (plot_result_id, access_log_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        params = (plot_result.plot_result_id,
                  plot_result.access_log_id,
                  plot_result.plot_result_finish_date_time,
                  plot_result.plot_result_finish_state,
                  plot_result.plot_result_local_path,
                  plot_result.plot_result_upload_date_time,
                  plot_result.plot_result_upload_state,
                  plot_result.plot_result_url)

        try:
            result = self._execute_cursor.execute(insert_sql, params)
        except Exception as err:
            plot_result_dao_logger.error("单条INSERT操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            plot_result_dao_logger.info("单条INSERT操作已执行，受影响行数: {0}".format(result))

        return result

    def delete_one_exc_by_id(self, plot_result: PlotResult) -> int:
        """
        根据plot_result_id，单条DELETE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        delete_sql = 'DELETE FROM plot_result WHERE plot_result_id = %s'
        params = (plot_result.plot_result_id,)

        try:
            result = self._execute_cursor.execute(delete_sql, params)
        except Exception as err:
            plot_result_dao_logger.error("根据plot_result_id单条DELETE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            plot_result_dao_logger.info("根据plot_result_id单条DELETE操作已执行，受影响行数: {0}".format(result))

        return result

    def update_one_exc_by_id(self, plot_result: PlotResult) -> int:
        """
        根据plot_result_id，单条UPDATE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        update_sql = 'UPDATE plot_result SET access_log_id = %s, plot_result_finish_date_time = %s, plot_result_finish_state = %s, plot_result_local_path = %s, plot_result_upload_date_time = %s, plot_result_upload_state = %s, plot_result_url = %s WHERE plot_result_id = %s'
        params = (plot_result.access_log_id,
                  plot_result.plot_result_finish_date_time,
                  plot_result.plot_result_finish_state,
                  plot_result.plot_result_local_path,
                  plot_result.plot_result_upload_date_time,
                  plot_result.plot_result_upload_state,
                  plot_result.plot_result_url,
                  plot_result.plot_result_id,
                  plot_result.access_log_id)

        try:
            result = self._execute_cursor.execute(update_sql, params)
        except Exception as err:
            plot_result_dao_logger.error("根据plot_result_id单条UPDATE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            plot_result_dao_logger.info("根据根据plot_result_id单条UPDATE操作已执行，受影响行数: {0}".format(result))

        return result

    def select_one_exc_by_id(self, plot_result: PlotResult) -> PlotResult | None:
        """
        根据plot_result_id，单条SELECT操作
        """
        select_one_by_id_sql = 'SELECT plot_result_id, access_log_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url FROM plot_result WHERE plot_result_id = %s LIMIT 0, 1'
        params = (plot_result.plot_result_id,)

        result = self._execute_cursor.execute(select_one_by_id_sql, params)

        if result:
            plot_result_dao_logger.info("根据plot_result_id，单条SELECT操作，查询到{0}条结果".format(result))

            try:
                select_result = self._execute_cursor.fetchone()
                plot_result_result = PlotResult(select_result['plot_result_id'],
                                                select_result['access_log_id'],
                                                select_result['plot_result_finish_date_time'],
                                                select_result['plot_result_finish_state'],
                                                select_result['plot_result_local_path'],
                                                select_result['plot_result_upload_date_time'],
                                                select_result['plot_result_upload_state'],
                                                select_result['plot_result_url'])
            except Exception as select_exc_err:
                plot_result_dao_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result

        else:
            plot_result_dao_logger.info("select_one_exc_by_id未查到任何结果")
            return None

    def select_list_exc_by_access_log_id(self, plot_result: PlotResult) -> List[PlotResult] | None:
        """
        根据access_log_id，批量SELECT操作
        """
        select_list_by_plot_task_id_sql = 'SELECT plot_result_id, access_log_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url FROM plot_result WHERE access_log_id LIKE %s'
        params = (plot_result.access_log_id,)

        result = self._execute_cursor.execute(select_list_by_plot_task_id_sql, params)

        if result:
            plot_result_dao_logger.info("根据access_token，批量SELECT操作，查询到{0}条结果".format(result))
            plot_result_result_list = []

            try:
                # 遍历查询到的所有row
                for select_result in self._execute_cursor:
                    plot_result_result = PlotResult(select_result['plot_result_id'],
                                                    select_result['access_log_id'],
                                                    select_result['plot_result_finish_date_time'],
                                                    select_result['plot_result_finish_state'],
                                                    select_result['plot_result_local_path'],
                                                    select_result['plot_result_upload_date_time'],
                                                    select_result['plot_result_upload_state'],
                                                    select_result['plot_result_url'])

                    plot_result_result_list.append(plot_result_result)
            except Exception as select_exc_err:
                plot_result_dao_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result_list

        else:
            plot_result_dao_logger.info("select_list_exc_by_plot_task_id未查到任何结果")
            return None
