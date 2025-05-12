from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy, QHBoxLayout
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt

from src.main import MainWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion - Bibliothèque")
        self.setGeometry(100, 100, 500, 550)
        self.setWindowIcon(QIcon("src/assets/icon.png"))  # Assurez-vous que le chemin est correct

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Titre avec icône
        title_layout = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(QIcon("src/assets/icon.png").pixmap(48, 48))
        title = QLabel("Bienvenue à la Bibliothèque")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title)
        layout.addLayout(title_layout)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.username_label = QLabel("Nom d'utilisateur :")
        self.username_label.setFont(QFont("Arial", 13))
        self.username_input = QLineEdit()
        self.username_input.setFont(QFont("Arial", 13))
        self.username_input.setPlaceholderText("Entrez votre nom d'utilisateur")
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel("Mot de passe :")
        self.password_label.setFont(QFont("Arial", 13))
        self.password_input = QLineEdit()
        self.password_input.setFont(QFont("Arial", 13))
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Entrez votre mot de passe")
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Boutons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Se connecter")
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

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username == "admin" and password == "admin":
            QMessageBox.information(self, "Succès", "Connexion réussie !")
            self.close()
            self.main_window = MainWindow()
            self.main_window.show()
        else:
            QMessageBox.warning(self, "Erreur", "Nom d'utilisateur ou mot de passe incorrect.")

def main():
    app = QApplication([])
    login = LoginWindow()
    login.show()
    app.exec_()

if __name__ == "__main__":
    main()