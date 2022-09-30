import sqlite3

from PyQt5.QtGui import QImage, QPalette, QBrush


def setting_background(self):
    image = QImage("picture/background.jpg").scaled(self.size())
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(image))
    self.setPalette(palette)


def account_verification(login, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    result = cur.execute(f"""SELECT id FROM users 
                             WHERE login == '{login}' and password == '{password}'
                             """).fetchall()
    con.close()
    if result:
        return result[0][0]
    return 0
