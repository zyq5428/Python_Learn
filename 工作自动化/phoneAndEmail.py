import os
os.getcwd()
os.chdir('f:\Python_Learn')
os.getcwd()

os.makedirs('f:\\Python_Learn\\test')

os.path.abspath('.')
os.path.abspath('.\\test')
os.path.isabs('.')
os.path.isabs(os.path.abspath('.'))

os.path.relpath('C:\\Windows', 'C:\\')
os.path.realpath('C:\\Windows','C:\\spam\\eggs')
os.getcwd ()

path = 'C:\\Windows\\System32\\calc.exe'
os.path.basename(path)
os.path.dirname(path)

calcFilePath = 'C:\\Windows\\System32\\calc.exe'
os.path.split(calcFilePath)
(os.path.dirname(calcFilePath),os.path.basename(calcFilePath))
calcFilePath.split(os.path.sep)
' /usr/bin'.split(os.path.sep)

os.path.getsize('C:\\Windows\\System32\\calc.exe')
os.listdir('C:\\Windows\\System32')
#这个是错误的，运行不了
totalSize = 0
for file in os.listdir('C:\\Windows\\System32'):
    totalSize = totalSize + os.path.getsize(os.path.join('C:\\Windows\\System32',filename))
    print(totalSize)  

os.path.exists('f:\\Python_Learn')
os.path.exists('f:\\Python_Learn\\kate')
os.path.isdir('f:\\Python_Learn\\test')
os.path.isfile('f:\\Python_Learn\\test')
os.path.isdir('f:\\Python_Learn\\test\\lucy.xpi')
os.path.isfile('f:\\Python_Learn\\test\\lucy.xpi')
os.path.exists('D:\\')

helloFile = open('f:\\Python_Learn\\hello.txt')
hellocontent = helloFile.read()
hellocontent

sonnetFile = open('f:\\Python_Learn\\sonnet29.txt')
sonnetFile.readlines()

baconFile = open('f:\\Python_Learn\\bacon.txt','w')
baconFile.write('Hello world!\n')
baconFile.close()
baconFile = open('f:\\Python_Learn\\bacon.txt','a')
baconFile.write('Bacon is not a vegetable.')

baconFile.close()
baconFile = open('bacon.txt')
content = baconFile.read()
baconFile.close()
print(content)

