import datetime
import unittest

from api.domain.access_log import AccessLog
from api.domain.plot_result import PlotResult
from api.dao.access_log_dao import AccessLogDao
from api.dao.plot_result_dao import PlotResultDao

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

    def test_a_single_insert_and_single_select(self):
        # 手动新建一个AccessLog对象
        access_log = AccessLog("9DA61402-A1CB-7041-A629-6191494C5767",
                               date_time_now,
                               "test_token_test_token",
                               0,
                               "This is a test")

        # 将这个AccessLog对象信息插入数据库
        with AccessLogDao() as access_log_dao:
            access_log_dao.insert_exc(access_log)

        # 验证过程，另外开启一个连接，查询刚刚插入的信息
        with AccessLogDao() as access_log_dao:
            new_access_log = access_log_dao.select_one_exc_by_id(access_log)

        print(new_access_log)
        self.assertEqual(access_log.access_log_id, new_access_log.access_log_id)
        self.assertEqual(access_log.access_date_time, new_access_log.access_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(access_log.access_token, new_access_log.access_token)
        self.assertEqual(access_log.access_state, new_access_log.access_state)
        self.assertEqual(access_log.access_log_message, new_access_log.access_log_message)

    def test_b_multi_insert(self):
        with AccessLogDao() as access_log_dao:
            effect_row = 0

            for uuid in uuid_list:
                access_log = AccessLog(uuid,
                                       date_time_now,
                                       "test_token_test_token",
                                       0,
                                       "This is a test")

                exc_result = access_log_dao.insert_exc(access_log)

                effect_row += exc_result

            self.assertEqual(effect_row, 10)

    def test_c_multi_select(self):
        access_token = "test_token_test_token"
        access_log = AccessLog(access_token=access_token)

        with AccessLogDao() as access_log_dao:
            result_list = access_log_dao.select_list_exc_by_access_token(access_log)

        print(result_list)

        for result in result_list:
            print(result.access_log_id, end=',')

        self.assertEqual(len(result_list), 11)

    def test_d_delete(self):
        access_log_id = '9DA61402-A1CB-7041-A629-6191494C57D1'
        access_log = AccessLog(access_log_id=access_log_id)

        with AccessLogDao() as access_log_dao:
            access_log_dao.delete_exc(access_log)

        with AccessLogDao() as access_log_dao:
            result = access_log_dao.select_one_exc_by_id(access_log)

        self.assertIsNone(result)


class PlotResultDaoBaseTest(unittest.TestCase):
    """
    对PlotResultDao的基本测试
    """

    def test_a_single_insert_and_single_select(self):
        plot_result = PlotResult(plot_result_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                 access_log_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                 plot_result_finish_date_time=date_time_now,
                                 plot_result_finish_state=1,
                                 plot_result_local_path="/tmp/test/temp_plot/test_result",
                                 plot_result_upload_date_time=date_time_now,
                                 plot_result_upload_state=1,
                                 plot_result_url="test_example_url")

        with PlotResultDao() as prd:
            prd.insert_exc(plot_result)

        with PlotResultDao() as prd:
            new_plot_result = prd.select_one_exc_by_id(plot_result)

        self.assertEqual(plot_result.plot_result_id, new_plot_result.plot_result_id)
        self.assertEqual(plot_result.access_log_id, new_plot_result.access_log_id)
        self.assertEqual(plot_result.plot_result_finish_date_time,
                         new_plot_result.plot_result_finish_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_result.plot_result_finish_state, new_plot_result.plot_result_finish_state)
        self.assertEqual(plot_result.plot_result_local_path, new_plot_result.plot_result_local_path)
        self.assertEqual(plot_result.plot_result_upload_date_time,
                         new_plot_result.plot_result_upload_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_result.plot_result_upload_state, new_plot_result.plot_result_upload_state)
        self.assertEqual(plot_result.plot_result_url, new_plot_result.plot_result_url)

    def test_b_multi_insert(self):
        with PlotResultDao() as prd:
            effect_row = 0

            for uuid, index in zip(uuid_list, range(10)):
                plot_result = PlotResult(plot_result_id=uuid,
                                         access_log_id="9DA61402-A1CB-7041-A629-6191494C5767",
                                         plot_result_finish_date_time=date_time_now,
                                         plot_result_finish_state=1,
                                         plot_result_local_path="/tmp/test/temp_plot/test_result{0}".format(index),
                                         plot_result_upload_date_time=date_time_now,
                                         plot_result_upload_state=1,
                                         plot_result_url="test_example_url")

                exc_result = prd.insert_exc(plot_result)

                effect_row += exc_result

        self.assertEqual(effect_row, 10)

    def test_c_multi_select(self):
        access_log_id = "9DA61402-A1CB-7041-A629-6191494C5767"
        plot_result = PlotResult(access_log_id=access_log_id)

        with PlotResultDao() as prd:
            result_list = prd.select_list_exc_by_access_log_id(plot_result)

        print(result_list)

        for result in result_list:
            print(result.plot_result_local_path, end=',')

        self.assertEqual(len(result_list), 11)

    def test_d_delete(self):
        plot_result_id = '9DA61402-A1CB-7041-A629-6191494C57D1'
        plot_result = PlotResult(plot_result_id=plot_result_id)

        with PlotResultDao() as prd:
            prd.delete_exc(plot_result)

        with PlotResultDao() as prd:
            result = prd.select_one_exc_by_id(plot_result)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()