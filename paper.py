"""
    模拟售票系统
"""
from threading import Thread
from time import sleep

# 票存储器
list_ticket = []

# 线程列表
jobs = []


def generate_tickets():
    """
        模拟生成车票
    :param list_target:指定的存储列表
    :return: None
    """
    for index in range(1, 501):
        list_ticket.append("T%d" % index)


# 定义线程函数
def sell_ticket():
    if len(list_ticket) == 0:

        return
    ticket = list_ticket.pop()

    print("ticket %s 已卖出..." % ticket)


# 创建线程类
class MyThread(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        while len(list_ticket) != 0:
            sell_ticket()
            sleep(0.2)
        print(self.getName() + ": " + "票已售完...")


def create_thread(n):
    """
        # 创建线程
    :param n: 指定的线程数量
    :return: None
    """
    for i in range(1, 11):
        thread = MyThread()
        thread.setName("售票管理器%d" % i)
        thread.start()
        jobs.append(thread)


def recycle_thread(list_thread):
    for i in list_thread:
        i.join()


def main():
    generate_tickets()
    create_thread(10)
    recycle_thread(jobs)


if __name__ == '__main__':
    main()
