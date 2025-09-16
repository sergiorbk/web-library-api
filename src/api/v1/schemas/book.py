import uuid

from pydantic import BaseModel


class BookSchema(BaseModel):
    book_id: uuid.UUID
    title: str
    author: str
    isbn: str
