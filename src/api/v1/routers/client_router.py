from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from src.container import Container
from src.core.security import get_current_user, require_roles
from src.schemas.client import ClientSchema, CreateClientRequest, UpdateClientRequest, ClientSearchRequest
from src.services.client_service import ClientService

router = APIRouter(prefix="/api/v1/clients", tags=["clients", "v1"])


@router.get("/", response_model=List[ClientSchema])
@inject
async def get_all_clients(
    user = Depends(get_current_user),
    client_service: ClientService = Depends(Provide[Container.client_service])
):
    return client_service.get_all_clients()


@router.get("/{client_id}", response_model=ClientSchema)
@inject
async def get_client_by_id(
    client_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    client_service: ClientService = Depends(Provide[Container.client_service])
):
    client = client_service.get_client_by_id(client_id)
    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return client


@router.post("/", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
@inject
async def create_client(
    request: CreateClientRequest,
    user = Depends(require_roles(["admin"])),
    client_service: ClientService = Depends(Provide[Container.client_service])
):
    return client_service.create_client(request)


@router.put("/{client_id}", response_model=ClientSchema)
@inject
async def update_client(
    client_id: uuid.UUID,
    request: UpdateClientRequest,
    user = Depends(require_roles(["admin"])),
    client_service: ClientService = Depends(Provide[Container.client_service])
):
    updated_client = client_service.update_client(client_id, request)
    if not updated_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )
    return updated_client


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_client(
    client_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    client_service: ClientService = Depends(Provide[Container.client_service])
):
    success = client_service.delete_client(client_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Client not found"
        )


@router.post("/search", response_model=List[ClientSchema])
@inject
async def search_clients(
    request: ClientSearchRequest,
    user = Depends(require_roles(["admin"])),
    client_service: ClientService = Depends(Provide[Container.client_service])
):
    return client_service.search_clients(request)