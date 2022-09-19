from PyQt5.QtGui import QImage, QPalette, QBrush


def setting_background(self):
    image = QImage("picture/background.jpg").scaled(self.size())
    palette = QPalette()
    palette.setBrush(QPalette.Window, QBrush(image))
    self.setPalette(palette)
