import csv
from typing import TextIO

import dialogs
import ui_mainWindow
import ghost_icon_rc

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox
import os
from tkinter import Tk, filedialog

lib_name = "lib.csv"


def get_mme_item(dirname, filename, writer) -> dict:
    return {"dirname": dirname, "filename": filename, "writer": writer}


class MainWindow(QMainWindow):
    code_wait_handle = 0
    code_add_item = 1
    code_ignore_item = 2

    code_shift_jis = "Shift_JIS"
    code_gb18030 = "GB18030"

    def __init__(self):
        super().__init__()
        # 初始化界面 来自qt designer和pyuic
        self.ui = ui_mainWindow.Ui_mainWindow()
        self.ui.setupUi(self)



        # icon = QIcon()
        # icon.addPixmap(QPixmap('ghost_white.png'))
        # “:/icon.png” 是从编译后的 .qrc 文件中加载图标的语法
        # https://blog.csdn.net/qq_42750240/article/details/131141491
        self.setWindowIcon(QIcon(":/ghost_white.png"))

        self.encode = self.code_gb18030
        # 字典列表，读取lib.csv
        self.library = list()
        # true的时候写库
        self.library_changed_flag = False
        # 详细信息，包括mme名 作者 路径，也是字典列表
        # 存lib的引用
        self.datas = list()
        # 字典列表
        self.wait_data_list = list()
        # 专给滤镜开的，有这个前缀就只匹配路径名不看文件名了不然烦死了
        # self.filter_prefix = list()
        # self.read_filter_prefix()
        # self.detailed_info_dialog = dialogs.DetailedDialog(self.datas)

        # 初始不显示的
        self.ui.add_emm_button.hide()
        self.ui.emm_name_label.hide()
        self.ui.emm_filename_browser.hide()

        self.show_add_labels = False

    def read_lib(self):
        # 把库清空再重新读一遍
        try:
            with open(lib_name, 'r', encoding='utf-8-sig') as csv_file:
                self.library.clear()
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.library.append(row)

        except FileNotFoundError:
            print("file mme_lib doesn't exist")
            return

    def write_lib(self):
        if self.library_changed_flag is True:
            try:
                with open(lib_name, 'w', newline='', encoding='utf-8-sig') as csv_file:
                    fieldnames = ['dirname', 'filename', 'writer']
                    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                    # 写入表头
                    csv_writer.writeheader()
                    # 写入数据
                    csv_writer.writerows(self.library)
                    # it = item.MMEitem("PAToon","PAToon僐儞僩儘乕儔乕.pmx","P.I.P")
                    # file.write(json.dumps(library, indent=2, ensure_ascii=False))
                self.library_changed_flag = False
            except FileNotFoundError:
                print("file mme_lib doesn't exist")

    def get_file_path(self) -> str:
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="读取emm文件", defaultextension=".emm")  # 获得选择好的文件
        print('filepath:', file_path)
        if file_path == "" or file_path is None:
            return ""
        name, extension = os.path.splitext(file_path)
        if extension != '.emm':
            print('please read .emm file')
            QMessageBox.critical(self, "提示", "请打开.emm文件！")
            return ""

        root.destroy()
        # 每次都读一次表
        try:
            self.read_lib()
        except Exception as e:
            print({e})
            return ""
        return file_path

    # 读取emm文件的槽
    def read_emm_files(self):
        file_path = self.get_file_path()
        if file_path == "":
            return
            # print(self.library)
            # 清空上次结果
        self.ui.result_browser.setText("")
        self.ui.not_handle_browser.setText("")
        # self.writer_list.clear()
        self.datas.clear()
        self.wait_data_list.clear()
        self.ui.emm_filename_browser.clear()

        self.exec(file_path)

        if self.show_add_labels is False:
            self.ui.add_emm_button.show()
            self.ui.emm_name_label.show()
            self.ui.emm_filename_browser.show()
            self.show_add_labels = True

    # 追加emm文件的槽
    def add_emm_files(self):
        file_path = self.get_file_path()
        if file_path == "":
            return
        # print(self.library)
        self.exec(file_path)

    # 读取和追加共用的流程，读emm写表
    def exec(self, file_path: str):

        # 打开emm，先用gb18030读，不行再用shift-jis
        try:
            with open(file_path, 'r', encoding='GB18030') as emm_file:
                # self.encode = self.code_gb18030
                self.emm_file_analysis(emm_file)

        except Exception as e0:
            print(f"Can't open file as UTF-8,Exception:{e0}")
            QMessageBox.information(self, "提示", "尝试用中文编码打开时出现乱码\n改为使用日文编码", QMessageBox.Close)
            try:
                with open(file_path, 'r', encoding='shift-JIS') as emm_file:
                    # self.encode = self.code_shift_jis
                    self.emm_file_analysis(emm_file)
            except Exception as e:
                QMessageBox.information(self, "提示", "日文编码也报错，请反馈给作者", QMessageBox.Close)
                print(f"Exception: {e} ")
                return

        if len(self.datas) > 0:
            self.gen_writer_list()

        if len(self.wait_data_list) > 0:
            self.gen_waiting_list()

        self.write_lib()

    def emm_file_analysis(self, emm_file: TextIO):
        self.ui.emm_filename_browser.append(emm_file.name)
        # self.ui.emm_name_label.setText("读取文件: "+emm_file.name)
        lines = emm_file.readlines()
        datas = list()
        read_begin_flag = False
        # 读取[Object]栏开始，空行结束
        for line in lines:
            if read_begin_flag is True:
                if line == '\n':
                    break
                else:
                    # 去除前面的acs/pmd,再用空格拼回来
                    new_line = ' '.join(line.replace('\n', '').split(" ")[2:])
                    # print("line after work: " + new_line)
                    datas.append(new_line)
            elif line == '[Object]\n':
                read_begin_flag = True
        # print(datas)
        for data in datas:
            mme_path = os.path.dirname(data)
            mme_name = os.path.basename(data)
            print(mme_path, mme_name)
            # 保存路径一样名字不一样的
            match_mem_item = None
            find_mme_flag = False
            for lib_item in self.library:
                # 判断是同一个文件夹下但不是同一个.x/.pmx
                # print(lib_item["dirname"])
                if self.is_path_match(mme_path, lib_item["dirname"]):
                    print("path is match:" + lib_item["dirname"])
                    # .x也一样，判断为同一个
                    if mme_name == lib_item["filename"]:
                        self.datas.append(lib_item)
                        find_mme_flag = True
                        break
                    else:
                        # 不一样，接着往下找
                        match_mem_item = lib_item
                        continue

            if find_mme_flag is False:
                # 有同类但不是同一个.x，自己加
                if match_mem_item is not None:
                    #
                    it = get_mme_item(match_mem_item["dirname"], mme_name, match_mem_item["writer"])
                    self.add_item_to_lib(it)
                    self.datas.append(it)
                    continue
                # 没找到对应的 弹窗提示是增加还是忽略
                dialog = dialogs.AddDialog(mme_path, mme_name)
                dialog.exec()
                self.dialog_info_handler(dialog.status_code, dialog.dirname, dialog.filename, dialog.writer)

                dialog.destroy()

    def is_path_match(self, ab_dir_name, item_dir_name) -> bool:
        # 库中存的是绝对路径
        if os.path.isabs(item_dir_name):
            return item_dir_name == ab_dir_name
        # 相对
        item_dirs = item_dir_name.split("\\")
        ab_dirs = ab_dir_name.split("\\")
        # 只有一级相对文件名，取最后一级

        for i in range(min(len(item_dirs), len(ab_dirs))):
            if item_dirs[-(i + 1)] != ab_dirs[-(i + 1)]:
                return False
        return True

    def dialog_info_handler(self, code: int, dirname: str, filename: str, writer: str):
        print("get Code:" + str(code))
        it = get_mme_item(dirname, filename, writer)
        if code == self.code_wait_handle:
            # 加入等待列表
            self.wait_data_list.append(it)
            # print(it)
            # print("未处理："+str(it))
        elif code == self.code_add_item:
            # 同时添加进data和lib，同一个引用
            self.add_item_to_lib(it)
            self.datas.append(it)

            # self.add_writer_to_list(writer)
            # 同时添加进库
            # print("添加成功:"+item)
        else:
            print("忽略本项")
            pass

    def add_item_to_lib(self, it: dict):
        self.library.append(it)
        self.library_changed_flag = True

    # 把作者名（可能多个）加入list
    # def add_writer_to_list(self, writer_str: str):
    #     writers = writer_str.split(",")
    #     for writer in writers:
    #         if writer not in self.writer_list:
    #             self.writer_list.append(writer)

    def gen_writer_list(self):
        writer_list = set()
        for data in self.datas:
            writers = data["writer"].split("/")
            for writer in writers:
                if writer not in writer_list:
                    writer_list.add(writer)

        result = "/".join(writer_list)
        self.ui.result_browser.setText(result)

    def gen_waiting_list(self):
        wait_data_result = ""
        for data in self.wait_data_list:
            wait_data_result += data["dirname"] + "\t" + data["filename"] + "\n"
            # wait_data_result +=
        if wait_data_result != "":
            self.ui.not_handle_browser.setText(wait_data_result)
            # try:
            #     encode_result = wait_data_result.encode(self.encode)
            #
            #     print(str(encode_result))
            #     self.ui.not_handle_browser.setText(str(encode_result))
            # except Exception as e:
            #     print(e)

    # 写了好像没用的乱码转换，先放着
    #
    #
    # def wait_list_encode_to_jis(self):
    #     self.encode = self.code_shift_jis
    #     self.gen_waiting_list()
    #
    # def wait_list_encode_to_gb(self):
    #     self.encode = self.code_gb18030
    #     self.gen_waiting_list()

    def copy_event(self):

        result = self.ui.result_browser.toPlainText()
        if result != "":
            QMessageBox.information(self, '提示', '复制成功', QMessageBox.Close)
            root = Tk()
            # 复制到剪贴板
            root.clipboard_append(result)
            root.destroy()

    def copy_details_event(self):

        result_dict = {}

        for data in self.datas:
            writer = data["writer"]
            dirname = data["dirname"]

            # 处理一下dirname，路径存的是\但是作者名是/，好弱智
            dirname = dirname.replace("\\","/")
            # 不知道会不会有绝对路径
            if writer not in result_dict.keys():
                result_dict[writer] = dirname
            else:
                if dirname not in result_dict[writer]:
                    result_dict[writer] += '\n\t' + dirname
        if result_dict:
            result = ''
            for key in result_dict:
                result += key + ':\n\t' + result_dict[key] + '\n\n'
            print(result)
            QMessageBox.information(self, '提示', '复制详细列表成功', QMessageBox.Close)
            root = Tk()
            # # 复制到剪贴板
            root.clipboard_append(result)
            root.destroy()

    def print_detailed_info(self):
        detailed_info_dialog = dialogs.DetailedDialog(self.datas)
        detailed_info_dialog.exec()
        if detailed_info_dialog.delete_flag is True:
            self.gen_writer_list()
        if detailed_info_dialog.rewrite_flag is True:
            self.gen_writer_list()
            self.write_lib()
        detailed_info_dialog.destroy()

    # def read_filter_prefix(self):
    #     try:
    #         file_path = "files/filter.txt"
    #         with open(file_path, 'r', encoding='GB18030') as file:
    #             lines = file.readlines()
    #             for line in lines:
    #                 self.filter_prefix.append(line.replace("\n", ""))
    #     except FileNotFoundError as e:
    #         # 没单独设文档，默认添加如下
    #         print("无文档，采用默认设置")
    # self.filter_prefix = ["ikClut", "PostMovie", "ScreenTex", "o_Tonemap", "Drop Colors",
    #                       "1color 1.1_winglayer"]
    # print(self.filter_prefix)
