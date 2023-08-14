# 数据库准备

```sql
create database data_visualization;
CREATE USER 'data_visualization'@'%' IDENTIFIED BY 'data_visualization';
GRANT ALL PRIVILEGES ON `data_visualization`.* TO 'data_visualization'@'%' WITH GRANT OPTION;
```

```sql
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
```

# 依赖安装

```bash
pip install -r requirements.txt
```

# 示例接口

### 1. 根据ip地址统计访问次数

GET http://127.0.0.1:5001/sysinfo/ip_access_count?ip_address=127.0.0.1

### 2. 提供两个数据序列绘图

当序列长度小于7时，是柱状图，当序列长度大于7时，是折线图。

POST http://127.0.0.1:5001/plot/source

##### 示例1

请求体：

```json
{
  "plot_title": "订单量",
  "time_data_list": ["工人1", "工人2", "工人3", "工人4", "工人5", "工人6", "工人7"],
  "num_data_list": [1, 2, 3, 4, 5, 6, 7]
}
```

响应

```json
{
  "code": 0,
  "data": "https://fs.zhulin.xin/group1/M00/00/07/dT7MrWTaHEOARmpRAAAknNr7VZM568.png",
  "msg": "绘图成功"
}
```

##### 示例2

请求体

```json
{
  "plot_title": "订单量",
  "time_data_list": ["工人1", "工人2", "工人3", "工人4", "工人5", "工人6", "工人7"],
  "num_data_list": [1, 2, 3, 4, 5, 6, 7, 8]
}
```

响应

```json
{
  "code": 1,
  "data": null,
  "msg": "数据序列长度不一致"
}
```