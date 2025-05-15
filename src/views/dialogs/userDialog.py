from PyQt5.QtWidgets import (
    QLineEdit, QDialog, QFormLayout, QComboBox, QDialogButtonBox
)


class UserDialog(QDialog):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un utilisateur" if user is None else "Modifier utilisateur")
        self.setMinimumWidth(370)
        layout = QFormLayout(self)
        layout.setSpacing(18)
        self.username = QLineEdit()
        self.username.setPlaceholderText("Nom d'utilisateur")
        self.username.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #1976D2;}")
        self.password = QLineEdit()
        self.password.setPlaceholderText("Mot de passe")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #1976D2;}")
        self.full_name = QLineEdit()
        self.full_name.setPlaceholderText("Nom complet")
        self.full_name.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #1976D2;}")
        self.faculty = QLineEdit()
        self.faculty.setPlaceholderText("Faculté")
        self.faculty.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #1976D2;}")
        self.class_ = QLineEdit()
        self.class_.setPlaceholderText("Promotion")
        self.class_.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #1976D2;}")
        self.user_type = QComboBox()
        self.user_type.addItems(["librarian", "academic", "student"])
        self.user_type.setStyleSheet("QComboBox {padding: 8px; border-radius: 8px; border: 1.5px solid #1976D2;}")

        layout.addRow("Nom d'utilisateur:", self.username)
        layout.addRow("Mot de passe:", self.password)
        layout.addRow("Nom complet:", self.full_name)
        layout.addRow("Faculté:", self.faculty)
        layout.addRow("Promotion:", self.class_)
        layout.addRow("Type:", self.user_type)
        if user:
            self.username.setText(user[1])
            self.password.setText(user[2])
            self.full_name.setText(user[3])
            self.faculty.setText(user[4])
            self.class_.setText(user[5])
            self.user_type.setCurrentText(user[6])
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Valider")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        self.buttons.setStyleSheet("""
            QDialogButtonBox QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 14px;
                min-width: 100px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #1565C0;
            }
        """)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        return (
            self.username.text(),
            self.password.text(),
            self.full_name.text(),
            self.faculty.text(),
            self.class_.text(),
            self.user_type.currentText()
        )
