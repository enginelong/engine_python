"""
    web server

自定义网页服务器(IO多路复用 http)

"""

from socket import socket
from select import *
import re


class WebSever:
    def __init__(self, host='0.0.0.0', port=80, html=None):
        self.host = host
        self.port = port
        self.html = html
        self.create_socket()
        self.bind()
        # IO并发模型(select)
        self.rlist = []
        self.wlist = []
        self.xlist = []

    # 创建套接字
    def create_socket(self):
        self.socket = socket()
        self.socket.setblocking(False)

    # 绑定服务器
    def bind(self):
        self.address = (self.host, self.port)
        self.socket.bind(self.address)

    # 启动服务器
    def start(self):
        # 监听客户端链接
        self.socket.listen(5)
        print("Listen the port %s " % self.port)
        # 设置IO并发模型
        self.rlist.append(self.socket)
        # 监控IO事件的发生
        while True:
            rs, ws, xs = select(self.rlist, self.wlist, self.xlist)
            for ele in rs:
                if ele == self.socket:
                    # 处理客户端连接
                    # 注意connfd 不可以设置为属性
                    connfd, addr = ele.accept()
                    connfd.setblocking(False)
                    self.rlist.append(connfd)
                    # print("Connect from browser ", addr)
                # 处理客户端请求
                else:
                    # 网速慢可能导致网页未加载完成客户端就会
                    # 断开链接,因此需要捕获异常,需要再次刷新
                    # 网页重新链接
                    try:
                        # 处理客户端http请求
                        self.handle(ele)
                    except:
                        self.rlist.remove(ele)
                        ele.close()
    def handle(self, connfd):
        msg = connfd.recv(1024).decode()
        # if not msg:
        #     self.rlist.remove(connfd)
        #     connfd.close()
        # print("Recv from the blowser > ", msg)

        # 解析请求内容
        pattern = r"[A-Z]+\s+(?P<engine>/\S*)"
        result = re.match(pattern, msg)
        if result:
            # 提取请求内容
            info = result.group("engine")
            print("请求内容: ", info)
            self.send_response(connfd, info)
        else:
            # 没有匹配到内容
            self.rlist.remove(connfd)
            connfd.close()
            return

    def send_response(self, connfd, info):
        if info == '/':
            filename = self.html + '/' + "index.html"
        else:
            filename = self.html + info

        # 直接打开文件,打开则说明存在,否则不存在
        try:
            print(filename)
            file  = open(filename, 'rb')
        except:
            response = "HTTP/1.1 404 Not Found\r\n"
            response += "Content-Type:text/html\r\n"
            response += "\r\n"
            response += "<h1>Sorry.....</h1>"
            response = response.encode()
        else:
            data = file.read()
            response = "HTTP/1.1 200 OK\r\n"
            response += "Content-Type:text/html\r\n"
            response += "Content-Length:%d\r\n"%(len(data))
            response += "\r\n"
            response  = response.encode() + data
            file.close()
        finally:
            # 发送相应给客户端
            connfd.send(response)



if __name__ == '__main__':
    # 实例化对象,传入相关数据
    httpd = WebSever(host='0.0.0.0', port=8000, html='/home/tarena/PycharmProjects/static')
    httpd.start()
