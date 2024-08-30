from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
import ghost_icon_rc
from PyQt5.QtCore import Qt


class SilentMessageBox(QDialog):

# 定义类属性，在外部可以通过SilentMessageBox.Yes判断
    Yes = QDialog.Accepted
    No = QDialog.Rejected
    def __init__(self,parent,text:str, dialog_type='information' ):
        super(SilentMessageBox, self).__init__(parent)
        self.setWindowTitle(" ")
        # 如果你调用 setModal(True)，这个对话框将成为模态对话框。
        # 当模态对话框显示时，用户无法与该对话框之外的其他窗口进行交互，直到关闭这个对话框。
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.init_ui('\n'+text+'\n', dialog_type)
        self.setWindowIcon(QIcon(":/ghost_white.png"))

        # 存储yes或者no的返回值
        self.result = self.exec_()


    def init_ui(self, text, dialog_type):
        layout = QVBoxLayout()

        # 添加提示文本
        label = QLabel(text)
        layout.addWidget(label)
        #label.setAlignment(Qt.AlignCenter)
        label.setAlignment(Qt.AlignLeft)
        # 创建按钮布局
        button_layout = QHBoxLayout()

        if dialog_type == 'information':
            # 只有一个关闭按钮

            close_button = QPushButton("Close")
            close_button.clicked.connect(self.close)
            button_layout.addWidget(close_button)
        elif dialog_type == 'question':
            # Yes 和 No 按钮
            yes_button = QPushButton("Yes")
            yes_button.clicked.connect(self.accept)
            button_layout.addWidget(yes_button)

            no_button = QPushButton("No")
            no_button.clicked.connect(self.reject)
            button_layout.addWidget(no_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    @staticmethod
    def question(parent,text):
        dialog = SilentMessageBox(parent,text, dialog_type='question')
        return dialog.result

    @staticmethod
    def info(parent,text):
        SilentMessageBox(parent,text, dialog_type='information')
        return None

# #
# # 应用程序实例
# app = QApplication([])
#
# # 创建和显示带有关闭按钮的对话框
# close_dialog = SilentMessageBox("This is a silent dialog with a Close button.", dialog_type='information')
# close_dialog.exec_()
#
# # 创建和显示带有 Yes 和 No 按钮的对话框
# yes_no_dialog = SilentMessageBox("Do you want to continue?", dialog_type='question')
# if yes_no_dialog.exec_() == QDialog.Accepted:
#     print("User selected Yes")
# else:
#     print("User selected No")
