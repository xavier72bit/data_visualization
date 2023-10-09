from visualization.utils.do.data_object import PlotResult
from visualization.utils.db.pymysql_util import MysqlUtil


def insert(plot_result: PlotResult) -> int:
    """
    INSERT

    :return: 操作影响行数
    """
    sql = 'INSERT INTO plot_result (plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_local_path, plot_result_upload_date_time, plot_result_url, plot_result_state, plot_result_type, plot_result_title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
    args = (
        plot_result.plot_result_id,
        plot_result.plot_task_id,
        plot_result.plot_result_finish_date_time,
        plot_result.plot_result_local_path,
        plot_result.plot_result_upload_date_time,
        plot_result.plot_result_url,
        plot_result.plot_result_state,
        plot_result.plot_result_type,
        plot_result.plot_result_title
    )

    with MysqlUtil() as mu:
        result = mu.insert(sql, args)

    return result


def delete(plot_result: PlotResult) -> int:
    """
    DELETE

    :return: 操作影响行数
    """
    sql = 'DELETE FROM plot_result WHERE plot_result_id = %s;'
    args = (
        plot_result.plot_result_id,
    )

    with MysqlUtil() as mu:
        result = mu.delete(sql, args)

    return result


def update(plot_result: PlotResult) -> int:
    """
    UPDATE

    :return: 操作影响行数
    """
    sql = 'UPDATE plot_result SET plot_result_id = %s, plot_task_id = %s, plot_result_finish_date_time = %s, plot_result_local_path = %s, plot_result_upload_date_time = %s, plot_result_url = %s, plot_result_state = %s, plot_result_type = %s, plot_result_title = %s WHERE plot_result_id = %s;'
    args = (
        plot_result.plot_result_id,
        plot_result.plot_task_id,
        plot_result.plot_result_finish_date_time,
        plot_result.plot_result_local_path,
        plot_result.plot_result_upload_date_time,
        plot_result.plot_result_url,
        plot_result.plot_result_state,
        plot_result.plot_result_type,
        plot_result.plot_result_title,
        plot_result.plot_result_id
    )

    with MysqlUtil() as mu:
        result = mu.update(sql, args)

    return result


def select_one(plot_result: PlotResult) -> PlotResult | None:
    """
    SELECT

    :return: 查询到：PlotResult对象；未查询到：None。
    """
    sql = 'SELECT plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_local_path, plot_result_upload_date_time, plot_result_url, plot_result_state, plot_result_type, plot_result_title FROM plot_result WHERE plot_result_id = %s LIMIT 0, 1;'
    args = (
        plot_result.plot_result_id,
    )

    with MysqlUtil() as mu:
        result = mu.select_one(sql, args)

    if result is not None:
        plot_result_result = PlotResult(**result)
    else:
        plot_result_result = None

    return plot_result_result


def select_one_by_plot_task_id_and_plot_result_type(plot_result: PlotResult) -> PlotResult | None:
    sql = 'SELECT plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_local_path, plot_result_upload_date_time, plot_result_url, plot_result_state, plot_result_type, plot_result_title FROM plot_result WHERE plot_task_id LIKE %s AND plot_result_type LIKE %s LIMIT 0, 1;'
    args = (
        plot_result.plot_task_id,
        plot_result.plot_result_type
    )

    with MysqlUtil() as mu:
        result = mu.select_one(sql, args)

    if result is not None:
        plot_result_result = PlotResult(**result)
    else:
        plot_result_result = None

    return plot_result_result


def select_list_by_plot_task_id(plot_result: PlotResult) -> list[PlotResult] | None:
    """
    SELECT

    :return: 查询到：包含多个PlotResult数据对象的列表；未查询到：None。
    """
    sql = 'SELECT plot_result_id, plot_task_id, plot_result_finish_date_time, plot_result_local_path, plot_result_upload_date_time, plot_result_url, plot_result_state, plot_result_type, plot_result_title FROM plot_result WHERE plot_task_id LIKE %s;'
    args = (
        plot_result.plot_task_id,
    )

    with MysqlUtil() as mu:
        result = mu.select_list(sql, args)

    # 这一步是判断result是否为空列表或None
    if result:
        plot_result_result_list = [PlotResult(**row) for row in result]
    else:
        plot_result_result_list = None

    return plot_result_result_list
