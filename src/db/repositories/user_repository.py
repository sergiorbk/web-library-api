import uuid

from pydantic import EmailStr
from sqlalchemy.orm import Session

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

    def delete_by_id(self, user_id: uuid.UUID) -> None:
        self.__db.delete(self.get_by_id(user_id))

    def exists_by_email(self, email: EmailStr) -> bool:
        stmt = self.__db.query(User).filter(User.email == email)
        return self.__db.execute(stmt).scalar()
