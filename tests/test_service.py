import unittest

from data_visualization.service import access_log_service


class AccessLogServiceTest(unittest.TestCase):
    """
    对AccessLogService的基本测试
    """

    def test_a_create_a_new_access_log(self):
        """
        create_a_new_access_log测试
        """
        access_log_id = access_log_service.creat_a_new_access_log(access_token="access_token",
                                                                  access_log_message="test_access_log_a")

        access_log = access_log_service.read_a_access_log_by_id(access_log_id)

        self.assertEqual(str(access_log_id), str(access_log.access_log_id))


if __name__ == '__main__':
    unittest.main()
