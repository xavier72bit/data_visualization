__all__ = ["AccessLog"]


class AccessLog:
    """
    access_log表的数据对象
    """
    __slots__ = ['access_log_id', 'access_date_time', 'access_token',
                 'access_state', 'delete_flag', 'access_log_message']

    def __init__(self, access_log_id=None, access_date_time=None, access_token=None,
                 access_state=None, delete_flag=None, access_log_message=None):
        self.access_log_id = access_log_id
        self.access_date_time = access_date_time
        self.access_token = access_token
        self.access_state = access_state
        self.delete_flag = delete_flag
        self.access_log_message = access_log_message
