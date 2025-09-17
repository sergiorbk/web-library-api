class BookException(Exception):
    """Base exception for book-related errors"""
    pass


class BookNotFoundException(BookException):
    """Raised when a requested book is not found"""
    pass


class BookAlreadyExistsException(BookException):
    """Raised when trying to create a book that already exists"""
    pass


class BookNotAvailableException(BookException):
    """Raised when trying to checkout a book that is not available"""
    pass


class InvalidISBNException(BookException):
    """Raised when ISBN format is invalid"""
    pass