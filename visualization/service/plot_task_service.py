from project_common import DATE_TIME_NOW
from visualization.dao import plot_task_dao
from visualization.utils.do.data_object import PlotTask
from visualization.utils.do.data_object_util import general_primary_key


def create(plot_task: PlotTask) -> PlotTask | None:
    """
    创建一个新的plot_task并插入数据库。

    :return: 成功plot_result，失败None。
    """
    # 验证access_log_id非空
    if plot_task.access_log_id is None:
        return None

    # 设置主键ID
    plot_task.plot_task_id = general_primary_key()

    # 设置plot_task创建时间
    plot_task.plot_task_create_time = DATE_TIME_NOW

    # 插入操作
    insert_result = plot_task_dao.insert(plot_task)

    # 根据影响行数判断是否插入成功
    if insert_result:
        return plot_task
    else:
        return None


def delete(plot_task: PlotTask) -> bool:
    """
    从数据库中删除

    :return: 成功True，失败False。
    """
    delete_result = plot_task_dao.delete(plot_task)

    if delete_result:
        return True
    else:
        return False


def update(plot_task: PlotTask) -> bool:
    """
    更新plot_task信息。

    :return: 成功True，失败False。
    """
    # 验证传入的plot_result在数据库中是否有记录
    old_plot_result = plot_task_dao.select_one(plot_task)

    if old_plot_result is None:
        return False

    # 更新操作
    update_result = plot_task_dao.update(plot_task)

    # 根据影响行数判断是否更新成功
    if update_result:
        return True
    else:
        return False


def read_one(plot_task: PlotTask) -> PlotTask | None:
    """
    从数据库读取plot_task

    :return: 成功PlotTask，失败None。
    """
    return plot_task_dao.select_one(plot_task)


def read_list_by_access_log_id(plot_task: PlotTask) -> list[PlotTask] | None:
    """
    根据access_log_id，从数据库读取plot_task列表

    :return: 成功List[PlotResult]，失败None
    """
    return plot_task_dao.select_list_by_access_log_id(plot_task)
