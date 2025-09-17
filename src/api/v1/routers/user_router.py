from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from src.container import Container
from src.core.security import get_current_user, require_roles
from src.schemas.user import RegisterUserRequest, UserSchema, UserUpdateFullRequest, UserUpdatePartlyRequest
from src.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users", "v1"])

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
@inject
async def register_user(
    request: RegisterUserRequest,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        return user_service.register_user(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User registration failed: {e}"
        )

@router.post("/create", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
@inject
async def create_user(
        request: RegisterUserRequest,
        user = Depends(require_roles(["admin"])),
        user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        return user_service.register_user(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User creation failed: {e}"
        )


@router.get("/", response_model=List[UserSchema])
@inject
async def get_all_users(
    user_service: UserService = Depends(Provide[Container.user_service]),
    user = Depends(require_roles(["admin"])),
):
    try:
        return user_service.get_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch users: {e}"
        )


@router.get("/{user_id}", response_model=UserSchema)
@inject
async def get_user_by_id(
    user_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user: {e}"
        )


@router.put("/{user_id}", response_model=UserSchema)
@inject
async def update_user_full(
    user_id: uuid.UUID,
    request: UserUpdateFullRequest,
    user = Depends(get_current_user),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        updated_user = user_service.update_user_full(user_id, request)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {e}"
        )


@router.patch("/{user_id}", response_model=UserSchema)
@inject
async def update_user_partial(
    user_id: uuid.UUID,
    request: UserUpdatePartlyRequest,
    user = Depends(get_current_user),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        updated_user = user_service.update_user_partial(user_id, request)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {e}"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        success = user_service.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {e}"
        )
