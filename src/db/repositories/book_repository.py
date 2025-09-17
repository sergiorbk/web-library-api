import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from src.db.models.orm_book import Book


class BookRepository:
    def __init__(self, db_session: Session):
        self.__db = db_session

    def create(self, book: Book) -> Book:
        self.__db.add(book)
        self.__db.commit()
        self.__db.refresh(book)
        return book

    def get_by_id(self, book_id: uuid.UUID) -> Optional[Book]:
        return self.__db.get(Book, book_id)

    def get_all(self) -> List[Book]:
        return self.__db.query(Book).all()

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        return self.__db.query(Book).filter(Book.isbn == isbn).first()

    def update(self, book_id: uuid.UUID, **kwargs) -> Optional[Book]:
        book = self.get_by_id(book_id)
        if not book:
            return None

        for key, value in kwargs.items():
            if hasattr(book, key) and value is not None:
                setattr(book, key, value)

        self.__db.commit()
        self.__db.refresh(book)
        return book

    def delete_by_id(self, book_id: uuid.UUID) -> bool:
        book = self.get_by_id(book_id)
        if not book:
            return False

        self.__db.delete(book)
        self.__db.commit()
        return True

    def exists_by_isbn(self, isbn: str) -> bool:
        return self.__db.query(Book).filter(Book.isbn == isbn).first() is not None

    def search_by_title(self, title: str) -> List[Book]:
        return self.__db.query(Book).filter(Book.title.ilike(f"%{title}%")).all()

    def search_by_author(self, author: str) -> List[Book]:
        return self.__db.query(Book).filter(Book.author.ilike(f"%{author}%")).all()