from src.db.strategies import SQLiteStrategy
from src.models.baseModel import BaseModel

class BookModel(BaseModel):
    """
    Model for book operations using the database context (strategy pattern).
    """
    def __init__(self, db_stategy:SQLiteStrategy):
        self.db = db_stategy
        self.db.connect()

    def create(self, title, author_id, category_id, isbn, total_copies=1):
        """
        Create a new book.
        """
        query = """
            INSERT INTO books (title, author_id, category_id, isbn, total_copies, available_copies)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (title, author_id, category_id, isbn, total_copies, total_copies)
        self.db.execute(query, params)
        self.db.commit()

    def get_by_id(self, book_id):
        """
        Get a book by ID.
        """
        query = "SELECT * FROM books WHERE id = %s"
        self.db.execute(query, (book_id,))
        return self.db.fetchone()

    def get_all(self):
        """
        Get all books.
        """
        query = "SELECT * FROM books"
        self.db.execute(query)
        return self.db.fetchall()

    def update(self, book_id, data):
        """
        Update book information.
        """
        fields = []
        params = []
        for key, value in data.items():
            fields.append(f"{key} = %s")
            params.append(value)
        params.append(book_id)
        query = f"UPDATE books SET {', '.join(fields)} WHERE id = %s"
        self.db.execute(query, tuple(params))
        self.db.commit()

    def delete(self, book_id):
        """
        Delete a book by ID.
        """
        query = "DELETE FROM books WHERE id = %s"
        self.db.execute(query, (book_id,))
        self.db.commit()