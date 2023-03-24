# 类

## File

### 定义

是一个文件类，成员变量是一个report列表

### 成员属性

#### reports

`reports` 是一个Report类型的列表

#### reports_errorNum

存储出现错误序列号的`ErrorReport`列表

#### reports_errorTime

存储出现错误时间的`ErrorReport`列表

#### reports_Sort

排序后的报文列表

#### file_path

文件路径

### 内部类

#### ErrorReport

用于记录错误的报文，包含出现异常的**本条报文**和**上一条报文**，以及一个**提示信息**

包含一个打印自身的方法

打印格式如下

![image-20230323100037854](E:\snoopy\git\github\WorkTool\ReportTool\img\ErrorReport-print.png)

### 成员方法

#### def \_\_init\_\_(self,file_path):

初始化自身

通过调用[ReadFile](#ReadFile)方法对[reports](#reports)

初始化成功打印`test\TCP_20828_20230307_us-1_Sort.txt---file import`

#### ReadFile

用于读取单个文件，需要传入文件的路径

读取成功打印`test\TCP_20828_20230307_us-1_Sort.txt---report num:2516`

#### ErrorNum

筛选错误的序列号

`long`为序列号步长

`reportsType`是进行排序的报文类型，可以针对原始序列筛选，也可以针对排序后的列表筛选，默认是原始报文，如果输入了错误的类型，就会自动检测该文件是否进行了排序，如果进行了排序就对排序的报文进行筛选，否则对原始报文进行筛选

`isFilter`为是否过滤序列号相同的情况，默认为过滤

筛选完毕返回一个`ErrorReport`列表

筛选完毕输出`test\TCP_20828_20230307_us-1_Sort.txt---error report num:3`

#### ErrorTime

传入应该的时间偏移量`diff`，需要筛选的报文类型`reportType`筛选的时间类型[`timeType`](#ETimeType)，默认值为分钟min，能接受的精度`accura`，偏移+-accura值的会被过滤，不认为异常，默认为1

筛选完毕返回一个`ErrorReport`列表

筛选完毕输出`test\868487004361069,GD530MG_test8,QMS_Sort.txt---error report time:99`

#### SeclctReport

筛选某一类型的报文

返回一个报文列表

#### SeclctBuff

筛选buff报文，可以传入一个报文列表进行筛选

如果不传入报文列表则筛选本文件的所有报文

返回一个buff报文列表

#### Sort

对报文进行排序

通过检测buff报文，再将buff报文插入到离它最近的一个序列号报文后面，实现排序

排序之后会为该file类的`reports_Sort`变量赋值，并返回它

## Report

### 成员变量

`time`  

`type` GTFRI

`type_head`+RESP

`data`是一个分割好的数据列表

`data_str`未分割的数据列表

### 成员方法

对外封装可以获取某一个数据、获取int类型的序列号、获取datatime时间、获取报文类型方法

# 文件操作

fileOpear.py

### 枚举

#### EReportType

用于标识`File`类里存储的不同报文列表

### 方法

#### get_txt_files 

批量读取某个文件夹下的所有.txt文件

返回所有文件的相对路径列表

#### Save

将文件读取至某个文件夹

# 公共操作

text.py

## 枚举

### ETimeType

有三个值`min` `sec` `datatime`

## 方法

### SliceLine

传入一行文本，返回一个以指定符号分割的数据列表

分割符号默认是','

### GetTime

传入一个指定格式的字符串数字 将其转化成datatime类型并返回

指定格式默认值为`"%Y%m%d%H%M%S"`

如果转化不成功会返回一个false

### TimeDiff

传入开始时间和结束时间 计算时间差

根据传入不同的[`timeType`](#ETimeType)可以返回不同格式的值

