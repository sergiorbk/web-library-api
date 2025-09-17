import datetime
import uuid
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class Role(str, Enum):
    ADMIN = 'admin'
    USER = 'user'

class UserSchema(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    roles: List[Role]
    registration_date: datetime.datetime

class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str

class UserUpdateFullRequest(BaseModel):
    email: EmailStr
    roles: List[Role]

class UserUpdatePartlyRequest(BaseModel):
    email: Optional[EmailStr] = None
    roles: Optional[List[Role]] = None