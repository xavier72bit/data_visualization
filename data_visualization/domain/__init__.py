from typing import List, Protocol

"""
data_visualization.domain 软件包的说明：

该软件包为所有表的数据对象，将表的一条记录转化为一个对象。

__init__.py提供：
1. Domain：注解表达式所需的类型
2. DomainInterface：该包下所有Domain类的通用父类

其他的.py文件创建规则：
一个数据对象对应一个py文件。（比如access_log表对应一个access_log.py）
"""


class Domain(Protocol):
    """
    Domain类型的注解表达式
    """

    @classmethod
    def get_all_attributes(cls) -> List:
        pass


class DomainInterface:
    # Domain数据对象的所有的属性都存在__slots__中
    __slots__ = []

    @classmethod
    def get_all_attributes(cls) -> List:
        """
        获取__slots__列表
        """
        return cls.__slots__
