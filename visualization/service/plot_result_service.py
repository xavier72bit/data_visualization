from visualization.dao import plot_result_dao

from visualization.utils.do.data_object import PlotResult
from visualization.utils.do.data_object_util import general_primary_key


def create(plot_result: PlotResult) -> PlotResult | None:
    """
    创建一个新的plot_result并插入数据库。

    :return: 成功plot_result，失败None。
    """
    # 验证access_log_id非空
    if plot_result.access_log_id is None:
        return None

    # 设置主键ID
    plot_result.plot_result_id = general_primary_key()

    # 插入操作
    insert_result = plot_result_dao.insert(plot_result)

    # 根据影响行数判断是否插入成功
    if insert_result:
        return plot_result
    else:
        return None


def delete(plot_result: PlotResult) -> bool:
    """
    从数据库中删除

    :return:
    """
    delete_result = plot_result_dao.delete(plot_result)

    if delete_result:
        return True
    else:
        return False


def update(plot_result: PlotResult) -> bool:
    """
    更新plot_result信息。

    :return: 成功True，失败False。
    """
    # 验证传入的plot_result在数据库中是否有记录
    old_plot_result = plot_result_dao.select_one(plot_result)

    if old_plot_result is None:
        return False

    # 更新操作
    update_result = plot_result_dao.update(plot_result)

    # 根据影响行数判断是否更新成功
    if update_result:
        return True
    else:
        return False


def read_one(plot_result: PlotResult) -> PlotResult | None:
    """
    从数据库读取plot_result

    :return: 成功PlotResult，失败None。
    """

    return plot_result_dao.select_one(plot_result)


def read_list_by_access_log_id(plot_result: PlotResult) -> list[PlotResult] | None:
    """
    根据access_log_id，从数据库读取plot_result列表

    :return: 成功List[PlotResult]，失败None
    """

    return plot_result_dao.select_list_by_access_log_id(plot_result)
