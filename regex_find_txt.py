# 导入所需要的模块

import os
import re

# 1、让用户输入表达式，然后转换为程序能识别的正则表达式

user_exp = input("Please input your expression：")

# 2、查找当前文件夹下的所有txt文件

txt_path = 'f:\\Python_Learn\\txt_file'
file_regex = re.compile(r'.+\.txt')

txt_name = []

os.chdir(txt_path)

for name in os.listdir(txt_path):
    if file_regex.search(name):
        txt_name.append(name)

print(txt_name)

# 3、依次打开txt文件，然后用正则表达式匹配，并保存匹配内容

# input_regex = '\d{3}\.\d{3}\.\d{4}'
input_regex = user_exp
user_regex = re.compile(input_regex)

matched_content = []

for file_name in txt_name:
    try:
        with open(file_name, 'r') as open_file:
            single_matched_content = []
            single_matched_content.append(file_name)
            file_content = open_file.read()
            for matched in user_regex.findall(file_content):
                single_matched_content.append(matched)
            if (len(single_matched_content) >= 2):
                matched_content.append(single_matched_content)
    except FileNotFoundError as e:
        print('指定的文件无法打开--{}'.format(file_name))
    except IOError as e:
        print('读写文件出现错误')
    finally:
        pass

# 4、对匹配的内容进行处理，如打印出来

print(matched_content)