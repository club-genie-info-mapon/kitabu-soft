-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    user_type TEXT CHECK(user_type IN ('librarian', 'academic', 'student')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Books table
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
    available_copies INTEGER DEFAULT 1,
);

-- Book loans table (history of all borrowings)
CREATE TABLE book_loans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('borrowed', 'returned')) NOT NULL DEFAULT 'borrowed',
    borrowed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    returned_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
);

-- Index for quick lookup of active loans
CREATE INDEX idx_book_loans_active ON book_loans(user_id, book_id, returned_at);
 