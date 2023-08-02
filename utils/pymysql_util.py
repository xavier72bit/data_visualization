import pymysql
from utils import config_util, logging_util
from dbutils.pooled_db import PooledDB

__all__ = ["connection_pool"]

# -----------------------------------------------------
# 模块初始化
# -----------------------------------------------------

# 初始化本模块的日志
pymysql_util_logger = logging_util.std_init_module_logging(__name__, 'DEBUG', '{0}.log'.format(__name__))

# 导入配置
database_connection_pool_config = config_util.read_yaml('properties.yaml')['database_connection_pool']
pymysql_util_logger.info('数据库连接池配置：{0}'.format(database_connection_pool_config))

# -----------------------------------------------------
# 数据库连接池初始化
# -----------------------------------------------------

try:
    pymysql_util_logger.info('开始初始化数据库连接池')
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
    pymysql_util_logger.critical('初始化数据库连接池失败，错误: {0}'.format(e))
else:
    pymysql_util_logger.info('数据库连接池初始化成功')
