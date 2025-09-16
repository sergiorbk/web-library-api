import datetime
import uuid

from pydantic import BaseModel


class BookCheckoutSchema(BaseModel):
    checkout_id: uuid.UUID
    book_id: uuid.UUID
    client_id: uuid.UUID
    checkout_date: datetime.date
    expiration_date: datetime.date

