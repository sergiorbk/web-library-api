import uuid
from typing import List, Optional
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from src.db.models.orm_book_checkout import BookCheckout


class BookCheckoutRepository:
    def __init__(self, db_session: Session):
        self.__db = db_session

    def create(self, checkout: BookCheckout) -> BookCheckout:
        self.__db.add(checkout)
        self.__db.commit()
        self.__db.refresh(checkout)
        return checkout

    def get_by_id(self, checkout_id: uuid.UUID) -> Optional[BookCheckout]:
        return self.__db.get(BookCheckout, checkout_id)

    def get_all(self) -> List[BookCheckout]:
        return self.__db.query(BookCheckout).all()

    def get_by_client_id(self, client_id: uuid.UUID) -> List[BookCheckout]:
        return self.__db.query(BookCheckout).filter(BookCheckout.client_id == client_id).all()

    def get_by_book_id(self, book_id: uuid.UUID) -> List[BookCheckout]:
        return self.__db.query(BookCheckout).filter(BookCheckout.book_id == book_id).all()

    def get_active_checkouts(self) -> List[BookCheckout]:
        """Get all checkouts that haven't expired yet"""
        current_date = datetime.now()
        return self.__db.query(BookCheckout).filter(
            BookCheckout.expiration_date > current_date
        ).all()

    def get_expired_checkouts(self) -> List[BookCheckout]:
        """Get all checkouts that have expired"""
        current_date = datetime.now()
        return self.__db.query(BookCheckout).filter(
            BookCheckout.expiration_date <= current_date
        ).all()

    def get_checkouts_by_date_range(self, start_date: datetime, end_date: datetime) -> List[BookCheckout]:
        return self.__db.query(BookCheckout).filter(
            and_(
                BookCheckout.checkout_date >= start_date,
                BookCheckout.checkout_date <= end_date
            )
        ).all()

    def get_active_checkout_for_book(self, book_id: uuid.UUID) -> Optional[BookCheckout]:
        """Check if a book is currently checked out (not expired)"""
        current_date = datetime.now()
        return self.__db.query(BookCheckout).filter(
            and_(
                BookCheckout.book_id == book_id,
                BookCheckout.expiration_date > current_date
            )
        ).first()

    def get_client_active_checkouts(self, client_id: uuid.UUID) -> List[BookCheckout]:
        """Get all active checkouts for a specific client"""
        current_date = datetime.now()
        return self.__db.query(BookCheckout).filter(
            and_(
                BookCheckout.client_id == client_id,
                BookCheckout.expiration_date > current_date
            )
        ).all()

    def update(self, checkout_id: uuid.UUID, **kwargs) -> Optional[BookCheckout]:
        checkout = self.get_by_id(checkout_id)
        if not checkout:
            return None

        for key, value in kwargs.items():
            if hasattr(checkout, key) and value is not None:
                setattr(checkout, key, value)

        self.__db.commit()
        self.__db.refresh(checkout)
        return checkout

    def delete_by_id(self, checkout_id: uuid.UUID) -> bool:
        checkout = self.get_by_id(checkout_id)
        if not checkout:
            return False

        self.__db.delete(checkout)
        self.__db.commit()
        return True

    def extend_checkout(self, checkout_id: uuid.UUID, new_expiration_date: datetime) -> Optional[BookCheckout]:
        """Extend the expiration date of a checkout"""
        return self.update(checkout_id, expiration_date=new_expiration_date)

    def is_book_available(self, book_id: uuid.UUID) -> bool:
        """Check if a book is available for checkout (not currently checked out)"""
        return self.get_active_checkout_for_book(book_id) is None