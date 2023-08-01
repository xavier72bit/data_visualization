__all__ = ["PlotResult"]


class PlotResult:
    """
    plot_result表的数据对象
    """
    __slots__ = ['plot_result_id', 'plot_task_id', 'plot_result_finish_date_time',
                 'plot_result_finish_state', 'plot_result_local_path', 'plot_result_upload_date_time',
                 'plot_result_upload_state', 'plot_result_url', 'delete_flag']

    def __init__(self, plot_result_id=None, plot_task_id=None, plot_result_finish_date_time=None,
                 plot_result_finish_state=None, plot_result_local_path=None, plot_result_upload_date_time=None,
                 plot_result_upload_state=None, plot_result_url=None, delete_flag=None):
        self.plot_result_id = plot_result_id
        self.plot_task_id = plot_task_id
        self.plot_result_finish_date_time = plot_result_finish_date_time
        self.plot_result_finish_state = plot_result_finish_state
        self.plot_result_local_path = plot_result_local_path
        self.plot_result_upload_date_time = plot_result_upload_date_time
        self.plot_result_upload_state = plot_result_upload_state
        self.plot_result_url = plot_result_url
        self.delete_flag = delete_flag