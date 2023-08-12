import requests
import unittest


class SysinfoTest(unittest.TestCase):
    """
    测试sysinfo接口
    """

    def test_a_count_access_times_by_ip(self):
        http_param = {'ip_address': '123.123.123.123'}

        r = requests.get('http://127.0.0.1:5001/sysinfo/ip_access_count', params=http_param)
        print(r)

        self.assertEqual(r.text, 3000)
