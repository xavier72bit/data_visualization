import datetime
import unittest
from pymysql_toolkit import MysqlConnection, AccessLog, AccessLogDao, PlotResult, PlotResultDao, PlotTask, PlotTaskDao

date_time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

uuid_list = ["9DA61402-A1CB-7041-A629-6191494C57DC",
             "9DA61402-A1CB-7041-A629-6191494C57D1",
             "9DA61402-A1CB-7041-A629-6191494C57D2",
             "9DA61402-A1CB-7041-A629-6191494C57D3",
             "9DA61402-A1CB-7041-A629-6191494C57D4",
             "9DA61402-A1CB-7041-A629-6191494C57D5",
             "9DA61402-A1CB-7041-A629-6191494C57D6",
             "9DA61402-A1CB-7041-A629-6191494C57D7",
             "9DA61402-A1CB-7041-A629-6191494C57D8",
             "9DA61402-A1CB-7041-A629-6191494C57D9"]


class AccessLogDaoBaseTest(unittest.TestCase):
    """
    对AccessLogDao的基本测试
    """

    def test_single_insert_and_single_select(self):
        # 手动新建一个AccessLog对象
        access_log = AccessLog("9DA61402-A1CB-7041-A629-6191494C5767",
                               date_time_now,
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

        print(new_access_log)
        self.assertEqual(access_log.access_log_id, new_access_log.access_log_id)
        self.assertEqual(access_log.access_date_time, new_access_log.access_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(access_log.access_token, new_access_log.access_token)
        self.assertEqual(access_log.access_state, new_access_log.access_state)
        self.assertEqual(access_log.delete_flag, new_access_log.delete_flag)
        self.assertEqual(access_log.access_log_message, new_access_log.access_log_message)

    def test_multi_insert(self):
        with MysqlConnection(transaction=True) as connection:
            cursor = connection.get_cursor()
            access_log_dao = AccessLogDao(cursor)
            effect_row = 0

            for uuid in uuid_list:
                access_log = AccessLog(uuid,
                                       date_time_now,
                                       "test_token_test_token",
                                       0,
                                       0,
                                       "This is a test")

                exc_result = access_log_dao.insert_exc(access_log)

                effect_row += exc_result

            self.assertEqual(effect_row, 10)

    def test_multi_select(self):
        access_token = "test_token_test_token"
        access_log = AccessLog(access_token=access_token)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            access_log_dao = AccessLogDao(cursor)

            result_list = access_log_dao.select_list_exc_by_access_token(access_log)

        print(result_list)

        for result in result_list:
            print(result.access_log_id, end=',')

        self.assertEqual(len(result_list), 11)

    def test_delete(self):
        access_log_id = '9DA61402-A1CB-7041-A629-6191494C57D1'
        access_log = AccessLog(access_log_id=access_log_id)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            access_log_dao = AccessLogDao(cursor)

            access_log_dao.delete_exc(access_log)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            access_log_dao = AccessLogDao(cursor)

            result = access_log_dao.select_one_exc_by_id(access_log)

        self.assertIsNone(result)


class PlotResultDaoBaseTest(unittest.TestCase):
    """
    对PlotResultDao的基本测试
    """

    def test_single_insert_and_single_select(self):
        plot_result = PlotResult(plot_result_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                 plot_task_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                 plot_result_finish_date_time=date_time_now,
                                 plot_result_finish_state=1,
                                 plot_result_local_path="/tmp/test/temp_plot/test_result",
                                 plot_result_upload_date_time=date_time_now,
                                 plot_result_upload_state=1,
                                 plot_result_url="test_example_url",
                                 delete_flag=0)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_result_dao = PlotResultDao(cursor)
            plot_result_dao.insert_exc(plot_result)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_result_dao = PlotResultDao(cursor)
            new_plot_result = plot_result_dao.select_one_exc_by_id(plot_result)

        self.assertEqual(plot_result.plot_result_id, new_plot_result.plot_result_id)
        self.assertEqual(plot_result.plot_task_id, new_plot_result.plot_task_id)
        self.assertEqual(plot_result.plot_result_finish_date_time,
                         new_plot_result.plot_result_finish_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_result.plot_result_finish_state, new_plot_result.plot_result_finish_state)
        self.assertEqual(plot_result.plot_result_local_path, new_plot_result.plot_result_local_path)
        self.assertEqual(plot_result.plot_result_upload_date_time,
                         new_plot_result.plot_result_upload_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_result.plot_result_upload_state, new_plot_result.plot_result_upload_state)
        self.assertEqual(plot_result.plot_result_url, new_plot_result.plot_result_url)
        self.assertEqual(plot_result.delete_flag, new_plot_result.delete_flag)

    def test_multi_insert(self):
        with MysqlConnection(transaction=True) as connection:
            cursor = connection.get_cursor()
            plot_result_dao = PlotResultDao(cursor)
            effect_row = 0

            for uuid, index in zip(uuid_list, range(10)):
                plot_result = PlotResult(plot_result_id=uuid,
                                         plot_task_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                         plot_result_finish_date_time=date_time_now,
                                         plot_result_finish_state=1,
                                         plot_result_local_path="/tmp/test/temp_plot/test_result{0}".format(index),
                                         plot_result_upload_date_time=date_time_now,
                                         plot_result_upload_state=1,
                                         plot_result_url="test_example_url",
                                         delete_flag=0)

                exc_result = plot_result_dao.insert_exc(plot_result)

                effect_row += exc_result

            self.assertEqual(effect_row, 10)

    def test_multi_select(self):
        plot_task_id = "9DA61402-A1CB-7041-A629-6191494C5767"
        plot_result = PlotResult(plot_task_id=plot_task_id)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_result_dao = PlotResultDao(cursor)

            result_list = plot_result_dao.select_list_exc_by_plot_task_id(plot_result)

        print(result_list)

        for result in result_list:
            print(result.plot_result_local_path, end=',')

        self.assertEqual(len(result_list), 11)

    def test_delete(self):
        plot_result_id = '9DA61402-A1CB-7041-A629-6191494C57D1'
        plot_result = PlotResult(plot_result_id=plot_result_id)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_result_dao = PlotResultDao(cursor)

            plot_result_dao.delete_exc(plot_result)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_result_dao = PlotResultDao(cursor)

            result = plot_result_dao.select_one_exc_by_id(plot_result)

        self.assertIsNone(result)


class PlotTaskDaoBaseTest(unittest.TestCase):
    """
    对PlotTaskDao的基本测试
    """
    def test_single_insert_and_single_select(self):
        plot_task = PlotTask(plot_task_id="9DA61402-A1CB-7041-A629-6191494C5767",
                             plot_task_create_date_time=date_time_now,
                             plot_task_finish_date_time=date_time_now,
                             plot_task_state=0,
                             access_log_id="9DA61402-A1CB-7041-A629-6191494C5767",
                             delete_flag=0)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_task_dao = PlotTaskDao(cursor)
            plot_task_dao.insert_exc(plot_task)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_task_dao = PlotTaskDao(cursor)
            new_plot_task = plot_task_dao.select_one_exc_by_id(plot_task)

        self.assertEqual(plot_task.plot_task_id, new_plot_task.plot_task_id)
        self.assertEqual(plot_task.plot_task_create_date_time,
                         new_plot_task.plot_task_create_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_task.plot_task_finish_date_time,
                         new_plot_task.plot_task_finish_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_task.plot_task_state, new_plot_task.plot_task_state)
        self.assertEqual(plot_task.access_log_id, new_plot_task.access_log_id)
        self.assertEqual(plot_task.delete_flag, new_plot_task.delete_flag)

    def test_multi_insert(self):
        with MysqlConnection(transaction=True) as connection:
            cursor = connection.get_cursor()
            plot_task_dao = PlotTaskDao(cursor)
            effect_row = 0

        for uuid in uuid_list:
            plot_task = PlotTask(plot_task_id=uuid,
                                 plot_task_create_date_time=date_time_now,
                                 plot_task_finish_date_time=date_time_now,
                                 plot_task_state=1,
                                 access_log_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                 delete_flag=0)

            exc_result = plot_task_dao.insert_exc(plot_task)

            effect_row += exc_result

        self.assertEqual(effect_row, 10)

    def test_multi_select(self):
        access_log_id = "9DA61402-A1CB-7041-A629-6191494C5767"
        plot_task = PlotTask(access_log_id=access_log_id)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_task_dao = PlotTaskDao(cursor)

            result_list = plot_task_dao.select_list_exc_by_access_log_id(plot_task)

        print(result_list)

        for result in result_list:
            print(result.plot_task_id, end=',')

        self.assertEqual(len(result_list), 11)

    def test_delete(self):
        plot_task_id = '9DA61402-A1CB-7041-A629-6191494C57D1'
        plot_task = PlotTask(plot_task_id=plot_task_id)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_task_dao = PlotTaskDao(cursor)

            plot_task_dao.delete_exc(plot_task)

        with MysqlConnection() as connection:
            cursor = connection.get_cursor()
            plot_task_dao = PlotTaskDao(cursor)

            result = plot_task_dao.select_one_exc_by_id(plot_task)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
