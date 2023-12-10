import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口
        self.setWindowTitle("Chat Interface with Side-by-Side Log Area")
        self.setGeometry(100, 100, 1200, 600)  # 增加窗口宽度以容纳两个区域

        # 创建中央小部件和布局
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)  # 修改为水平布局

        # 创建聊天区域的布局和控件
        chat_layout = QVBoxLayout()
        main_layout.addLayout(chat_layout)

        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        chat_layout.addWidget(self.chat_display)

        self.message_input = QLineEdit(self)
        chat_layout.addWidget(self.message_input)

        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.send_message)
        chat_layout.addWidget(send_button)

        # 创建日志区域的布局和控件
        log_layout = QVBoxLayout()
        main_layout.addLayout(log_layout)

        self.log_display = QTextEdit(self)
        self.log_display.setReadOnly(True)
        log_layout.addWidget(self.log_display)

    def send_message(self):
        # 获取输入文本并清空输入框
        message = self.message_input.text()
        self.message_input.clear()

        # 将消息显示在聊天记录区域
        self.chat_display.append("You: " + message)

        # 在日志区域显示信息
        self.log_display.append("Message sent.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = ChatWindow()
    mainWin.show()
    sys.exit(app.exec_())
