# 请求记录表
create table access_log
(
    access_log_id      varchar(36)  not null comment '请求记录ID'
        primary key,
    access_date_time   datetime     null comment '请求日期时间',
    access_token       varchar(100) null comment '请求token',
    access_state       tinyint      null comment '请求结果状态',
    access_log_message varchar(500) null comment '请求消息内容',
    access_ip          varchar(50)  null comment '请求源IP地址'
)
    comment '请求记录表' collate = utf8mb4_unicode_ci;



#绘图结果表
create table plot_result
(
    plot_result_id               varchar(36)   not null comment '绘图结果ID'
        primary key,
    access_log_id                varchar(36)   null comment '绘图所属访问ID',
    plot_result_finish_date_time datetime      null comment '绘图完成日期时间',
    plot_result_finish_state     tinyint       null comment '绘图结果完成状态',
    plot_result_local_path       varchar(1000) null comment '绘图本地路径',
    plot_result_upload_date_time datetime      null comment '绘图上传日期时间',
    plot_result_upload_state     tinyint       null comment '绘图上传状态',
    plot_result_url              varchar(1000) null comment '绘图访问URL'
)
    comment '绘图结果' collate = utf8mb4_unicode_ci;


