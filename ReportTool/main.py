import test,fileOpera
from datetime import datetime
class File:
    reports=[]

    class ErrorReport:
        lastReport=None
        nowReport=None
        tip="FF"

        def __init__(self,lastReport,nowReport,tip):
            self.lastReport=lastReport
            self.nowReport=nowReport
            self.tip=tip

    def __init__(self,file_path):
        self.reports=self.ReadFile(file_path)
        print(file_path+"---file import")

    def ReadFile(self,file_path):
        """
        获取文件文本
        :param file_name: string类型 要读取的文本名
        """
        reports=[]
        file = open(file_path, "r", encoding="utf-8")
        for line in file:
            if (line != "\n" and "+" in line):
                reports.append(Report(line))
        file.close()
        return reports

    def ErrorNum(self,long):
        index=1
        errorReports=[]
        while index<len(self.reports):
            timeDiff=self.reports[index]-self.reports[index-1]
            if(timeDiff!=long):
                tip="NumDiff : "+timeDiff
                report=ErrorReport(self.reports[index],self.reports[index],tip)






"""Report是一个列表 装载了数据集合"""
class Report:
    time=datetime(2000,7,10,0,0,0)
    type="GTDEFAULT"
    type_head="FFFF"
    data=[]

    def __init__(self,line):
        self.data=test.SliceLine(line)
        self.time=self.GetTime()
        self.num=self.GetNum()
        self.type=self.GetType()

    def GetElement(self,index):
        return self.data[index]

    def GetNum(self):
        return int(self.data[-1][0:4],16)

    def GetTime(self):
        time_str=self.data[-2]
        return test.GetTime(time_str)

    def GetType(self):
        type_str=self.data[0]
        type_str=type_str.split(']')[-1]
        self.type_head=type_str.split(':')[0]
        return type_str


files_path=fileOpera.get_txt_files("test")
files=[]
for path in files_path:
    files.append(File(path))
print(1)