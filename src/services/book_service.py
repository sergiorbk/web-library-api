import uuid
from typing import List, Optional

from src.db.repositories.book_repository import BookRepository
from src.exceptions.book_exceptions import BookNotFoundException, BookAlreadyExistsException, InvalidISBNException
from src.mappers.book_mappers import map_book_orm_to_schema, map_create_request_to_orm
from src.schemas.book import BookSchema, CreateBookRequest, UpdateBookRequest


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.__book_repository = book_repository

    def create_book(self, request: CreateBookRequest) -> BookSchema:
        """Create a new book"""
        # Check if book with same ISBN already exists
        if self.__book_repository.exists_by_isbn(request.isbn):
            raise BookAlreadyExistsException(f"Book with ISBN {request.isbn} already exists")

        # Validate ISBN format (basic validation)
        if not self._is_valid_isbn(request.isbn):
            raise InvalidISBNException(f"Invalid ISBN format: {request.isbn}")

        book_orm = map_create_request_to_orm(request)
        created_book = self.__book_repository.create(book_orm)
        return map_book_orm_to_schema(created_book)

    def get_all_books(self) -> List[BookSchema]:
        """Get all books"""
        books = self.__book_repository.get_all()
        return [map_book_orm_to_schema(book) for book in books]

    def get_book_by_id(self, book_id: uuid.UUID) -> Optional[BookSchema]:
        """Get book by ID"""
        book = self.__book_repository.get_by_id(book_id)
        if not book:
            return None
        return map_book_orm_to_schema(book)

    def get_book_by_isbn(self, isbn: str) -> Optional[BookSchema]:
        """Get book by ISBN"""
        book = self.__book_repository.get_by_isbn(isbn)
        if not book:
            return None
        return map_book_orm_to_schema(book)

    def search_books_by_title(self, title: str) -> List[BookSchema]:
        """Search books by title"""
        books = self.__book_repository.search_by_title(title)
        return [map_book_orm_to_schema(book) for book in books]

    def search_books_by_author(self, author: str) -> List[BookSchema]:
        """Search books by author"""
        books = self.__book_repository.search_by_author(author)
        return [map_book_orm_to_schema(book) for book in books]

    def update_book(self, book_id: uuid.UUID, request: UpdateBookRequest) -> Optional[BookSchema]:
        """Update book"""
        if not self.__book_repository.get_by_id(book_id):
            raise BookNotFoundException(f"Book with ID {book_id} not found")

        # Check if ISBN is being changed and if it already exists
        if request.isbn:
            existing_book = self.__book_repository.get_by_isbn(request.isbn)
            if existing_book and existing_book.book_id != book_id:
                raise BookAlreadyExistsException(f"Book with ISBN {request.isbn} already exists")

            # Validate new ISBN format
            if not self._is_valid_isbn(request.isbn):
                raise InvalidISBNException(f"Invalid ISBN format: {request.isbn}")

        update_data = {}
        if request.title is not None:
            update_data['title'] = request.title
        if request.author is not None:
            update_data['author'] = request.author
        if request.isbn is not None:
            update_data['isbn'] = request.isbn

        updated_book = self.__book_repository.update(book_id, **update_data)
        if not updated_book:
            return None
        return map_book_orm_to_schema(updated_book)

    def delete_book(self, book_id: uuid.UUID) -> bool:
        """Delete book"""
        if not self.__book_repository.get_by_id(book_id):
            raise BookNotFoundException(f"Book with ID {book_id} not found")

        return self.__book_repository.delete_by_id(book_id)

    def _is_valid_isbn(self, isbn: str) -> bool:
        """Basic ISBN validation"""
        # Remove hyphens and spaces
        isbn = isbn.replace('-', '').replace(' ', '')

        # Check if it's ISBN-10 or ISBN-13
        if len(isbn) == 10:
            return isbn[:-1].isdigit() and (isbn[-1].isdigit() or isbn[-1].upper() == 'X')
        elif len(isbn) == 13:
            return isbn.isdigit()

        return False

