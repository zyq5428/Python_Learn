import time
import threading

# 生成一个锁对象
lock = threading.Lock()


def func():
    global num  # 全局变量
    lock.acquire()  # 获得锁，加锁
    num1 = num
    time.sleep(0.1)
    num = num1 - 1
    lock.release()  # 释放锁，解锁
    time.sleep(2)


num = 100
l = []

for i in range(100):  # 开启100个线程
    t = threading.Thread(target=func, args=())
    t.start()
    l.append(t)

# 等待线程运行结束
for i in l:
    i.join()

print(num)