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

    def insert_exc(self, plot_result: PlotResult):
        insert_sql = 'INSERT INTO plot_result (plot_result_id, access_log_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        params = (plot_result.plot_result_id,
                  plot_result.access_log_id,
                  plot_result.plot_result_finish_date_time,
                  plot_result.plot_result_finish_state,
                  plot_result.plot_result_local_path,
                  plot_result.plot_result_upload_date_time,
                  plot_result.plot_result_upload_state,
                  plot_result.plot_result_url)

        return self._execute_cursor.execute(insert_sql, params)

    def delete_exc(self, plot_result: PlotResult):
        delete_sql = 'DELETE FROM plot_result WHERE plot_result_id = %s'
        params = (plot_result.plot_result_id,)

        return self._execute_cursor.execute(delete_sql, params)

    def update_exc(self, plot_result: PlotResult):
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

        return self._execute_cursor.execute(update_sql, params)

    def select_one_exc_by_id(self, plot_result: PlotResult):
        select_one_by_id_sql = 'SELECT plot_result_id, access_log_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url FROM plot_result WHERE plot_result_id = %s LIMIT 0, 1'
        params = (plot_result.plot_result_id,)

        exc_result = self._execute_cursor.execute(select_one_by_id_sql, params)

        if exc_result:
            try:
                plot_result_dao_logger.info("select_one_exc_by_id查询到{0}条结果".format(exc_result))
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

    def select_list_exc_by_access_log_id(self, plot_result: PlotResult):
        select_list_by_plot_task_id_sql = 'SELECT plot_result_id, access_log_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url FROM plot_result WHERE access_log_id LIKE %s'
        params = (plot_result.access_log_id,)

        exc_result = self._execute_cursor.execute(select_list_by_plot_task_id_sql, params)
        plot_result_result_list = []

        if exc_result:
            try:
                plot_result_dao_logger.info("select_list_exc_by_plot_task_id查询到{0}条结果".format(exc_result))
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
