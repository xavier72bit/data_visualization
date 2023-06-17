### 数据库准备

```sql
create database data_visualization;
CREATE USER 'data_visualization'@'%' IDENTIFIED BY 'data_visualization';
GRANT ALL PRIVILEGES ON `data_visualization`.* TO 'data_visualization'@'%' WITH GRANT OPTION;
```