from data_visualization.domain import DomainInterface


__all__ = ["PlotResult"]


class PlotResult(DomainInterface):
    """
    plot_result表的数据对象
    """
    __slots__ = ['plot_result_id', 'access_log_id',
                 'plot_result_finish_date_time', 'plot_result_finish_state',
                 'plot_result_local_path', 'plot_result_upload_date_time',
                 'plot_result_upload_state', 'plot_result_url']

    def __init__(self,
                 plot_result_id=None,
                 access_log_id=None,
                 plot_result_finish_date_time=None,
                 plot_result_finish_state=None,
                 plot_result_local_path=None,
                 plot_result_upload_date_time=None,
                 plot_result_upload_state=None,
                 plot_result_url=None):
        self.plot_result_id = plot_result_id
        self.access_log_id = access_log_id
        self.plot_result_finish_date_time = plot_result_finish_date_time
        self.plot_result_finish_state = plot_result_finish_state
        self.plot_result_local_path = plot_result_local_path
        self.plot_result_upload_date_time = plot_result_upload_date_time
        self.plot_result_upload_state = plot_result_upload_state
        self.plot_result_url = plot_result_url
