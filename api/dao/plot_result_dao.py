from api.domain.plot_result import PlotResult
from utils.pymysql_util import db_util_logger


__all__ = ["PlotResultDao"]


class PlotResultDao:
    """
    plot_result表的操作
    """
    def __init__(self, cursor):
        self._execute_cursor = cursor

    def insert_exc(self, plot_result: PlotResult):
        insert_sql = 'INSERT INTO plot_result (plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url, delete_flag) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        params = (plot_result.plot_result_id,
                  plot_result.plot_task_id,
                  plot_result.plot_result_finish_date_time,
                  plot_result.plot_result_finish_state,
                  plot_result.plot_result_local_path,
                  plot_result.plot_result_upload_date_time,
                  plot_result.plot_result_upload_state,
                  plot_result.plot_result_url,
                  plot_result.delete_flag)

        return self._execute_cursor.execute(insert_sql, params)

    def delete_exc(self, plot_result: PlotResult):
        delete_sql = 'DELETE FROM plot_result WHERE plot_result_id = %s'
        params = (plot_result.plot_result_id,)

        return self._execute_cursor.execute(delete_sql, params)

    def update_exc(self, plot_result: PlotResult):
        update_sql = 'UPDATE plot_result SET plot_task_id = %s, plot_result_finish_date_time = %s, plot_result_finish_state = %s, plot_result_local_path = %s, plot_result_upload_date_time = %s, plot_result_upload_state = %s, plot_result_url = %s, delete_flag = %s WHERE plot_result_id = %s'
        params = (plot_result.plot_task_id,
                  plot_result.plot_result_finish_date_time,
                  plot_result.plot_result_finish_state,
                  plot_result.plot_result_local_path,
                  plot_result.plot_result_upload_date_time,
                  plot_result.plot_result_upload_state,
                  plot_result.plot_result_url,
                  plot_result.delete_flag,
                  plot_result.plot_result_id,
                  plot_result.plot_task_id)

        return self._execute_cursor.execute(update_sql, params)

    def select_one_exc_by_id(self, plot_result: PlotResult):
        select_one_by_id_sql = 'SELECT plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url, delete_flag FROM plot_result WHERE plot_result_id = %s LIMIT 0, 1'
        params = (plot_result.plot_result_id,)

        exc_result = self._execute_cursor.execute(select_one_by_id_sql, params)

        if exc_result:
            try:
                db_util_logger.info("select_one_exc_by_id查询到{0}条结果".format(exc_result))
                select_result = self._execute_cursor.fetchone()
                plot_result_result = PlotResult(select_result['plot_result_id'],
                                                select_result['plot_task_id'],
                                                select_result['plot_result_finish_date_time'],
                                                select_result['plot_result_finish_state'],
                                                select_result['plot_result_local_path'],
                                                select_result['plot_result_upload_date_time'],
                                                select_result['plot_result_upload_state'],
                                                select_result['plot_result_url'],
                                                select_result['delete_flag'])
            except Exception as select_exc_err:
                db_util_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result
        else:
            db_util_logger.info("select_one_exc_by_id未查到任何结果")
            return None

    def select_list_exc_by_plot_task_id(self, plot_result: PlotResult):
        select_list_by_plot_task_id_sql = 'SELECT plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time, plot_result_upload_state, plot_result_url, delete_flag FROM plot_result WHERE plot_task_id LIKE %s'
        params = (plot_result.plot_task_id,)

        exc_result = self._execute_cursor.execute(select_list_by_plot_task_id_sql, params)
        plot_result_result_list = []

        if exc_result:
            try:
                db_util_logger.info("select_list_exc_by_plot_task_id查询到{0}条结果".format(exc_result))
                for select_result in self._execute_cursor:
                    plot_result_result = PlotResult(select_result['plot_result_id'],
                                                    select_result['plot_task_id'],
                                                    select_result['plot_result_finish_date_time'],
                                                    select_result['plot_result_finish_state'],
                                                    select_result['plot_result_local_path'],
                                                    select_result['plot_result_upload_date_time'],
                                                    select_result['plot_result_upload_state'],
                                                    select_result['plot_result_url'],
                                                    select_result['delete_flag'])

                    plot_result_result_list.append(plot_result_result)
            except Exception as select_exc_err:
                db_util_logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result_list
        else:
            db_util_logger.info("select_list_exc_by_plot_task_id未查到任何结果")
            return None