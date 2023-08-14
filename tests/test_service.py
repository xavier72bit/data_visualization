import unittest
import numpy as np

from data_visualization.service import access_log_service
from data_visualization.service import plot_result_service


def generate_nums(catalog_data_list):
    """
    生成所需数据
    """
    return np.cumsum(np.random.randint(1, 200, size=len(catalog_data_list)))


class AccessLogServiceTest(unittest.TestCase):
    """
    对AccessLogService的基本测试
    """

    def test_A_create_a_new_access_log(self):
        """
        create_a_new_access_log测试
        """
        access_log_id = access_log_service.creat_a_new_access_log(access_token="access_token",
                                                                  access_log_message="test_access_log_a")

        access_log = access_log_service.read_a_access_log_by_id(access_log_id)

        self.assertEqual(str(access_log_id), str(access_log.access_log_id))


class PlotResultServiceTest(unittest.TestCase):
    """
    对PlotResultService的基本测试
    """
    time_data_list_short = ['2023-07-19', '2023-07-20', '2023-07-21', '2023-07-22', '2023-07-23', '2023-07-24']
    time_data_list_long = ['2023-07-19', '2023-07-20', '2023-07-21', '2023-07-22', '2023-07-23', '2023-07-24',
                           '2023-07-25', '2023-07-26', '2023-07-27', '2023-07-28', '2023-07-29', '2023-07-30']

    def test_A_plot_time_num_short(self):
        # 新建一个plot_result对象
        plot_result = plot_result_service.create_a_new_plot_result('test_access_log_id')

        # 绘图
        plot_result_id = plot_result_service.plot_time_num(plot_result,
                                                           self.time_data_list_short,
                                                           generate_nums(self.time_data_list_short),
                                                           '接单量')

        # 获取状态
        print(plot_result_service.read_state_by_id(plot_result_id))

        # 获取url
        print(plot_result_service.read_url_by_id(plot_result_id))

    def test_B_plot_time_num_long(self):
        # 新建一个plot_result对象
        plot_result = plot_result_service.create_a_new_plot_result('test_access_log_id')

        # 绘图
        plot_result_id = plot_result_service.plot_time_num(plot_result,
                                                           self.time_data_list_long,
                                                           generate_nums(self.time_data_list_long),
                                                           '接单量')

        # 获取状态
        print(plot_result_service.read_state_by_id(plot_result_id))

        # 获取url
        print(plot_result_service.read_url_by_id(plot_result_id))


if __name__ == '__main__':
    unittest.main()
