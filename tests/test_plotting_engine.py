import unittest
from data_visualization.utils.plotting import plotting_engine


class PlotDataSourceTestCase(unittest.TestCase):
    PlotDataSource = plotting_engine.PlotDataSource

    num_list_1 = [1, 2, 3, 4]
    num_list_2 = [1.1, 12, 3.4, 6.6, 34, 3.14159268848123]
    num_str_list = [1, 2, 3, 4, "test1"]
    str_list = ["test1", "test2", "test3", "test4", "test5", "test6"]
    str_datetime_list = ["test1", "test2", "2018/12/23", "12:36", "2019-01-01", "2019-03-21T13:32", "23:23:11"]
    datetime_list = ["2018/12/23", "12:36", "2019-01-01", "2019-03-21T13:32", "23:23:11"]
    error_dict_1 = {
        'catalog_1': [1, 2, 3, 4, 5],
        'catalog_2': [1, 2, 3, 4],
        'catalog_3': [1, 2, 3, 4, 5]
    }
    error_dict_2 = {
        'catalog_1': 1,
        'catalog_2': [1, 2, 3, 4],
        'catalog_3': [1, 2, 3, 4, 5]
    }
    error_dict_3 = {
        'catalog_1': [1, 2, 3, 4, 5],
        'catalog_2': [1, 2, 3, 4, 5],
        'catalog_3': [1, 2, "test", 4, 5]
    }
    correct_dict = {
        'catalog_1': [1, 2, 3, 4, 5],
        'catalog_2': [1, 2, 3, 4, 5],
        'catalog_3': [1, 2, 3, 4, 5]
    }

    def test_A_num_list_1(self):
        pds = self.PlotDataSource(self.num_list_1)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'list')
        self.assertEqual(pds.data_type, 'number')
        self.assertEqual(pds.is_data_valid, True)
        self.assertEqual(pds.data_source_length, 4)
        self.assertEqual(pds.data, self.num_list_1)

    def test_B_num_list_2(self):
        pds = self.PlotDataSource(self.num_list_2)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'list')
        self.assertEqual(pds.data_type, 'number')
        self.assertEqual(pds.is_data_valid, True)
        self.assertEqual(pds.data_source_length, 6)
        self.assertEqual(pds.data, self.num_list_2)

    def test_C_num_str_list(self):
        pds = self.PlotDataSource(self.num_str_list)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'list')
        self.assertEqual(pds.data_type, None)
        self.assertEqual(pds.is_data_valid, False)
        self.assertEqual(pds.data_source_length, 5)
        self.assertEqual(pds.data, self.num_str_list)

    def test_D_str_list(self):
        pds = self.PlotDataSource(self.str_list)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'list')
        self.assertEqual(pds.data_type, 'catalog')
        self.assertEqual(pds.is_data_valid, True)
        self.assertEqual(pds.data_source_length, 6)
        self.assertEqual(pds.data, self.str_list)

    def test_E_str_datetime_list(self):
        pds = self.PlotDataSource(self.str_datetime_list)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'list')
        self.assertEqual(pds.data_type, None)
        self.assertEqual(pds.is_data_valid, False)
        self.assertEqual(pds.data_source_length, 7)
        self.assertEqual(pds.data, list(map(plotting_engine.string_2_datetime_test, self.str_datetime_list)))

    def test_F_datetime_list(self):
        pds = self.PlotDataSource(self.datetime_list)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'list')
        self.assertEqual(pds.data_type, 'datetime')
        self.assertEqual(pds.is_data_valid, True)
        self.assertEqual(pds.data_source_length, 5)
        self.assertEqual(pds.data, list(map(plotting_engine.string_2_datetime_test, self.datetime_list)))

    def test_G_error_dict_1(self):
        pds = self.PlotDataSource(self.error_dict_1)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'dict')
        self.assertEqual(pds.data_type, None)
        self.assertEqual(pds.is_data_valid, False)
        self.assertEqual(pds.data_source_length, 0)
        self.assertEqual(pds.data, self.error_dict_1)

    def test_H_error_dict_2(self):
        pds = self.PlotDataSource(self.error_dict_2)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'dict')
        self.assertEqual(pds.data_type, None)
        self.assertEqual(pds.is_data_valid, False)
        self.assertEqual(pds.data_source_length, 0)
        self.assertEqual(pds.data, self.error_dict_2)

    def test_I_error_dict_3(self):
        pds = self.PlotDataSource(self.error_dict_3)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'dict')
        self.assertEqual(pds.data_type, None)
        self.assertEqual(pds.is_data_valid, False)
        self.assertEqual(pds.data_source_length, 5)
        self.assertEqual(pds.data, self.error_dict_3)

    def test_J_correct_dict(self):
        pds = self.PlotDataSource(self.correct_dict)

        print(pds.data)
        print(pds.data_source_type)
        print(pds.data_source_length)
        print(pds.data_type)
        print(pds.is_data_valid)
        self.assertEqual(pds.data_source_type, 'dict')
        self.assertEqual(pds.data_type, 'number')
        self.assertEqual(pds.is_data_valid, True)
        self.assertEqual(pds.data_source_length, 5)
        self.assertEqual(pds.data, self.correct_dict)


if __name__ == '__main__':
    unittest.main()
