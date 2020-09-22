"""
    创建两个线程同时执行
    一个线程打印 A-Z
    一个线程打印1-52
    打印顺序要求为 12A34B56C...5152Z
"""

from threading import Thread, Lock, Event
from time import time, sleep


# 线程储存器
jobs = []
# 创建互斥机制
lock = Lock()
lock1 = Lock()
# 创建同步机制
event= Event()

# 创建执行函数 负责打印 A-Z
def print_alpha():
    for j in range(65, 91):
        lock1.acquire()
        print(chr(j), end='')
        lock.release()

# 打印数字
def print_number():

    for i in range(1,52, 2):
        lock.acquire()
        print(i, i+1, sep='', end='')
        lock1.release()


# 创建线程
def create_thread():
    thread = Thread(target=print_number)
    jobs.append(thread)


    thread1 = Thread(target=print_alpha)
    jobs.append(thread1)

    thread.start()
    thread1.start()

def recycle_thread():
    """
        回收线程资源
    :return: None
    """
    for thread in jobs:
        thread.join()



def main():
    # 先给打印字母上锁
    lock1.acquire()
    create_thread()
    recycle_thread()


if __name__ == '__main__':
    main()