import datetime
import uuid
from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    ADMIN = 'admin'
    USER = 'user'

class UserSchema(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    roles: List[Role]
    registration_date: datetime.datetime