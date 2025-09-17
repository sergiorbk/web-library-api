import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class ClientSchema(BaseModel):
    client_id: uuid.UUID
    user_id: uuid.UUID
    email: EmailStr
    name: str
    surname: str
    patronymic: Optional[str] = None
    birthdate: datetime.date


class CreateClientRequest(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    name: str
    surname: str
    patronymic: Optional[str] = None
    birthdate: datetime.date


class UpdateClientRequest(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    birthdate: Optional[datetime.date] = None


class ClientSearchRequest(BaseModel):
    name: Optional[str] = None
    start_birthdate: Optional[datetime.date] = None
    end_birthdate: Optional[datetime.date] = None