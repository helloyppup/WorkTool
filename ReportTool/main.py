import test,fileOpera,copy
from datetime import datetime
from test import ETimeType
from enum import Enum
from fileOpera import EReportType

class File:

    reports=[]
    file_path="none"
    EReportType=[]
    reports_errorTime={}
    reports_errorNum=[]
    reports_Sort=[]


    class ErrorReport:
        lastReport=None
        nowReport=None
        tip="FF"

        def __init__(self,lastReport,nowReport,tip):
            self.lastReport=lastReport
            self.nowReport=nowReport
            self.tip=tip

        def __str__(self):
            return (self.lastReport.data_str+"\n"+self.nowReport.data_str+"\n"+"-----"+self.tip+"\n\n")

    def __init__(self,file_path):
        self.file_path=file_path
        self.reports=self.ReadFile(file_path)
        self.IsBuffHigh()
        print(self.file_path+"---file import")

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
        print(self.file_path + "---report num:"+str(len(reports)))
        file.close()
        return reports

    def ErrorNum(self,long,isFilter=True):
        index=1
        while index<len(self.reports_Sort):
            numDiff=self.reports_Sort[index].num-self.reports_Sort[index-1].num
            if(isFilter and numDiff!=0):
                if(numDiff!=long):
                    tip="NumDiff : "+str(numDiff)
                    self.reports_errorNum.append(File.ErrorReport(self.reports_Sort[index-1],self.reports_Sort[index],tip))
            index+=1
        print("---------------------------------------")
        print(self.file_path + "---error report num:" + str(len(self.reports_errorNum)))
        print("---------------------------------------")
        return self.reports_errorNum

    def ErrorTime(self,diff,reportType,timeType=ETimeType.min,accura=1):

        index = 1
        errorReports = []
        typeReports=self.SeclctReport(reportType)

        while index < len(typeReports):
            timeDiff=test.TimeDiff(typeReports[index-1].time,typeReports[index].time)
            if abs(timeDiff-diff)>accura:
                tip_time="min" if timeType==ETimeType.min else "sec"
                tip = "TimeDiff : " + str(timeDiff)+tip_time
                errorReports.append(File.ErrorReport(typeReports[index-1],typeReports[index],tip))
            index+=1
        if(len(errorReports)!=0):
            self.reports_errorTime[reportType]=errorReports

            print("---------------------------------------")
            print(self.file_path +"--"+ reportType +"---error report time:" +str(len(errorReports)))
            print("---now have error report type :")
            for key in self.reports_errorTime.keys():
                print(key)
            print("---------------------------------------")

            return errorReports

    def SeclctReport(self,reportType):
        """
        筛选某一类型的报文
        :param reportType:筛选的报文类型
        :return:
        """
        if len(self.reports_Sort)!=0:
            reports=self.reports_Sort
        else:
            reports=self.reports

        temReports=[]
        for r in reports:
            if r.type==reportType:
                temReports.append(r)
                # print("add--"+str(r))
        return temReports

    def SeclctBuff(self,reports=None):
        buffReports=[]
        if reports!=None:
            for r in reports:
                if(r.type_head == "+BUFF"):
                    buffReports.append(r)
        else:
            for r in self.reports:
                if (r.type_head == "+BUFF"):
                    buffReports.append(r)
        return buffReports

    def Sort(self):
        """
        这个方法用于将buff报文插入到它应该在的地方 == buff高优先级的报文
        :return:
        """
        reports=copy.copy(self.reports)

        index = 0
        buffs=[]
        # 获取所有buff
        while index<len(reports):
            buffOne=[]
            #print(index)
            while reports[index].type_head == "+BUFF":
                buffOne.append(reports[index])
                index+=1
                if index>=len(reports):
                    index-=1
                    break
            if(len(buffOne)!=0):
                buffs.append(buffOne)
            index+=1


        #删除报文中的buff
        reports_buffer=self.SeclctBuff()
        for r in reports_buffer:
            reports.remove(r)
            #print("del--" + str(r))

        #记录断点
        breakPoint = []
        index = 1
        while index < len(reports):
            # print(reports[index - 1])
            # print(reports[index])
            numDiff = reports[index].num - reports[index - 1].num
            if (numDiff != 1) and (numDiff != 0):
                breakPoint.append(index-1)
                # print(reports[index - 1])
                # print(reports[index])
                # print("\n")
            index += 1

        for b in reversed(buffs):
            isOver = False
            index=len(breakPoint)-1
            while index>=0:
                if(reports[breakPoint[index]].num<b[-1].num):
                    reports[breakPoint[index]+1:breakPoint[index]+1]=b
                    breakPoint=list(map(lambda x:x+len(b),breakPoint))
                    print("insert:"+str(reports[breakPoint.pop(index)]))
                    isOver=True
                index-=1
            #如果再断点列表中没有找到可以插入的地方，就说明这段buff应该在最上面 插入到整个列表前面
            if not isOver:
                reports=b+reports

        self.reports_Sort=reports
        return self.reports_Sort

    def IsBuffHigh(self):
        index=1
        while index<len(self.reports):
                #发生报文回退
            if (self.reports[index].type_head=="+BUFF") and \
            (self.reports[index].num-self.reports[index-1].num)<0 :
                break
            index += 1


        if index!=len(self.reports):
            self.Sort()
            return False
        else: return True


"""Report是一个列表 装载了数据集合"""
class Report:
    time=datetime(2000,7,10,0,0,0)
    type="GTDEFAULT"
    type_head="FFFF"
    data=[]
    data_str=""

    def __init__(self,line):
        self.data_str=line.strip()
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
        type_str=self.data[1]
        self.type_head = (type_str.split(':'))[1].strip()
        type_str=type_str.split(':')[-1].strip()
        return type_str

    def __str__(self):
        return self.data_str+"\n"


# files_path=fileOpera.get_txt_files("test")
# files=[]
# for path in files_path:
#     files.append(File(path))
# for f in files:
#    #f.ErrorNum(1)
#     f.ErrorTime(1,"GTFRI")
#     fileOpera.Save(f.file_path,f.EReportType,"错误序列号")
#     fileOpera.Save(f.file_path,f.reports_errorTime,"错误时间")

files_path=fileOpera.get_txt_files("report")
files=[]
for path in files_path:
    files.append(File(path))

files[0].ErrorNum(1)
files[0].ErrorTime(100,"GTFRI")
print(files[0].IsBuffHigh())

fileOpera.Save(files[0].file_path,files[0].reports_Sort,"Sort")
fileOpera.Save(files[0].file_path,files[0].reports_errorNum,"错误序列号")
fileOpera.Save(files[0].file_path,files[0].reports_errorTime,"错误时间")
print("+++++++++++++++++++++END++++++++++++++++++++++")