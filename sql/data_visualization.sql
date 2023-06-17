# 访问记录表
create table access_log
(
    access_log_id      varchar(36)  not null comment '请求记录ID',
    access_date_time   DATETIME     null comment '请求日期时间',
    access_token       varchar(50)  null comment '请求token',
    access_state       tinyint      null comment '请求结果状态',
    delete_flag        tinyint      null comment '删除标志',
    access_log_message varchar(500) null comment '请求消息内容',
    constraint access_log_pk
        primary key (access_log_id)
)
    comment '请求记录' collate = utf8mb4_unicode_ci;

# 绘图任务单表
create table plot_task
(
    plot_task_id               varchar(36) not null comment '任务单ID',
    plot_task_create_date_time datetime    null comment '任务单创建日期时间',
    plot_task_finish_date_time datetime    null comment '任务单完成日期时间',
    plot_task_state            tinyint     null comment '任务单状态',
    access_log_id         varchar(36) not null comment '任务单所属的访问记录ID',
    delete_flag           tinyint     null comment '删除标志',
    constraint access_log_pk
        primary key (plot_task_id)
)
    comment '绘图任务单' collate = utf8mb4_unicode_ci;

#绘图任务表
create table plot_result
(
    plot_result_id               varchar(38)   not null comment '绘图结果ID',
    plot_task_id                 varchar(36)   not null comment '绘图结果所属的绘图任务单ID',
    plot_result_finish_date_time datetime      null comment '绘图完成日期时间',
    plot_result_finish_state     tinyint       null comment '绘图结果完成状态',
    plot_result_local_path       varchar(1000) null comment '绘图本地路径',
    plot_result_upload_date_time datetime      null comment '绘图上传日期时间',
    plot_result_upload_state     tinyint       null comment '绘图上传状态',
    plot_result_url              varchar(1000) null comment '绘图URL',
    delete_flag                  tinyint       null comment '删除标志',
    constraint plot_result_pk
        primary key (plot_result_id)
)
    comment '绘图结果' collate = utf8mb4_unicode_ci;
