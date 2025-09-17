import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr


class ClientSchema(BaseModel):
    client_id: uuid.UUID
    email: EmailStr
    name: str
    surname: str
    patronymic: Optional[str] = None
    birthdate: datetime.date