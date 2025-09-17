import uuid
from typing import Optional

from pydantic import BaseModel


class BookSchema(BaseModel):
    book_id: uuid.UUID
    title: str
    author: str
    isbn: str


class CreateBookRequest(BaseModel):
    title: str
    author: str
    isbn: str


class UpdateBookRequest(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
