import os

def get_txt_files(folder_path):
    """ 获取指定文件夹中所有的 .txt 文件，并返回它们的相对路径列表。 """
    txt_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            txt_path = os.path.join(folder_path, file_name)
            txt_files.append(txt_path)
    return txt_files