# 写在前面

本项目代码已迁移到其他私有仓库，此处不再进行更新（或随缘更新）。

这是我写的第一个python项目，项目开始于2023年4月23日，中间断断续续的边学边开发，挺有纪念意义的，就让它作为里程碑留在我的GitHub主页吧！

# 项目理论基础

![](static/choose_chart.jpg)

# 数据库准备

```sql
CREATE SCHEMA `data_visualization` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'data_visualization'@'%' IDENTIFIED BY 'data_visualization';
GRANT ALL PRIVILEGES ON `data_visualization`.* TO 'data_visualization'@'%' WITH GRANT OPTION;
```

# 环境准备

## 依赖安装

```bash
pip3 install -r requirements.txt
```

## SimSun字体安装(Linux)

### 1. 下载SimSun字体文件

github上有一个收集常用字体的仓库，建议fork：https://github.com/Haixing-Hu/latex-chinese-fonts

在Linux系统中下载SimSun字体：

```bash
cd
wget https://github.com/Haixing-Hu/latex-chinese-fonts/raw/master/chinese/宋体/SimSun.ttc
mv SimSun.ttc SimSun.ttf
```

### 2. 将字体文件移动到matplotlib的字体目录中

#### 2.1 先获取matplotlib的mpl-data目录的位置

一定要在项目的虚环境中打开python-shell

```bash
shell> cd /root/yunzhu/dingwei-draw-image
shell> source venv/bin/activate
(venv)shell> python3
python>>> import matplotlib
python>>> matplotlib.get_data_path()
'/root/yunzhu/dingwei-draw-image/venv/lib/python3.10/site-packages/matplotlib/mpl-data'
```

#### 2.2 移动字体文件到matplotlib的字体目录中

```bash
cd /root/yunzhu/dingwei-draw-image/venv/lib/python3.10/site-packages/matplotlib/mpl-data/fonts/ttf
mv /root/SimSun.ttf .
```

### 3. 清理matplotlib的缓存

#### 3.1 先获取matplotlib缓存目录

一定要在项目的虚环境中打开python-shell

```bash
shell> cd /root/yunzhu/dingwei-draw-image
shell> source venv/bin/activate
(venv)shell> python3
python>>> import matplotlib
python>>> matplotlib.get_cachedir()
'/root/.cache/matplotlib'
```

#### 3.2 删除缓存目录下的所有文件

```bash
rm -f /root/.cache/matplotlib/*
```

# 项目启动

运行 main.py

# 接口使用说明

### 1. 测试服务可用

GET http://127.0.0.1:5001/sysinfo/test

### 2. 提供数据源

直接向接口提供绘图所需数据

POST http://127.0.0.1:5001/2d/data/submit

##### 示例

```json
{
    "data_source": {
        "data_source_1": {
            "data": [1, 2, 3, 4, 5, 6],
            "comment": "接单量"
        },
        "data_source_2": {
            "data": ["工人1", "工人2", "工人3", "工人4", "工人5", "工人6"],
            "comment": "工人"
        },
        "data_source_3": {
            "data": [12, 0, 14, 15, 16, 3],
            "comment": "工作量"
        }
    }
}
```

响应

```json
{
  "code": 0,
  "data": {
    "A": {
      "comment": "接单量-工人",
      "data_source_combination": ["data_source_1", "data_source_2"],
      "support_plot_type": [1, 2, 3, 4, 5]
    },
    "B": {
      "comment": "工人-工作量",
      "data_source_combination": ["data_source_2", "data_source_3"],
      "support_plot_type": [1, 2, 3, 4, 5]
    }
  },
  "msg": "480f861d-44ef-43e8-b030-1945594e4e16"
}
```

### 3. 绘图

POST http://127.0.0.1:5001/2d/chart/plotting

向绘图接口提交两个参数：

1. plot_key: 提供数据源接口返回的plot_key

```json
{
  "code": 0,
  "data": {
    "A": {
      "comment": "接单量-工人",
      "data_source_combination": ["data_source_1", "data_source_2"],
      "support_plot_type": [1, 2, 3, 4, 5]
    },
    "B": {
      "comment": "工人-工作量",
      "data_source_combination": ["data_source_2", "data_source_3"],
      "support_plot_type": [1, 2, 3, 4, 5]
    }
  },
  "msg": "480f861d-44ef-43e8-b030-1945594e4e16"   <-----这个就是plot_key
}
```

2. plot_requirement_list: 绘图要求列表，形式如下

* `["A1", "A2"]`
* `["A1"]`
* `["A1", "B1", "C1"]`

##### 示例

请求体

```json
{
    "plot_key": "480f861d-44ef-43e8-b030-1945594e4e16",
    "plot_requirement": {
        "figure1": {
            "type": ["A1", "B2"],
            "plot_title": "test figure"
        },
        "figure2": {
            "type": ["A1", "B2"],
            "plot_title": "test figure"
        },
        "figure3": {
            "type": ["A1"],
            "plot_title": "test figure"
        }
    }
}
```

响应

```json
{
    "code": 0,
    "data": {
        "figure1": "192.168.64.17:9001/py-data-visualization/8c329873-24de-4672-b8fc-f120e922571c.png",
        "figure2": "192.168.64.17:9001/py-data-visualization/8c329873-24de-4672-b8fc-f120e922571c.png",
        "figure3": "192.168.64.17:9001/py-data-visualization/da933a80-548a-46a6-807b-3220d22a16e2.png"
    },
    "msg": "绘图成功"
}
```