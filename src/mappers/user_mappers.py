from src.db.models.orm_user import User
from src.schemas.user import UserSchema, Role


def map_user_orm_to_schema(orm_user: User) -> UserSchema:
    return UserSchema(
        user_id=orm_user.user_id,
        email=orm_user.email,
        roles=[Role(role) for role in orm_user.roles],
        registration_date=orm_user.registration_date,
    )