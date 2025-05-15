from PyQt5.QtWidgets import (
    QLineEdit, QDialog, QFormLayout, QDialogButtonBox, QDateEdit
)
from PyQt5.QtCore import QDate


class BookDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter un livre" if book is None else "Modifier livre")
        self.setMinimumWidth(370)
        layout = QFormLayout(self)
        layout.setSpacing(18)
        self.title = QLineEdit()
        self.title.setPlaceholderText("Titre du livre")
        self.title.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.inventory_number = QLineEdit()
        self.inventory_number.setPlaceholderText("Numéro d'inventaire")
        self.inventory_number.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.entry_date = QDateEdit(self)
        self.entry_date.setDate(QDate.currentDate())
        self.entry_date.setCalendarPopup(True)
        self.entry_date.setStyleSheet("QDateEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.cote = QLineEdit()
        self.cote.setPlaceholderText("Côte")
        self.cote.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.author = QLineEdit()
        self.author.setPlaceholderText("Auteur(s)")
        self.author.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.edition = QLineEdit()
        self.edition.setPlaceholderText("Edition")
        self.edition.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.category = QLineEdit()
        self.category.setPlaceholderText("Catégorie(s)")
        self.category.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.isbn = QLineEdit()
        self.isbn.setPlaceholderText("ISBN")
        self.isbn.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")
        self.copies = QLineEdit()
        self.copies.setPlaceholderText("Nombre d'exemplaires")
        self.copies.setStyleSheet("QLineEdit {padding: 8px; border-radius: 8px; border: 1.5px solid #388E3C;}")

        layout.addRow("Titre:", self.title)
        layout.addRow("Numéro d'inventaire:", self.inventory_number)
        layout.addRow("Date d'entrée:", self.entry_date)
        layout.addRow("Côte", self.cote)
        layout.addRow("Auteur:", self.author)
        layout.addRow("edition:", self.edition)
        layout.addRow("Catégorie:", self.category)
        layout.addRow("ISBN:", self.isbn)
        layout.addRow("Exemplaires:", self.copies)
        if book:
            self.title.setText(book[5])
            self.entry_date.setDate(QDate.fromString(book[1], "yyyy-MM-dd"))
            self.inventory_number.setText(book[2])
            self.cote.setText(book[3])
            self.author.setText(str(book[4]))
            self.edition.setText(str(book[6]))
            self.category.setText(str(book[7]))
            self.isbn.setText(str(book[8]))
            self.copies.setText(str(book[9]))
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.button(QDialogButtonBox.Ok).setText("Valider")
        self.buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        self.buttons.setStyleSheet("""
            QDialogButtonBox QPushButton {
                background-color: #388E3C;
                color: white;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 14px;
                min-width: 100px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #2E7D32;
            }
        """)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        return (
            self.title.text(),
            self.entry_date.text(),
            self.inventory_number.text(),
            self.cote.text(),
            self.author.text(),
            self.edition.text(),
            self.category.text(),
            self.isbn.text(),
            self.copies.text()
        )
