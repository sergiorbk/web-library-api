from datetime import datetime, timedelta
from typing import Any, Dict, List

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from src.config import get_app_config

# Get configuration
config = get_app_config()
SECRET_KEY = config.secret_key
ALGORITHM = config.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.jwt_expire_minutes

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, roles: List[str] | None = None) -> str:
    to_encode: Dict[str, Any] = data.copy()
    now = datetime.now()
    iat = int(now.timestamp())
    exp = int((now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp())
    to_encode.update({
        "iat": iat,
        "exp": exp,
    })
    # Use roles from data if present, otherwise use the roles parameter
    if "roles" not in to_encode:
        to_encode["roles"] = roles or []
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id: str | None = payload.get("sub")
    roles: list[str] = payload.get("roles", [])

    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    return {"user_id": user_id, "roles": roles}


def require_roles(required_roles: list[str]):
    def wrapper(user: dict = Depends(get_current_user)):
        user_roles = set(user["roles"])
        if not set(required_roles).intersection(user_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )
        return user
    return wrapper
