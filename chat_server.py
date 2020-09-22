"""
Author: engine
Email: 2878341748@qq.com
Time: 2020-9-15
Env: python 3.6
socket and Process exercise
"""

from socket import *

# 服务器地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

def do_login():
    pass

def chat():
    pass

# 框架 启动函数
def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind(ADDR)

    # 循环等待接受请求 (总分处理模式)
    while True:
        # 所有都在这接受
        data, addr = sock.recvfrom(1024)
        # 将客户端请求简单的分割
        temp = data.decode().split(' ')
        print(data.decode())
        if temp[0] == 'L':
            do_login()
        elif temp[0]=='C':
            chat()

if __name__ == '__main__':
    main()







