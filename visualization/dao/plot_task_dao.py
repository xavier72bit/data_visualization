from visualization.utils.do.data_object import PlotTask
from visualization.utils.db.pymysql_util import MysqlUtil


def insert(plot_task: PlotTask) -> int:
    """
    INSERT

    :return: 操作影响行数(0为False)
    """

    sql = 'INSERT INTO plot_task (plot_task_id, access_log_id, plot_task_support_flag, plot_task_support_type, plot_task_create_time, plot_task_data) VALUES (%s, %s, %s, %s, %s, %s);'
    args = (
        plot_task.plot_task_id,
        plot_task.access_log_id,
        plot_task.plot_task_support_flag,
        plot_task.plot_task_support_type,
        plot_task.plot_task_create_time,
        plot_task.plot_task_data
    )

    with MysqlUtil() as mu:
        result = mu.insert(sql, args)

    return result


def delete(plot_task: PlotTask) -> int:
    """
    DELETE

    :return: 操作影响行数(0为False)
    """
    sql = 'DELETE FROM plot_task WHERE plot_task_id = %s;'
    args = (
        plot_task.plot_task_id
    )

    with MysqlUtil() as mu:
        result = mu.delete(sql, args)

    return result


def update(plot_task: PlotTask) -> int:
    """
    UPDATE

    :return: 操作影响行数(0为False)
    """
    sql = 'UPDATE plot_task SET plot_task_id = %s, access_log_id = %s, plot_task_support_flag = %s, plot_task_support_type = %s, plot_task_create_time = %s, plot_task_data = %s WHERE plot_task_id = %s;'
    args = (
        plot_task.plot_task_id,
        plot_task.access_log_id,
        plot_task.plot_task_support_flag,
        plot_task.plot_task_support_type,
        plot_task.plot_task_create_time,
        plot_task.plot_task_data,
        plot_task.plot_task_id
    )

    with MysqlUtil() as mu:
        result = mu.update(sql, args)

    return result


def select_one(plot_task: PlotTask) -> PlotTask | None:
    """
    SELECT

    :return: 查询到：PlotTask对象；未查询到：None。
    """
    sql = 'SELECT plot_task_id, access_log_id, plot_task_support_flag, plot_task_support_type, plot_task_create_time, plot_task_data FROM plot_task WHERE plot_task_id = %s LIMIT 0, 1;'
    args = (
        plot_task.plot_task_id,
    )

    with MysqlUtil() as mu:
        result = mu.select_one(sql, args)

    if result is not None:
        plot_task_result = PlotTask(**result)
    else:
        plot_task_result = None

    return plot_task_result


def select_list_by_access_log_id(plot_task: PlotTask) -> list[PlotTask] | None:
    """
    SELECT

    :return: 查询到：包含多个PlotTask数据对象的列表；未查询到：None。
    """
    sql = 'SELECT plot_task_id, access_log_id, plot_task_support_flag, plot_task_support_type, plot_task_create_time, plot_task_data FROM plot_task WHERE access_log_id LIKE %s;'
    args = (
        plot_task.access_log_id,
    )

    with MysqlUtil() as mu:
        result = mu.select_list(sql, args)

    # 这一步是判断result是否为空列表或None
    if result:
        plot_task_result_list = [PlotTask(**row) for row in result]
    else:
        plot_task_result_list = None

    return plot_task_result_list
