from api.domain.plot_task import PlotTask
from utils.pymysql_util import db_util_logger


class PlotTaskDao:
    """
    plot_task表的操作
    """
    def __init__(self, cursor):
        self._execute_cursor = cursor

    def insert_exc(self, plot_task: PlotTask):
        insert_sql = 'INSERT INTO plot_task (plot_task_id, plot_task_create_date_time, plot_task_finish_date_time, plot_task_state, access_log_id, delete_flag) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (plot_task.plot_task_id,
                  plot_task.plot_task_create_date_time,
                  plot_task.plot_task_finish_date_time,
                  plot_task.plot_task_state,
                  plot_task.access_log_id,
                  plot_task.delete_flag)

        return self._execute_cursor.execute(insert_sql, params)

    def delete_exc(self, plot_task: PlotTask):
        delete_sql = 'DELETE FROM plot_task WHERE plot_task_id = %s'
        params = (plot_task.plot_task_id,)

        return self._execute_cursor.execute(delete_sql, params)

    def update_exc(self, plot_task: PlotTask):
        update_sql = 'UPDATE plot_task SET plot_task_id = %s, plot_task_create_date_time = %s, plot_task_finish_date_time = %s, plot_task_state = %s, access_log_id = %s, delete_flag = %s WHERE plot_task_id = %s'
        params = (plot_task.plot_task_id,
                  plot_task.plot_task_create_date_time,
                  plot_task.plot_task_finish_date_time,
                  plot_task.plot_task_state,
                  plot_task.access_log_id,
                  plot_task.delete_flag,
                  plot_task.plot_task_id)

        return self._execute_cursor.execute(update_sql, params)

    def select_one_exc_by_id(self, plot_task: PlotTask):
        select_one_by_id_sql = 'SELECT plot_task_id, plot_task_create_date_time, plot_task_finish_date_time, plot_task_state, access_log_id, delete_flag FROM plot_task WHERE plot_task_id = %s LIMIT 0, 1'
        params = (plot_task.plot_task_id,)

        exc_result = self._execute_cursor.execute(select_one_by_id_sql, params)

        if exc_result:
            try:
                db_util_logger.info("select_one_exc_by_id查询到{0}条结果".format(exc_result))
                select_result = self._execute_cursor.fetchone()
                plot_task_result = PlotTask(select_result['plot_task_id'],
                                            select_result['plot_task_create_date_time'],
                                            select_result['plot_task_finish_date_time'],
                                            select_result['plot_task_state'],
                                            select_result['access_log_id'],
                                            select_result['delete_flag'])
            except Exception as select_exc_err:
                db_util_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_task_result
        else:
            db_util_logger.info("select_one_exc_by_id未查询到任何结果")
            return None

    def select_list_exc_by_access_log_id(self, plot_task: PlotTask):
        select_list_by_access_log_id_sql = 'SELECT plot_task_id, plot_task_create_date_time, plot_task_finish_date_time, plot_task_state, access_log_id, delete_flag FROM plot_task WHERE access_log_id LIKE %s'
        params = (plot_task.access_log_id,)

        exc_result = self._execute_cursor.execute(select_list_by_access_log_id_sql, params)
        plot_task_result_list = []

        if exc_result:
            try:
                db_util_logger.info("select_list_exc_by_access_log_id查询到{0}条结果".format(exc_result))
                for select_result in self._execute_cursor:
                    plot_task_result = PlotTask(select_result['plot_task_id'],
                                                select_result['plot_task_create_date_time'],
                                                select_result['plot_task_finish_date_time'],
                                                select_result['plot_task_state'],
                                                select_result['access_log_id'],
                                                select_result['delete_flag'])

                    plot_task_result_list.append(plot_task_result)
            except Exception as select_exc_err:
                db_util_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_task_result_list
        else:
            db_util_logger.info("select_list_exc_by_access_log_id未查询到任何结果")
            return None