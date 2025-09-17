class CheckoutException(Exception):
    """Base exception for checkout-related errors"""
    pass


class CheckoutNotFoundException(CheckoutException):
    """Raised when a requested checkout is not found"""
    pass


class BookAlreadyCheckedOutException(CheckoutException):
    """Raised when trying to checkout a book that is already checked out"""
    pass


class CheckoutExpiredException(CheckoutException):
    """Raised when trying to operate on an expired checkout"""
    pass


class InvalidCheckoutDateException(CheckoutException):
    """Raised when checkout date is invalid"""
    pass


class MaxCheckoutsExceededException(CheckoutException):
    """Raised when client has reached maximum number of checkouts"""
    pass