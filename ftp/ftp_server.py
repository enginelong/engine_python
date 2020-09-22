"""
    ftp服务端
"""
import os
from socket import socket
from threading import Thread, Event
from time import time, sleep

HOST = '127.0.0.1'
PORT = 8889
ADDR = (HOST, PORT)

# 文件库路径
path = '/home/tarena/my_file/'


def show(sock):
    file_list = os.listdir(path)
    if not file_list:
        return
    sock.send(b"YES")
    sleep(0.1)
    # 向客户端发送文件名
    filename = '\n'.join(file_list)
    sock.send(filename.encode())
    sleep(0.1)


def up():
    print("up")


def down():
    print("down")


def end():
    print("end")


class MyThread(Thread):
    def __init__(self, tcp_socket=None):
        super().__init__()
        self.tcp_socket = tcp_socket

    def run(self):
        while True:
            command = self.tcp_socket.recv(1024)
            command = command.decode().split(' ')
            if command[0] == 'LIST':
                self.show()
            elif command[0] == "STOR":
                self.upfile(command[1])
            elif command[0] == "RETR":
                self.download(command[1])

    def show(self):
        filename = os.listdir(path)
        if not filename:
            self.tcp_socket.send(b"ON")
        self.tcp_socket.send(b"YES")
        sleep(0.1)
        self.tcp_socket.send('\n'.join(filename).encode())

    def upfile(self, file_path):
        filename = file_path.split('/')[-1]
        file = path + filename
        for file in os.listdir(path):
            if filename == file_path:
                self.tcp_socket.send(b"NO")
                return
        self.file_copy(file_path, file)
        self.tcp_socket.send(b"YES")

    def download(self, filename):
        # 查看文件库是否为空或者要下载文件不存在
        file_cat = os.listdir(path)
        if not file_cat:
            self.tcp_socket.send(b"NO")
            return
        flag = 0
        for file_name in file_cat:
            if file_name == filename:
                flag = 1
                break
        if flag == 0:
            print('这里')
            self.tcp_socket.send(b"NO")
            return

        file = path + filename
        dest_file = '/home/tarena/下载/' + filename
        self.file_copy(file, dest_file)

        self.tcp_socket.send(b"YES")

    def file_copy(self, file_path, file):
        fr = open(file_path, 'rb')
        fw = open(file, 'wb')
        while True:
            content = fr.read(1024)
            if not content:
                break
            fw.write(content)

        fr.close()
        fw.close()


def main():
    # 创建tcp套接字
    tcp_socket = socket()
    # 绑定主机
    tcp_socket.bind(ADDR)
    # 设置监听
    tcp_socket.listen(6)

    while True:
        # 等待客户端链接
        print("Waiting clients to connect...")
        data_socket, addr = tcp_socket.accept()
        print("客户端" + str(addr) + '链接成功...')

        # 为客户创建独立的进程
        thread = MyThread(data_socket)
        thread.start()


if __name__ == '__main__':
    main()
