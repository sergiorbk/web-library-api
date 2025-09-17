from src.db.models.orm_user import User
from src.db.repositories.user_repository import UserRepository
from src.exceptions.user_exceptions import UserAlreadyExistsException
from src.mappers.user_mappers import map_user_orm_to_schema
from src.schemas.user import RegisterUserRequest, UserSchema
from src.utils.password_hasher import hash_password


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def register_user(self, request: RegisterUserRequest) -> UserSchema:
        # check if user with such email already exists
        if self.__user_repository.exists_by_email(request.email):
            # raise exception if user already exists
            raise UserAlreadyExistsException(f"User with email {request.email} already exists")

        # prepare orm user
        user_to_register = User(
            email=request.email,
            password_hash=hash_password(request.password),
        )

        created_user = self.__user_repository.create(user_to_register)

        return map_user_orm_to_schema(created_user)
