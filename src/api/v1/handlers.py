from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from jwt import ExpiredSignatureError, InvalidTokenError

from src.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException
from src.exceptions.auth_exceptions import AuthException, InvalidCredentialsException, AccessTokenExpiredException
from src.exceptions.book_exceptions import (
    BookNotFoundException,
    BookAlreadyExistsException,
    BookNotAvailableException,
    InvalidISBNException
)
from src.exceptions.client_exceptions import (
    ClientNotFoundException,
    ClientAlreadyExistsException,
    InvalidClientDataException
)
from src.exceptions.checkout_exceptions import (
    CheckoutNotFoundException,
    BookAlreadyCheckedOutException,
    CheckoutExpiredException,
    InvalidCheckoutDateException,
    MaxCheckoutsExceededException
)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "detail": "Invalid request data",
            "errors": exc.errors()
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity constraint violations"""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Database Constraint Violation",
            "detail": "The requested operation violates database constraints"
        }
    )


# User Exception Handlers
async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "User Already Exists",
            "detail": str(exc)
        }
    )


async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "User Not Found",
            "detail": str(exc)
        }
    )


# Auth Exception Handlers
async def auth_exception_handler(request: Request, exc: AuthException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Authentication Error",
            "detail": str(exc)
        }
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Invalid Credentials",
            "detail": str(exc)
        }
    )


async def expired_token_handler(request: Request, exc: ExpiredSignatureError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Token Expired",
            "detail": "Your authentication token has expired. Please login again."
        }
    )


async def invalid_token_handler(request: Request, exc: InvalidTokenError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Invalid Token",
            "detail": "Your authentication token is invalid. Please login again."
        }
    )

async def access_token_expired_handler(request: Request, exc: AccessTokenExpiredException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Access Token Expired",
            "detail": "Your authentication token is expired. Please login again."
        }
    )


# Book Exception Handlers
async def book_not_found_handler(request: Request, exc: BookNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Book Not Found",
            "detail": str(exc)
        }
    )


async def book_already_exists_handler(request: Request, exc: BookAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Book Already Exists",
            "detail": str(exc)
        }
    )


async def book_not_available_handler(request: Request, exc: BookNotAvailableException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Book Not Available",
            "detail": str(exc)
        }
    )


async def invalid_isbn_handler(request: Request, exc: InvalidISBNException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid ISBN",
            "detail": str(exc)
        }
    )


# Client Exception Handlers
async def client_not_found_handler(request: Request, exc: ClientNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Client Not Found",
            "detail": str(exc)
        }
    )


async def client_already_exists_handler(request: Request, exc: ClientAlreadyExistsException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Client Already Exists",
            "detail": str(exc)
        }
    )


async def invalid_client_data_handler(request: Request, exc: InvalidClientDataException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid Client Data",
            "detail": str(exc)
        }
    )


# Checkout Exception Handlers
async def checkout_not_found_handler(request: Request, exc: CheckoutNotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Checkout Not Found",
            "detail": str(exc)
        }
    )


async def book_already_checked_out_handler(request: Request, exc: BookAlreadyCheckedOutException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Book Already Checked Out",
            "detail": str(exc)
        }
    )


async def checkout_expired_handler(request: Request, exc: CheckoutExpiredException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Checkout Expired",
            "detail": str(exc)
        }
    )


async def invalid_checkout_date_handler(request: Request, exc: InvalidCheckoutDateException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Invalid Checkout Date",
            "detail": str(exc)
        }
    )


async def max_checkouts_exceeded_handler(request: Request, exc: MaxCheckoutsExceededException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Maximum Checkouts Exceeded",
            "detail": str(exc)
        }
    )


# Generic Exception Handler
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle any unhandled exceptions"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": "An unexpected error occurred. Please try again later."
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers with the FastAPI app"""

    # Standard FastAPI/Pydantic exceptions
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)

    # JWT exceptions
    app.add_exception_handler(ExpiredSignatureError, expired_token_handler)
    app.add_exception_handler(InvalidTokenError, invalid_token_handler)
    app.add_exception_handler(AccessTokenExpiredException, access_token_expired_handler)

    # User exceptions
    app.add_exception_handler(UserAlreadyExistsException, user_already_exists_handler)
    app.add_exception_handler(UserNotFoundException, user_not_found_handler)

    # Auth exceptions
    app.add_exception_handler(AuthException, auth_exception_handler)
    app.add_exception_handler(InvalidCredentialsException, invalid_credentials_handler)

    # Book exceptions
    app.add_exception_handler(BookNotFoundException, book_not_found_handler)
    app.add_exception_handler(BookAlreadyExistsException, book_already_exists_handler)
    app.add_exception_handler(BookNotAvailableException, book_not_available_handler)
    app.add_exception_handler(InvalidISBNException, invalid_isbn_handler)

    # Client exceptions
    app.add_exception_handler(ClientNotFoundException, client_not_found_handler)
    app.add_exception_handler(ClientAlreadyExistsException, client_already_exists_handler)
    app.add_exception_handler(InvalidClientDataException, invalid_client_data_handler)

    # Checkout exceptions
    app.add_exception_handler(CheckoutNotFoundException, checkout_not_found_handler)
    app.add_exception_handler(BookAlreadyCheckedOutException, book_already_checked_out_handler)
    app.add_exception_handler(CheckoutExpiredException, checkout_expired_handler)
    app.add_exception_handler(InvalidCheckoutDateException, invalid_checkout_date_handler)
    app.add_exception_handler(MaxCheckoutsExceededException, max_checkouts_exceeded_handler)

    # Generic exception handler (should be last)
    app.add_exception_handler(Exception, generic_exception_handler)