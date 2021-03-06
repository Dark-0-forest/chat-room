from PyQt5.QtWidgets import *
import sys
import socket
from threading import Thread


class Client(QWidget):
    def __init__(self):
        super(Client, self).__init__()
        self.initui()

    # 初始化ui
    def initui(self):
        # 设置窗口大小和位置
        self.setGeometry(600, 300, 360, 300)
        # 标题
        self.setWindowTitle("chat room")
        self.add_textbox()
        # 与server连接
        self.client = socket.socket()
        self.client.connect(("81.68.192.48", 8989))
        self.word_thread()

    # 设置组件
    def add_textbox(self):
        # 多行文本显示框
        self.content = QTextBrowser(self)
        self.content.setGeometry(30, 30, 300, 150)

        # 单行文本，消息发送框
        self.message = QLineEdit(self)
        self.message.setPlaceholderText("请输入内容")
        self.message.setGeometry(30, 200, 300, 30)

        # 发送button
        self.button = QPushButton("发送", self)
        self.button.setGeometry(270, 250, 60, 30)

    #发送消息
    def send_msg(self):
        msg = self.message.text()
        self.client.send(msg.encode())
        if msg == "Q":
            self.client.close()
            self.destroy()
        self.message.clear()

    #接受消息
    def recv_msg(self):
        while True:
            try:
                data = self.client.recv(1024).decode()
                print(data)
                data += "\n"
                self.content.append(data)
            except:
                exit()

    def button_send(self):
        self.button.clicked.connect(self.send_msg)

    #线程处理
    def word_thread(self):
        Thread(target=self.button_send).start()
        Thread(target=self.recv_msg).start()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    sys.exit(app.exec_())
