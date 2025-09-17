from src.db.models.orm_book import Book
from src.schemas.book import BookSchema, CreateBookRequest


def map_book_orm_to_schema(book: Book) -> BookSchema:
    """Map Book ORM model to BookSchema"""
    return BookSchema(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        isbn=book.isbn
    )


def map_create_request_to_orm(request: CreateBookRequest) -> Book:
    """Map CreateBookRequest to Book ORM model"""
    return Book(
        title=request.title,
        author=request.author,
        isbn=request.isbn
    )