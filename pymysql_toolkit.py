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
# MySQL数据库连接
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
# Domain 数据对象
# -----------------------------------------------------
# TODO: 加上注释
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
# Dao 数据库表操作
# -----------------------------------------------------
# TODO: 可以考虑使用工厂函数去制造不同的Dao类
class AccessLogDao:
    def __init__(self, cursor):
        self._execute_cursor = cursor

    def insert_exc(self, access_log: AccessLog):
        insert_sql = 'INSERT INTO access_log (access_log_id, access_date_time, access_token, access_state, delete_flag, access_log_message) VALUES (%s, %s, %s, %s, %s, %s)'
        params = (access_log.access_log_id, access_log.access_date_time, access_log.access_token,
                  access_log.access_state, access_log.delete_flag, access_log.access_log_message)

        return self._execute_cursor.execute(insert_sql, params)

    def delete_exc(self, access_log: AccessLog):
        delete_sql = 'DELETE FROM access_log WHERE access_log_id = %s'
        params = (access_log.access_log_id,)

        return self._execute_cursor.execute(delete_sql, params)

    def update_exc(self, access_log: AccessLog):
        update_sql = 'UPDATE access_log SET access_date_time = %s, access_token = %s, access_state = %s, delete_flag = %s, access_log_message = %s WHERE access_log_id = %s'
        params = (access_log.access_date_time, access_log.access_token, access_log.access_state,
                  access_log.delete_flag, access_log.access_log_message, access_log.access_log_id)

        return self._execute_cursor.execute(update_sql, params)

    def select_one_exc_by_id(self, access_log: AccessLog):
        select_one_by_id_sql = 'SELECT access_log_id, access_date_time, access_token, access_state, delete_flag, access_log_message FROM access_log WHERE access_log_id = %s LIMIT 0, 1'
        params = (access_log.access_log_id,)

        exc_result = self._execute_cursor.execute(select_one_by_id_sql, params)
        # TODO: 换成日志
        print(exc_result)

        try:
            select_result = self._execute_cursor.fetchone()
            access_log_result = AccessLog(select_result['access_log_id'],
                                          select_result['access_date_time'],
                                          select_result['access_token'],
                                          select_result['access_state'],
                                          select_result['delete_flag'],
                                          select_result['access_log_message'])
        except Exception as select_exc_err:
            # TODO: 换成日志
            print(select_exc_err)
            return None
        else:
            return access_log_result

    def select_list_exc_by_access_token(self, access_log: AccessLog):
        select_list_by_access_token_sql = 'SELECT access_log_id, access_date_time, access_token, access_state, delete_flag, access_log_message FROM access_log WHERE access_token LIKE %s'
        params = (access_log.access_token,)

        exc_result = self._execute_cursor.execute(select_list_by_access_token_sql, params)
        # TODO: 换成日志
        print(exc_result)
        # TODO: 注意这里，如果有问题换成元组
        access_log_result_list = []

        try:
            for select_result in self._execute_cursor:
                access_log_result = AccessLog(select_result['access_log_id'],
                                              select_result['access_date_time'],
                                              select_result['access_token'],
                                              select_result['access_state'],
                                              select_result['delete_flag'],
                                              select_result['access_log_message'])

                access_log_result_list.append(access_log_result)
        except Exception as select_exc_err:
            # TODO: 换成日志
            print(select_exc_err)
            return None
        else:
            return access_log_result_list


class PlotResultDao:
    pass


class PlotTaskDao:
    pass


# -----------------------------------------------------
# Service 业务
# -----------------------------------------------------

class AccessLogService:
    pass


class PlotResultService:
    pass


class PlotTaskService:
    pass
