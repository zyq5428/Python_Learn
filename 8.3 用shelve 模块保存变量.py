import shelve
with shelve.open(filename) as object:
    object = shelve.open(filename)
shelfFile = shelve.open('test')
cats = ['Zophie', 'Pooka', 'Simon' ]
shelfFile['cates'] = cats
shelfFile.close()
shelfFile = shelve.open('test')
type(shelfFile)
shelfFile['cates']
shelfFile.close()

shelfFile = shelve.open('test')
list(shelfFile.keys())
list(shelfFile.values())
shelfFile.close()


import pprint
cats = [{'name': 'Zophie', 'desc': 'chubby'}, {'name': 'Pooka', 'desc': 'fluffy'}]
pprint.pformat(cats)
fileobj = open('myCats.py', 'w')
fileobj.write('cats = ' + pprint.pformat(cats) + '\n')
fileobj.close()
