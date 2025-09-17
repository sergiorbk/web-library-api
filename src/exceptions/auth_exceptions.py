class AuthException(Exception):
    """Base exception for authentication errors"""
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidPasswordException(AuthException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg


class InvalidCredentialsException(AuthException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg

class AccessTokenExpiredException(AuthException):
    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg