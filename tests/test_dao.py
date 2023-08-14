import uuid
import unittest

from project_common import DATE_TIME_NOW
from data_visualization.domain.access_log import AccessLog
from data_visualization.domain.plot_result import PlotResult
from data_visualization.dao.access_log_dao import AccessLogDao
from data_visualization.dao.plot_result_dao import PlotResultDao


class AccessLogDaoBaseTest(unittest.TestCase):
    """
    对AccessLogDao的基本测试
    """
    def test_a_insert_one_exc_and_select_one_exc_by_id(self):
        """
        单条插入 与 单条查询 测试
        """
        # 新建一个access_log
        access_log = AccessLog(str(uuid.uuid4()),
                               DATE_TIME_NOW,
                               "test_token_from_test_a",
                               "This is a test",
                               "123.123.123.123")

        # 插入操作
        with AccessLogDao() as ald:
            ald.insert_one_exc(access_log)

        # 查询刚刚插入的信息
        with AccessLogDao() as ald:
            new_access_log = ald.select_one_exc_by_pk(access_log)

        print(new_access_log)
        self.assertEqual(str(access_log.access_log_id), str(new_access_log.access_log_id))
        self.assertEqual(access_log.access_date_time, new_access_log.access_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(access_log.access_token, new_access_log.access_token)
        self.assertEqual(access_log.access_log_message, new_access_log.access_log_message)
        self.assertEqual(access_log.access_ip, new_access_log.access_ip)

    def test_b_multi_insert_one_exc(self):
        """
        单条插入 执行1000次
        """
        affect_row = 0

        with AccessLogDao() as ald:
            access_token = "test_token_from_test_b" + DATE_TIME_NOW
            for i in range(5423):
                # 新建一个access_log
                access_log = AccessLog(str(uuid.uuid4()),
                                       DATE_TIME_NOW,
                                       access_token,
                                       "This is a test{0}".format(i),
                                       "127.0.0.1")

                # 将这个access_log信息插入数据库
                exec_affect_row = ald.insert_one_exc(access_log)
                affect_row += exec_affect_row

        self.assertEqual(affect_row, 1000)

    def test_c_select_list_exc_by_access_token(self):
        """
        多条查询测试，查询test_b中插入的1000条数据
        """
        # 新建access_log
        access_token = "test_token_from_test_b" + DATE_TIME_NOW
        access_log = AccessLog(access_token=access_token)

        with AccessLogDao() as ald:
            result_list = ald.select_list_exc_by_column_name(access_log, 'access_token')

        print(result_list)

        for result in result_list:
            print(result.access_log_id, end=',')

        self.assertEqual(len(result_list), 1000)

    def test_d_insert_one_exc_and_delete_one_exc_by_id(self):
        """
        单条插入 和 单条删除 测试
        """

        # 生成并插入一个access_log
        access_log = AccessLog(str(uuid.uuid4()),
                               DATE_TIME_NOW,
                               "test_token_from_test_c",
                               "This is a test",
                               "123.123.123.123")

        with AccessLogDao() as ald:
            ald.insert_one_exc(access_log)

        # 删除这条记录
        with AccessLogDao() as ald:
            ald.delete_one_exc_by_id(access_log)

        # 最后查询这条记录
        with AccessLogDao() as ald:
            result = ald.select_one_exc_by_pk(access_log)

        self.assertIsNone(result)

    def test_e_select_list_exc_by_access_ip(self):
        """
        多条查询测试，查询test_b中插入的1000条数据
        """
        access_log = AccessLog(access_ip='123.123.123.124')

        with AccessLogDao() as ald:
            result_list = ald.select_list_exc_by_column_name(access_log, 'access_ip')

        print(result_list)

        for result in result_list:
            print(result.access_log_id, end=',')

        self.assertEqual(len(result_list), 1000)


class PlotResultDaoBaseTest(unittest.TestCase):
    """
    对PlotResultDao的基本测试
    """

    def test_a_single_insert_and_single_select(self):
        """
        单条插入 与 单条查询 测试
        """
        # 手动生成一个plot_result
        plot_result = PlotResult(plot_result_id=str(uuid.uuid4()),
                                 access_log_id=str(uuid.uuid4()),
                                 plot_result_finish_date_time=DATE_TIME_NOW,
                                 plot_result_local_path="/tmp/test/temp_plot/test_result",
                                 plot_result_upload_date_time=DATE_TIME_NOW,
                                 plot_result_url="test_example_url",
                                 plot_result_state=0,
                                 plot_result_type='test')

        # 插入这条plot_result
        with PlotResultDao() as prd:
            prd.insert_one_exc(plot_result)

        # 查询刚生成的这条plot_result
        with PlotResultDao() as prd:
            new_plot_result = prd.select_one_exc_by_pk(plot_result)

        print(new_plot_result)
        self.assertEqual(str(plot_result.plot_result_id),
                         str(new_plot_result.plot_result_id))
        self.assertEqual(str(plot_result.access_log_id),
                         str(new_plot_result.access_log_id))
        self.assertEqual(plot_result.plot_result_finish_date_time,
                         new_plot_result.plot_result_finish_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_result.plot_result_local_path,
                         new_plot_result.plot_result_local_path)
        self.assertEqual(plot_result.plot_result_upload_date_time,
                         new_plot_result.plot_result_upload_date_time.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(plot_result.plot_result_url,
                         new_plot_result.plot_result_url)
        self.assertEqual(plot_result.plot_result_state,
                         new_plot_result.plot_result_state)
        self.assertEqual(plot_result.plot_result_type,
                         new_plot_result.plot_result_type)

    def test_b_multi_insert_one_exc(self):
        """
        单条插入 执行1000次
        """
        affect_row = 0
        access_log_id = "9DA61402-A1CB-7041-A629-6191494C5767"

        with PlotResultDao() as prd:
            for i in range(1000):
                # 新建一个plot_result
                plot_result = PlotResult(plot_result_id=str(uuid.uuid4()),
                                         access_log_id=access_log_id,
                                         plot_result_finish_date_time=DATE_TIME_NOW,
                                         plot_result_local_path="/tmp/test/temp_plot/test_result",
                                         plot_result_upload_date_time=DATE_TIME_NOW,
                                         plot_result_url="test_example_url",
                                         plot_result_state=0,
                                         plot_result_type='test')

                # 将这条plot_result信息插入数据库
                exec_affect_row = prd.insert_one_exc(plot_result)
                affect_row += exec_affect_row

            self.assertEqual(affect_row, 1000)

    def test_c_select_list_exc_by_access_id(self):
        """
        多条查询测试，查询test_b中插入的1000条数据
        """
        # 新建plot_result
        access_log_id = "9DA61402-A1CB-7041-A629-6191494C5767"
        plot_result = PlotResult(access_log_id=access_log_id)

        with PlotResultDao() as prd:
            result_list = prd.select_list_exc_by_column_name(plot_result, 'access_log_id')

        print(result_list)

        for result in result_list:
            print(result.plot_result_local_path, end=',')

        self.assertEqual(len(result_list), 1000)

    def test_d_insert_one_exc_and_delete_one_exc_by_id(self):
        """
        单条插入 和 单条删除 测试
        """
        # 生成并插入一个plot_result
        plot_result = PlotResult(plot_result_id=str(uuid.uuid4()),
                                 access_log_id=str(uuid.uuid4()),
                                 plot_result_finish_date_time=DATE_TIME_NOW,
                                 plot_result_local_path="/tmp/test/temp_plot/test_result",
                                 plot_result_upload_date_time=DATE_TIME_NOW,
                                 plot_result_url="test_example_url",
                                 plot_result_state=0,
                                 plot_result_type='test')

        with PlotResultDao() as prd:
            prd.insert_one_exc(plot_result)

        # 删除这条记录
        with PlotResultDao() as prd:
            prd.delete_one_exc(plot_result)

        # 最后查询这条记录
        with PlotResultDao() as prd:
            result = prd.select_one_exc_by_pk(plot_result)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
