"""
    http请求 响应实例
"""
from socket import socket

sockfd = socket()
sockfd.bind(('0.0.0.0', 8899))
sockfd.listen(5)

while True:
    # 浏览器输入地址后自动链接客户端
    connfd, addr = sockfd.accept()
    print("Connect from ", addr)

    # 接收的是来自浏览器的http请求
    request = connfd.recv(1024 * 10)
    print("接收请求 ", request.decode())
    request = request.decode()

    # 防止浏览器出现异常退出
    if not request:
        continue

    # 提取请求内容
    info = request.split(' ')[1]

    # 分情况讨论
    if info == '/first.html':
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        with open('first.html') as f:
            response += f.read()
    else:
        response = "HTTP/1.1 404 Not Found\r\n"
        response += "Content-Type:text/html\r\n"
        response += "\r\n"
        response += "<h1>Sorry.....</h1>"

    connfd.send(response.encode())
    # 关闭传输套接字
    connfd.close()

# 关闭套接字
sockfd.close()
