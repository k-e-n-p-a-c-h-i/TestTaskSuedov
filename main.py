import datetime
import sqlite3
import sys

from functions import setting_background, account_verification
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QVBoxLayout, QDialog, QPushButton
from PyQt5.QtCore import Qt, QCoreApplication


class AccountError(Exception):
    pass


class DataError(Exception):
    pass


class Authorization(QMainWindow):
    def __init__(self):
        super(Authorization, self).__init__()
        uic.loadUi('Ui_files/authorization.ui', self)
        self.initUi()

    def initUi(self):
        self.pushButton.clicked.connect(self.authorization)
        self.setFixedSize(1343, 756)
        setting_background(self)

    def authorization(self):
        try:
            user_id = account_verification(self.login.text(), self.password.text())
            if user_id:
                self.main_window = MainWindow(user_id)
                self.main_window.show()
                self.hide()
            else:
                raise AccountError
        except AccountError:
            QMessageBox.critical(self, "ERROR", "There is no account with such authorization data."
                                                " Contact your administrator to clarify the data", QMessageBox.Ok)


class MainWindow(QMainWindow):
    def __init__(self, user_id):
        super(MainWindow, self).__init__()
        uic.loadUi('UI_files/main.ui', self)
        self.user_id = user_id
        self.task_list = TaskList(self)
        self.add_task_win = AddTask(self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1343, 756)
        self.pushButton.clicked.connect(self.open_win)
        self.pushButton_2.clicked.connect(self.open_win)
        self.pushButton_3.clicked.connect(self.open_win)
        setting_background(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QCoreApplication.instance().quit()

    def open_win(self):
        if self.sender() == self.pushButton:
            self.task_list.update()
            self.task_list.show()
            self.hide()
        elif self.sender() == self.pushButton_2:
            pass
        elif self.sender() == self.pushButton_3:
            self.add_task_win.clean()
            self.add_task_win.show()


class TaskList(QWidget):
    def __init__(self, parents):
        super(TaskList, self).__init__()
        uic.loadUi('UI_files/task_list.ui', self)
        self.parents = parents
        self.initUI()

    def initUI(self):
        self.pushButton.clicked.connect(self.return_parents)
        self.setFixedSize(1343, 756)
        setting_background(self)

    def update(self):
        self.widget = QWidget(self)
        self.vbox = QVBoxLayout(self.widget)
        self.scroll.setWidget(self.widget)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT name, id FROM task """).fetchall()
        for elem in result:
            button = QPushButton(f'{elem[0]} :{elem[1]}')
            button.setStyleSheet("""color:rgb(243, 243, 243);
                                       background-color: rgba(54, 54, 54, 150);
                                       border-style: outset;
                                       border-radius:10px;
                                       font: 14pt "MS Shell Dlg 2";""")
            button.setFixedHeight(33)
            button.clicked.connect(self.inf)
            self.vbox.addWidget(button)
        con.close()

    def return_parents(self):
        self.hide()
        self.parents.show()

    def inf(self):
        self.task = ViewTask()
        self.task.show()
        print('таску нажали')


class AddTask(QDialog):
    def __init__(self, parents):
        super(AddTask, self).__init__()
        self.parents = parents
        self.setModal(True)
        uic.loadUi("UI_files/add_task.ui", self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(812, 448)
        self.pushButton.clicked.connect(self.add_record)
        setting_background(self)
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        result = cur.execute(f"""SELECT username FROM users
                                 WHERE id != {self.parents.user_id}""").fetchall()
        for users in result:
            self.comboBox.addItem(users[0])

    def clean(self):
        self.textEdit.setText('')
        self.lineEdit.setText('')

    def add_record(self):
        try:
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            executor = self.comboBox.currentText()
            customer_id = self.parents.user_id
            description = self.textEdit.toPlainText()
            start_date = datetime.date.today()
            date_of_completion = self.dateEdit.dateTime().toString('dd-MM-yyyy')
            name = self.lineEdit.text()
            task_id = max([el[0] for el in cur.execute(f"""SELECT id FROM task""").fetchall()]) + 1
            if description == '' or name == '':
                raise DataError
            cur.execute("""INSERT INTO task VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""", (executor,
                                                                                   customer_id,
                                                                                   description,
                                                                                   start_date,
                                                                                   date_of_completion,
                                                                                   0,
                                                                                   1,
                                                                                   name,
                                                                                   task_id
                                                                                   ))
            con.commit()
            self.close()
        except sqlite3.IntegrityError:
            QMessageBox.critical(self, "Ошибка", "Такое название существует", QMessageBox.Ok)
        except DataError:
            QMessageBox.critical(self, "Ошибка", "Заполните пустые поля", QMessageBox.Ok)


class ViewTask(QDialog):
    def __init__(self):
        super(ViewTask, self).__init__()
        self.setModal(True)
        uic.loadUi('Ui_files/view_task.ui', self)
        setting_background(self)
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()

    def delete(self):
        a = 'Вы действительно хотите удалить эту запись?'
        if QMessageBox.question(self, ' ', a, QMessageBox.Yes,
                                QMessageBox.No) == QMessageBox.Yes:
            self.close()
            self.cur.execute(f"DELETE FROM task WHERE name = '{self.but.text()}'")
            self.con.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('picture/icon.png'))

    form = Authorization()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
