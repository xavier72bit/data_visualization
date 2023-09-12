# 请求记录表
create table access_log
(
    access_log_id    varchar(36)  not null comment '请求记录ID'
        primary key,
    access_date_time datetime     null comment '请求日期时间',
    access_ip        varchar(50)  null comment '请求源IP地址',
    access_url       varchar(100) null comment '请求url',
    access_param     json         null comment '请求数据',
    access_plot_type varchar(50)  null comment '请求数据能够绘制的图形类别',
    access_plot_flag tinyint      null comment '请求数据是否可以绘图'
)
    comment '请求记录表' collate = utf8mb4_unicode_ci;


# 绘图结果表
create table plot_result
(
    plot_result_id               varchar(36)   not null comment '绘图结果ID'
        primary key,
    access_log_id                varchar(36)   null comment '绘图所属访问ID',
    plot_result_finish_date_time datetime      null comment '绘图完成日期时间',
    plot_result_local_path       varchar(1000) null comment '绘图本地路径',
    plot_result_upload_date_time datetime      null comment '绘图上传日期时间',
    plot_result_url              varchar(1000) null comment '绘图访问URL',
    plot_result_state            tinyint       null comment '绘图状态',
    plot_result_type             varchar(10)   null comment '绘图类型'
)
    comment '绘图结果' collate = utf8mb4_unicode_ci;