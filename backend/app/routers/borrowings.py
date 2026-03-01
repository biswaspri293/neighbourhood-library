from fastapi import APIRouter, status, HTTPException, Query, Request
from typing import List, Optional

from app.utils.schemas import BorrowCreate, BorrowResponse, BorrowingStatus
from app.services.borrowing_service import (
    borrow_book,
    return_book,
    get_borrowings,
    get_borrowings_by_member
)

router = APIRouter()


@router.post(
    "/",
    response_model=BorrowResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_borrowing(data: BorrowCreate, request: Request):
    borrow_id = borrow_book(request.state.db, data)
    return borrow_id


@router.patch(
    "/{borrow_id}/return",
    response_model=BorrowResponse,
)
def return_borrowing(borrow_id: int, request: Request):
    updated = return_book(request.state.db, borrow_id)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Borrow record not found"
        )
    return updated


@router.get(
    "/member/{member_id}",
    response_model=List[BorrowResponse],
)
def list_member_borrowings(
    member_id: int,
    request: Request,
    status: Optional[BorrowingStatus] = Query(None),
):
    return get_borrowings_by_member(
        conn=request.state.db,
        member_id=member_id,
        status=status,
    )


@router.get(
    "/",
    response_model=List[BorrowResponse],
)
def list_borrowings(
    request: Request,
    status: Optional[BorrowingStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    return get_borrowings(
        conn=request.state.db,
        status=status,
        skip=skip,
        limit=limit,
    )