from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from src.container import Container
from src.core.security import get_current_user, require_roles
from src.schemas.book_checkout import (
    BookCheckoutSchema,
    CreateCheckoutRequest,
    UpdateCheckoutRequest,
    ExtendCheckoutRequest,
    CheckoutSearchRequest
)
from src.services.book_checkout_service import BookCheckoutService

router = APIRouter(prefix="/api/v1/checkouts", tags=["checkouts", "v1"])


@router.get("/", response_model=List[BookCheckoutSchema])
@inject
async def get_all_checkouts(
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.get_all_checkouts()


@router.get("/active", response_model=List[BookCheckoutSchema])
@inject
async def get_active_checkouts(
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.get_active_checkouts()


@router.get("/expired", response_model=List[BookCheckoutSchema])
@inject
async def get_expired_checkouts(
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.get_expired_checkouts()


@router.get("/{checkout_id}", response_model=BookCheckoutSchema)
@inject
async def get_checkout_by_id(
    checkout_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    checkout = checkout_service.get_checkout_by_id(checkout_id)
    if not checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checkout not found"
        )
    return checkout


@router.post("/", response_model=BookCheckoutSchema, status_code=status.HTTP_201_CREATED)
@inject
async def create_checkout(
    request: CreateCheckoutRequest,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.create_checkout(request)


@router.post("/quick", response_model=BookCheckoutSchema, status_code=status.HTTP_201_CREATED)
@inject
async def quick_checkout(
    book_id: uuid.UUID,
    client_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.quick_checkout(book_id, client_id)


@router.put("/{checkout_id}", response_model=BookCheckoutSchema)
@inject
async def update_checkout(
    checkout_id: uuid.UUID,
    request: UpdateCheckoutRequest,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    updated_checkout = checkout_service.update_checkout(checkout_id, request)
    if not updated_checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checkout not found"
        )
    return updated_checkout


@router.patch("/{checkout_id}/extend", response_model=BookCheckoutSchema)
@inject
async def extend_checkout(
    checkout_id: uuid.UUID,
    request: ExtendCheckoutRequest,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    extended_checkout = checkout_service.extend_checkout(checkout_id, request)
    if not extended_checkout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checkout not found"
        )
    return extended_checkout


@router.delete("/{checkout_id}/return", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def return_book(
    checkout_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    success = checkout_service.return_book(checkout_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Checkout not found"
        )


@router.get("/client/{client_id}", response_model=List[BookCheckoutSchema])
@inject
async def get_checkouts_by_client(
    client_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.get_checkouts_by_client(client_id)


@router.get("/client/{client_id}/active", response_model=List[BookCheckoutSchema])
@inject
async def get_client_active_checkouts(
    client_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.get_client_active_checkouts(client_id)


@router.get("/book/{book_id}", response_model=List[BookCheckoutSchema])
@inject
async def get_checkouts_by_book(
    book_id: uuid.UUID,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.get_checkouts_by_book(book_id)


@router.get("/book/{book_id}/available")
@inject
async def is_book_available(
    book_id: uuid.UUID,
    user = Depends(get_current_user),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    available = checkout_service.is_book_available(book_id)
    return {"book_id": book_id, "available": available}


@router.post("/search", response_model=List[BookCheckoutSchema])
@inject
async def search_checkouts(
    request: CheckoutSearchRequest,
    user = Depends(require_roles(["admin"])),
    checkout_service: BookCheckoutService = Depends(Provide[Container.book_checkout_service])
):
    return checkout_service.search_checkouts(request)