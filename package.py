# pyinstaller -F -w main.py -p mainWindow.py -p addDialog.py -p
# ui_dialog.py -p ui_mainWindow.py --hidden-import mainWindow --hidden-import addDialog
# --hidden-import utils --hidden-import ui_mainWindow --hidden-import ui_dialog
import os
import shutil


path = "v1-2"
os.makedirs(path,exist_ok=True)
shutil.copy("main.py",path + "/main.py")
shutil.copy("mainWindow.py",path + "/mainWindow.py")
shutil.copy("dialogs.py",path + "/dialogs.py")
shutil.copy("ui_mainWindow.py",path + "/ui_mainWindow.py")
shutil.copy("ui_dialog.py",path + "/ui_dialog.py")

# pyinstaller 参考
# https://blog.csdn.net/tb_youth/article/details/105754733
# https://xiaokang2022.blog.csdn.net/article/details/127585881
# 最终执行命令： 然后去暴力删包！
# 有个internal，要求pyinstaller版本6.0往上
# pyinstaller -D -w -i "ghost.ico" .\main.py


# 没有internal 38M大的exe，但是启动速度要慢一点
# pyinstaller -F -w -i "ghost.ico" .\main.py


# 暴力瘦身法
# https://blog.csdn.net/qq_41887747/article/details/121367574