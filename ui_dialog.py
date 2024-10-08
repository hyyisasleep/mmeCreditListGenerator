# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(743, 461)
        self.tips_label = QtWidgets.QLabel(Dialog)
        self.tips_label.setEnabled(True)
        self.tips_label.setGeometry(QtCore.QRect(20, 20, 381, 21))
        self.tips_label.setObjectName("tips_label")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 60, 701, 181))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.text_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.text_layout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.text_layout.setContentsMargins(0, 0, 0, 0)
        self.text_layout.setSpacing(10)
        self.text_layout.setObjectName("text_layout")
        self.dirname_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.dirname_label.setTextFormat(QtCore.Qt.PlainText)
        self.dirname_label.setObjectName("dirname_label")
        self.text_layout.addWidget(self.dirname_label)
        self.dir_text_edit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.dir_text_edit.setMaximumSize(QtCore.QSize(16777215, 87))
        self.dir_text_edit.setObjectName("dir_text_edit")
        self.text_layout.addWidget(self.dir_text_edit)
        self.filename_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.filename_label.setObjectName("filename_label")
        self.text_layout.addWidget(self.filename_label)
        self.file_text_edit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.file_text_edit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.file_text_edit.setObjectName("file_text_edit")
        self.text_layout.addWidget(self.file_text_edit)
        self.writer_label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.writer_label.setObjectName("writer_label")
        self.text_layout.addWidget(self.writer_label)
        self.writer_text_edit = QtWidgets.QTextEdit(self.verticalLayoutWidget)
        self.writer_text_edit.setObjectName("writer_text_edit")
        self.text_layout.addWidget(self.writer_text_edit)
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(180, 260, 361, 191))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.choice_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.choice_layout.setContentsMargins(0, 0, 0, 0)
        self.choice_layout.setObjectName("choice_layout")
        self.cancel_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.cancel_button.setObjectName("cancel_button")
        self.choice_layout.addWidget(self.cancel_button, 1, 0, 1, 1)
        self.open_dir_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.open_dir_button.setObjectName("open_dir_button")
        self.choice_layout.addWidget(self.open_dir_button, 2, 0, 1, 1)
        self.add_item_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.add_item_button.setObjectName("add_item_button")
        self.choice_layout.addWidget(self.add_item_button, 0, 0, 1, 1)
        self.reset_text_button = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.reset_text_button.setObjectName("reset_text_button")
        self.choice_layout.addWidget(self.reset_text_button, 7, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.cancel_button.clicked.connect(Dialog.ignore_item) # type: ignore
        self.open_dir_button.clicked.connect(Dialog.open_dir) # type: ignore
        self.add_item_button.clicked.connect(Dialog.add_item) # type: ignore
        self.reset_text_button.clicked.connect(Dialog.reset_text) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "MME录入"))
        self.tips_label.setText(_translate("Dialog", "未能识别该项，请自行修改以下信息："))
        self.dirname_label.setText(_translate("Dialog", "文件目录名："))
        self.filename_label.setText(_translate("Dialog", "MME名："))
        self.writer_label.setText(_translate("Dialog", "<html><head/><body><p>作者名：（如有多个作者中间请用“/”分割）</p></body></html>"))
        self.cancel_button.setText(_translate("Dialog", "这是场景/模型文件，忽略"))
        self.open_dir_button.setText(_translate("Dialog", "打开文件目录（有乱码会打不开）"))
        self.add_item_button.setText(_translate("Dialog", "添加至库中"))
        self.reset_text_button.setText(_translate("Dialog", "还原为默认内容"))
