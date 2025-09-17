from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
import uuid

from src.container import Container
from src.schemas.book import BookSchema, CreateBookRequest, UpdateBookRequest
from src.services.book_service import BookService

router = APIRouter(prefix="/api/v1/books", tags=["books", "v1"])


@router.get("/", response_model=List[BookSchema])
@inject
async def get_all_books(
    book_service: BookService = Depends(Provide[Container.book_service])
):
    try:
        return await book_service.get_all_books()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch books"
        )


@router.get("/{book_id}", response_model=BookSchema)
@inject
async def get_book_by_id(
    book_id: uuid.UUID,
    book_service: BookService = Depends(Provide[Container.book_service])
):
    try:
        book = await book_service.get_book_by_id(book_id)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch book"
        )


@router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
@inject
async def create_book(
    request: CreateBookRequest,
    book_service: BookService = Depends(Provide[Container.book_service])
):
    try:
        return await book_service.create_book(request)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create book"
        )


@router.put("/{book_id}", response_model=BookSchema)
@inject
async def update_book(
    book_id: uuid.UUID,
    request: UpdateBookRequest,
    book_service: BookService = Depends(Provide[Container.book_service])
):
    try:
        updated_book = await book_service.update_book(book_id, request)
        if not updated_book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
        return updated_book
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update book"
        )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_book(
    book_id: uuid.UUID,
    book_service: BookService = Depends(Provide[Container.book_service])
):
    try:
        success = await book_service.delete_book(book_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete book"
        )