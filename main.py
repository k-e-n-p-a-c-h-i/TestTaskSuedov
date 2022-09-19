import sys
from functions import setting_background
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QCoreApplication


class Authorization(QMainWindow):
    def __init__(self):
        super(Authorization, self).__init__()
        uic.loadUi('Ui_files/authorization.ui', self)
        self.initUi()

    def initUi(self):
        setting_background(self)
        self.setFixedSize(1344, 756)


class MyWidget(QMainWindow):
    def __init__(self):
        super(MyWidget, self).__init__()
        self.tools_win = Authorization()
        uic.loadUi('UI_files/main.ui', self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1344, 756)
        self.pushButton_3.clicked.connect(self.new_win)
        setting_background(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def new_win(self):
        if self.sender() == self.pushButton_3:
            self.tools_win.show()
        self.hide()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('picture/icon.png'))

    form = Authorization()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
