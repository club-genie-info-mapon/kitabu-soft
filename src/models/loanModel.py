from src.models.baseModel import BaseModel

class LoanModel(BaseModel):
    """
    Model for book loan operations using the database context (strategy pattern).
    """
    def __init__(self, db_context):
        self.db = db_context

    def create(self, user_id, book_id):
        """
        Create a new book loan (borrow a book).
        """
        query = """
            INSERT INTO book_loans (user_id, book_id)
            VALUES (%s, %s)
        """
        params = (user_id, book_id)
        self.db.execute(query, params)
        self.db.commit()

    def return_book(self, loan_id):
        """
        Mark a book as returned by setting the returned_at timestamp.
        """
        query = """
            UPDATE book_loans
            SET returned_at = CURRENT_TIMESTAMP
            WHERE id = %s AND returned_at IS NULL
        """
        self.db.execute(query, (loan_id,))
        self.db.commit()

    def get_active_loans_by_user(self, user_id):
        """
        Get all currently borrowed books for a user.
        """
        query = """
            SELECT * FROM book_loans
            WHERE user_id = %s AND returned_at IS NULL
        """
        self.db.execute(query, (user_id,))
        return self.db.fetchall()

    def get_loan_history_by_user(self, user_id):
        """
        Get the loan history for a user.
        """
        query = """
            SELECT * FROM book_loans
            WHERE user_id = %s
            ORDER BY borrowed_at DESC
        """
        self.db.execute(query, (user_id,))
        return self.db.fetchall()

    def get_active_loans(self):
        """
        Get all currently borrowed books (not yet returned).
        """
        query = """
            SELECT * FROM book_loans
            WHERE returned_at IS NULL
        """
        self.db.execute(query)
        return self.db.fetchall()

    def get_by_id(self, loan_id):
        """
        Get a loan record by its ID.
        """
        query = "SELECT * FROM book_loans WHERE id = %s"
        self.db.execute(query, (loan_id,))
        return self.db.fetchone()