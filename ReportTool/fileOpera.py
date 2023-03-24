import os
from enum import Enum


class EReportType(Enum):
    origin = 0
    sort = 1
    errorNum = 2
    errorTime = 3

def get_txt_files(folder_path):
    """ 获取指定文件夹中所有的 .txt 文件，并返回它们的相对路径列表。 """
    txt_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            txt_path = os.path.join(folder_path, file_name)
            txt_files.append(txt_path)
    return txt_files

def Save(path,datas,errorType=""):
    if len(datas)==0:
        print("未出现错误---"+path+"---"+errorType)
        return
    file_name=path.split('\\')[-1]
    file_name_last=file_name.split('.')[-1]
    file_name_last="."+file_name_last
    file_name=file_name.split('.')[0]

    path = path.rsplit('\\', 1)[0]
    folder_path = os.path.join(path, '处理数据')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_name=file_name+"_"+errorType

    if isinstance(datas,dict):

        # temp_dir_path = os.path.join(folder_path, file_name)
        # if not os.path.exists(temp_dir_path):
        #     os.makedirs(temp_dir_path)

        for key,value in datas.items():
            temp_file_path=os.path.join(folder_path,file_name+"_"+key+file_name_last)
            with open(temp_file_path, 'w') as f:
                for line in value:
                    f.write(str(line))
            print("写入文件---"+temp_file_path)

    else:
        file_name += file_name_last
        temp_file_path = os.path.join(folder_path, file_name)
        with open(temp_file_path, 'w') as f:
            for data in datas:
                f.write(str(data))