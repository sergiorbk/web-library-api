import uuid
from typing import List, Optional

from src.db.models.orm_user import User
from src.db.repositories.user_repository import UserRepository
from src.exceptions.user_exceptions import UserAlreadyExistsException, UserNotFoundException
from src.mappers.user_mappers import map_user_orm_to_schema
from src.schemas.user import RegisterUserRequest, UserSchema, UserUpdateFullRequest, UserUpdatePartlyRequest, Role
from src.core.password_hasher import hash_password


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
            roles=[Role.USER]
        )

        created_user = self.__user_repository.create(user_to_register)

        return map_user_orm_to_schema(created_user)

    def get_all_users(self) -> List[UserSchema]:
        """Get all users"""
        users = self.__user_repository.get_all()
        return [map_user_orm_to_schema(user) for user in users]

    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[UserSchema]:
        """Get user by ID"""
        user = self.__user_repository.get_by_id(user_id)
        if not user:
            return None
        return map_user_orm_to_schema(user)

    def get_user_by_email(self, email: str) -> Optional[UserSchema]:
        """Get user by email"""
        user = self.__user_repository.get_by_email(email)
        if not user:
            return None
        return map_user_orm_to_schema(user)

    def update_user_full(self, user_id: uuid.UUID, request: UserUpdateFullRequest) -> Optional[UserSchema]:
        """Update user with all fields"""
        if not self.__user_repository.get_by_id(user_id):
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Check if email is already taken by another user
        existing_user = self.__user_repository.get_by_email(request.email)
        if existing_user and existing_user.user_id != user_id:
            raise UserAlreadyExistsException(f"User with email {request.email} already exists")

        updated_user = self.__user_repository.update(
            user_id,
            email=request.email,
            roles=request.roles
        )

        if not updated_user:
            return None
        return map_user_orm_to_schema(updated_user)

    def update_user_partial(self, user_id: uuid.UUID, request: UserUpdatePartlyRequest) -> Optional[UserSchema]:
        """Update user with partial fields"""
        if not self.__user_repository.get_by_id(user_id):
            raise UserNotFoundException(f"User with ID {user_id} not found")

        # Check if email is already taken by another user
        if request.email:
            existing_user = self.__user_repository.get_by_email(request.email)
            if existing_user and existing_user.user_id != user_id:
                raise UserAlreadyExistsException(f"User with email {request.email} already exists")

        update_data = {}
        if request.email is not None:
            update_data['email'] = request.email
        if request.roles is not None:
            update_data['roles'] = request.roles

        updated_user = self.__user_repository.update(user_id, **update_data)

        if not updated_user:
            return None
        return map_user_orm_to_schema(updated_user)

    def delete_user(self, user_id: uuid.UUID) -> bool:
        """Delete user by ID"""
        if not self.__user_repository.get_by_id(user_id):
            raise UserNotFoundException(f"User with ID {user_id} not found")

        return self.__user_repository.delete_by_id(user_id)
