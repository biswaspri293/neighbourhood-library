from typing import List

from fastapi import APIRouter, status, HTTPException, Request, Query

from app.utils.schemas import BookCreate, BookUpdate, BookResponse
from app.services.book_service import (
    create_book,
    get_books,
    get_book_by_id,
    update_book,
    delete_book,
)

router = APIRouter()


# -------------------------------------------------
# Create Book
# -------------------------------------------------
@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(data: BookCreate, request: Request):
    return create_book(request.state.db, data)


# -------------------------------------------------
# List All Books
# -------------------------------------------------
@router.get(
    "/",
    response_model=List[BookResponse],
)
def list_books(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    return get_books(conn=request.state.db, skip=skip, limit=limit)


# -------------------------------------------------
# Get Book By ID
# -------------------------------------------------
@router.get(
    "/{book_id}",
    response_model=BookResponse,
)
def get_book(book_id: int, request: Request):
    book = get_book_by_id(conn=request.state.db, book_id=book_id)

    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return book


# -------------------------------------------------
# Update Book
# -------------------------------------------------
@router.put(
    "/{book_id}",
    response_model=BookResponse,
)
def update(book_id: int, data: BookUpdate, request: Request):
    updated = update_book(request.state.db, book_id, data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return updated


# -------------------------------------------------
# Delete Book
# -------------------------------------------------
@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete(book_id: int, request: Request):
    deleted = delete_book(request.state.db, book_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )

    return None