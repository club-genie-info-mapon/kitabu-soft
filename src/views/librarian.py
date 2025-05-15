from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QStackedWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QSizePolicy, QSplitter,
    QPushButton, QLineEdit, QMessageBox, QDialog
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize
import os
from src.controllers.userController import UserController
from src.models.userModel import UserModel
from src.utils.helpers import resource_path
from src.db.strategies import SQLiteStrategy
from src.controllers.bookController import BookController
from src.models.bookModel import BookModel
from src.views.dialogs.bookDialog import BookDialog
from src.views.dialogs.userDialog import UserDialog


class LibrarianWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Bibliothécaire")
        self.setGeometry(200, 100, 1100, 700)
        self.setWindowIcon(QIcon("src/assets/icon.png"))

        # Strategies, Models and Controllers
        strategy  = SQLiteStrategy(resource_path(os.path.join("src", "db", "library.db")))
        
        userModel = UserModel(strategy)
        self.userController = UserController(userModel)

        bookModel = BookModel(strategy)
        self.bookController = BookController(bookModel)

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
        self.users_table = QTableWidget(3, 7)
        self.users_table.setHorizontalHeaderLabels(["ID", "Nom d'utilisateur", "Mot de passe", "Nom complet","Faculté","Promotion","Type"])
        self.users_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        users_layout.addWidget(self.users_table)
        
        users = self.userController.get_all_users()
        self.users_data = [[user[0], user[1], user[2], user[3], user[4],user[5],user[6]] for user in users]

        self.refresh_users_table()
        # CRUD Buttons
        crud_layout = QHBoxLayout()
        btn_add_user = QPushButton("Ajouter")
        btn_edit_user = QPushButton("Modifier")
        btn_delete_user = QPushButton("Supprimer")
        for btn, color in zip(
            [btn_add_user, btn_edit_user, btn_delete_user],
            ["#1976D2", "#FFA000", "#D32F2F"]
        ):
            btn.setFont(QFont("Arial", 12, QFont.Bold))
            btn.setMinimumWidth(120)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 8px;
                    padding: 10px 24px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: #1565C0 if {color} == "#1976D2" else "#FFB300" if {color} == "#FFA000" else "#B71C1C";
                }}
            """)
            crud_layout.addWidget(btn)
        users_layout.addLayout(crud_layout)
        btn_add_user.clicked.connect(self.add_user)
        btn_edit_user.clicked.connect(self.edit_user)
        btn_delete_user.clicked.connect(self.delete_user)
        self.pages.addWidget(users_page)

        # Books Page with CRUD and search
        books_page = QWidget()
        books_layout = QVBoxLayout()
        books_page.setLayout(books_layout)
        books_title = QLabel("Liste des livres")
        books_title.setFont(QFont("Arial", 18, QFont.Bold))
        books_layout.addWidget(books_title)

        # --- Search zone ---
        search_layout = QHBoxLayout()
        self.book_search_input = QLineEdit()
        self.book_search_input.setPlaceholderText("🔍 Rechercher par titre, auteur, catégorie ou ISBN...")
        self.book_search_input.setFont(QFont("Arial", 12))
        self.book_search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 16px;
                border: 2px solid #1976D2;
                border-radius: 18px;
                background: #f9f9f9;
                font-size: 14px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 2px solid #1976D2;
                background: #fff;
            }
        """)
        book_search_btn = QPushButton("Rechercher")
        book_search_btn.setFont(QFont("Arial", 12, QFont.Bold))
        book_search_btn.setCursor(Qt.PointingHandCursor)
        book_search_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976D2;
                color: white;
                border-radius: 18px;
                padding: 8px 24px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #0461f7;
            }
        """)
        book_search_btn.clicked.connect(self.search_books)
        search_layout.addStretch()
        search_layout.addWidget(self.book_search_input)
        search_layout.addWidget(book_search_btn)
        search_layout.addStretch()
        books_layout.addLayout(search_layout)

        # --- Table with details button ---
        self.books_table = QTableWidget(0, 12)
        self.books_table.setHorizontalHeaderLabels([
            "ID", "Date d'entrée", "N. Inventaire", "Côte", "Auteur", "Titre", "Edition", "Catégorie", "ISBN", "Total","Disponibles", "Détails"
        ])
        self.books_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.books_table.setFont(QFont("Arial", 10))
        self.books_table.horizontalHeader().setFont(QFont("Arial", 10, QFont.Bold))
        self.books_table.verticalHeader().setDefaultSectionSize(40)
        books_layout.addWidget(self.books_table)

        # Load books from controller
        self.books_data = self.bookController.get_all_books()
        self.refresh_books_table()

        # CRUD Buttons
        crud_books_layout = QHBoxLayout()
        btn_add_book = QPushButton("Ajouter")
        btn_edit_book = QPushButton("Modifier")
        btn_delete_book = QPushButton("Supprimer")
        for btn, color in zip(
            [btn_add_book, btn_edit_book, btn_delete_book],
            ["#1976D2", "#FFA000", "#D32F2F"]
        ):
            btn.setFont(QFont("Arial", 12, QFont.Bold))
            btn.setMinimumWidth(120)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border-radius: 8px;
                    padding: 10px 24px;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: #2E7D32 if {color} == "#1976D2" else "#FFB300" if {color} == "#FFA000" else "#B71C1C";
                }}
            """)
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
            username, password, full_name, faculty,class_,user_type = dialog.get_data()
            # verify data are not empty
            if not (username and password and full_name and user_type):
                QMessageBox.warning(self, "Données vides", "Veuillez remplir tous les champs")
                return
            self.userController.create_user(username, password, full_name, faculty, class_, user_type)
            # Refresh User table to populate the new inserted user
            self.users_data = self.userController.get_all_users()
            self.refresh_users_table()

    def edit_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un utilisateur à modifier.")
            return
        user = self.users_data[row]
        dialog = UserDialog(self, user)
        if dialog.exec_() == QDialog.Accepted:
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Êtes-vous sûr de vouloir modifier cet utilisateur ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                username, password, full_name, faculty, class_, user_type = dialog.get_data()
                user_id = user[0]
                data = {
                    'username': username,
                    'password': password,
                    'full_name': full_name,
                    'faculty': faculty,
                    'class': class_,
                    'user_type': user_type
                }
                self.userController.update_user(user_id, data)
                self.users_data = self.userController.get_all_users()
                self.refresh_users_table()

    def delete_user(self):
        row = self.users_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un utilisateur à supprimer.")
            return
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer cet utilisateur ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            user_id = self.users_data[row][0]
            self.userController.delete_user(user_id)
            self.users_data = self.userController.get_all_users()
            self.refresh_users_table()

    # --- Book CRUD ---
    def refresh_books_table(self, filtered=None):
        data = filtered if filtered is not None else self.books_data
        self.books_table.setRowCount(len(data))
        for row, book in enumerate(data):
            for col, value in enumerate(book):
                item = QTableWidgetItem(str(value))
                item.setFont(QFont("Arial", 10))
                self.books_table.setItem(row, col, item)
            # Add "Détails" button
            btn = QPushButton("Détails")
            btn.setFont(QFont("Arial", 10, QFont.Bold))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #178afc;
                    color: white;
                    border-radius: 8px;
                    padding: 6px 18px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
            """)
            btn.clicked.connect(lambda _, b=book: self.show_book_details(b))
            self.books_table.setCellWidget(row, 11, btn)

    def add_book(self):
        dialog = BookDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            title, entry_date, inventory_number, cote, author, edition, category, isbn, copies = dialog.get_data()
            if copies.isdigit():
                self.bookController.add_book([
                    title, entry_date, inventory_number, cote, author, edition, category, isbn, copies
                ])
                self.books_data = self.bookController.get_all_books()
                self.refresh_books_table()
            else:
                QMessageBox.critical(self,
                "Echec",
                "Echec, Le nombre d'exemplaire doit être un entier")

    def edit_book(self):
        row = self.books_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un livre à modifier.")
            return
        book = self.books_data[row]
        book_id = book[0]
        dialog = BookDialog(self, book)
        if dialog.exec_() == QDialog.Accepted:
            reply = QMessageBox.question(
                self,
                "Confirmation",
                "Êtes-vous sûr de vouloir modifier cet utilisateur ?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                title, entry_date, inventory_number, cote, author, edition, category, isbn, copies = dialog.get_data()
                if copies.isdigit():
                    copies = int(copies)
                    self.bookController.update_book(book_id,{
                        'title':title, 
                        'entry_date':entry_date, 
                        'inventory_number':inventory_number, 
                        'cote':cote, 
                        'authors':author, 
                        'edition':edition, 
                        'categories':category, 
                        'isbn':isbn, 
                        'total_copies':copies
                    })
                    self.books_data = self.bookController.get_all_books()
                    self.refresh_books_table()
                else:
                    QMessageBox.critical(self, "Erreur", "Le nombre d'exemplaire doit être un entier")

    def delete_book(self):
        row = self.books_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Sélection requise", "Veuillez sélectionner un livre à supprimer.")
            return
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer ce livre ?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            book_id = self.books_data[row][0]
            self.bookController.delete_book(book_id)
            self.books_data = self.bookController.get_all_books()
            self.refresh_books_table()

    def search_books(self):
        text = self.book_search_input.text().lower()
        if not text:
            self.refresh_books_table()
            return
        filtered = [
            book for book in self.books_data
            if any(text in str(field).lower() for field in book[:5])
        ]
        self.refresh_books_table(filtered)

    def show_book_details(self, book):
        details = (
            f"<b>ID:</b> {book[0]}<br>"
            f"<b>Titre:</b> {book[1]}<br>"
            f"<b>Auteur:</b> {book[2]}<br>"
            f"<b>Catégorie:</b> {book[3]}<br>"
            f"<b>ISBN:</b> {book[4]}<br>"
            f"<b>Disponibles:</b> {book[5]}"
        )
        QMessageBox.information(self, "Détails du livre", details)