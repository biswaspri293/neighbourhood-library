import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.services import borrowing_service
from app.utils.schemas import BorrowCreate


# --------------------------------------------------
# 1. Borrow Book - Success
# --------------------------------------------------
def test_borrow_book_success(mock_borrow_execute_one):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    # First fetch → book available
    # Second fetch → inserted id
    mock_cursor.fetchone.side_effect = [
        (5,),   # available_copies
        (1,)    # borrow_id
    ]

    mock_borrow_execute_one.return_value = {"id": 1}

    data = BorrowCreate(member_id=1, book_id=1)

    result = borrowing_service.borrow_book(mock_conn, data)

    assert result["id"] == 1


# --------------------------------------------------
# 2. Borrow Book - No Copies
# --------------------------------------------------
def test_borrow_book_no_copies():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (0,)

    data = BorrowCreate(member_id=1, book_id=1)

    with pytest.raises(HTTPException) as exc:
        borrowing_service.borrow_book(mock_conn, data)

    assert exc.value.status_code == 400


# --------------------------------------------------
# 3. Borrow Book - Not Found
# --------------------------------------------------
def test_borrow_book_not_found():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    data = BorrowCreate(member_id=1, book_id=1)

    with pytest.raises(HTTPException) as exc:
        borrowing_service.borrow_book(mock_conn, data)

    assert exc.value.status_code == 404


# --------------------------------------------------
# 4. Return Book - Success
# --------------------------------------------------
def test_return_book_success(mock_borrow_execute_one):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "BORROWED")

    mock_borrow_execute_one.return_value = {"id": 1}

    result = borrowing_service.return_book(mock_conn, 1)

    assert result["id"] == 1


# --------------------------------------------------
# 5. Return Book - Already Returned
# --------------------------------------------------
def test_return_book_already_returned():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1, "RETURNED")

    with pytest.raises(HTTPException) as exc:
        borrowing_service.return_book(mock_conn, 1)

    assert exc.value.status_code == 400


# --------------------------------------------------
# 6. Return Book - Not Found
# --------------------------------------------------
def test_return_book_not_found():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    mock_cursor.fetchone.return_value = None

    with pytest.raises(HTTPException) as exc:
        borrowing_service.return_book(mock_conn, 1)

    assert exc.value.status_code == 404


# --------------------------------------------------
# 7. Get Borrowings - All
# --------------------------------------------------
def test_get_borrowings_all(mock_borrow_execute_many):
    mock_conn = object()

    mock_borrow_execute_many.return_value = [
        {"id": 1},
        {"id": 2}
    ]

    result = borrowing_service.get_borrowings(conn=mock_conn)

    assert len(result) == 2


# --------------------------------------------------
# 8. Get Borrowings - By Status
# --------------------------------------------------
def test_get_borrowings_by_status(mock_borrow_execute_many):
    mock_conn = object()

    mock_borrow_execute_many.return_value = [
        {"id": 1, "status": "BORROWED"}
    ]

    result = borrowing_service.get_borrowings(
        conn=mock_conn,
        status=type("Status", (), {"value": "BORROWED"})()
    )

    assert result[0]["status"] == "BORROWED"


# --------------------------------------------------
# 9. Get Borrowings By Member
# --------------------------------------------------
def test_get_borrowings_by_member(mock_borrow_execute_many):
    mock_conn = object()

    mock_borrow_execute_many.return_value = [
        {"id": 1, "member_id": 1}
    ]

    result = borrowing_service.get_borrowings_by_member(
        conn=mock_conn,
        member_id=1
    )

    assert result[0]["member_id"] == 1


# --------------------------------------------------
# 10. Get Borrowings By Member + Status
# --------------------------------------------------
def test_get_borrowings_by_member_and_status(mock_borrow_execute_many):
    mock_conn = object()

    mock_borrow_execute_many.return_value = [
        {"id": 1, "member_id": 1, "status": "RETURNED"}
    ]

    result = borrowing_service.get_borrowings_by_member(
        conn=mock_conn,
        member_id=1,
        status=type("Status", (), {"value": "RETURNED"})()
    )

    assert result[0]["status"] == "RETURNED"