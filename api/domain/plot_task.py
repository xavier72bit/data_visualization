__all__ = ["PlotTask"]

class PlotTask:
    """
    plot_task表的数据对象
    """
    __slots__ = ['plot_task_id', 'plot_task_create_date_time', 'plot_task_finish_date_time',
                 'plot_task_state', 'access_log_id', 'delete_flag']

    def __init__(self, plot_task_id=None, plot_task_create_date_time=None, plot_task_finish_date_time=None,
                 plot_task_state=None, access_log_id=None, delete_flag=None):
        self.plot_task_id = plot_task_id
        self.plot_task_create_date_time = plot_task_create_date_time
        self.plot_task_finish_date_time = plot_task_finish_date_time
        self.plot_task_state = plot_task_state
        self.access_log_id = access_log_id
        self.delete_flag = delete_flag