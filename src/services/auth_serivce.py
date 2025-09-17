from src.db.repositories.user_repository import UserRepository
from src.exceptions.auth_exceptions import InvalidPasswordException
from src.exceptions.user_exceptions import UserNotFoundException
from src.schemas.auth import LoginRequest, LoginResponse
from src.utils.jwt_utils import create_access_token
from src.utils.password_hasher import validate_password


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def login(self, request: LoginRequest) -> LoginResponse:
        # retrieve user from db by email
        user = self.__user_repository.get_by_email(email=request.email)

        # check if user exists
        if user is None:
            raise UserNotFoundException

        # validate password
        password_hash = user.password_hash
        if not validate_password(request.password, password_hash):
            # raise exception if password is incorrect
            raise InvalidPasswordException(f"Invalid password for {user.email}")

        # issue token if password correct
        token = create_access_token({
            "sub": str(user.user_id),
            "roles": user.roles
        })

        return LoginResponse(token=token)


