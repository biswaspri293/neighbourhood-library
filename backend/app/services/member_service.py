from app.utils.db import execute_and_return_one, execute_and_return_many
from fastapi import HTTPException, status
import psycopg2


# -------------------------------------------------
# Create Member
# -------------------------------------------------
def create_member(conn, data):
    try:
        return execute_and_return_one(
            conn,
            """
            INSERT INTO members (name, email, phone)
            VALUES (%s, %s, %s)
            RETURNING *
            """,
            (data.name, data.email, data.phone),
        )
    except psycopg2.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Member with same email already exists"
        )


# -------------------------------------------------
# Get Member By ID
# -------------------------------------------------
def get_member_by_id(conn, member_id: int):
    member = execute_and_return_one(
        conn,
        "SELECT * FROM members WHERE id = %s",
        (member_id,),
    )
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


# -------------------------------------------------
# List Members
# -------------------------------------------------
def get_members(conn, skip=0, limit=100):
    return execute_and_return_many(
        conn,
        """
        SELECT *
        FROM members
        ORDER BY created_at DESC
        OFFSET %s LIMIT %s
        """,
        (skip, limit),
    )


# -------------------------------------------------
# Update Member
# -------------------------------------------------
def update_member(conn, member_id: int, data):
    existing = get_member_by_id(conn, member_id)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )

    data_dict = data.dict(exclude_unset=True)

    new_name = data_dict.get("name", existing["name"])
    new_email = data_dict.get("email", existing["email"])
    new_phone = data_dict.get("phone", existing["phone"])

    try:
        return execute_and_return_one(
            conn,
            """
            UPDATE members
            SET name = %s,
                email = %s,
                phone = %s
            WHERE id = %s
            RETURNING *
            """,
            (new_name, new_email, new_phone, member_id),
        )
    except psycopg2.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )


# -------------------------------------------------
# Delete Member
# -------------------------------------------------
def delete_member(conn, member_id: int):
    active_borrowing = execute_and_return_one(
        conn,
        """
        SELECT 1
        FROM borrowings
        WHERE member_id = %s
        AND status = 'BORROWED'
        LIMIT 1
        """,
        (member_id,)
    )

    if active_borrowing:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete member with active borrowed books"
        )

    return execute_and_return_one(
        conn,
        """
        DELETE FROM members
        WHERE id = %s
        RETURNING id
        """,
        (member_id,)
    )