"""
    聊天室客户端
"""
from socket import *
from multiprocessing import Process
from time import sleep

# 生成套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)

# 服务器地址
ADDR = ('127.0.0.1', 8888)


# 客户端接收来自服务端的消息
def recv_from_server():
    while True:
        data, addr = udp_socket.recvfrom(1024)
        print(data.decode()+'\n' + '发言: ', end = '')


def login():
    # 注意子进程不可以使用input()
    while True:
        msg = input("Please input your name>> ")
        msg = 'L ' + msg
        udp_socket.sendto(msg.encode(), ADDR)
        data, addr = udp_socket.recvfrom(1024)

        if data.decode() == 'login---OK':
            print("欢迎你进入聊天室...\n")
            return


def main():
    # 创建账户
    login()
    # 设置接收消息的子进程
    recv_process = Process(target=recv_from_server)
    recv_process.start()
    # 父进程负责发送消息
    while True:
        msg = input("发言: ")
        msg  =   'C ' + msg
        udp_socket.sendto(msg.encode(), ADDR)
        sleep(0.01)

    recv_process.join()


if __name__ == '__main__':
    main()
