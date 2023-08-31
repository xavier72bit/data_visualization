import datetime

datetime_format_string_tuple = (
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


def string_2_datetime_test(test_string: str) -> str | datetime.datetime:
    """
    字符串转换为datetime测试，测试标准是datetime_format_string_tuple

    :return: 成功返回datetime.datetime类，失败返回原字符串
    """
    datetime_type_data = None
    for datetime_format in datetime_format_string_tuple:  # 使用预定义的时间字符串格式化模版解析
        try:
            datetime_type_data = datetime.datetime.strptime(test_string, datetime_format)

            if datetime_type_data is not None:  # 当发现解析成功时，更新flag，直接跳出循环
                return datetime_type_data
        except ValueError:
            continue  # 如果当前模板无法解析，则使用下一个模板进行解析

    if datetime_type_data is None:
        return test_string


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

    def __init__(self, data: dict | list | None):
        """
        直接将数据传进来，分析数据源在这里进行
        """
        # -----------------------------------------------------
        # 1. 先存储数据
        # -----------------------------------------------------

        self.data = data

        # -----------------------------------------------------
        # 2. 判定数据源是否为空
        # -----------------------------------------------------

        if self.data is None:
            self.is_data_valid = False

        # -----------------------------------------------------
        # 3. 判断数据源类型，同时判断数据源是否有效
        # -----------------------------------------------------

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
                    self.is_data_valid = False if self.data_source_length == 0 else True
                else:  # 不相同，设置数据源无效
                    self.is_data_valid = False

        else: # 其他数据类型的数据源无效
            self.is_data_valid = False

        # -----------------------------------------------------
        # 4. 判断并校验数据源中的数据类型
        # -----------------------------------------------------

        if self.data_source_type == 'list' and self.is_data_valid:  # 当数据源为list
            list_data_type_set = {type(item) for item in self.data}

            if list_data_type_set <= {int, float}:  # list_data_type_set 是 {int}、{float} 或 {int, float}
                self.data_type = 'number'
                self.is_data_valid = True

            elif list_data_type_set == {str}:  # list_data_type_set 是 {str}
                self.data = list(map(string_2_datetime_test, self.data))  # 执行一次datetime转换

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
