from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
from typing import Optional
from enum import Enum

# ------------------------
# BOOKS
# ------------------------

class BookCreate(BaseModel):
    title: str
    author: str
    total_copies: int

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    total_copies: int
    available_copies: int
    created_at: datetime


class BookUpdate(BaseModel):
    title: str
    author: str
    total_copies: int


# ------------------------
# MEMBERS
# ------------------------

class MemberCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class MemberUpdate(BaseModel):  # For PUT (full replace)
    name: str
    email: EmailStr
    phone: Optional[str] = None

class MemberPatch(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class MemberResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: Optional[str]
    created_at: datetime


# ------------------------
# BORROWINGS
# ------------------------

class BorrowingStatus(str, Enum):
    BORROWED = "BORROWED"
    RETURNED = "RETURNED"


class BorrowCreate(BaseModel):
    member_id: int
    book_id: int



class BorrowResponse(BaseModel):
    id: int
    member_id: int
    member_name: str
    book_id: int
    book_title: str
    borrowed_at: datetime
    due_date: datetime
    returned_at: Optional[datetime]
    status: BorrowingStatus


class BorrowPatch(BaseModel):
    status: BorrowingStatus