# 1.利用os.walk()函数遍历文件夹中的pdf文件
import os

for folderName, subfolders, filenames in os.walk('D:\\Git\\Explorer'):
    print('The current folder is ' + folderName)
    for subfolder in subfolders:
        print('SUBFOLDER OF' + folderName + ':' + subfolder)
    for filename in filenames:
        if filename.endswith('.pdf'):
            print('FILE INSIDE' + folderName + ':' + filename)
    print('')
