from dataclasses import dataclass


@dataclass
class AccessLog:
    """
    access_log(请求记录表)对应的数据对象

    access_log_id(PK)[str | None]: 请求记录ID，一个UUID字符串
    access_date_time[str | None]: 请求日期时间，一个"%Y-%m-%d %H:%M:%S"格式的时间字符串
    access_ip[str | None]: 请求IP，一个字符串
    access_url[str | None]: 请求URL，一个字符串
    access_param[str | None]: 请求参数（POST方法的body），一个json字符串，在为此属性赋值时要使用json.dumps(arg: dict | list)
    """
    access_log_id: str | None = None
    access_date_time: str | None = None
    access_ip: str | None = None
    access_url: str | None = None
    access_param: str | None = None


@dataclass
class PlotTask:
    """
    plot_task(绘图任务表)对应的数据对象

    plot_task_id(PK)[str | None]: 绘图任务ID，一个UUID字符串
    access_log_id[str | None]: 绘图任务所属的访问记录ID，一个UUID字符串，access_log表的PK
    plot_task_support_flag[int | None]: 绘图任务状态标识，一个整数
    plot_task_support_type[str | None]: 绘图任务所支持的绘图类型，一个json字符串，在为此属性赋值时要使用json.dumps(arg: list[int])
    plot_task_create_time[str | None]: 绘图任务创建时间，一个"%Y-%m-%d %H:%M:%S"格式的时间字符串
    plot_task_data[str | None]: 绘图任务的绘图数据，一个json字符串，在为此属性赋值时要使用json.dumps(arg: dict | list)
    """
    plot_task_id: str | None = None
    access_log_id: str | None = None
    plot_task_support_flag: int | None = None
    plot_task_support_type: str | None = None
    plot_task_create_time: str | None = None
    plot_task_data: str | None = None


@dataclass
class PlotResult:
    """
    plot_result(绘图结果表)对应的数据对象

    plot_result_id(PK)[str | None]: 绘图结果ID，一个UUID字符串
    plot_task_id[str | None]: 绘图结果所属的绘图任务ID，一个UUID字符串，plot_task表的PK
    plot_result_finish_date_time[str | None]: 绘图结果完成时间，一个"%Y-%m-%d %H:%M:%S"格式的时间字符串
    plot_result_local_path[str | None]: 绘图结果图片本地路径，一个字符串
    plot_result_upload_date_time[str | None]: 绘图结果图片上传时间，一个"%Y-%m-%d %H:%M:%S"格式的时间字符串
    plot_result_url[str | None]: 绘图结果的远程URL，一个字符串
    plot_result_state[int | None]: 绘图状态，一个整数
    plot_result_type[str | None]: 绘图类型，一个json字符串，在为此属性赋值时要使用json.dumps(arg: list)
    """
    plot_result_id: str | None = None
    plot_task_id: str | None = None
    plot_result_finish_date_time: str | None = None
    plot_result_local_path: str | None = None
    plot_result_upload_date_time: str | None = None
    plot_result_url: str | None = None
    plot_result_state: int | None = None
    plot_result_type: str | None = None
    plot_result_title: str | None = None
