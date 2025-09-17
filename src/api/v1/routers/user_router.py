from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from src.container import Container
from src.schemas.user import RegisterUserRequest, UserSchema, UserUpdateFullRequest, UserUpdatePartlyRequest
from src.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users", "v1"])

@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
@inject
async def register_user(
    request: RegisterUserRequest,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    return user_service.register_user(request)
    # try:
    #     return await user_service.register_user(request)
    # except Exception as e:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"User registration failed"
    #     )


@router.get("/", response_model=List[UserSchema])
@inject
async def get_all_users(
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        return await user_service.get_all_users()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch users"
        )


@router.get("/{user_id}", response_model=UserSchema)
@inject
async def get_user_by_id(
    user_id: uuid.UUID,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        user = await user_service.get_user_by_id(user_id)
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
            detail="Failed to fetch user"
        )


@router.put("/{user_id}", response_model=UserSchema)
@inject
async def update_user_full(
    user_id: uuid.UUID,
    request: UserUpdateFullRequest,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        updated_user = await user_service.update_user_full(user_id, request)
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
            detail="Failed to update user"
        )


@router.patch("/{user_id}", response_model=UserSchema)
@inject
async def update_user_partial(
    user_id: uuid.UUID,
    request: UserUpdatePartlyRequest,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        updated_user = await user_service.update_user_partial(user_id, request)
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
            detail="Failed to update user"
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_user(
    user_id: uuid.UUID,
    user_service: UserService = Depends(Provide[Container.user_service])
):
    try:
        success = await user_service.delete_user(user_id)
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
            detail="Failed to delete user"
        )
