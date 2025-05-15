from src.models.bookModel import BookModel


class BookController:
    def __init__(self, book_model:BookModel):
        self.book_model = book_model
    def get_all_books(self):
        return self.book_model.get_all()

    def get_book_by_id(self, book_id):
        return self.book_model.get_book_by_id(book_id)

    def add_book(self, book_data):
        return self.book_model.create(*book_data)

    def update_book(self, book_id, book_data):
        return self.book_model.update_book(book_id, book_data)

    def delete_book(self, book_id):
        return self.book_model.delete_book(book_id)