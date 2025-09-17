import datetime
import uuid
from typing import Optional

from pydantic import BaseModel


class BookCheckoutSchema(BaseModel):
    checkout_id: uuid.UUID
    book_id: uuid.UUID
    client_id: uuid.UUID
    checkout_date: datetime.datetime
    expiration_date: datetime.datetime


class CreateCheckoutRequest(BaseModel):
    book_id: uuid.UUID
    client_id: uuid.UUID
    checkout_date: datetime.datetime
    expiration_date: datetime.datetime


class UpdateCheckoutRequest(BaseModel):
    expiration_date: Optional[datetime.datetime] = None


class ExtendCheckoutRequest(BaseModel):
    days_to_extend: int = 7


class CheckoutSearchRequest(BaseModel):
    client_id: Optional[uuid.UUID] = None
    book_id: Optional[uuid.UUID] = None
    start_date: Optional[datetime.datetime] = None
    end_date: Optional[datetime.datetime] = None
    active_only: bool = False
    expired_only: bool = False

