from app.utils.db import execute_and_return_one, execute_and_return_many
from fastapi import HTTPException, status
from app.utils.schemas import BookUpdate, BookCreate
import psycopg2


# -------------------------------------------------
# Create Book
# -------------------------------------------------

def create_book(conn, data: BookCreate):
    try:
        return execute_and_return_one(
            conn,
            """
            INSERT INTO books (title, author, total_copies, available_copies)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (
                data.title,
                data.author,
                data.total_copies,
                data.total_copies,
            ),
        )

    except psycopg2.errors.UniqueViolation:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Book with same title and author already exists"
        )


# -------------------------------------------------
# Get Book By ID
# -------------------------------------------------

def get_book_by_id(conn, book_id: int):
    return execute_and_return_one(
        conn,
        "SELECT * FROM books WHERE id = %s",
        (book_id,),
    )


# -------------------------------------------------
# List Books
# -------------------------------------------------

def get_books(conn, skip=0, limit=100):
    return execute_and_return_many(
        conn,
        """
        SELECT *
        FROM books
        ORDER BY created_at DESC
        OFFSET %s LIMIT %s
        """,
        (skip, limit),
    )


# -------------------------------------------------
# Update Book
# -------------------------------------------------

def update_book(conn, book_id: int, data: BookUpdate):
    # Step 1: Fetch current book
    book = execute_and_return_one(
        conn,
        "SELECT * FROM books WHERE id = %s",
        (book_id,)
    )

    if not book:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )


    current_total = book["total_copies"]
    current_available = book["available_copies"]

    # Calculate borrowed count
    borrowed_count = current_total - current_available

    # Step 2: If total_copies is being updated
    if data.total_copies is not None:

        new_total = data.total_copies

        # Validate invariant
        if new_total < borrowed_count:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Total copies cannot be less than currently borrowed copies"
            )

        # Recalculate available copies
        new_available = new_total - borrowed_count

    else:
        # If total not changing, preserve values
        new_total = current_total
        new_available = current_available

    # Step 3: Update record
    updated = execute_and_return_one(
        conn,
        """
        UPDATE books
        SET title = %s,
            author = %s,
            total_copies = %s,
            available_copies = %s
        WHERE id = %s
        RETURNING *
        """,
        (
            data.title,
            data.author,
            new_total,
            new_available,
            book_id,
        ),
    )

    return updated


# -------------------------------------------------
# Delete Book
# -------------------------------------------------

def delete_book(conn, book_id: int):
    # Check active borrowings
    active_borrowing = execute_and_return_one(
        conn,
        """
        SELECT 1
        FROM borrowings
        WHERE book_id = %s
        AND status = 'BORROWED'
        LIMIT 1
        """,
        (book_id,),
    )

    if active_borrowing:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete book while it is currently borrowed"
        )

    return execute_and_return_one(
        conn,
        """
        DELETE FROM books
        WHERE id = %s
        RETURNING id
        """,
        (book_id,),
    )