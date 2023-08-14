import functools

"""
data_visualization.service 软件包的说明：

在本项目中，Service层的职责：
1. 处理domain对象
2. 为api提供不同的功能函数
3. 进行数据处理与数据校验
"""


def check_two_data_list_len(func):
    """
    检查两个数据序列长度是否相同
    """
    @functools.wraps(func)
    def wrapper(data_list1, data_list2, plot_title):
        if len(data_list1) != len(data_list2):
            return 1
        else:
            return func(data_list1, data_list2, plot_title)

    return wrapper

