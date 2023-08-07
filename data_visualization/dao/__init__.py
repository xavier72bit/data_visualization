from logging import Logger
from itertools import repeat
from pymysql.cursors import DictCursor

from data_visualization.domain import Domain
from data_visualization.utils.pymysql_util import connection_pool

"""
data_visualization.dao 软件包的说明：

该软件包为dao层功能代码。

Dao：
对数据库进行数据持久化操作，它的方法语句是直接针对数据库操作的，
主要实现一些数据的增删改查。核心思想是把数据库封装一下，
让与数据库的交道看起来像在和一个对象打交道，这个对象通常就是DAO。

在本项目中，DAO层的职责：
1. 维护数据库连接的开启与关闭
2. 维护业务所需的sql（Dao类的属性）
3. 执行sql，返回执行结果，记录执行日志（Dao类的方法）

__init__.py提供：
1. DaoInterface：该包下所有Dao类的通用父类
2. BasicSqlGenerator：sql生成工具类

其他的.py文件创建规则：
一张表对应一个py文件。（比如access_log表对应一个access_log_dao.py）

其他的.py文件应该完成的工作：（读一遍本包下其他的dao.py文件可辅助理解）
1. 导入 data_visualization.dao包 下的 DaoInterface，BasicSqlGenerator
   导入 data_visualization.utils包 下的 logging_util
   导入 data_visualization.domain包 下的 对应Domain对象
2. 调用 logging_util.std_init_module_logging 函数，初始化 本模块的日志Logger
3. 将 BasicSqlGenerator 与 本模块的日志Logger 绑定，创建一个 sql语句生成器对象
4. 定义Dao类（比如AccessLogDao），该对象继承DaoInterface
5. 将 定义的Dao类 与 本模块的日志Logger 绑定
"""


class DaoInterface:
    """
    dao层 所有Dao类的统一规范接口，此类禁止实例化。
    此类定义了所有Dao通用的`__init__`、`__enter__`、`__exit__`方法

    为了记录日志，**请在定义完子类后，调用init_logger类方法绑定Logger**
    """

    @classmethod
    def init_logger(cls, logger: Logger):
        """
        为类绑定一个logger
        """
        cls.logger = logger

    def __init__(self):
        self.logger.info("初始化{0}对象".format(self.__class__))
        self.logger.info(self)

    def __enter__(self):
        """
        进入环境管理器时，自动获取mysql连接与光标

        :return: Dao
        """
        self.logger.info("获取MySQL连接")
        try:
            self._mysql_connection = connection_pool.connection()
        except Exception as e:
            self.logger.error("获取MySQL连接失败，错误原因: {0}".format(e))
        else:
            self.logger.info("获取MySQL连接成功")

        self.logger.info("获取MySQL操作光标")
        try:
            self._execute_cursor = self._mysql_connection.cursor(DictCursor)
        except Exception as e:
            self.logger.error("MySQL光标获取失败，错误原因: {0}".format(e))
        else:
            self.logger.info("MySQL光标获取成功")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        退出环境管理器时，自动关闭mysql连接与光标
        """
        self.logger.info("关闭MySQL光标: {0}".format(self._execute_cursor))
        self._execute_cursor.close()

        self.logger.info("关闭MySQL连接: {0}".format(self._mysql_connection))
        self._mysql_connection.close()


class BasicSqlGenerator:
    """
    用于生成包括以下5种基础SQL语句：

    1. 单条INSERT [INSERT INTO exp_table (exp_column_1_pk, exp_column_2) VALUES (1, 2)]
    2. 根据主键 单条DELETE [DELETE FROM exp_table WHERE exp_column_1_pk = %s]
    3. 根据主键 单条UPDATE [UPDATE exp_table set exp_column_1_pk = 1, exp_column_2 = 3, WHERE exp_column_1_pk = 1]
    4. 根据主键 单条SELECT [SELECT exp_column_1_pk, exp_column_2 from exp_table WHERE exp_column_1_pk = %s LIMIT 0, 1]
    5. 根据除主键外的某一个字段 多条SELECT [SELECT exp_column_1_pk, exp_column_2 from exp_table WHERE exp_column_2 LIKE %s]
    """

    # 定义sql语句模版
    insert_sql_format_template = 'INSERT INTO {0} ({1}) VALUES ({2})'
    delete_sql_format_template = 'DELETE FROM {0} WHERE {1} = %s'
    update_sql_format_template = 'UPDATE {0} SET {1} WHERE {2} = %s'
    select_one_sql_format_template = 'SELECT {0} FROM {1} WHERE {2} = %s LIMIT 0, 1'
    select_list_sql_format_template = 'SELECT {0} FROM {1} WHERE {2} LIKE %s'

    @classmethod
    def init_logger(cls, logger: Logger):
        """
        为类绑定一个logger
        """
        cls.logger = logger

    def __init__(self, table_name: str, domain: Domain):
        self._table_name = table_name
        self._column_list = domain.get_all_attributes()
        self._pk = self._column_list[0]

    def insert_sql(self) -> str:
        """
        生成 单条INSERT SQL语句
        """
        sql_str = self.insert_sql_format_template.format(self._table_name,
                                                         ', '.join(self._column_list),
                                                         ', '.join(repeat('%s', len(self._column_list))))
        self.logger.info("单条INSERT_SQL已生成: {0}".format(sql_str))

        return sql_str

    def delete_sql(self) -> str:
        """
        生成 根据主键单条DELETE SQL语句
        """
        sql_str = self.delete_sql_format_template.format(self._table_name,
                                                         self._pk)
        self.logger.info("根据主键单条DELETE_SQL已生成: {0}".format(sql_str))

        return sql_str

    def update_sql(self) -> str:
        """
        生成 根据主键单条UPDATE SQL语句
        """
        sql_str = self.update_sql_format_template.format(self._table_name,
                                                         ', '.join([column + ' = %s' for column in self._column_list]),
                                                         self._pk)
        self.logger.info("根据主键单条UPDATE_SQL已生成: {0}".format(sql_str))

        return sql_str

    def select_one(self) -> str:
        """
        生成 根据主键单条SELECT SQL语句
        """
        sql_str = self.select_one_sql_format_template.format(', '.join(self._column_list),
                                                             self._table_name,
                                                             self._pk)
        self.logger.info("根据主键单条SELECT_SQL已生成: {0}".format(sql_str))

        return sql_str

    def select_list(self, column: str) -> str | None:
        """
        生成 根据除主键外的某一个字段 多条SELECT
        """
        if column in self._column_list:
            sql_str = self.select_list_sql_format_template.format(', '.join(self._column_list),
                                                                  self._table_name,
                                                                  column)
            self.logger.info("根据除主键外的某一个字段多条SELECT_SQL已生成: {0}".format(sql_str))

            return sql_str
        else:
            self.logger.error("指定字段不在表定义内！SQL执行失败！")
            return None
