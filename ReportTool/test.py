from datetime import datetime
import os
from enum import Enum


class ETimeType(Enum):
    min=0
    sec=1
    dataTime=2

def SliceLine(line,slicsym=','):
    """切割单行文本"""
    #if(line!="\n"  and "ASC" in line):
    line_unity=line.split(slicsym)
    return line_unity

def GetTime(date_time_str,format="%Y%m%d%H%M%S"):
    try:
      datetime.strptime(date_time_str, format)
      return datetime.strptime(date_time_str, format)
    except ValueError:
        return  False

def TimeDiff(startTime,endTime,timeType=ETimeType.min):
    if(timeType==ETimeType.min):
        return (endTime-startTime).seconds//60
    elif(timeType==ETimeType.sec):
        return (endTime-startTime).seconds
    else:
        return (endTime-startTime)

def Sort(reports):
    """用来排序一个报文队列，将其转化成buff高优先报文 但是懒得写"""
