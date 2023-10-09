"""
定义在这里的类：

PlotDataSource:
1. PlotDataSource是绘图所需的数据源，一个列表

PlotChart：
1. PlotChart对应一个图片中的一个图表，比如折线图中的一条线就是一个PlotChart
2. 包含两个PlotDataSource，一个2D图表中有两个绘图数据源

PlotFigure:
1. PlotFigure对应一张图片，绘图的结果图片就是一个PlotFigure
2. PlotFigure中组合了plt.Figure和plt.Axes(或plt.PolarAxes)两个类
    * plt.Figure负责图片的保存
    * plt.Axes(或plt.PolarAxes)负责根据PlotChart的属性绘制图表
"""
import datetime
import itertools
from loguru import logger
import matplotlib.pyplot as plt

from visualization.utils.plotting import plotting_util
from visualization.utils.plotting.functions import (
    draw_plot_column,
    draw_plot_line,
    draw_plot_pie,
    draw_plot_bar,
    draw_plot_radar
)

# -----------------------------------------------------
# 设置pyplot样式
# -----------------------------------------------------

# 设置主题
plt.style.use('ggplot')

# 设置字体
font_rc = {
    'family': 'SimSun',
    'size': '12'
}

plt.rc('font', **font_rc)

# -----------------------------------------------------
# 本模块内部使用的常量
# -----------------------------------------------------

# 日期时间字符串解析格式
_CONST_DATETIME_FORMAT_STRING_TUPLE = (
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
    '%Y-%m',
    '%Y/%m',
    '%m-%d',
    '%m/%d',
    '%H:%M:%S',
    '%H:%M'
)

# 绘图类型与绘图函数对照字典
_CONST_PLOTTING_TYPE_FUNCTION_DICT = {
    1: draw_plot_line.draw_one_line,
    2: draw_plot_column.draw_one_column,
    3: draw_plot_bar.draw_bar,
    4: draw_plot_pie.draw_pie,
    5: draw_plot_radar.draw_radar,
}

# 需要用到极坐标的绘图类型元组
_CONST_PLOTTING_TYPE_IS_POLAR_AXES_TUPLE = (
    5,
)

# 柱状图与折线图的公用颜色循环(解决柱状图与折线图颜色相同的问题)
_CONST_COLUMN_AND_LINE_COLOR_CYCLE_TUPLE = tuple(item['color'] for item in plt.rcParams['axes.prop_cycle'])

# -----------------------------------------------------
# 本模块内部使用的工具函数
# -----------------------------------------------------


def _convert_string_2_datetime(test_string: str) -> str | datetime.datetime:
    """
    字符串转换为datetime测试，测试标准是datetime_format_string_tuple

    :return: 成功返回datetime.datetime类，失败返回原字符串
    """
    datetime_type_data = None
    for datetime_format in _CONST_DATETIME_FORMAT_STRING_TUPLE:  # 使用预定义的时间字符串格式化模版解析
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
    绘图所需数据源类，存储数据源

    数据类型示例：
    1. 数字类型(number) -> int | float: `1` `3.1415926`
    2. 类别类型(catalog) -> str: `"人"` `"牛马"` `"13#"` `"1234"`
    3. 时间类型(datetime) -> str: `"2018-01-01"` `"03:23"` `"2018-01-01 03:23:23"` `"2018-01-01T20:30:38"` `2018/01/01`
    """
    # 数据源中的具体数据
    data: list | dict | None = None
    # 数据源的长度
    data_source_length: int = 0
    # 数据源中的数据类型：['catalog' | 'datetime' | 'number']
    data_type: str | None = None
    # 数据源是否有效
    is_data_valid: bool = False
    # 数据源的注释（图例要用）
    data_source_comment: str = ""

    def __init__(self, data: dict | list | None, comment: str):
        self.set_data(data)
        self.data_source_comment = comment

    def set_data(self, data: dict | list | None):
        """
        分析并保存数据源
        """
        # 第一步：先存储数据
        self.data = data

        # 第二步：判定数据源是否为空
        if self.data is None:
            self.is_data_valid = False

        # 第三步：判断数据源是否有效
        if type(self.data) is list:  # 当数据源为list
            self.data_source_length = len(self.data)
            self.is_data_valid = False if self.data_source_length == 0 else True
        else:  # 其他数据类型的数据源无效
            self.is_data_valid = False

        # 第四步：判断并校验数据源中的数据类型
        if self.is_data_valid:  # 当数据源有效
            data_type_set = {type(item) for item in self.data}

            if data_type_set <= {int, float}:  # data_type_set 是 {int}、{float} 或 {int, float}
                self.data_type = 'number'
                self.is_data_valid = True

            elif data_type_set == {str}:  # data_type_set 是 {str}
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


class PlotChart:
    """
    绘制的图表类
    """
    # 所使用的两个数据源对象list，分别是[x轴数据, y轴数据]
    plot_data_source_object_list: list[PlotDataSource] | None = None
    # 图表类型
    plot_type: int | None = None
    # 是否需要极坐标
    is_polar_ax: bool = False
    # 绘图使用的matplotlib.Axes
    plot_execute_ax: plt.Axes | None = None
    # 该图表的绘制数据源长度
    plot_data_source_length: int = 0

    def __init__(self, plot_data_source_object_list, plot_type):
        self.plot_data_source_object_list = plot_data_source_object_list
        self.plot_type = plot_type

        # 判断是否需要极坐标
        if self.plot_type in _CONST_PLOTTING_TYPE_IS_POLAR_AXES_TUPLE:
            self.is_polar_ax = True

        # 获取图表绘制长度
        self.plot_data_source_length = plot_data_source_object_list[0].data_source_length

    def set_plot_execute_ax(self, plot_execute_ax: plt.Axes | plt.PolarAxes):
        self.plot_execute_ax = plot_execute_ax

    def plotting(self, color: str | None = None) -> bool:
        """
        执行绘图过程
        """
        # 校验
        if (self.plot_data_source_object_list is None
                or len(self.plot_data_source_object_list) != 2):
            logger.error("数据源对象个数有误")
            return False

        if self.plot_type is None:
            logger.error("未指定plot_type")
            return False

        if self.plot_execute_ax is None:
            logger.error("没有绘图所需的Axe对象")
            return False

        # 1. 获取两个plot_data_source_object(x,y)
        pdsox, pdsoy = self.plot_data_source_object_list

        # 2. 分析数据源中的数据类型是否为datetime
        is_xa_time = True if pdsox.data_type == 'datetime' else False

        # 获取绘图函数
        try:
            plotting_function = _CONST_PLOTTING_TYPE_FUNCTION_DICT[self.plot_type]
            logger.info("执行函数: {0}".format(plotting_function.__name__))
        except KeyError:
            logger.error("不支持的plot_type")
            return False

        return plotting_function(
            self.plot_execute_ax,
            pdsox.data,
            pdsoy.data,
            is_xa_time=is_xa_time,
            label=pdsoy.data_source_comment,
            color=color
        )


class PlotFigure:
    """
    绘图的图片类
    """
    # plt.Figure对象
    fig: plt.Figure | None = None
    # plt.Axe对象
    ax: plt.Axes | plt.PolarAxes | None = None
    # 图片存储本地路径
    fig_local_path: str | None = None

    def __init__(self, is_polar_ax: bool = False, fig_title: str | None = None):
        # 生成画布与坐标系
        # TODO: 动态调整图片大小，长还是短，高还是矮
        if is_polar_ax:
            self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10.24, 7.68))
        else:
            self.fig, self.ax = plt.subplots(figsize=(10.24, 7.68))

        # 设置图片标题
        if fig_title is not None:
            self.ax.set_title(fig_title)

    def figure_save(self, file_name: str):
        """
        存储图片
        """
        self.fig_local_path = plotting_util.plot_storage(self.fig, file_name)


# -----------------------------------------------------
# 绘图引擎核心函数
# -----------------------------------------------------

def plot_charts_on_figure(plot_figure: PlotFigure, plot_chart_list: list[PlotChart]) -> bool:
    """
    在PlotFigure 上依次绘制 plot_chart_list 中的 PlotChart

    :param plot_figure: 需要进行绘图的PlotFigure类
    :param plot_chart_list: 包含PlotChart的列表

    :return: 绘图操作结果
    """
    # 开始循环绘图
    for pc, color in zip(plot_chart_list, itertools.cycle(_CONST_COLUMN_AND_LINE_COLOR_CYCLE_TUPLE)):
        # 绑定绘制PlotChart所需的plt.Axes对象
        pc.set_plot_execute_ax(plot_figure.ax)

        # 绘图
        if not pc.plotting(color=color):
            return False

    return True


def plot_multi_column_charts_on_figure(plot_figure: PlotFigure, plot_chart_list: list[PlotChart]) -> bool:
    """
    在PlotFigure 上依次绘制 plot_chart_list 中的 PlotChart
    需要绘制多个柱状图，则调用此函数，先绘制并列柱状图，再绘制其他图形

    :param plot_figure: 需要进行绘图的PlotFigure类
    :param plot_chart_list: 包含PlotChart的列表

    :return: 绘图操作结果
    """
    # 处理plot_chart_list，过滤出所有柱状图类型的图表(ctcl: column_type_chart_list)
    ctcl = list(filter(lambda x: x.plot_type == 2, plot_chart_list))

    # 获取x轴数据源(xpdso: x_plot_data_source_object)
    # 在plot_stream中已经过了“多个绘图数据共享X轴的校验”，所以拿ctcl的第一个元素就行
    xpdso: PlotDataSource = ctcl[0].plot_data_source_object_list[0]
    # 获取x轴数据列表(dlx: data_list_x)
    dlx: list = xpdso.data

    # 获取多个y轴数据列表组成的字典(ddy: data_dict_y)
    ddy: dict = dict()
    for pc in ctcl:
        # 获取y轴数据源(ypdso: y_plot_data_source_object)
        ypdso: PlotDataSource = pc.plot_data_source_object_list[1]
        ddy[ypdso.data_source_comment] = ypdso.data

    # 绘制并列柱状图
    if not draw_plot_column.draw_multi_column(plot_figure.ax, dlx, ddy):
        return False

    # 绘制剩余的图
    if set(ctcl) == set(plot_chart_list):
        return True
    else:
        # 将绘制并列柱状图时使用过的颜色移到颜色循环元组的最后面
        # TODO: 该操作是否有更优的算法？
        color_offset: int = len(ddy)
        cct = _CONST_COLUMN_AND_LINE_COLOR_CYCLE_TUPLE
        new_color_cycle_tuple = cct[color_offset::1] + cct[0:color_offset:1]

        for pc, color in zip(set(plot_chart_list) - set(ctcl), itertools.cycle(new_color_cycle_tuple)):
            # 绑定绘制PlotChart所需的plt.Axes对象
            pc.set_plot_execute_ax(plot_figure.ax)

            # 绘图
            if not pc.plotting(color=color):
                return False

        return True
