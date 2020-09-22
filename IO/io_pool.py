"""
    基于POOL方法的IO多路复用模型
"""
from socket import socket
from select import *

# 创建监听套接子,作为初始化监控对象
sockfd = socket()
sockfd.bind(('0.0.0.0', 8889))
sockfd.listen(5)

# IO设置为非阻塞
sockfd.setblocking(False)

# 生成pool对象
pool_io = poll()

# 注册关注事件
pool_io.register(sockfd, )

# 建立IO字典
dict_io = {}
dict_io[sockfd.fileno()] = sockfd




# 循环监控IO
while True:
    for fil_id, cls in pool_io.poll():
        obj = dict_io[fil_id]
        if obj is sockfd:
            obj = dict_io[fil_id]
            connfd, addr = obj.accept()
            print("Connect form ", addr)
            sockfd.setblocking(False)
            pool_io.register(connfd, POLLIN)
            dict_io[connfd.fileno()] = connfd

        else:
            # 某个客户端发送消息
            data = obj.recv(1024).decode()
            if not data:
                pool_io.unregister(fil_id)
                del dict_io[fil_id]
                obj.close()
            print(data)



