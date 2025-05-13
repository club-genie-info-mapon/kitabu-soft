from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QStackedWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QSizePolicy, QSplitter,
    QPushButton, QLineEdit, QMessageBox, QDialog, QFormLayout, QComboBox, QDialogButtonBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class UserDialog(QDialog):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.setWindowTitle("Utilisateur" if user is None else "Modifier utilisateur")
        self.setMinimumWidth(350)
        layout = QFormLayout(self)
        self.username = QLineEdit()
        self.password = QLineEdit()
        self.full_name = QLineEdit()
        self.user_type = QComboBox()
        self.user_type.addItems(["librarian", "academic", "student"])
        layout.addRow("Nom d'utilisateur:", self.username)
        layout.addRow("Mot de passe:", self.password)
        layout.addRow("Nom complet:", self.full_name)
        layout.addRow("Type:", self.user_type)
        if user:
            self.username.setText(user[1])
            self.password.setText(user[2])
            self.full_name.setText(user[3])
            self.user_type.setCurrentText(user[4])
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        return (
            self.username.text(),
            self.password.text(),
            self.full_name.text(),
            self.user_type.currentText()
        )

class BookDialog(QDialog):
    def __init__(self, parent=None, book=None):
        super().__init__(parent)
        self.setWindowTitle("Livre" if book is None else "Modifier livre")
        self.setMinimumWidth(350)
        layout = QFormLayout(self)
        self.title = QLineEdit()
        self.author = QLineEdit()
        self.category = QLineEdit()
        self.isbn = QLineEdit()
        self.copies = QLineEdit()
        layout.addRow("Titre:", self.title)
        layout.addRow("Auteur:", self.author)
        layout.addRow("Catégorie:", self.category)
        layout.addRow("ISBN:", self.isbn)
        layout.addRow("Exemplaires:", self.copies)
        if book:
            self.title.setText(book[1])
            self.author.setText(book[2])
            self.category.setText(book[3])
            self.isbn.setText(book[4])
            self.copies.setText(str(book[5]))
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        layout.addWidget(self.buttons)

    def get_data(self):
        return (
            self.title.text(),
            self.author.text(),
            self.category.text(),
            self.isbn.text(),
            self.copies.text()
        )

class LibrarianWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Bibliothécaire")
        self.setGeometry(200, 100, 1100, 700)
        self.setWindowIcon(QIcon("src/assets/icon.png"))

        # Main widget and splitter
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setMinimumWidth(120)
        self.sidebar.setMaximumWidth(400)
        self.sidebar.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.sidebar.setSpacing(8)
        self.sidebar.setStyleSheet("""
            QListWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #232526, stop:1 #414345);
                color: #fff;
                border: none;
                padding-top: 30px;
            }
            QListWidget::item {
                background: transparent;
                padding: 18px 10px;
                margin-bottom: 6px;
                border-radius: 12px;
                color: #ececec;
            }
            QListWidget::item:selected {
                background: #1976D2;
                color: #fff;
                border-left: 6px solid #42A5F5;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background: #1565C0;
                color: #fff;
            }
        """)
        dashboard_item = QListWidgetItem(QIcon("src/assets/icon.png"), "  Tableau de bord")
        users_item = QListWidgetItem("  Utilisateurs")
        books_item = QListWidgetItem("  Livres")
        loans_item = QListWidgetItem("  Emprunts actifs")
        history_item = QListWidgetItem("  Historique des prêts")
        for item in [dashboard_item, users_item, books_item, loans_item, history_item]:
            item.setSizeHint(QSize(220, 48))
            self.sidebar.addItem(item)
        splitter.addWidget(self.sidebar)
        splitter.setStretchFactor(0, 0)

        # Stacked widget for pages
        self.pages = QStackedWidget()
        splitter.addWidget(self.pages)
        splitter.setStretchFactor(1, 1)

        # Dashboard Page
        dashboard_page = QWidget()
        dash_layout = QVBoxLayout()
        dashboard_page.setLayout(dash_layout)
        dash_title = QLabel("Bienvenue dans l'espace Bibliothécaire")
        dash_title.setFont(QFont("Arial", 22, QFont.Bold))
        dash_title.setAlignment(Qt.AlignCenter)
        dash_layout.addWidget(dash_title)
        dash_layout.addStretch()
        self.pages.addWidget(dashboard_page)

        # Users Page with CRUD
        users_page = QWidget()
        users_layout = QVBoxLayout()
        users_page.setLayout(users_layout)
        users_title = QLabel("Liste des utilisateurs")
        users_title.setFont(QFont("Arial", 18, QFont.Bold))
        users_layout.addWidget(users_title)
        self.users_table = QTableWidget(3, 5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur", "Mot de passe", "Nom complet", "Type"])
        self.users_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        users_layout.addWidget(self.users_table)
        # Dummy data
        self.users_data = [
            [1, "admin", "admin", "Administrateur", "librarian"],
            [2, "alice", "password123", "Alice Dupont", "academic"],
            [3, "bob", "password456", "Bob Martin", "student"]
        ]
        self.refresh_users_table()
        # CRUD Buttons
        crud_layout = QHBoxLayout()
        btn_add_user = QPushButton("Ajouter")
        btn_edit_user = QPushButton("Modifier")
        btn_delete_user = QPushButton("Supprimer")
        for btn in [btn_add_user, btn_edit_user, btn_delete_user]:
            btn.setFont(QFont("Arial", 11))
            btn.setMinimumWidth(100)
            crud_layout.addWidget(btn)
        users_layout.addLayout(crud_layout)
        btn_add_user.clicked.connect(self.add_user)
        btn_edit_user.clicked.connect(self.edit_user)
        btn_delete_user.clicked.connect(self.delete_user)
        self.pages.addWidget(users_page)

        # Books Page with CRUD
        books_page = QWidget()
        books_layout = QVBoxLayout()
        books_page.setLayout(books_layout)
        books_title = QLabel("Liste des livres")
        books_title.setFont(QFont("Arial", 18, QFont.Bold))
        books_layout.addWidget(books_title)
        self.books_table = QTableWidget(3, 6)
        self.books_table.setHorizontalHeaderLabels(["ID", "Titre", "Auteur", "Catégorie", "ISBN", "Disponibles"])
        self.books_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        books_layout.addWidget(self.books_table)
        # Dummy data
        self.books_data = [
            [1, "Les Misérables", "Victor Hugo", "Roman", "9782070409189", 3],
            [2, "Relativité", "Albert Einstein", "Science", "9782012792412", 1],
            [3, "Vingt mille lieues sous les mers", "Jules Verne", "Roman", "9782253006329", 2]
        ]
        self.refresh_books_table()
        # CRUD Buttons
        crud_books_layout = QHBoxLayout()
        btn_add_book = QPushButton("Ajouter")
        btn_edit_book = QPushButton("Modifier")
        btn_delete_book = QPushButton("Supprimer")
        for btn in [btn_add_book, btn_edit_book, btn_delete_book]:
            btn.setFont(QFont("Arial", 11))
            btn.setMinimumWidth(100)
            crud_books_layout.addWidget(btn)
        books_layout.addLayout(crud_books_layout)
        btn_add_book.clicked.connect(self.add_book)
        btn_edit_book.clicked.connect(self.edit_book)
        btn_delete_book.clicked.connect(self.delete_book)
        self.pages.addWidget(books_page)

        # Active Loans Page
        loans_page = QWidget()
        loans_layout = QVBoxLayout()
        loans_page.setLayout(loans_layout)
        loans_title = QLabel("Emprunts actifs")
        loans_title.setFont(QFont("Arial", 18, QFont.Bold))
        loans_layout.addWidget(loans_title)
        loans_table = QTableWidget(2, 5)
        loans_table.setHorizontalHeaderLabels(["ID Emprunt", "Utilisateur", "Livre", "Emprunté le", "Statut"])
        dummy_loans = [
            [1, "bob", "Les Misérables", "2024-05-01", "En cours"],
            [2, "alice", "Relativité", "2024-05-10", "En cours"]
        ]
        for row, loan in enumerate(dummy_loans):
            for col, value in enumerate(loan):
                loans_table.setItem(row, col, QTableWidgetItem(str(value)))
        loans_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        loans_layout.addWidget(loans_table)
        self.pages.addWidget(loans_page)

        # Loan History Page
        history_page = QWidget()
        history_layout = QVBoxLayout()
        history_page.setLayout(history_layout)
        history_title = QLabel("Historique des prêts")
        history_title.setFont(QFont("Arial", 18, QFont.Bold))
        history_layout.addWidget(history_title)
        history_table = QTableWidget(3, 6)
        history_table.setHorizontalHeaderLabels(["ID Emprunt", "Utilisateur", "Livre", "Emprunté le", "Rendu le", "Statut"])
        dummy_history = [
            [1, "bob", "Les Misérables", "2024-04-01", "2024-04-10", "Rendu"],
            [2, "alice", "Relativité", "2024-03-10", "2024-03-20", "Rendu"],
            [3, "bob", "Vingt mille lieues sous les mers", "2024-02-01", "2024-02-15", "Rendu"]
        ]
        for row, hist in enumerate(dummy_history):
            for col, value in enumerate(hist):
                history_table.setItem(row, col, QTableWidgetItem(str(value)))
        history_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        history_layout.addWidget(history_table)
        self.pages.addWidget(history_page)

        # Sidebar navigation
        self.sidebar.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

        self.setStyleSheet("""
            QMainWindow { background-color: #f5f5f5; }
            QLabel { color: #263238; }
            QTableWidget { background: #fff; border: 1px solid #bdbdbd; border-radius: 6px; }
            QHeaderView::section { background: #1976D2; color: #fff; font-weight: bold; }
        """)

    # --- User CRUD ---
    def refresh_users_table(self):
        self.users_table.setRowCount(len(self.users_data))
        for row, user in enumerate(self.users_data):
            for col, value in enumerate(user):
                self.users_table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_id = max([u[0] for u in self.users_data]) + 1 if self.users_data else 1
            username, password, full_name, user_type = dialog.get_data()
            self.users_data.append([new_id, username, password, full_name, user_type])
            self.refresh_users_table()

    def edit_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un utilisateur à modifier.")
            return
        user = self.users_data[row]
        dialog = UserDialog(self, user)
        if dialog.exec_() == QDialog.Accepted:
            username, password, full_name, user_type = dialog.get_data()
            self.users_data[row] = [user[0], username, password, full_name, user_type]
            self.refresh_users_table()

    def delete_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un utilisateur à supprimer.")
            return
        del self.users_data[row]
        self.refresh_users_table()

    # --- Book CRUD ---
    def refresh_books_table(self):
        self.books_table.setRowCount(len(self.books_data))
        for row, book in enumerate(self.books_data):
            for col, value in enumerate(book):
                self.books_table.setItem(row, col, QTableWidgetItem(str(value)))

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            new_id = max([b[0] for b in self.books_data]) + 1 if self.books_data else 1
            title, author, category, isbn, copies = dialog.get_data()
            self.books_data.append([new_id, title, author, category, isbn, int(copies)])
            self.refresh_books_table()

    def edit_book(self):
        row = self.books_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un livre à modifier.")
            return
        book = self.books_data[row]
        dialog = BookDialog(self, book)
        if dialog.exec_() == QDialog.Accepted:
            title, author, category, isbn, copies = dialog.get_data()
            self.books_data[row] = [book[0], title, author, category, isbn, int(copies)]
            self.refresh_books_table()

    def delete_book(self):
        row = self.books_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un livre à supprimer.")
            return
        del self.books_data[row]
        self.refresh_books_table()