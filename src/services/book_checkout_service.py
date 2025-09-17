import uuid
from typing import List, Optional
from datetime import datetime, timedelta

from src.db.repositories.book_checkout_repository import BookCheckoutRepository
from src.db.repositories.book_repository import BookRepository
from src.db.repositories.client_repository import ClientRepository
from src.exceptions.checkout_exceptions import (
    CheckoutNotFoundException,
    BookAlreadyCheckedOutException,
    CheckoutExpiredException,
    InvalidCheckoutDateException,
    MaxCheckoutsExceededException
)
from src.mappers.checkout_mappers import map_checkout_orm_to_schema, map_create_request_to_orm
from src.schemas.book_checkout import (
    BookCheckoutSchema,
    CreateCheckoutRequest,
    UpdateCheckoutRequest,
    ExtendCheckoutRequest,
    CheckoutSearchRequest
)


class BookCheckoutService:
    MAX_CHECKOUTS_PER_CLIENT = 5  # Business rule: max 5 books per client
    DEFAULT_CHECKOUT_DAYS = 14    # Default checkout period

    def __init__(
        self,
        checkout_repository: BookCheckoutRepository,
        book_repository: BookRepository,
        client_repository: ClientRepository
    ):
        self.__checkout_repository = checkout_repository
        self.__book_repository = book_repository
        self.__client_repository = client_repository

    def create_checkout(self, request: CreateCheckoutRequest) -> BookCheckoutSchema:
        """Create a new book checkout"""
        # Validate that book exists
        if not self.__book_repository.get_by_id(request.book_id):
            raise CheckoutNotFoundException(f"Book with ID {request.book_id} not found")

        # Validate that client exists
        if not self.__client_repository.get_by_id(request.client_id):
            raise CheckoutNotFoundException(f"Client with ID {request.client_id} not found")

        # Check if book is available
        if not self.__checkout_repository.is_book_available(request.book_id):
            raise BookAlreadyCheckedOutException(f"Book with ID {request.book_id} is already checked out")

        # Check client's current active checkouts
        client_checkouts = self.__checkout_repository.get_client_active_checkouts(request.client_id)
        if len(client_checkouts) >= self.MAX_CHECKOUTS_PER_CLIENT:
            raise MaxCheckoutsExceededException(f"Client has reached maximum number of checkouts ({self.MAX_CHECKOUTS_PER_CLIENT})")

        # Validate checkout date is not in the past
        if request.checkout_date < datetime.now() - timedelta(days=1):
            raise InvalidCheckoutDateException("Checkout date cannot be in the past")

        # Validate expiration date is after checkout date
        if request.expiration_date <= request.checkout_date:
            raise InvalidCheckoutDateException("Expiration date must be after checkout date")

        checkout_orm = map_create_request_to_orm(request)
        created_checkout = self.__checkout_repository.create(checkout_orm)
        return map_checkout_orm_to_schema(created_checkout)

    def quick_checkout(self, book_id: uuid.UUID, client_id: uuid.UUID) -> BookCheckoutSchema:
        """Quick checkout with default parameters"""
        checkout_date = datetime.now()
        expiration_date = checkout_date + timedelta(days=self.DEFAULT_CHECKOUT_DAYS)

        request = CreateCheckoutRequest(
            book_id=book_id,
            client_id=client_id,
            checkout_date=checkout_date,
            expiration_date=expiration_date
        )

        return self.create_checkout(request)

    def get_all_checkouts(self) -> List[BookCheckoutSchema]:
        """Get all checkouts"""
        checkouts = self.__checkout_repository.get_all()
        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def get_checkout_by_id(self, checkout_id: uuid.UUID) -> Optional[BookCheckoutSchema]:
        """Get checkout by ID"""
        checkout = self.__checkout_repository.get_by_id(checkout_id)
        if not checkout:
            return None
        return map_checkout_orm_to_schema(checkout)

    def get_checkouts_by_client(self, client_id: uuid.UUID) -> List[BookCheckoutSchema]:
        """Get all checkouts for a client"""
        checkouts = self.__checkout_repository.get_by_client_id(client_id)
        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def get_checkouts_by_book(self, book_id: uuid.UUID) -> List[BookCheckoutSchema]:
        """Get all checkouts for a book"""
        checkouts = self.__checkout_repository.get_by_book_id(book_id)
        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def get_active_checkouts(self) -> List[BookCheckoutSchema]:
        """Get all active (non-expired) checkouts"""
        checkouts = self.__checkout_repository.get_active_checkouts()
        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def get_expired_checkouts(self) -> List[BookCheckoutSchema]:
        """Get all expired checkouts"""
        checkouts = self.__checkout_repository.get_expired_checkouts()
        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def get_client_active_checkouts(self, client_id: uuid.UUID) -> List[BookCheckoutSchema]:
        """Get active checkouts for a specific client"""
        checkouts = self.__checkout_repository.get_client_active_checkouts(client_id)
        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def extend_checkout(self, checkout_id: uuid.UUID, request: ExtendCheckoutRequest) -> Optional[BookCheckoutSchema]:
        """Extend checkout expiration date"""
        checkout = self.__checkout_repository.get_by_id(checkout_id)
        if not checkout:
            raise CheckoutNotFoundException(f"Checkout with ID {checkout_id} not found")

        # Check if checkout is already expired
        if checkout.expiration_date <= datetime.now():
            raise CheckoutExpiredException("Cannot extend an expired checkout")

        new_expiration_date = checkout.expiration_date + timedelta(days=request.days_to_extend)
        extended_checkout = self.__checkout_repository.extend_checkout(checkout_id, new_expiration_date)

        if not extended_checkout:
            return None
        return map_checkout_orm_to_schema(extended_checkout)

    def return_book(self, checkout_id: uuid.UUID) -> bool:
        """Return a book (delete checkout record)"""
        if not self.__checkout_repository.get_by_id(checkout_id):
            raise CheckoutNotFoundException(f"Checkout with ID {checkout_id} not found")

        return self.__checkout_repository.delete_by_id(checkout_id)

    def update_checkout(self, checkout_id: uuid.UUID, request: UpdateCheckoutRequest) -> Optional[BookCheckoutSchema]:
        """Update checkout"""
        if not self.__checkout_repository.get_by_id(checkout_id):
            raise CheckoutNotFoundException(f"Checkout with ID {checkout_id} not found")

        update_data = {}
        if request.expiration_date is not None:
            # Validate new expiration date
            checkout = self.__checkout_repository.get_by_id(checkout_id)
            if request.expiration_date <= checkout.checkout_date:
                raise InvalidCheckoutDateException("Expiration date must be after checkout date")
            update_data['expiration_date'] = request.expiration_date

        updated_checkout = self.__checkout_repository.update(checkout_id, **update_data)
        if not updated_checkout:
            return None
        return map_checkout_orm_to_schema(updated_checkout)

    def search_checkouts(self, request: CheckoutSearchRequest) -> List[BookCheckoutSchema]:
        """Search checkouts based on criteria"""
        checkouts = []

        if request.client_id:
            checkouts = self.__checkout_repository.get_by_client_id(request.client_id)
        elif request.book_id:
            checkouts = self.__checkout_repository.get_by_book_id(request.book_id)
        elif request.start_date and request.end_date:
            checkouts = self.__checkout_repository.get_checkouts_by_date_range(
                request.start_date,
                request.end_date
            )
        elif request.active_only:
            checkouts = self.__checkout_repository.get_active_checkouts()
        elif request.expired_only:
            checkouts = self.__checkout_repository.get_expired_checkouts()
        else:
            checkouts = self.__checkout_repository.get_all()

        return [map_checkout_orm_to_schema(checkout) for checkout in checkouts]

    def is_book_available(self, book_id: uuid.UUID) -> bool:
        """Check if a book is available for checkout"""
        return self.__checkout_repository.is_book_available(book_id)