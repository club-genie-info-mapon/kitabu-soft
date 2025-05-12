from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
import os
from src.controllers.userController import UserController
from src.models.userModel import UserModel
from src.db.strategies import SQLiteStrategy
from src.main import MainWindow
from src.utils.languages import load_translations
from src.utils.helpers import resource_path


class LoginWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the login window with the given language.
        """
        super().__init__() 
        self.translations = load_translations().get("LoginWindow")
        self.setWindowTitle(self.translations.get("title"))
        self.setGeometry(100, 100, 550, 550)
        icon_path = resource_path(os.path.join("src", "assets", "icon.png"))
        self.setWindowIcon(QIcon(icon_path))
        self.initUI()

    def initUI(self):
        """
        Initialize the UI components of the login window.
        """
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Titre avec icône
        title_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_path = resource_path(os.path.join("src", "assets", "icon.png"))
        icon_label.setPixmap(QIcon(icon_path).pixmap(48, 48))
        title = QLabel(self.translations.get("title_label"))
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title)
        layout.addLayout(title_layout)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.username_label = QLabel(self.translations.get("username_label"))
        self.username_label.setFont(QFont("Arial", 13))
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont("Arial", 13))
        self.username_input.setPlaceholderText(self.translations.get("username_placeholder"))
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel(self.translations.get("password_label"))
        self.password_label.setFont(QFont("Arial", 13))
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Arial", 13))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText(self.translations.get("password_placeholder"))   
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Checkbox to toggle password visibility
        self.show_password_checkbox = QCheckBox("Afficher le mot de passe")
        self.show_password_checkbox.setFont(QFont("Arial", 11))
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_password_checkbox)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Boutons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton(self.translations.get("login_button"))
        self.login_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.login_button.setStyleSheet(
            "QPushButton {background-color: #1976D2; color: white; border-radius: 8px; padding: 12px 0; min-width: 140px;}"
            "QPushButton:hover {background-color: #1565C0;}"
        )
        self.login_button.clicked.connect(self.handle_login)

        button_layout.addWidget(self.login_button)
        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
            }
            QLineEdit {
                border: 1.5px solid #bdbdbd;
                border-radius: 7px;
                padding: 10px;
                background: #fff;
            }
            QLabel {
                color: #333;
            }
        """)

    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        try:
            if username and password:
                strategy  = SQLiteStrategy(resource_path(os.path.join("src", "db", "library.db")))
                model = UserModel(strategy)
                user = UserController(model)

                if user.signin(username, password):
                    QMessageBox.information(self, 
                        self.translations.get("login_success_title"), 
                        self.translations.get("login_success_message"),
                        )
                    self.close()
                    self.main_window = MainWindow()
                    self.main_window.show()
                else:
                    QMessageBox.warning(self, 
                    self.translations.get("login_error_title"),
                    self.translations.get("login_error_message"), 
                    )
            else:
                QMessageBox.warning(self, 
                    "Missing Information",
                    "Please enter both username and password.", 
                    )
        except Exception as e:
            QMessageBox.critical(self, 
                "Error",
                f'An error occurred: {e}'
                )
            print(f"Error: {e}")

def main():
    app = QApplication([])
    login = LoginWindow()
    login.show()
    app.exec_()

if __name__ == "__main__":
    main()