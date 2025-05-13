from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget,
    QStackedWidget, QListWidgetItem, QTableWidget, QTableWidgetItem, QSizePolicy, QSplitter, QLineEdit, QPushButton
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QSize

class StudentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Espace Étudiant")
        self.setGeometry(250, 120, 1000, 650)
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
        self.sidebar.setMaximumWidth(350)
        self.sidebar.setFont(QFont("Segoe UI", 13, QFont.Bold))
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
                padding: 16px 10px;
                margin-bottom: 6px;
                border-radius: 10px;
                color: #ececec;
            }
            QListWidget::item:selected {
                background: #388E3C;
                color: #fff;
                border-left: 6px solid #66BB6A;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background: #2E7D32;
                color: #fff;
            }
        """)
        dashboard_item = QListWidgetItem(QIcon("src/assets/icon.png"), "  Tableau de bord")
        books_item = QListWidgetItem("  Livres disponibles")
        my_loans_item = QListWidgetItem("  Mes emprunts")
        history_item = QListWidgetItem("  Historique")
        for item in [dashboard_item, books_item, my_loans_item, history_item]:
            item.setSizeHint(QSize(200, 44))
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
        dash_title = QLabel("Bienvenue dans votre espace étudiant")
        dash_title.setFont(QFont("Arial", 20, QFont.Bold))
        dash_title.setAlignment(Qt.AlignCenter)
        dash_layout.addWidget(dash_title)
        dash_layout.addStretch()
        self.pages.addWidget(dashboard_page)

        # Books Page with pretty search
        books_page = QWidget()
        books_layout = QVBoxLayout()
        books_page.setLayout(books_layout)
        books_title = QLabel("Livres disponibles")
        books_title.setFont(QFont("Arial", 16, QFont.Bold))
        books_layout.addWidget(books_title)

        # Pretty Search bar
        search_bar = QWidget()
        search_bar_layout = QHBoxLayout()
        search_bar_layout.setContentsMargins(0, 0, 0, 0)
        search_bar.setLayout(search_bar_layout)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Rechercher par titre, auteur ou catégorie...")
        self.search_input.setFont(QFont("Arial", 12))
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 16px;
                border: 2px solid #388E3C;
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
        search_btn = QPushButton("Rechercher")
        search_btn.setFont(QFont("Arial", 12, QFont.Bold))
        search_btn.setCursor(Qt.PointingHandCursor)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #388E3C;
                color: white;
                border-radius: 18px;
                padding: 8px 24px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #2E7D32;
            }
        """)
        search_btn.clicked.connect(self.search_books)
        search_bar_layout.addStretch()
        search_bar_layout.addWidget(self.search_input)
        search_bar_layout.addWidget(search_btn)
        search_bar_layout.addStretch()
        books_layout.addWidget(search_bar)

        self.books_table = QTableWidget(3, 5)
        self.books_table.setHorizontalHeaderLabels(["ID", "Titre", "Auteur", "Catégorie", "Disponibles"])
        self.books_data = [
            [1, "Les Misérables", "Victor Hugo", "Roman", 3],
            [2, "Relativité", "Albert Einstein", "Science", 1],
            [3, "Vingt mille lieues sous les mers", "Jules Verne", "Roman", 2]
        ]
        self.refresh_books_table()
        self.books_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        books_layout.addWidget(self.books_table)
        self.pages.addWidget(books_page)

        # My Loans Page
        my_loans_page = QWidget()
        my_loans_layout = QVBoxLayout()
        my_loans_page.setLayout(my_loans_layout)
        my_loans_title = QLabel("Mes emprunts en cours")
        my_loans_title.setFont(QFont("Arial", 16, QFont.Bold))
        my_loans_layout.addWidget(my_loans_title)
        my_loans_table = QTableWidget(2, 4)
        my_loans_table.setHorizontalHeaderLabels(["ID Emprunt", "Livre", "Emprunté le", "Statut"])
        dummy_loans = [
            [1, "Les Misérables", "2024-05-01", "En cours"],
            [2, "Relativité", "2024-05-10", "En cours"]
        ]
        for row, loan in enumerate(dummy_loans):
            for col, value in enumerate(loan):
                my_loans_table.setItem(row, col, QTableWidgetItem(str(value)))
        my_loans_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        my_loans_layout.addWidget(my_loans_table)
        self.pages.addWidget(my_loans_page)

        # History Page
        history_page = QWidget()
        history_layout = QVBoxLayout()
        history_page.setLayout(history_layout)
        history_title = QLabel("Historique de mes emprunts")
        history_title.setFont(QFont("Arial", 16, QFont.Bold))
        history_layout.addWidget(history_title)
        history_table = QTableWidget(2, 5)
        history_table.setHorizontalHeaderLabels(["ID Emprunt", "Livre", "Emprunté le", "Rendu le", "Statut"])
        dummy_history = [
            [1, "Les Misérables", "2024-04-01", "2024-04-10", "Rendu"],
            [2, "Vingt mille lieues sous les mers", "2024-03-10", "2024-03-20", "Rendu"]
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
            QHeaderView::section { background: #388E3C; color: #fff; font-weight: bold; }
        """)

    def refresh_books_table(self, filtered=None):
        data = filtered if filtered is not None else self.books_data
        self.books_table.setRowCount(len(data))
        for row, book in enumerate(data):
            for col, value in enumerate(book):
                self.books_table.setItem(row, col, QTableWidgetItem(str(value)))

    def search_books(self):
        text = self.search_input.text().lower()
        if not text:
            self.refresh_books_table()
            return
        filtered = [
            book for book in self.books_data
            if text in str(book[1]).lower() or text in str(book[2]).lower() or text in str(book[3]).lower()
        ]
        self.refresh_books_table(filtered)