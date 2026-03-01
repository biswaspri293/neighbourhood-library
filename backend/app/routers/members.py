from fastapi import APIRouter, status, HTTPException, Request, Query
from typing import List

from app.utils.schemas import MemberCreate, MemberUpdate, MemberResponse, MemberPatch
from app.services.member_service import (
    create_member,
    get_members,
    get_member_by_id,
    update_member,
    delete_member,
)

router = APIRouter()


@router.post(
    "/",
    response_model=MemberResponse,
    status_code=status.HTTP_201_CREATED,
)
def create(data: MemberCreate, request: Request):
    return create_member(request.state.db, data)


@router.get(
    "/",
    response_model=List[MemberResponse],
)
def list_members(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    return get_members(conn=request.state.db, skip=skip, limit=limit)


@router.get(
    "/{member_id}",
    response_model=MemberResponse,
)
def get_member(member_id: int, request: Request):
    member = get_member_by_id(conn=request.state.db, member_id=member_id)

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@router.put(
    "/{member_id}",
    response_model=MemberResponse,
)
def update_full(member_id: int, data: MemberUpdate, request: Request):
    return update_member(request.state.db, member_id, data)


@router.patch(
    "/{member_id}",
    response_model=MemberResponse,
)
def update_partial(member_id: int, data: MemberPatch, request: Request):
    return update_member(request.state.db, member_id, data)


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_member_api(member_id: int, request: Request):
    deleted = delete_member(request.state.db, member_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    return None