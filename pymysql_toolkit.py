import pymysql
import config_util
import logging_util
from dbutils.pooled_db import PooledDB

__all__ = ["MysqlConnection"]

# -----------------------------------------------------
# 模块初始化
# -----------------------------------------------------

# 初始化本模块的日志
db_util_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', 'db_util.log')

# 导入配置
database_connection_pool_config = config_util.read_yaml('properties.yaml')['database_connection_pool']
db_util_logger.info('数据库连接池配置：{0}'.format(database_connection_pool_config))

# -----------------------------------------------------
# 数据库连接池初始化
# -----------------------------------------------------

try:
    db_util_logger.info('开始初始化数据库连接池')
    connection_pool = PooledDB(creator=pymysql,
                               host=database_connection_pool_config['host'],
                               database=database_connection_pool_config['db'],
                               user=database_connection_pool_config['user'],
                               password=database_connection_pool_config['password'],
                               port=database_connection_pool_config['port'],
                               charset=database_connection_pool_config['charset'],
                               mincached=database_connection_pool_config['min_cached'],
                               maxcached=database_connection_pool_config['max_cached'],
                               maxshared=database_connection_pool_config['max_shared'],
                               maxconnections=database_connection_pool_config['max_connections'],
                               blocking=database_connection_pool_config['blocking'],
                               maxusage=database_connection_pool_config['max_usage'],
                               setsession=database_connection_pool_config['set_session'],
                               reset=database_connection_pool_config['reset']
                               )
except Exception as e:
    db_util_logger.critical('初始化数据库连接池失败，错误: {0}'.format(e))
else:
    db_util_logger.info('数据库初始化成功')


# -----------------------------------------------------
# MySQL数据库连接 工具类
# -----------------------------------------------------

class MysqlConnection:
    """
    MySQL连接
    """

    def __init__(self, transaction=False):
        self._transaction = transaction

    def __enter__(self):
        db_util_logger.debug("从连接池获取连接")

        try:
            self._this_connection = connection_pool.connection()
        except Exception as get_connection_err:
            db_util_logger.error("MySQL连接开启失败，错误原因：{0}".format(get_connection_err))
        else:
            db_util_logger.info("MySQL连接开启，当前连接{0}".format(self._this_connection))

        try:
            self._this_cursor = self._this_connection.cursor(pymysql.cursors.DictCursor)
        except Exception as get_cursor_err:
            db_util_logger.error("MySQL光标获取失败，错误原因：{0}".format(get_cursor_err))
        else:
            db_util_logger.info("MySQL光标获取成功，当前光标{0}".format(self._this_cursor))

        # 判断是否显式开启事务
        if self._transaction:
            self._this_connection.begin()
            db_util_logger.info("开启事务")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is None:
            if self._transaction:
                # 未发生异常提交事务
                self._this_connection.commit()
                db_util_logger.info("事务已提交")
        else:
            if self._transaction:
                # 发生异常回滚
                self._this_connection.rollback()
                db_util_logger.info("事务已回滚")

        # 退出环境时自动关闭连接与光标
        self._this_cursor.close()
        db_util_logger.info('光标：{0}，已关闭'.format(self._this_cursor))
        self._this_connection.close()
        db_util_logger.info('连接：{0}，已关闭'.format(self._this_connection))

    def get_cursor(self):
        """
        从数据库连接中获取光标

        :return: cursor
        """
        return self._this_cursor


# -----------------------------------------------------
# Domain 数据对象 工具类
# -----------------------------------------------------

class AccessLog:
    __slots__ = ['access_log_id', 'access_date_time', 'access_token',
                 'access_state', 'delete_flag', 'access_log_message']

    def __init__(self, access_log_id, access_date_time, access_token,
                 access_state, delete_flag, access_log_message):
        self.access_log_id = access_log_id
        self.access_date_time = access_date_time
        self.access_token = access_token
        self.access_state = access_state
        self.delete_flag = delete_flag
        self.access_log_message = access_log_message


class PlotResult:
    __slots__ = ['plot_result_id', 'plot_task_id', 'plot_result_finish_date_time',
                 'plot_result_finish_state', 'plot_result_local_path', 'plot_result_upload_date_time',
                 'plot_result_upload_state', 'plot_result_url', 'delete_flag']

    def __init__(self, plot_result_id, plot_task_id, plot_result_finish_date_time,
                 plot_result_finish_state, plot_result_local_path, plot_result_upload_date_time,
                 plot_result_upload_state, plot_result_url, delete_flag):
        self.plot_result_id = plot_result_id
        self.plot_task_id = plot_task_id
        self.plot_result_finish_date_time = plot_result_finish_date_time
        self.plot_result_finish_state = plot_result_finish_state
        self.plot_result_local_path = plot_result_local_path
        self.plot_result_upload_date_time = plot_result_upload_date_time
        self.plot_result_upload_state = plot_result_upload_state
        self.plot_result_url = plot_result_url
        self.delete_flag = delete_flag


class PlotTask:
    __slots__ = ['plot_task_id', 'plot_task_create_date_time', 'plot_task_finish_date_time',
                 'plot_task_state', 'access_log_id', 'delete_flag']

    def __init__(self, plot_task_id, plot_task_create_date_time, plot_task_finish_date_time,
                 plot_task_state, access_log_id, delete_flag):
        self.plot_task_id = plot_task_id
        self.plot_task_create_date_time = plot_task_create_date_time
        self.plot_task_finish_date_time = plot_task_finish_date_time
        self.plot_task_state = plot_task_state
        self.access_log_id = access_log_id
        self.delete_flag = delete_flag


# -----------------------------------------------------
# Dao 层 工具类
# -----------------------------------------------------

class AccessLogDao:
    pass


class PlotResultDao:
    pass


class PlotTaskDao:
    pass


# -----------------------------------------------------
# Service 层 工具类
# -----------------------------------------------------

class AccessLogService:
    pass


class PlotResultService:
    pass


class PlotTaskService:
    pass
