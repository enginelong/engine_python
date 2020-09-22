""""
    IO
"""
from socket import *
from time import time, sleep, ctime

# 创建日志文件
file_log = open("mylog", 'a')

# 创建套接字
socketfd = socket()

# 绑定主机
socketfd.bind(('0.0.0.0', 8891))

# 设置监听
socketfd.listen(5)

# 设置非阻塞
socketfd.setblocking(False)
socketfd.settimeout(3)

while True:
    # 等待客户端链接
    try:
        print("Waiting for connect...")
        connfd, addr = socketfd.accept()
        print(addr)
        print("Connect with " + addr[0] +  " successfully...")
    except BlockingIOError as e:
        # IO阻塞异常处理
        print('Block')
        msg = "%s : %s\n" % (ctime(), e)
        file_log.write(msg)
        file_log.flush()
        sleep(2)
    except timeout as e:
        # 超时处理
        print('timeout')
        msg = "%s : %s\n" % (ctime(), e)
        file_log.write(msg)
        file_log.flush()
    else:
        # 客户端链接不会报错
        data = connfd.recv(1024)
        print(data.decode())