"""
    线程使用 (类似于进程创建和使用)
"""
import threading
from time import time, sleep
import  os

a = 1

#  创建目标函数
def music():
    global a
    for i in range(4):
        sleep(2)

        print(os.getpid(), "播放: 铠甲勇士")

# 实例化线程对象
thread = threading.Thread(target = music)
thread.setName("engine")


# 启动线程
thread.start()

# 使用主线程
for i in range(4):
    sleep(1)
    print(os.getpid(), "播放: 中国心")


# 回收线程
thread.join(timeout = 2)