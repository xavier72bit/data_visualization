import datetime
import matplotlib.pyplot as plt

from data_visualization.utils.plotting import plotting_util
from data_visualization.utils.plotting.plotting_functions import draw_plot_column, draw_plot_line, draw_plot_pie, draw_plot_bar, draw_plot_radar


# -----------------------------------------------------
# 本模块内部使用的常量
# -----------------------------------------------------


# 日期时间字符串解析格式
_datetime_format_string_tuple = (
    '%Y-%m-%d %H:%M:%S',
    '%Y/%m/%d %H:%M:%S',
    '%Y-%m-%dT%H:%M:%S',
    '%Y/%m/%dT%H:%M:%S',
    '%Y-%m-%d %H:%M',
    '%Y/%m/%d %H:%M',
    '%Y-%m-%dT%H:%M',
    '%Y/%m/%dT%H:%M',
    '%Y-%m-%d',
    '%Y/%m/%d',
    '%m-%d',
    '%m/%d',
    '%H:%M:%S',
    '%H:%M'
)

# 绘图类型与绘图函数对照字典
_plotting_type_function_dict = {
    '1': draw_plot_line.draw_one_line,
    '2': draw_plot_column.draw_one_column,
    '3': draw_plot_bar.draw_bar,
    '4': draw_plot_pie.draw_pie,
    '5': draw_plot_radar.draw_radar,
    '6': draw_plot_line.draw_multi_line,
    '7': draw_plot_column.draw_multi_column
}

# 需要用到极坐标的绘图类型元组
_plotting_type_is_polar_axes_tuple = (
    '5',
)


# -----------------------------------------------------
# 本模块内部使用的工具函数
# -----------------------------------------------------


def _convert_string_2_datetime(test_string: str) -> str | datetime.datetime:
    """
    字符串转换为datetime测试，测试标准是datetime_format_string_tuple

    :return: 成功返回datetime.datetime类，失败返回原字符串
    """
    datetime_type_data = None
    for datetime_format in _datetime_format_string_tuple:  # 使用预定义的时间字符串格式化模版解析
        try:
            datetime_type_data = datetime.datetime.strptime(test_string, datetime_format)

            if datetime_type_data is not None:  # 当发现解析成功时，更新flag，直接跳出循环
                return datetime_type_data
        except ValueError:
            continue  # 如果当前模板无法解析，则使用下一个模板进行解析

    if datetime_type_data is None:
        return test_string


# -----------------------------------------------------
# 绘图数据源类
# -----------------------------------------------------


class PlotDataSource:
    """
    数据源类，存储数据源

    数据源类型示例：
    1. 列表数据源
    * [1, 2, 3, 4, 5, 6]
    * ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']

    2. 字典数据源（key: str, value: List）
    * {
          '类别1': [1, 2, 3, 4],
          '类别2': [11, 22, 33, 44],
          '类别3': [111, 222, 333, 444]
      }

    数据类型示例：
    1. 数字类型(number) -> int | float: `1` `3.1415926`
    2. 类别类型(catalog) -> str: `"人"` `"牛马"` `"13#"` `"1234"`
    3. 时间类型(datetime) -> str: `"2018-01-01"` `"03:23"` `"2018-01-01 03:23:23"` `"2018-01-01T20:30:38"` `2018/01/01`
    """
    # 数据源中的具体数据
    data: list | dict | None = None
    # 数据源的类型：['dict' | 'list']
    data_source_type: str | None = None
    # 数据源的长度
    data_source_length: int = 0
    # 数据源中的数据类型：['catalog' | 'datetime' | 'number']
    data_type: str | None = None
    # 数据源是否有效（当为字典数据源时，所有的value列表的长度相同才为True）
    is_data_valid: bool = False
    # 字典数据源的keys()长度
    dict_data_source_key_length: int = 0

    def __init__(self, data: dict | list | None):
        """
        直接将数据传进来，分析数据源在这里进行
        """
        # 第一步：先存储数据
        self.data = data

        # 第二步：判定数据源是否为空
        if self.data is None:
            self.is_data_valid = False

        # 第三步：判断数据源类型，同时判断数据源是否有效
        if type(self.data) is list:  # 当数据源为list
            self.data_source_type = 'list'
            self.data_source_length = len(self.data)
            self.is_data_valid = False if self.data_source_length == 0 else True

        elif type(self.data) is dict:  # 当数据源为dict
            self.data_source_type = 'dict'

            # 判断 字典数据源 所有的 value 是否为列表
            dict_data_source_value_set = {type(value) for value in self.data.values()}
            if not dict_data_source_value_set == {list}:  # 当字典数据源 所有的 value的数据类型 不是列表
                self.is_data_valid = False
            else:
                # 判断 字典数据源 所有的 value列表 的 长度 是否相同
                dict_data_source_length_set = {len(value_list) for value_list in self.data.values()}

                if len(dict_data_source_length_set) == 1:  # 相同，继续判断数据源长度
                    self.data_source_length = dict_data_source_length_set.pop()
                    self.dict_data_source_key_length = len(self.data)
                    self.is_data_valid = False if self.data_source_length == 0 else True
                else:  # 不相同，设置数据源无效
                    self.is_data_valid = False

        else:  # 其他数据类型的数据源无效
            self.is_data_valid = False

        # 第四步：判断并校验数据源中的数据类型
        if self.data_source_type == 'list' and self.is_data_valid:  # 当数据源为list
            list_data_type_set = {type(item) for item in self.data}

            if list_data_type_set <= {int, float}:  # list_data_type_set 是 {int}、{float} 或 {int, float}
                self.data_type = 'number'
                self.is_data_valid = True

            elif list_data_type_set == {str}:  # list_data_type_set 是 {str}
                self.data = list(map(_convert_string_2_datetime, self.data))  # 执行一次datetime转换

                # 再次检查字符串数据源中的数据类型
                str_type_set = {type(item) for item in self.data}
                if str_type_set == {datetime.datetime}:  # 字符串数据源里全是datetime类型
                    self.data_type = 'datetime'
                    self.is_data_valid = True
                elif str_type_set == {str}:  # 字符串数据源里都是str类型
                    self.data_type = 'catalog'
                    self.is_data_valid = True
                else:  # 其他的情况都不符合要求
                    self.is_data_valid = False

            else:  # 其他的情况都不符合要求
                self.is_data_valid = False

        if self.data_source_type == 'dict' and self.is_data_valid:  # 当数据源为dict
            dict_data_type_set = set()

            for dict_value in self.data.values():  # 判断字典数据源中的每一个value list
                for value_list_item in dict_value:  # 判断每一个value list中的每一项
                    dict_data_type_set.add(type(value_list_item))

            if dict_data_type_set <= {int, float}:
                self.data_type = 'number'
                self.is_data_valid = True
            else:
                self.is_data_valid = False


# -----------------------------------------------------
# 绘图引擎核心函数
# -----------------------------------------------------


def plotting_picture(data_source_1: list | dict,
                     data_source_2: list | dict,
                     plotting_requirement_list: list,
                     picture_file_name: str) -> str | int:
    """
    传入两个数据源和数据绘图需求列表['1', '2', '3']，执行绘图过程

    错误码：1-绘图失败，2-图片保存失败
    :return: 成功：绘图结果的本地路径，失败：错误码
    """
    # 存储数据
    plot_data_source_1_object = PlotDataSource(data_source_1)
    plot_data_source_2_object = PlotDataSource(data_source_2)

    # 1. 生成画布
    fig: plt.Figure = plt.figure()

    # 2. 分析数据源中的数据类型
    is_xa_time = True if plot_data_source_1_object.data_type == 'datetime' or plot_data_source_2_object.data_type == 'datetime' else False

    # 3. 生成坐标系
    axes_number: int = len(plotting_requirement_list)

    # TODO: 暂定坐标系都放同一排
    axes_list: list = []
    for index, plot_type in zip(range(axes_number), plotting_requirement_list):
        # index从1开始
        index += 1

        # 判定是否需要生成极坐标系
        if plot_type in _plotting_type_is_polar_axes_tuple:
            axes_list.append(fig.add_subplot(1, axes_number, index, projection='polar'))
        else:
            axes_list.append(fig.add_subplot(1, axes_number, index))

    # 4. 对各坐标系应用绘图函数
    for axes, plot_type in zip(axes_list, plotting_requirement_list):
        plot_result = _plotting_type_function_dict[plot_type](axes,
                                                              plot_data_source_1_object.data,
                                                              plot_data_source_2_object.data,
                                                              is_xa_time=is_xa_time)
        if not plot_result:  # 绘图不成功
            return 1

    # 5. 绘图存储
    plot_storage_result = plotting_util.plot_storage(fig, picture_file_name)

    if plot_storage_result is None:  # 图片存储不成功
        return 2
    else:
        return plot_storage_result
