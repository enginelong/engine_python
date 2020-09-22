"""
    基于seleect方法的IO多路复用模型
"""
from socket import socket
from select import select

# 创建监听套接子,作为初始化监控对象
sockfd = socket()
sockfd.bind(('0.0.0.0', 8888))
sockfd.listen(5)

# IO设置为非阻塞
sockfd.setblocking(False)

# 设置好关注列表
rlist = [sockfd]     # 关注监听套接子
wlist = []
xlist = []

# 循环监控IO
while True:
    rs, ws, xs = select(rlist, wlist, xlist )
    # 遍历就绪的IO列表.分情况  讨论(监听套接字和客户端套接子)
    for r in rs:
        if r is sockfd:
            # 将链接的客户端链接套接子加入关注的IO
            connfd, addr = rs[0].accept()
            print("Connect form ", addr)
            sockfd.setblocking(False)
            rlist.append(connfd)
        else:
            # 某个客户端发送消息
            data = r.recv(1024).decode()
            if not data:
                rlist.remove(r)  # 取消关注
                r.close()
            print(data)



