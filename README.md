# 数据库准备

```sql
CREATE SCHEMA `data_visualization` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
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

# 项目启动

运行 main.py

# 示例接口

### 1. 根据ip地址统计访问次数

GET http://127.0.0.1:5001/sysinfo/ip_access_count?ip_address=127.0.0.1

### 2. 提供两个数据序列绘图

当序列长度小于7时，是柱状图，当序列长度大于7时，是折线图。

POST http://127.0.0.1:5001/plot/source/two

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
  "data": "http://192.168.64.17:9001/py-data-visualization/f803e961-0bf0-410e-b387-25592b935b23.png",
  "msg": "绘图成功"
}
```

##### 示例2

请求体：

```json
{
  "plot_title": "订单量",
  "time_data_list": ["07-03", "07-04", "07-05", "07-06", "07-07", "07-08", "07-09", "07-10", "07-11", "07-12"],
  "num_data_list": [123, 32, 85, 93, 73, 88, 94, 83, 88, 79]
}
```

响应

```json
{
  "code": 0,
  "data": "http://192.168.64.17:9001/py-data-visualization/b6762940-b61f-40d6-a8fb-eacb12e5067a.png",
  "msg": "绘图成功"
}
```

##### 示例3

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

### 3. 提供一个数据序列，一个数据字典绘图

数据字典项少于3，是并列柱状图，大于3，是多条折线图

POST http://127.0.0.1:5001/plot/source/three

##### 示例1

请求体：

```json
{
  "plot_title": "订单量",
  "time_data_list": ["07-03", "07-04", "07-05", "07-06", "07-07", "07-08", "07-09", "07-10", "07-11", "07-12"],
  "catalog_num_data_dict": {
    "工人1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "工人2": [15, 2, 4, 5, 7, 1, 2, 33, 45, 77],
    "工人3": [17, 16, 44, 32, 56, 7, 9, 12, 33, 32]
  }
}
```

响应：

```json
{
  "code": 0,
  "data": "http://192.168.64.17:9001/py-data-visualization/ac3707fb-0d60-4946-b801-b7a674d1e8bf.png",
  "msg": "绘图成功"
}
```

##### 示例2

请求体：

```json
{
  "plot_title": "订单量",
  "time_data_list": ["07-03", "07-04", "07-05", "07-06", "07-07", "07-08", "07-09", "07-10", "07-11", "07-12"],
  "catalog_num_data_dict": {
    "工人1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "工人2": [15, 2, 4, 5, 7, 1, 2, 33, 45, 77],
    "工人3": [17, 16, 44, 32, 56, 7, 9, 12, 33, 32],
    "工人4": [12, 66, 89, 3, 67, 12, 44, 78, 55, 21],
    "工人5": [88, 32, 15, 31, 51, 66, 9, 3, 9, 43],
    "工人6": [5, 3, 12, 22, 90, 75, 12, 36, 99, 32]
  }
}
```

响应：

```json
{
  "code": 0,
  "data": "http://192.168.64.17:9001/py-data-visualization/9676610f-989e-40f7-af47-336eae0c0fd8.png",
  "msg": "绘图成功"
}
```

##### 示例3

请求体：

```json
{
  "plot_title": "订单量",
  "time_data_list": ["07-03", "07-04", "07-05", "07-06", "07-07", "07-08", "07-09", "07-10", "07-11", "07-12"],
  "catalog_num_data_dict": {
    "工人1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "工人2": [15, 2, 4, 5, 7, 1, 2, 33, 45]
  }
}
```

响应：

```json
{
  "code": 1,
  "data": null,
  "msg": "数据序列长度不一致"
}
```