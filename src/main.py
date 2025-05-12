from PyQt5.QtWidgets import (
    QMainWindow, QApplication
)
from PyQt5.QtGui import QIcon
import os

from src.utils.languages import load_translations
from src.utils.helpers import resource_path

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the main window.
        """
        super().__init__()
        self.translations = load_translations().get("MainWindow")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.setWindowTitle(self.translations.get("title"))
        icon_path = resource_path(os.path.join('src', 'assets', 'icon.png'))
        self.setWindowIcon(QIcon(icon_path))
