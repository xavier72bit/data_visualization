from typing import List

from data_visualization.dao import DaoInterface
from data_visualization.utils import logging_util
from data_visualization.domain.plot_result import PlotResult
from data_visualization.dao import BasicSqlGenerator, SqlParamGenerator

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
plot_result_basic_sql_generator = BasicSqlGenerator("plot_result", PlotResult)

# -----------------------------------------------------
# 初始化SQL参数工具
# -----------------------------------------------------

# 绑定本模块的logger
SqlParamGenerator.init_logger(plot_result_dao_logger)
plot_result_sql_param_generator = SqlParamGenerator()


# -----------------------------------------------------
# 定义本模块的Dao类
# -----------------------------------------------------


class PlotResultDao(DaoInterface):
    def insert_one_exc(self, plot_result: PlotResult) -> int:
        """
        单条INSERT操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        insert_sql = plot_result_basic_sql_generator.insert_sql()
        sql_params = plot_result_sql_param_generator.get_all_column_value(plot_result)

        try:
            result = self._execute_cursor.execute(insert_sql, sql_params)
        except Exception as err:
            self._logger.error("单条INSERT操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            self._logger.info("单条INSERT操作已执行，受影响行数: {0}".format(result))

        return result

    def delete_one_exc(self, plot_result: PlotResult) -> int:
        """
        根据plot_result_id，单条DELETE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        delete_sql = plot_result_basic_sql_generator.delete_sql()
        sql_params = plot_result_sql_param_generator.get_pk_value(plot_result)

        try:
            result = self._execute_cursor.execute(delete_sql, sql_params)
        except Exception as err:
            self._logger.error("根据plot_result_id单条DELETE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            self._logger.info("根据plot_result_id单条DELETE操作已执行，受影响行数: {0}".format(result))

        return result

    def update_one_exc(self, plot_result: PlotResult) -> int:
        """
        根据plot_result_id，单条UPDATE操作

        :return: 操作影响行数（该返回值仅为测试用例test_dao中的effect_row变量服务）
        :rtype: int
        """
        update_sql = plot_result_basic_sql_generator.update_sql()
        sql_params = plot_result_sql_param_generator.get_all_column_value(plot_result) + plot_result_sql_param_generator.get_pk_value(plot_result)

        try:
            result = self._execute_cursor.execute(update_sql, sql_params)
        except Exception as err:
            self._logger.error("根据plot_result_id单条UPDATE操作执行失败，错误原因: {0}".format(err))
            result = 0
        else:
            self._logger.info("根据plot_result_id单条UPDATE操作已执行，受影响行数: {0}".format(result))

        return result

    def select_one_exc_by_pk(self, plot_result: PlotResult) -> PlotResult | None:
        """
        根据plot_result_id，单条SELECT操作
        """
        select_one_by_pk_sql = plot_result_basic_sql_generator.select_one()
        sql_params = plot_result_sql_param_generator.get_pk_value(plot_result)

        result = self._execute_cursor.execute(select_one_by_pk_sql, sql_params)

        if result:
            self._logger.info("根据plot_result_id，单条SELECT操作，查询到{0}条结果".format(result))

            try:
                select_result = self._execute_cursor.fetchone()
                plot_result_result = PlotResult(**select_result)
            except Exception as select_exc_err:
                self._logger.warning("row转换为数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result

        else:
            self._logger.info("根据plot_result_id，单条SELECT操作，未查到任何结果")
            return None

    def select_list_exc_by_column_name(self, plot_result: PlotResult, column_name: str) -> List[PlotResult] | None:
        """
        根据除主键外的字段名，批量SELECT操作
        """
        select_list_by_column_name_sql = plot_result_basic_sql_generator.select_list(column_name)
        sql_params = plot_result_sql_param_generator.get_column_value(plot_result, column_name)

        result = self._execute_cursor.execute(select_list_by_column_name_sql, sql_params)

        if result:
            self._logger.info("根据{0}，批量SELECT操作，查询到{1}条结果".format(column_name, result))
            plot_result_result_list = []

            try:
                # 遍历查询到的所有row
                for select_result in self._execute_cursor:
                    plot_result_result = PlotResult(**select_result)

                    plot_result_result_list.append(plot_result_result)
            except Exception as select_exc_err:
                self._logger.warning("row转换数据对象失败, {0}".format(select_exc_err))
                return None
            else:
                return plot_result_result_list

        else:
            self._logger.info("根据{0}，批量SELECT操作，未查到任何结果".format(column_name))
            return None


# -----------------------------------------------------
# 为PlotResultDao绑定logger
# -----------------------------------------------------

PlotResultDao.init_logger(plot_result_dao_logger)
