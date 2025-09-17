import uuid
from typing import List, Optional

from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import update

from src.db.models.orm_user import User


class UserRepository:
    def __init__(self, db_session: Session):
        self.__db = db_session

    def create(self, user: User) -> User:
        self.__db.add(user)
        self.__db.commit()
        self.__db.refresh(user)
        return user

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.__db.get(User, user_id)

    def get_by_email(self, email: EmailStr) -> User | None:
        return self.__db.query(User).filter(User.email == email).first()

    def get_all(self) -> List[User]:
        return self.__db.query(User).all()

    def update(self, user_id: uuid.UUID, **kwargs) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        self.__db.commit()
        self.__db.refresh(user)
        return user

    def delete_by_id(self, user_id: uuid.UUID) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.__db.delete(user)
        self.__db.commit()
        return True

    def exists_by_email(self, email: EmailStr) -> bool:
        return self.__db.query(User).filter(User.email == email).first() is not None
