import datetime
import unittest
from pymysql_toolkit import MysqlConnection, AccessLog, AccessLogDao, PlotResult, PlotResultDao, PlotTask, PlotTaskDao

mysql_date_time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class AccessLogDaoBaseTest(unittest.TestCase):
    """
    对AccessLogDao的基本测试

    测试用例简述：
    1. 单条插入
    2. 多条插入（开启事务）
    4. 单条查询
    5. 多条查询
    6. 单条更新
    7. 多条更新（开启事务）
    8. 单条删除
    9. 多条删除（开启事务）
    """

    def test_single_insert_and_single_select(self):
        # 手动新建一个AccessLog对象
        access_log = AccessLog("9DA61402-A1CB-7041-A629-6191494C57DC",
                               mysql_date_time_now,
                               "test_token_test_token",
                               0,
                               0,
                               "This is a test")

        # 将这个AccessLog对象信息插入数据库
        with MysqlConnection() as connection:
            # 新建一个AccessLogDao对象，将当前的连接的Cursor传入
            cursor = connection.get_cursor()
            access_log_dao = AccessLogDao(cursor)
            access_log_dao.insert_exc(access_log)

        # 验证过程，另外开启一个连接，查询
        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            access_log_dao = AccessLogDao(cursor)
            new_access_log = access_log_dao.select_one_exc_by_id(access_log)

        self.assertEqual(access_log.access_log_id, new_access_log.access_log_id)
        self.assertEqual(access_log.access_date_time, new_access_log.access_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(access_log.access_token, new_access_log.access_token)
        self.assertEqual(access_log.access_state, new_access_log.access_state)
        self.assertEqual(access_log.delete_flag, new_access_log.delete_flag)
        self.assertEqual(access_log.access_log_message, new_access_log.access_log_message)


if __name__ == '__main__':
    unittest.main()
