from psycopg2 import errors
from app.utils.db import execute_and_return_many, execute_and_return_one

# -------------------------------------------------
# Borrow Book (Atomic + Race Safe)
# -------------------------------------------------
from fastapi import HTTPException, status

from app.utils.schemas import BorrowCreate


def borrow_book(conn, data: BorrowCreate):
    with conn.cursor() as cursor:

        # Lock the book row
        cursor.execute(
            """
            SELECT available_copies
            FROM books
            WHERE id = %s
            FOR UPDATE
            """,
            (data.book_id,)
        )

        book = cursor.fetchone()

        if not book:
            raise HTTPException(
                status_code=404,
                detail="Book not found"
            )

        if book[0] <= 0:
            raise HTTPException(
                status_code=400,
                detail="No copies available"
            )

        # Decrement available copies
        cursor.execute(
            """
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE id = %s
            """,
            (data.book_id,)
        )
        try:
            # Insert borrowing
            cursor.execute(
                """
                INSERT INTO borrowings
                (member_id, book_id, borrowed_at, due_date, status)
                VALUES (%s, %s, NOW(), NOW() + INTERVAL '14 days', 'BORROWED')
                RETURNING id
                """,
                (data.member_id, data.book_id)
            )
        except errors.UniqueViolation:
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Member already has this book borrowed"
            )


        borrow_id = cursor.fetchone()[0]

        conn.commit()

        return execute_and_return_one(
            conn,
            """
            SELECT 
                b.id,
                b.member_id,
                m.name AS member_name,
                b.book_id,
                bk.title AS book_title,
                b.borrowed_at,
                b.due_date,
                b.returned_at,
                b.status
            FROM borrowings b
            INNER JOIN members m ON b.member_id = m.id
            INNER JOIN books bk ON b.book_id = bk.id
            WHERE b.id = %s
            """,
            (borrow_id,)
        )


# -------------------------------------------------
# Return Book (Atomic + Safe)
# -------------------------------------------------

def return_book(conn, borrow_id: int):
    with conn.cursor() as cursor:

        cursor.execute(
            """
            SELECT book_id, status
            FROM borrowings
            WHERE id = %s
            FOR UPDATE
            """,
            (borrow_id,)
        )

        borrowing = cursor.fetchone()

        if not borrowing:
            conn.rollback()
            raise HTTPException(
                status_code=404,
                detail="Borrowing not found"
            )

        book_id, status_value = borrowing

        if status_value == "RETURNED":
            conn.rollback()
            raise HTTPException(
                status_code=400,
                detail="Already returned"
            )

        # Mark returned
        cursor.execute(
            """
            UPDATE borrowings
            SET status = 'RETURNED',
                returned_at = NOW()
            WHERE id = %s
            """,
            (borrow_id,)
        )

        # Increase available copies
        cursor.execute(
            """
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE id = %s
            """,
            (book_id,)
        )

        conn.commit()

        return execute_and_return_one(
            conn,
            """
            SELECT 
                b.id,
                b.member_id,
                m.name AS member_name,
                b.book_id,
                bk.title AS book_title,
                b.borrowed_at,
                b.due_date,
                b.returned_at,
                b.status
            FROM borrowings b
            INNER JOIN members m ON b.member_id = m.id
            INNER JOIN books bk ON b.book_id = bk.id
            WHERE b.id = %s
            """,
            (borrow_id,)
        )


# -------------------------------------------------
# List Borrowings For Member
# -------------------------------------------------
def get_borrowings_by_member(conn, member_id=None, status=None):
    if member_id is not None and status:
        return execute_and_return_many(
            conn,
            """
                SELECT 
                b.id,
                b.member_id,
                m.name AS member_name,
                b.book_id,
                bk.title AS book_title,
                b.borrowed_at,
                b.due_date,
                b.returned_at,
                b.status
            FROM borrowings b
            INNER JOIN members m ON b.member_id = m.id
            INNER JOIN books bk ON b.book_id = bk.id
                WHERE member_id = %s
                AND status = %s
                ORDER BY borrowed_at DESC
            """,
            (member_id, status.value)
        )
    elif member_id:
        return execute_and_return_many(
            conn,
            """
            SELECT 
            b.id,
            b.member_id,
            m.name AS member_name,
            b.book_id,
            bk.title AS book_title,
            b.borrowed_at,
            b.due_date,
            b.returned_at,
            b.status
        FROM borrowings b
        INNER JOIN members m ON b.member_id = m.id
        INNER JOIN books bk ON b.book_id = bk.id
            WHERE member_id = %s
            ORDER BY borrowed_at DESC
            """,
            (member_id,)
        )


def get_borrowings(conn, status=None, skip=0, limit=100):

    if status:
        return execute_and_return_many(
            conn,
            """
            SELECT 
            b.id,
            b.member_id,
            m.name AS member_name,
            b.book_id,
            bk.title AS book_title,
            b.borrowed_at,
            b.due_date,
            b.returned_at,
            b.status
        FROM borrowings b
        INNER JOIN members m ON b.member_id = m.id
        INNER JOIN books bk ON b.book_id = bk.id
            WHERE status = %s
            ORDER BY borrowed_at DESC
            OFFSET %s LIMIT %s
            """,
            (status.value, skip, limit),
        )

    return execute_and_return_many(
        conn,
        """
        SELECT 
            b.id,
            b.member_id,
            m.name AS member_name,
            b.book_id,
            bk.title AS book_title,
            b.borrowed_at,
            b.due_date,
            b.returned_at,
            b.status
        FROM borrowings b
        INNER JOIN members m ON b.member_id = m.id
        INNER JOIN books bk ON b.book_id = bk.id
        ORDER BY borrowed_at DESC
        """
        )