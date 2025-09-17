import datetime
import uuid

from pydantic import EmailStr
from sqlalchemy import String, Date, ForeignKey
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.base import Base


class Client(Base):
    __tablename__ = 'clients'

    client_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('users.user_id'), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(50))
    birthdate: Mapped[datetime.date] = mapped_column(Date, nullable=False)