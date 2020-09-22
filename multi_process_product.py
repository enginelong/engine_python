"""
    基于多进程的网络并发模型(TCP)
"""

from multiprocessing import Process
from socket import *
from signal import *

# 网络地址
HOST= "0.0.0.0"
PORT= 8888
ADDR= (HOST, PORT)

# 处理客户端请求
def handle(connfd):
    while True:
        data = connfd.recv(1024)
        if not  data:
            break
        print(data.decode())
        connfd.send(b"OK")
    connfd.close()


def main():
    # 创建套接字(TCP)
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)
    print("Listen the port %d" % PORT)


    # 循环等待客户端链接
    while True:
        connfd, addr = sock.accept()
        print("Connect from ", addr)

        # 为链接的客户端创建新的进程
        # 告知操作系统父进程不会处理任何关于子进程的异常
        signal(SIGCHLD, SIG_IGN)
        p = Process(target=handle, args=(connfd,))
        p.start()



if __name__ == '__main__':
    main()
