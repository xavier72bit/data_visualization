import pymysql
from loguru import logger
from pymysql.cursors import DictCursor
from dbutils.pooled_db import PooledDB

from visualization.utils import config_util


class MysqlConnectionPool:
    _instance = None
    _connection_pool = None
    database_connection_pool_config = config_util.read_yaml('properties.yaml')['database_connection_pool']

    def __new__(cls, *args, **kwargs):
        if cls._instance:
            return cls._instance

        cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection_pool is None:
            logger.info('数据库连接池配置：{0}'.format(self.database_connection_pool_config))

            self._connection_pool = PooledDB(
                creator=pymysql,
                host=self.database_connection_pool_config['host'],
                database=self.database_connection_pool_config['db'],
                user=self.database_connection_pool_config['user'],
                password=self.database_connection_pool_config['password'],
                port=self.database_connection_pool_config['port'],
                charset=self.database_connection_pool_config['charset'],
                mincached=self.database_connection_pool_config['min_cached'],
                maxcached=self.database_connection_pool_config['max_cached'],
                maxshared=self.database_connection_pool_config['max_shared'],
                maxconnections=self.database_connection_pool_config['max_connections'],
                blocking=self.database_connection_pool_config['blocking'],
                maxusage=self.database_connection_pool_config['max_usage'],
                setsession=self.database_connection_pool_config['set_session'],
                reset=self.database_connection_pool_config['reset']
            )

            logger.info('数据库连接池初始化成功')

    def get_connection(self):
        return self._connection_pool.connection()


class MysqlUtil:
    def __init__(self):
        self._connection_pool = MysqlConnectionPool()

    def __enter__(self):
        """
        进入环境管理器时，自动获取mysql连接与光标
        """
        try:
            self._mysql_connection = self._connection_pool.get_connection()
        except Exception as get_connection_err:
            logger.error("获取MySQL连接失败，错误原因: {0}".format(get_connection_err))
        else:
            logger.info("获取MySQL连接成功")

        logger.info("获取MySQL操作光标")
        try:
            self._cursor = self._mysql_connection.cursor(DictCursor)
        except Exception as get_cursor_err:
            logger.error("MySQL光标获取失败，错误原因: {0}".format(get_cursor_err))
        else:
            logger.info("MySQL光标获取成功")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出环境管理器时，自动关闭mysql连接与光标
        """
        logger.info("关闭MySQL光标: {0}".format(self._cursor))
        self._cursor.close()

        logger.info("关闭MySQL连接: {0}".format(self._mysql_connection))
        self._mysql_connection.close()

    def insert(self, sql, args):
        try:
            result = self._cursor.execute(sql, args)
        except Exception as insert_err:
            logger.error("单条INSERT操作执行失败，错误原因: {0}".format(insert_err))
            result = 0
        else:
            logger.info("单条INSERT操作已执行，受影响行数: {0}".format(result))

        return result

    def delete(self, sql, args):
        try:
            result = self._cursor.execute(sql, args)
        except Exception as delete_err:
            logger.error("DELETE操作执行失败，错误原因: {0}".format(delete_err))
            result = 0
        else:
            logger.info("DELETE操作已执行，受影响行数: {0}".format(result))

        return result

    def update(self, sql, args):
        try:
            result = self._cursor.execute(sql, args)
        except Exception as update_err:
            logger.error("UPDATE操作执行失败，错误原因: {0}".format(update_err))
            result = 0
        else:
            logger.info("UPDATE操作已执行，受影响行数: {0}".format(result))

        return result

    def select_one(self, sql, args) -> dict | None:
        try:
            result = self._cursor.execute(sql, args)
        except Exception as select_one_err:
            logger.error("SELECT操作执行失败，错误原因: {0}".format(select_one_err))
            result = 0
        else:
            logger.info("SELECT操作已执行，查询到: {0}行".format(result))

        if result:
            try:
                select_result_dict = self._cursor.fetchone()
            except Exception as fetch_result_err:
                logger.error("获取查询结果失败! 错误原因: {0}".format(fetch_result_err))

                return None
            else:
                logger.info("查询结果: {0}".format(select_result_dict))

                return select_result_dict
        else:
            return None

    def select_list(self, sql, args) -> list[dict] | None:
        try:
            result = self._cursor.execute(sql, args)
        except Exception as select_one_err:
            logger.error("SELECT操作执行失败，错误原因: {0}".format(select_one_err))
            result = 0
        else:
            logger.info("SELECT操作已执行，查询到: {0}行".format(result))

        if result:
            try:
                select_result_list = self._cursor.fetchall()
            except Exception as fetch_list_err:
                logger.error("获取查询结果失败! 错误原因: {0}".format(fetch_list_err))

                return None
            else:
                logger.info("查询结果: {0}".format(select_result_list))

                return select_result_list
        else:
            return None
