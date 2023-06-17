# 数据可视化设计

图标选择的依据：

![](./static/choose_chart.jpg)

# 接口

## 接口列表

### 数据源绘图（POST）


示例：

```json
{
	user: 'user_name',
	access_time: '2022-03-01',
	plot_title: '标题',
	data_source: [
		{
			type: 'catalog',
			content: ['类别1', '类别2', '类别3'],
			annotation: '注释'
		},
		{
			type: 'date',
			content: ['2022-01-01', '2022-01-02', '2022-01-03'],
			annotation: '注释'
		},
		{
			type: 'date',
			date_start: '2022-01-01',
			date_end: '2022-01-03',
			date_delta: '1d',
			annotation: '注释'
		},
		{
			type: 'number',
			content: [123, 456, 789],
			annotation: '注释'
		}
	]
}
```

### 对象绘图（POST）


示例：

```json
{
	user: 'userName',
	access_time: '2022-03-01',
	plot_title: '标题',
	object_meta: {
		date_time: 'time',
		task_number: 'number',
		build_name: 'catalog'
	},
	objects: [
		{
			date_time: '2021-01-01',
			task_number: 123,
			build_name: '旅顺校区13号楼'
		},
		{
			date_time: '2021-01-02',
			task_number: 4,
			build_name: '旅顺校区13号楼'
		},
		{
			date_time: '2021-01-03',
			task_number: 643,
			build_name: '旅顺校区13号楼'
		},
		{
			date_time: '2021-01-04',
			task_number: 1234,
			build_name: '旅顺校区13号楼'
		},
		{
			date_time: '2021-01-05',
			task_number: 55,
			build_name: '旅顺校区13号楼'
		},
		{
			date_time: '2021-01-06',
			task_number: 32,
			build_name: '旅顺校区13号楼'
		},
		{
			date_time: '2021-01-07',
			task_number: 767,
			build_name: '旅顺校区13号楼'
		}
	]
}
```

### 系统信息（GET）

`/api/sysinfo`

### 任务单（GET）

`/api/task/{TASK_ID}`

## 数据规范

### 数据类型

1. 时间

开始时间（2020-01-01 或者 2020/01/01）  
结束时间（2022-01-07 或者 2020/01/07）  
时间间隔（1s、1m、1h、1d、1m、2y）  

值列表

2. 数据

值列表

3. 类别

值列表

### 维度规范

1. 二维数据是两个序列

2. 三维数据是一个序列和一个字典