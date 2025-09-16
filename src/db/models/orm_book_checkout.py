import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from src.db.base import Base


class BookCheckout(Base):
    __tablename__ = "book_checkouts"

    checkout_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    book_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.book_id"), nullable=False
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.client_id"), nullable=False
    )
    checkout_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
