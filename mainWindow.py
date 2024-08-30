import csv
from typing import TextIO

import addDialog
import detailedDialog
import ui_mainWindow
# 虽然它没被分析出来但不import真的出不了图标
import ghost_icon_rc
from silentMessageBox import SilentMessageBox

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow
import os
from tkinter import Tk, filedialog

lib_name = "lib.csv"


def get_mme_item(dirname, filename, writer) -> dict:
    return {"dirname": dirname, "filename": filename, "writer": writer}


def is_path_match(ab_dir_name, item_dir_name) -> bool:
    """
    匹配两个mme保存路径是否为同一个
    库里保存的是绝对的话直接判断内容相等
    相对的话从最后一级相对路径开始匹配
    :param ab_dir_name: 待匹配的绝对路径
    :param item_dir_name: 库中保存的路径，可能是绝对也可能是相对
    :return:
    """
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


class MainWindow(QMainWindow):
    code_wait_handle = 0
    code_add_item = 1
    code_quit = 2

    # code_shift_jis = "Shift_JIS"
    # code_gb18030 = "GB18030"

    def __init__(self):
        super().__init__()
        # 初始化界面 来自qt designer和pyuic
        self.ui = ui_mainWindow.Ui_mainWindow()
        self.ui.setupUi(self)

        # 设置应用图标
        # icon = QIcon()
        # icon.addPixmap(QPixmap('ghost_white.png'))
        # “:/icon.png” 是从编译后的 .qrc 文件中加载图标的语法
        # https://blog.csdn.net/qq_42750240/article/details/131141491
        self.setWindowIcon(QIcon(":/ghost_white.png"))

        # self.encode = self.code_gb18030
        # 字典列表，读取lib.csv
        self.library = list()
        # true的时候写库
        self.library_changed_flag = False
        # 详细信息，包括mme名 作者 路径，也是字典列表
        # 存lib的引用
        self.datas = list()
        # 生成时用的，成功生成再写进datas
        self.temp_datas = list()

        # 改成存字符串，路径名和文件名
        self.wait_data_list = list()
        self.temp_wait_data_list = list()
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
        """
            直接和csv文件交互，把内存中目前的lib清空后读取csv内容，存进self.library
        """
        # 把库清空再重新读一遍
        try:
            with open(lib_name, 'r', encoding='utf-8-sig') as csv_file:
                self.library.clear()
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    self.library.append(row)

        except FileNotFoundError:
            print("file mme_lib doesn't exist")

    def write_lib(self):
        """
            如果change_flag==True，即内存库被修改了，清空csv，把self.library内容写进csv

        :return:
        """
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
        """
        用tkinter读取emm文件，打开emm文件后会调用一次read_lib(不是为啥啊
        :return:成功返回文件名"xxx.emm",中途退出了返回""
        """
        root = Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename(title="读取emm文件", filetypes=[("EMM Files", "*.emm")])  # 获得选择好的文件
        print('filepath:', file_path)
        if file_path == "" or file_path is None:
            return ""
        name, extension = os.path.splitext(file_path)
        if extension != '.emm':
            print('please read .emm file')
            SilentMessageBox.info(self,text="请打开.emm文件！")

            return ""

        root.destroy()
        # 每次都读一次表
        try:
            self.read_lib()
        except Exception as e:
            print({e})
            return ""
        return file_path

    def read_emm_files(self):
        """
        从零读取emm文件的槽
        :return:
        """
        file_path = self.get_file_path()
        if file_path == "":
            return

        # 清空上次的全部结果
        self.ui.result_browser.setText("")
        self.ui.not_handle_browser.setText("")
        self.datas.clear()
        self.wait_data_list.clear()
        self.temp_datas.clear()
        self.temp_wait_data_list.clear()
        self.ui.emm_filename_browser.clear()

        # 调用exec执行生成
        if self.exec(file_path):
            # 第一次成功生成的话会显示读取了xxx文件以及出现追加emm文件按钮
            # 不成功的话就不显示了
            if self.show_add_labels is False:
                self.ui.add_emm_button.show()
                self.ui.emm_name_label.show()
                self.ui.emm_filename_browser.show()
                self.show_add_labels = True
        else:
            self.ui.add_emm_button.hide()
            self.show_add_labels = False


    #
    def add_emm_files(self):
        """
        追加emm文件的槽,跟 读取一样
        :return:
        """
        # 触发了追加就清空
        self.temp_datas.clear()
        self.temp_wait_data_list.clear()

        file_path = self.get_file_path()
        if file_path == "":
            return
        # print(self.library)
        self.exec(file_path)

    def exec(self, file_path: str):
        """
        # 读取和追加共用的流程，读emm写表

        :param file_path: str:xxx.emm
        :return:
        """
        # 打开emm，先用gb18030读，不行再用shift-jis

        prev_browser_text = self.ui.emm_filename_browser.toPlainText()
        try:
            with open(file_path, 'r', encoding='GB18030') as emm_file:
                # self.encode = self.code_gb18030
                # 这行本来是在analysis里的但是这样的话读日文编码会开两遍；）
                self.ui.emm_filename_browser.append(emm_file.name)
                if not self.ui.emm_filename_browser.isVisible():
                    self.ui.emm_name_label.show()
                    self.ui.emm_filename_browser.show()
                flag = self.emm_file_analysis(emm_file)

        except Exception as e0:
            print(f"Can't open file as UTF-8,Exception:{e0}")
            SilentMessageBox.info(self,text="尝试用中文编码打开时出现乱码\n->改为使用日文编码")

            try:
                with open(file_path, 'r', encoding='shift-JIS') as emm_file:
                    # self.encode = self.code_shift_jis
                    flag = self.emm_file_analysis(emm_file)
            except Exception as e:
                SilentMessageBox.info(self,text="日文编码也报错，请反馈给作者")
                print(f"Exception: {e} ")
                return
        if not flag:
            # 分析中途退出，在这处理
            self.temp_datas.clear()
            self.temp_wait_data_list.clear()
            # 还原回读入前的emm文件列表
            self.ui.emm_filename_browser.setText(prev_browser_text)
            return flag

        if len(self.temp_datas) > 0:
            self.move_temp_to_data_and_lib()
            self.gen_writer_list()

        if len(self.temp_wait_data_list) > 0:
            self.move_temp_wait_to_wait_data()
            self.gen_waiting_list()

        self.write_lib()
        return flag

    def emm_file_analysis(self, emm_file: TextIO) -> bool:

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
            # 开始在temp和lib里找
            match_mem_item = None
            find_mme_flag = False
            for lib_item in self.library:
                # 判断是同一个文件夹下但不是同一个.x/.pmx
                # print(lib_item["dirname"])
                if is_path_match(mme_path, lib_item["dirname"]):
                    print("path is match:" + lib_item["dirname"])
                    # .x也一样，判断为同一个
                    if mme_name == lib_item["filename"]:
                        # 把lib里的表项加进temp
                        self.temp_datas.append(lib_item)
                        find_mme_flag = True
                        break
                    else:
                        # 不一样，接着往下找
                        match_mem_item = lib_item
                        continue
            for temp_item in self.temp_datas:
                # 判断是同一个文件夹下但不是同一个.x/.pmx
                # print(lib_item["dirname"])
                if is_path_match(mme_path, temp_item["dirname"]):
                    print("path is match in tmp data:" + temp_item["dirname"])
                    # .x也一样，判断为同一个
                    if mme_name == temp_item["filename"]:
                        # self.temp_datas.append(lib_item)
                        find_mme_flag = True
                        break
                    else:
                        # 不一样，接着往下找
                        match_mem_item = temp_item
                        continue

            # 没出现在库或者temp里，视为新增
            if find_mme_flag is False:
                # 有同类但不是同一个.x，程序自己加进temp
                if match_mem_item is not None:
                    #
                    it = get_mme_item(match_mem_item["dirname"], mme_name, match_mem_item["writer"])
                    self.temp_datas.append(it)
                    continue
                # 没找到对应的 弹窗提示是增加还是忽略
                dialog = addDialog.AddDialog(mme_path, mme_name)
                dialog.exec()
                # 提前退出停止生成了
                if dialog.status_code == self.code_quit:
                    return False
                else:
                    # 走正常处理流程，加进tmp或者等待列表的tmp
                    self.dialog_info_handler(dialog.status_code,
                                             dialog.dirname, dialog.filename, dialog.writer)

                dialog.destroy()
        return True

    def dialog_info_handler(self, code: int, dirname: str, filename: str, writer: str):
        print("get Code:" + str(code))

        if code == self.code_wait_handle:
            # 加入等待列表
            self.temp_wait_data_list.append(f"{dirname} {filename}")
            # print(it)
            # print("未处理："+str(it))
        elif code == self.code_add_item:
            it = get_mme_item(dirname, filename, writer)
            # 新创建一个表项，添加进tmp_data里，等成功生成了再加入库
            self.temp_datas.append(it)

            # self.add_writer_to_list(writer)
            # 同时添加进库
            # print("添加成功:"+item)
        else:
            print("忽略本项")
            pass

    # 把作者名（可能多个）加入list
    # def add_writer_to_list(self, writer_str: str):
    #     writers = writer_str.split(",")
    #     for writer in writers:
    #         if writer not in self.writer_list:
    #             self.writer_list.append(writer)

    def move_temp_to_data_and_lib(self):
        for data in self.temp_datas:
            if data not in self.library:
                # 以免出现同一个对象被加几遍的问题？
                self.library.append(data)
                self.library_changed_flag = True
            self.datas.append(data)

    def move_temp_wait_to_wait_data(self):
        for data in self.temp_wait_data_list:
            self.wait_data_list.append(data)

    def gen_writer_list(self):
        """
        :return:
        """
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
            wait_data_result += data + "\n"
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
            SilentMessageBox.info(self,f"已将以下内容复制到剪贴板：\n===========================\n\n{result}")
            root = Tk()
            # 复制到剪贴板
            root.clipboard_append(result)
            root.destroy()
        else:
            SilentMessageBox.info(self, "复制失败，列表是空的QWQ")

    def copy_details_event(self):
        if not self.datas:
            SilentMessageBox.info(self, "复制失败，列表是空的QWQ")
            return

        result_dict = {}
        for data in self.datas:
            writer = data["writer"]
            dirname = data["dirname"]

            # 处理一下dirname，路径存的是\但是作者名是/，好弱智
            dirname = dirname.replace("\\", "/")
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
            SilentMessageBox.info(self,f"已将以下内容复制到剪贴板：\n===========================\n\n{result}")
            root = Tk()
            # # 复制到剪贴板
            root.clipboard_append(result)
            root.destroy()

    def copy_credit_list_event(self):
        result = f'bgm:\nmodel:\nstage:\nmotion:\nchoreography:\ncamera:\nmme:{self.ui.result_browser.toPlainText()}\n'
        root = Tk()
        # # 复制到剪贴板
        root.clipboard_append(result)
        root.destroy()
        SilentMessageBox.info(self,f"已将以下内容复制到剪贴板：\n===========================\n\n{result}")

    def print_detailed_info(self):
        if not self.datas:
            SilentMessageBox.info(self, "打开失败，列表是空的QWQ")
            return
        detailed_info_dialog = detailedDialog.DetailedDialog(self.datas)
        detailed_info_dialog.exec()
        if detailed_info_dialog.delete_flag is True:
            self.gen_writer_list()
        if detailed_info_dialog.rewrite_flag is True:
            self.gen_writer_list()
            self.library_changed_flag = True
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
