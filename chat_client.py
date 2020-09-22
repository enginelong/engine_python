"""
    聊天客户端
"""
from socket import *
from multiprocessing import Process


def login(sock):
    while True:
        name = input("请输入姓名: ")
        name = 'L ' + name
        sock.sendto(name.encode(), ADDR)
        # 等待回复
        data, addr = sock.recvfrom(1024)
        # 根据情况处理
        if data.decode() == 'OK':
            print("你已进入聊天室")
            return
        else:
            print("该用户已经存在")


# 服务器地址
ADDR = ('127.0.0.1', 8888)

def main():
    sock = socket(AF_INET, SOCK_DGRAM)
    # 进入聊天室
    login(sock)
    # data, addr = sock.recvfrom(1024)
    # print(data.decode())

if __name__ == '__main__':
    main()