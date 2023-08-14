from data_visualization.domain import DomainInterface


__all__ = ["AccessLog"]


class AccessLog(DomainInterface):
    """
    access_log表的数据对象
    """
    __slots__ = ['access_log_id',
                 'access_date_time',
                 'access_token',
                 'access_log_message',
                 'access_ip']

    def __init__(self,
                 access_log_id=None,
                 access_date_time=None,
                 access_token=None,
                 access_log_message=None,
                 access_ip=None):
        self.access_log_id = access_log_id
        self.access_date_time = access_date_time
        self.access_token = access_token
        self.access_log_message = access_log_message
        self.access_ip = access_ip
