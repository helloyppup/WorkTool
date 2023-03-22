from datetime import datetime
import os

def SliceLine(line):
    """切割单行文本"""
    #if(line!="\n"  and "ASC" in line):
    line_unity=line.split(',')
    return line_unity

def GetTime(date_time_str):
    try:
      datetime.strptime(date_time_str, "%Y%m%d%H%M%S")
      return datetime.strptime(date_time_str, "%Y%m%d%H%M%S")
    except ValueError:
        return  False

