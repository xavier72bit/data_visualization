from dataclasses import dataclass


@dataclass
class AccessLog:
    access_log_id: str | None = None
    access_date_time: str | None = None
    access_ip: str | None = None
    access_url: str | None = None
    access_param: str | None = None
    access_plot_type: str | None = None
    access_plot_flag: int | None = None


@dataclass
class PlotResult:
    plot_result_id: str | None = None
    access_log_id: str | None = None
    plot_result_finish_date_time: str | None = None
    plot_result_local_path: str | None = None
    plot_result_upload_date_time: str | None = None
    plot_result_url: str | None = None
    plot_result_state: int | None = None
    plot_result_type: str | None = None
