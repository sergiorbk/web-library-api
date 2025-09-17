class ClientException(Exception):
    """Base exception for client-related errors"""
    pass


class ClientNotFoundException(ClientException):
    """Raised when a requested client is not found"""
    pass


class ClientAlreadyExistsException(ClientException):
    """Raised when trying to create a client that already exists"""
    pass


class InvalidClientDataException(ClientException):
    """Raised when client data is invalid"""
    pass