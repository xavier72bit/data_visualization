import unittest
import numpy as np
from data_visualization import plotting
from data_visualization.plotting import draw_plot_line, draw_plot_radar, draw_plot_column, draw_plot_bar, draw_plot_pie


def generate_nums(catalog_data_list):
    """
    生成所需数据
    """
    return np.cumsum(np.random.randint(1, 200, size=len(catalog_data_list)))


class PlottingTimeNumTest(unittest.TestCase):
    one_week_sep_one_day = np.arange(np.datetime64('2023-05-01'),
                                     np.datetime64('2023-05-07'),
                                     np.timedelta64(24, 'h'))

    def test_A_draw_plot_time_num_line(self):
        fig = draw_plot_line.draw_time_num_line(self.one_week_sep_one_day,
                                                generate_nums(self.one_week_sep_one_day),
                                                'test_time_num_line')
        plotting.plot_storage(fig, file_name='test_time_num_line')

    def test_B_draw_plot_time_num_column(self):
        fig = draw_plot_column.draw_time_num_column(self.one_week_sep_one_day,
                                                    generate_nums(self.one_week_sep_one_day),
                                                    'test_time_num_column')
        plotting.plot_storage(fig, file_name='test_time_num_column')


class PlottingCatalogNumTest(unittest.TestCase):
    catalog_list = ['项目1', '项目2', '项目3', '项目4', '项目5']

    def test_A_draw_plot_catalog_num_pie(self):
        fig = draw_plot_pie.draw_catalog_num_pie(self.catalog_list,
                                                 generate_nums(self.catalog_list),
                                                 'test_catalog_num_pie')
        plotting.plot_storage(fig, 'test_catalog_num_pie')

    def test_B_draw_plot_catalog_num_bar(self):
        fig = draw_plot_bar.draw_catalog_num_bar(self.catalog_list,
                                                 generate_nums(self.catalog_list),
                                                 'test_catalog_num_bar')
        plotting.plot_storage(fig, 'test_catalog_num_bar')

    def test_C_draw_plot_catalog_num_column(self):
        fig = draw_plot_column.draw_catalog_num_column(self.catalog_list,
                                                       generate_nums(self.catalog_list),
                                                       'test_catalog_num_column')
        plotting.plot_storage(fig, 'test_catalog_num_column')

    def test_D_draw_plot_catalog_num_radar(self):
        fig = draw_plot_radar.draw_catalog_num_radar(self.catalog_list,
                                                     generate_nums(self.catalog_list),
                                                     'test_catalog_num_radar')
        plotting.plot_storage(fig, 'test_catalog_num_radar')


class PlottingCatalogTimeNumTest(unittest.TestCase):
    one_week_sep_one_day = np.arange(np.datetime64('2023-05-01'),
                                     np.datetime64('2023-05-07'),
                                     np.timedelta64(24, 'h'))

    catalog_list = ['项目{0}'.format(i) for i in range(3)]

    catalog_num_dict = {}
    for item in catalog_list:
        catalog_num_dict[item] = list(generate_nums(one_week_sep_one_day))

    def test_A_draw_plot_catalog_time_num_column(self):
        fig = draw_plot_column.draw_time_catalog_num_column(self.one_week_sep_one_day,
                                                            self.catalog_num_dict,
                                                            'test_time_catalog_num_column')
        plotting.plot_storage(fig, 'test_time_catalog_num_column')

    def test_B_draw_plot_catalog_time_num_line(self):
        fig = draw_plot_line.draw_time_catalog_num_line(self.one_week_sep_one_day,
                                                        self.catalog_num_dict,
                                                        'test_time_catalog_num_line')
        plotting.plot_storage(fig, 'test_time_catalog_num_line')


if __name__ == '__main__':
    unittest.main()
