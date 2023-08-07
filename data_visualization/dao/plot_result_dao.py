from typing import List

from data_visualization.dao import DaoInterface
from data_visualization.utils import logging_util
from data_visualization.dao import BasicSqlGenerator
from data_visualization.domain.plot_result import PlotResult

__all__ = ["PlotResultDao"]

# -----------------------------------------------------
# 初始化模块日志
# -----------------------------------------------------

plot_result_dao_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))

# -----------------------------------------------------
# 初始化SQL拼接模版工具
# -----------------------------------------------------

# 绑定本模块logger
BasicSqlGenerator.init_logger(plot_result_dao_logger)
basic_sql_generator = BasicSqlGenerator("plot_result", PlotResult)

# -----------------------------------------------------
# 定义本模块的Dao类
# -----------------------------------------------------


class PlotResultDao(DaoInterface):
    """
    plot_result表的操作
    """

    def __init__(self):
        super().__init__()
        self.insert_sql = basic_sql_generator.insert_sql()
        self.delete_sql = basic_sql_generator.delete_sql()
        self.update_sql = basic_sql_generator.update_sql()
        self.select_one_by_id_sql = basic_sql_generator.select_one()
        self.select_list_by_access_log_id_sql = basic_sql_generator.select_list("access_log_id")

    def insert_one_exc(self, plot_result: PlotResult) -> int:
        """
        单条INSERT操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        sql_params = (plot_result.plot_result_id,
                      plot_result.access_log_id,
                      plot_result.plot_result_finish_date_time,
                      plot_result.plot_result_finish_state,
                      plot_result.plot_result_local_path,
                      plot_result.plot_result_upload_date_time,
                      plot_result.plot_result_upload_state,
                      plot_result.plot_result_url)

        try:
            result = self._execute_cursor.execute(self.insert_sql, sql_params)
        except Exception as err:
            self.logger.error("单条INSERT操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            self.logger.info("单条INSERT操作已执行，受影响行数: {0}".format(result))

        return result

    def delete_one_exc_by_id(self, plot_result: PlotResult) -> int:
        """
        根据plot_result_id，单条DELETE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        sql_params = (plot_result.plot_result_id,)

        try:
            result = self._execute_cursor.execute(self.delete_sql, sql_params)
        except Exception as err:
            self.logger.error("根据plot_result_id单条DELETE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            self.logger.info("根据plot_result_id单条DELETE操作已执行，受影响行数: {0}".format(result))

        return result

    def update_one_exc_by_id(self, plot_result: PlotResult) -> int:
        """
        根据plot_result_id，单条UPDATE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        sql_params = (plot_result.access_log_id,
                      plot_result.plot_result_finish_date_time,
                      plot_result.plot_result_finish_state,
                      plot_result.plot_result_local_path,
                      plot_result.plot_result_upload_date_time,
                      plot_result.plot_result_upload_state,
                      plot_result.plot_result_url,
                      plot_result.plot_result_id,
                      plot_result.access_log_id)

        try:
            result = self._execute_cursor.execute(self.update_sql, sql_params)
        except Exception as err:
            self.logger.error("根据plot_result_id单条UPDATE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            self.logger.info("根据根据plot_result_id单条UPDATE操作已执行，受影响行数: {0}".format(result))

        return result

    def select_one_exc_by_id(self, plot_result: PlotResult) -> PlotResult | None:
        """
        根据plot_result_id，单条SELECT操作
        """
        sql_params = (plot_result.plot_result_id,)

        result = self._execute_cursor.execute(self.select_one_by_id_sql, sql_params)

        if result:
            self.logger.info("根据plot_result_id，单条SELECT操作，查询到{0}条结果".format(result))

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
                self.logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result

        else:
            self.logger.info("select_one_exc_by_id未查到任何结果")
            return None

    def select_list_exc_by_access_log_id(self, plot_result: PlotResult) -> List[PlotResult] | None:
        """
        根据access_log_id，批量SELECT操作
        """
        sql_params = (plot_result.access_log_id,)

        result = self._execute_cursor.execute(self.select_list_by_access_log_id_sql, sql_params)

        if result:
            self.logger.info("根据access_token，批量SELECT操作，查询到{0}条结果".format(result))
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
                self.logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result_list

        else:
            self.logger.info("select_list_exc_by_plot_task_id未查到任何结果")
            return None


# -----------------------------------------------------
# 为PlotResultDao绑定logger
# -----------------------------------------------------

PlotResultDao.init_logger(plot_result_dao_logger)
