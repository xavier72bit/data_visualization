import uuid
import os.path
import unittest

from data_visualization.utils import minio_util
from project_common import CURRENT_WORKSPACE, MINIO_SERVER_ADDRESS


class MinioUtilBaseTest(unittest.TestCase):
    """
    对minio_util的基准功能测试
    """
    test_file = os.path.join(CURRENT_WORKSPACE, "static", "choose_chart.jpg")

    def test_A_upload_file(self):
        """
        测试Minio Client上传功能
        """
        print(MINIO_SERVER_ADDRESS + minio_util.upload_file(self.test_file))
