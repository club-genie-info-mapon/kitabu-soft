from PyQt5.QtWidgets import (
    QMainWindow, QApplication
)
from PyQt5.QtGui import QIcon
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 700, 500)
        self.setWindowTitle("Gestion de Bibliothèque")
        self.setWindowIcon(QIcon("src/assets/icon.png"))
