import sqlite3
import os
import csv
from src.utils.helpers import resource_path

DB_PATH = os.path.join(os.path.dirname(__file__), 'library.db')

def create_tables(cursor):
    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            faculty TEXT,
            class TEXT,
            user_type TEXT CHECK(user_type IN ('librarian', 'academic', 'student')) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Books table
    cursor.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            entry_date DATE,
            inventory_number TEXT NOT NULL,
            cote TEXT NOT NULL,
            authors TEXT NOT NULL,
            title TEXT NOT NULL,
            edition TEXT,
            categories TEXT,
            isbn TEXT UNIQUE,
            total_copies INTEGER DEFAULT 1,
            available_copies INTEGER DEFAULT 1
        );
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

def get_books():
    file_path = resource_path(os.path.join('src', 'db', 'final.csv'))

    with open(file_path, 'r') as file:
        lines = file.readlines()
        data = csv.reader(lines, delimiter=';')
        books={}
        for row in data:
            book = {}
            book['entry_date']=row[0]
            book['inventory_number']=row[1]
            book['cote']=row[2]
            book['authors']=row[3]
            book['title']=row[4]
            book['edition']=row[5]
            book['categories']=row[6]
            book['total_copies']= books.get(row[4], {}).get('total_copies', 0) + 1
            books[row[4]] = book
    return list(books.values())

def seed():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create tables if not exist
    create_tables(cursor)

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
    books = get_books()
    books = books[1:]

    cursor.executemany(
        """INSERT OR IGNORE INTO books
            (entry_date, inventory_number, cote, authors, title, edition, categories, total_copies, available_copies)
            VALUES 
        (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        [(book['entry_date'], book['inventory_number'], book['cote'], book['authors'], book['title'],
          book['edition'], book['categories'], book['total_copies'], book['total_copies']) for book in books]
    )

    conn.commit()
    conn.close()
    print("Database created and seeded successfully.")

if __name__ == "__main__":
    seed()