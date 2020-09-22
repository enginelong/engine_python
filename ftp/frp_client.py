"""
    ftp 客户端
"""

from threading import Thread, Event, Lock
from socket import socket


def show_view():
    list_view = ['LIST', 'STOR', 'RETR', 'EXIT']
    print()
    print("---您可以使用以下命令进行操作---")
    print('*****************************')
    for index, view in enumerate(list_view):
        print("%d. %s" % (index + 1, view))
    print('*****************************')
    print()


class MyThread(Thread):
    def __init__(self, client_socket=None):
        super().__init__()
        self.client_socket = client_socket

    def show(self):
        self.client_socket.send(b'LIST')
        # 等待服务端回复
        msg = self.client_socket.recv(1024)
        if msg.decode() == 'YES':
            data = self.client_socket.recv(1024)
            print(data.decode())
        else:
            print("抱歉,文件库没有文件...")

    def upfile(self):
        file_path = input("请输入文件路径")
        file_path = "STOR " + file_path
        self.client_socket.send(file_path.encode())
        # 等待客户端回复
        msg = self.client_socket.recv(1024)
        if msg.decode() == 'YES':
            print("上传成功...")
        else:
            print("已有同名文件,不可以覆盖...")

    def download(self):
        filename = input("请输入文件名")
        msg = "RETR " + filename
        self.client_socket.send(msg.encode())
        # 等待服务端响应
        echo = self.client_socket.recv(1024)
        if echo.decode() == "YES":
            print("文件已经成功下载到本地/home/tarean/下载...")
        else:
            print("抱歉,您要下载的文件不存在...")


def main():
    # 创建tcp套接字
    client_socket = socket()
    # 链接服务器
    client_socket.connect(('127.0.0.1', 8889))

    thread = MyThread(client_socket)

    while True:
        show_view()
        command = input("请输入命令: ")
        if command == "LIST":
            thread.show()
        elif command == "STOR":
            thread.upfile()
        elif command == "RETR":
            thread.download()
        if command == "EXIT":
            break


if __name__ == '__main__':
    main()
