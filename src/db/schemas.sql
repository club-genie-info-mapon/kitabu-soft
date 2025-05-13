-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL,
    user_type TEXT CHECK(user_type IN ('librarian', 'academic', 'student')) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
-- commentary

-- Table des auteurs
CREATE TABLE auteurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL
);


-- Table des catégories
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT UNIQUE NOT NULL
);

-- Table de liaison entre auteurs et ouvrages
CREATE TABLE auteurs_ouvrages (
    auteur_id INTEGER NOT NULL,
    ouvrage_id INTEGER NOT NULL,
    PRIMARY KEY (auteur_id, ouvrage_id),
    FOREIGN KEY (auteur_id) REFERENCES auteurs(id),
    FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id)
);

-- Table de liaison entre ouvrages et catégories
CREATE TABLE ouvrages_categories (
    ouvrage_id INTEGER NOT NULL,
    categorie_id INTEGER NOT NULL,
    PRIMARY KEY (ouvrage_id, categorie_id),
    FOREIGN KEY (ouvrage_id) REFERENCES ouvrages(id),
    FOREIGN KEY (categorie_id) REFERENCES categories(id)
);

-- Table de liaison entre auteurs et catégories
CREATE TABLE auteurs_categories (
    auteur_id INTEGER NOT NULL,
    categorie_id INTEGER NOT NULL,
    PRIMARY KEY (auteur_id, categorie_id),
    FOREIGN KEY (auteur_id) REFERENCES auteurs(id),
    FOREIGN KEY (categorie_id) REFERENCES categories(id)
);

-- Table des ouvrages
CREATE TABLE ouvrages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_inventaire TEXT UNIQUE NOT NULL,
    cote TEXT NOT NULL,
    intitule TEXT NOT NULL,
    edition TEXT,
    total_copies INTEGER DEFAULT 1,
    copies_disponibles INTEGER DEFAULT 1
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
 