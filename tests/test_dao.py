import unittest

import json
from project_common import DATE_TIME_NOW
from data_visualization.dao import access_log_dao, plot_result_dao
from data_visualization.utils.do.data_object import AccessLog, PlotResult
from data_visualization.utils.do.data_object_util import general_primary_key


class AccessLogDaoTestCase(unittest.TestCase):
    ald = access_log_dao
    test_access_body = json.dumps({'testcase': 'testcase1'})
    test_plot_type = ','.join(['line', 'column', 'pie', 'radar'])

    def test_A_insert(self):
        # 创建一个新access_log
        access_log = AccessLog(access_log_id=general_primary_key(),
                               access_date_time=DATE_TIME_NOW,
                               access_ip='127.0.0.1',
                               access_url='test_url_from_test_A',
                               access_body=self.test_access_body,
                               access_plot_type=self.test_plot_type)

        # 插入数据
        ops_result = self.ald.insert(access_log)

        self.assertEqual(ops_result, 1)

    def test_B_delete(self):
        # 创建一个新access_log
        access_log = AccessLog(access_log_id=general_primary_key(),
                               access_date_time=DATE_TIME_NOW,
                               access_ip='127.0.0.1',
                               access_url='test_url_from_test_B',
                               access_body=self.test_access_body,
                               access_plot_type=self.test_plot_type)

        # 插入数据
        self.ald.insert(access_log)

        # 再删除数据
        opt_result = self.ald.delete(access_log)

        self.assertEqual(opt_result, 1)

    def test_C_update(self):
        # 创建一个新access_log
        access_log = AccessLog(access_log_id=general_primary_key(),
                               access_date_time=DATE_TIME_NOW,
                               access_ip='127.0.0.1',
                               access_url='test_url_from_test_C',
                               access_body=self.test_access_body,
                               access_plot_type=self.test_plot_type)

        # 插入数据
        self.ald.insert(access_log)

        # 更新access_log的信息
        access_log.access_url = 'test_url_from_test_C_updated'
        self.ald.update(access_log)

        # 查询数据
        updated_access_log = self.ald.select_one(access_log)

        self.assertIsNotNone(updated_access_log)
        self.assertEqual(updated_access_log.access_url, 'test_url_from_test_C_updated')

    def test_D_select_list_by_access_ip(self):
        test_access_log_ip = '127.0.0.1' + DATE_TIME_NOW

        # 插入10个用于测试的access_log
        for index in range(10):
            access_log = AccessLog(access_log_id=general_primary_key(),
                                   access_date_time=DATE_TIME_NOW,
                                   access_ip=test_access_log_ip,
                                   access_url='test_url_from_test_D_{0}'.format(index),
                                   access_body=self.test_access_body,
                                   access_plot_type=self.test_plot_type)

            self.ald.insert(access_log)

        # 批量查询这10个数据
        select_list = self.ald.select_list_by_access_ip(AccessLog(access_ip=test_access_log_ip))

        if select_list:
            for select_access_log in select_list:
                print(select_access_log, end=' ')

        self.assertEqual(len(select_list), 10)