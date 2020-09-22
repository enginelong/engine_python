"""
    聊天室服务器端
"""
from socket import *

# 创建udp套接字
udp_socket = socket(AF_INET, SOCK_DGRAM)

# 设定主机地址和端口
ADDR = '127.0.0.1'
PORT = 8888
addr_server = (ADDR, PORT)
udp_socket.bind(addr_server)

class User:
    """
        用户类.用来存储用户的账户信息
    """
    dict_user = {}
    user_socket = udp_socket
    def __init__(self, name="", user_addr="", udp_socket =None):
        self.name = name
        self.user_addr = user_addr
        self.udp_socket = udp_socket


    def join_dict(self):
        if self.name  in User.dict_user.keys():
            return False
        User.dict_user[self.name] = self.user_addr
        return True

    @classmethod
    def send_to_user(cls, name):
        """
            新用户加入时,服务器向其他所有用户广播这位新用户加入聊天室
        :return: None
        """
        for ele in User.dict_user.keys():

            if name != ele:

                temp_addr = User.dict_user[ele]
                temp_msg = "Welcome " + name +  " \nto our chat cellar..."
                User.user_socket.sendto(temp_msg.encode(), temp_addr)

    @classmethod
    def send_news(cls, addr, new):
        """
            服务端向其他用户转发消息
        :param addr: 发消息用户的地址
        :return: None
        """
        src_name = None
        for name in User.dict_user.keys():
            if User.dict_user[name] == addr:
                src_name = name

        for name, user_addr in User.dict_user.items():
            if user_addr != addr:
                temp_msg = src_name + ': ' + new + '\n'
                User.user_socket.sendto(temp_msg.encode(), user_addr)



# 登录处理操作
def login(name, user_addr):
    if User(name, user_addr).join_dict():
        return True
    return False


while True:
    data, addr = udp_socket.recvfrom(1024)
    msg = data.decode()
    print(msg)
    # 根据用户的请求调用不同的功能
    if msg[0] == 'L':
        name = msg.split(' ')[1]
        if login(name, addr):
            udp_socket.sendto(b"login---OK", addr)
            User.send_to_user(name)
        else:
            udp_socket.sendto(b"Sorry... This user has exists...\n"
                              b"Try another name...", addr)
    elif msg[0] =='C':
        new = msg.split(' ', 1)[1]
        User.send_news(addr, new)



