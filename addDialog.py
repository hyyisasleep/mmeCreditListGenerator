import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCloseEvent, QIcon
from PyQt5.QtWidgets import QDialog
import ui_dialog
from silentMessageBox import SilentMessageBox
import ghost_icon_rc
code_wait_handle = 0
code_add_item = 1
code_quit = 2


class AddDialog(QDialog):
    def __init__(self, dirname, filename):
        super().__init__()


        # 初始化界面 来自qtdesigner和pyuic
        self.ui = ui_dialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowIcon(QIcon(":/ghost_white.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        # 存放最初的方便还原
        self.init_dir = dirname
        self.init_file = filename
        # 要传回的可修改路径
        self.dirname = dirname
        self.filename = filename
        self.writer = ""
        # 表示结束后是要存还是放进等待区
        self.status_code = code_quit

        self.ui.dir_text_edit.setPlainText(self.dirname)
        self.ui.file_text_edit.setPlainText(self.filename)

        # self.ui.wait_handle_button.clicked.emit(code_wait_handle)

    def closeEvent(self, event: QCloseEvent):

        result = SilentMessageBox.question(self, "确定取消生成吗?前面的内容不会被保存")
        if result == SilentMessageBox.Yes:
            self.status_code = code_quit
            event.accept()
        else:
            event.ignore()

    def open_dir(self):

        self.dirname = self.ui.dir_text_edit.toPlainText()
        if os.path.exists(self.dirname):
            os.startfile(self.dirname)
        else:
            SilentMessageBox.info(self, "找不到该文件夹QAQ\n"
                                        "请检查文件目录名是否有问题\n")

    def add_item(self):
        # item = MMEitem(self.dirname,self.filename,self.writer)
        self.dirname = self.ui.dir_text_edit.toPlainText()
        self.filename = self.ui.file_text_edit.toPlainText()
        self.writer = self.ui.writer_text_edit.toPlainText()
        if self.writer != "":
            self.status_code = code_add_item
            self.accept()
        else:
            SilentMessageBox.info(self, "作者名不能为空")

    def reset_text(self):
        self.dirname = self.init_dir
        self.filename = self.init_file
        self.ui.dir_text_edit.setPlainText(self.dirname)
        self.ui.file_text_edit.setPlainText(self.filename)
        self.ui.writer_text_edit.clear()

    def ignore_item(self):
        self.status_code = code_wait_handle
        # 防止你忘了写场景所以还是跟稍后处理一起吧
        self.dirname = self.init_dir
        self.filename = self.init_file
        self.writer = ""
        self.accept()
