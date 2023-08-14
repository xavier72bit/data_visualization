# 请求记录表
create table access_log
(
    access_log_id      varchar(36)  not null comment '请求记录ID'
        primary key,
    access_date_time   datetime     null comment '请求日期时间',
    access_token       varchar(100) null comment '请求token',
    access_log_message varchar(500) null comment '请求消息内容',
    access_ip          varchar(50)  null comment '请求源IP地址'
)
    comment '请求记录表' collate = utf8mb4_unicode_ci;


# 绘图结果表
create table access_log
(
    access_log_id      varchar(36)  not null comment '请求记录ID'
        primary key,
    access_date_time   datetime     null comment '请求日期时间',
    access_token       varchar(100) null comment '请求token',
    access_log_message varchar(500) null comment '请求消息内容',
    access_ip          varchar(50)  null comment '请求源IP地址'
)
    comment '请求记录表' collate = utf8mb4_unicode_ci;
