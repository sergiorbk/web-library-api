import uuid
from typing import List, Optional
from datetime import date

from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.db.models.orm_client import Client


class ClientRepository:
    def __init__(self, db_session: Session):
        self.__db = db_session

    def create(self, client: Client) -> Client:
        self.__db.add(client)
        self.__db.commit()
        self.__db.refresh(client)
        return client

    def get_by_id(self, client_id: uuid.UUID) -> Optional[Client]:
        return self.__db.get(Client, client_id)

    def get_all(self) -> List[Client]:
        return self.__db.query(Client).all()

    def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Client]:
        return self.__db.query(Client).filter(Client.user_id == user_id).first()

    def get_by_email(self, email: EmailStr) -> Optional[Client]:
        return self.__db.query(Client).filter(Client.email == email).first()

    def update(self, client_id: uuid.UUID, **kwargs) -> Optional[Client]:
        client = self.get_by_id(client_id)
        if not client:
            return None

        for key, value in kwargs.items():
            if hasattr(client, key) and value is not None:
                setattr(client, key, value)

        self.__db.commit()
        self.__db.refresh(client)
        return client

    def delete_by_id(self, client_id: uuid.UUID) -> bool:
        client = self.get_by_id(client_id)
        if not client:
            return False

        self.__db.delete(client)
        self.__db.commit()
        return True

    def exists_by_email(self, email: EmailStr) -> bool:
        return self.__db.query(Client).filter(Client.email == email).first() is not None

    def search_by_name(self, name: str) -> List[Client]:
        return self.__db.query(Client).filter(
            Client.name.ilike(f"%{name}%") |
            Client.surname.ilike(f"%{name}%") |
            Client.patronymic.ilike(f"%{name}%")
        ).all()

    def get_by_birthdate_range(self, start_date: date, end_date: date) -> List[Client]:
        return self.__db.query(Client).filter(
            Client.birthdate >= start_date,
            Client.birthdate <= end_date
        ).all()