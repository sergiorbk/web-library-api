from src.db.repositories.book_repository import BookRepository


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.__book_repository = book_repository
