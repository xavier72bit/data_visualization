import pymysql
from utils import config_util, logging_util
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor

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
            self._this_cursor = self._this_connection.cursor(DictCursor)
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
