from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.container import Container
from src.schemas.auth import LoginRequest, LoginResponse
from src.services.auth_serivce import AuthService

router = APIRouter(prefix="/api/v1/auth", tags=["auth", "v1"])


@router.post("/login", response_model=LoginResponse)
@inject
async def login(
        request: LoginRequest,
        auth_service: AuthService = Depends(Provide[Container.auth_service]),
):
    try:
        return await auth_service.login(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )