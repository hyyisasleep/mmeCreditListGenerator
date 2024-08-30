
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QDialog, QTableWidget, QTableWidgetItem, QAbstractItemView

from silentMessageBox import SilentMessageBox
import ghost_icon_rc
code_wait_handle = 0
code_add_item = 1
code_quit = 2



class DetailedDialog(QDialog):

    def __init__(self, datas: list):
        super().__init__()

        self.setWindowIcon(QIcon(":/ghost_white.png"))
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.choose_item_flag = None
        self.datas = datas
        self.new_datas = datas
        # 如果有删除操作的话
        self.delete_list = list()
        # 记录改了哪条
        self.rewrite_flag = False
        self.delete_flag = False

        self.resize(1000, 400)

        self.setWindowTitle("详细信息表")
        row = len(datas)
        self.table_widget = QTableWidget(row, 4, self)
        self.table_widget.setHorizontalHeaderLabels(['MME文件', '作者', '文件路径', '操作'])
        # 只允许单选不许ctrl+a/shift/ctrl
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)

        # 录入数据
        cnt = 0
        for data in self.datas:
            self.table_widget.setItem(cnt, 0, QTableWidgetItem(data["filename"]))
            self.table_widget.setItem(cnt, 1, QTableWidgetItem(data["writer"]))
            self.table_widget.setItem(cnt, 2, QTableWidgetItem(data["dirname"]))
            item = QTableWidgetItem("删除该行")
            item.setBackground(QColor(200, 200, 200))
            self.table_widget.setItem(cnt, 3, item)
            cnt += 1

        self.table_widget.cellChanged.connect(self.CellChanged)
        # 修改完成后发射此信号
        self.table_widget.cellDoubleClicked.connect(self.CellDoubleClicked)
        # 渲染完了再显示
        self.setVisible(False)

    def adjust_and_show(self):
        # scroll_bar_width = self.table.verticalScrollBar().width()
        # print(f"Vertical scrollbar width after showing: {scroll_bar_width} pixels")
        #
        # # 根据滚动条宽度调整窗口大小
        # desired_width = self.table.width() + scroll_bar_width
        # self.resize(desired_width, self.height())
        # print(f"New window width: {desired_width} pixels")
        total_width = 0
        for i in range(self.table_widget.columnCount()):
            content_width = max(self.table_widget.sizeHintForColumn(i) ,100)  # 最小宽度为50

            # sizeHint 根据内容调整宽度
            self.table_widget.setColumnWidth(i, int(content_width))
            total_width += content_width
        print(f"四行宽度:{total_width}")

        total_width += self.table_widget.verticalHeader().width()
        print(f"加上表头宽度:{total_width}")

        # scroll_bar_range = (self.table_widget.verticalScrollBar().maximum()
        #                     - self.table_widget.verticalScrollBar().minimum())
        # if scroll_bar_range > 0:
        if self.table_widget.verticalScrollBar().isVisible():
            # 滚动条宽度默认100，得在渲染完成后才能调整到合适宽度
            # 来自gpt，所以用了showEvent，先在init渲染了个800*400再显示
            total_width += self.table_widget.verticalScrollBar().width()
            print(f"加上滚动条宽度:{total_width}")
        self.resize(total_width +2, self.height())
        # 调整完成后再显示窗口
        self.setVisible(True)

    # 双击单元格即开始修改单元格是发射此信号

    def showEvent(self, event):
        # self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_widget.resize(self.width(), self.height())
        super().showEvent(event)
        # 使用 QTimer 延迟调整大小，然后再显示窗口
        QTimer.singleShot(0, self.adjust_and_show)


    def resizeEvent(self, event):
        # super().resizeEvent(event)
        self.table_widget.resize(self.width(), self.height())
        # 发现不用写 呃呃

        # print(f"拖拽后尺寸:宽{self.width()},高{self.height()}")
        # # 之前的总列宽
        # prev_col_width = sum([self.table_widget.columnWidth(i)
        #                       for i in range(self.table_widget.columnCount())])
        # print(f"之前的总列宽：{prev_col_width}")
        # cur_col_width = self.width() - self.table_widget.verticalHeader().width()
        #
        # print(f"re：减去表头宽度:{cur_col_width}")
        # scroll_bar_range = self.table_widget.verticalScrollBar().maximum() - self.table_widget.verticalScrollBar().minimum()
        #
        # if scroll_bar_range > 0:
        #     cur_col_width -= self.table_widget.verticalScrollBar().width()
        #     # 不是为啥是height啊，测了一下宽100高30，用高反而是更贴近的
        #     print(f"re：减去滚动条宽度:{cur_col_width}")
        #
        # for i in range(self.table_widget.columnCount()):
        #     content_width = self.table_widget.columnWidth(i)  # 最小50
        #     self.table_widget.setColumnWidth(i, max(50,
        #                                             int(content_width / prev_col_width * cur_col_width)-1))


    def CellChanged(self, row, col):
        # 读取当前内容，有变化就写进新的备份数据里
        text = self.table_widget.item(row, col).text()
        if col < 3:
            colname = ""
            if col == 0:
                colname = "dirname"
            elif col == 1:
                colname = "filename"
            elif col == 2:
                colname = "writer"

            if text != self.datas[row][colname]:
                self.rewrite_flag = True
                self.setWindowTitle("详细信息表*")
        else:
            if text != "删除该行":
                SilentMessageBox(self, "请不要试图改这一行……")
                self.table_widget.item(row, col).setText("删除该行")

        self.choose_item_flag = False
        # 修改完成

    def CellDoubleClicked(self, row, col):
        self.choose_item_flag = True
        if col == 3:
            r = SilentMessageBox.question(self,
                                              f"确定删除 {self.table_widget.item(row, 0).text()} 这项吗？"
                                        )


            if r == SilentMessageBox.Yes:
                self.table_widget.removeRow(row)
                item = self.datas[row]
                self.delete_list.append(item)
                self.datas.remove(self.datas[row])
                self.delete_flag = True
                self.setWindowTitle("详细信息表*")

        # 开始修改

    def closeEvent(self, event):
        if self.choose_item_flag:
            # 正在修改中
            # 通过设置表格当前选择选择位置，模拟用户按下键盘“Enter”按键或点击了其他单元格
            self.table_widget.setCurrentItem(self.table_widget.item(0, 0))

        if self.rewrite_flag is True or self.delete_flag is True:

            r = SilentMessageBox.question(self, "退出前要保存修改吗？")

            if r == SilentMessageBox.Yes:
                for i in range(self.table_widget.rowCount()):
                    for j in range(3):
                        item = self.table_widget.item(i, j)
                        if j == 0:
                            self.datas[i]["filename"] = item.text()
                        elif j == 1:
                            self.datas[i]["writer"] = item.text()
                        else:
                            self.datas[i]["dirname"] = item.text()
            else:
                for data in self.delete_list:
                    self.datas.append(data)
                # 把删掉的都补回来
        event.accept()
