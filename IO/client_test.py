"""
    测试客户端
"""
from socket import socket
import time

# 创建套接字
sock = socket()
# 链接服务端
sock.connect(('127.0.0.1', 8889))

while True:
    msg = input('>> ')
    sock.send(msg.encode())
