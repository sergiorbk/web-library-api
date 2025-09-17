from src.db.models.orm_book_checkout import BookCheckout
from src.schemas.book_checkout import BookCheckoutSchema, CreateCheckoutRequest


def map_checkout_orm_to_schema(checkout: BookCheckout) -> BookCheckoutSchema:
    """Map BookCheckout ORM model to BookCheckoutSchema"""
    return BookCheckoutSchema(
        checkout_id=checkout.checkout_id,
        book_id=checkout.book_id,
        client_id=checkout.client_id,
        checkout_date=checkout.checkout_date,
        expiration_date=checkout.expiration_date
    )


def map_create_request_to_orm(request: CreateCheckoutRequest) -> BookCheckout:
    """Map CreateCheckoutRequest to BookCheckout ORM model"""
    return BookCheckout(
        book_id=request.book_id,
        client_id=request.client_id,
        checkout_date=request.checkout_date,
        expiration_date=request.expiration_date
    )