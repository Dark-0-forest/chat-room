import socket
from threading import Thread
import time


class Server:
    # 初始方法
    def __init__(self):
        self.server = socket.socket()
        self.server.bind(("172.17.0.5", 8989))
        self.server.listen(5)
        # 所有的客户端
        self.clients = []
        # 用户姓名和ip绑定
        self.client_name_ip = {}

        self.get_conn()

    # 监听客户端
    def get_conn(self):
        while True:
            # 获取客户端的信息
            client, address = self.server.accept()
            print(address)
            data = "请输入您的昵称:"
            # 通信要进行编码
            client.send(data.encode())
            # 将连接的用户添加到用户列表中
            self.clients.append(client)
            # 为每个客户创建一个线程
            Thread(target=self.get_msg, args=(client, self.clients, self.client_name_ip, address)).start()

    # 对客户端的信息进行处理
    def get_msg(self, client, clients, client_name_ip, address):
        # 接收客户端传来的昵称
        name = client.recv(1024).decode()
        print("from client " + name)
        # 昵称与IP进行绑定
        client_name_ip[address] = name
        # 循环监听客户端
        while True:
            # 获取消息
            try:
                recv_data = client.recv(1024).decode()
            except Exception as e:
                self.close_client(client, address)
                break

            # 用户输入Q时退出
            if recv_data == "Q":
                self.close_client(client, address)
                break
            # 把消息发送给每个客户
            for c in clients:
                # 昵称，时间，消息
                c.send((client_name_ip[address] + " " + time.strftime("%X") + "\n" + recv_data).encode())

    # 关闭资源
    def close_client(self, client, address):
        self.clients.remove(client)
        client.close()

        print(self.client_name_ip[address] + "离开了聊天室")
        # 把消息发送给每个客户
        for c in self.clients:
            c.sent((self.client_name_ip[address] + "离开了聊天室").encode())


if __name__ == '__main__':
    Server()



