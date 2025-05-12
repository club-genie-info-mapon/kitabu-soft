import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'library.db')

def create_tables(cursor):
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            user_type TEXT CHECK(user_type IN ('librarian', 'academic', 'student')) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Authors table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    # Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    # Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            isbn TEXT UNIQUE,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)
    # Book loans table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            borrowed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            returned_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    """)
    # Index for quick lookup of active loans
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_book_loans_active ON book_loans(user_id, book_id, returned_at)
    """)

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables if not exist
    create_tables(cursor)

    # Insert categories
    categories = [
        ('Roman',),
        ('Science',),
        ('Histoire',),
        ('Informatique',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO categories (name) VALUES (?)", categories)

    # Insert authors
    authors = [
        ('Victor Hugo',),
        ('Jules Verne',),
        ('Albert Einstein',),
        ('Isaac Newton',)
    ]
    cursor.executemany("INSERT OR IGNORE INTO authors (name) VALUES (?)", authors)

    # Insert users
    users = [
        ('admin', 'admin', 'Administrateur', 'librarian'),
        ('alice', 'password123', 'Alice Dupont', 'academic'),
        ('bob', 'password456', 'Bob Martin', 'student')
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO users (username, password, full_name, user_type) VALUES (?, ?, ?, ?)",
        users
    )

    # Insert books
    books = [
        ('Les Misérables', 1, 1, '9782070409189', 5, 5),
        ('Vingt mille lieues sous les mers', 2, 1, '9782253006329', 3, 3),
        ('Relativité', 3, 2, '9782012792412', 2, 2),
        ('Principia Mathematica', 4, 2, '9782080702530', 1, 1)
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO books (title, author_id, category_id, isbn, total_copies, available_copies) VALUES (?, ?, ?, ?, ?, ?)",
        books
    )

    conn.commit()
    conn.close()
    print("Database created and seeded successfully.")

if __name__ == "__main__":
    seed()