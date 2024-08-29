import os
import sys
from PyQt5.QtWidgets import QApplication
import mainWindow

if __name__ == '__main__':
    # os.makedirs("files", exist_ok=True)

    app = QApplication(sys.argv)
    mw = mainWindow.MainWindow()
    mw.show()
    sys.exit(app.exec_())

# qt designer 教程
# https://blog.csdn.net/weixin_40883833/article/details/126333030
# https://blog.csdn.net/weixin_40883833/article/details/126333046
