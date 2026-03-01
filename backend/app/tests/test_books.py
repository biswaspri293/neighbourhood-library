import pytest
from fastapi import HTTPException
from app.services import book_service
from app.utils.schemas import BookCreate, BookUpdate


# -------------------------------------------------
# Create Book
# -------------------------------------------------

def test_create_book_success(mock_book_execute_one):
    mock_conn = object()
    mock_book_execute_one.return_value = {
        "id": 1,
        "title": "Test",
        "author": "Author",
        "total_copies": 5,
        "available_copies": 5,
    }

    data = BookCreate(title="Test", author="Author", total_copies=5)

    result = book_service.create_book(mock_conn, data)

    assert result["id"] == 1
    assert result["available_copies"] == 5


# -------------------------------------------------
# Delete Book Blocked (Active Borrow Exists)
# -------------------------------------------------

def test_delete_book_blocked(mock_book_execute_one):
    mock_book_execute_one.side_effect = [
        {"exists": 1}
    ]

    with pytest.raises(HTTPException):
        book_service.delete_book(conn=None, book_id=1)


# -------------------------------------------------
# Delete Book Success
# -------------------------------------------------

def test_delete_book_success(mock_book_execute_one):
    mock_book_execute_one.side_effect = [
        None,
        {"id": 1}
    ]

    result = book_service.delete_book(conn=None, book_id=1)

    assert result["id"] == 1



def test_update_book_success(mock_book_execute_one):
    mock_conn = object()

    # 1st call → fetch existing book
    # 2nd call → return updated book
    mock_book_execute_one.side_effect = [
        {
            "id": 1,
            "title": "Old Title",
            "author": "Old Author",
            "total_copies": 5,
            "available_copies": 5,
        },
        {
            "id": 1,
            "title": "New Title",
            "author": "New Author",
            "total_copies": 10,
            "available_copies": 5,
        },
    ]

    data = BookUpdate(
        title="New Title",
        author="New Author",
        total_copies=10
    )

    result = book_service.update_book(mock_conn, 1, data)

    assert result["title"] == "New Title"
    assert result["total_copies"] == 10


# -------------------------------------------------
# Update Book - Not Found
# -------------------------------------------------

def test_update_book_not_found(mock_book_execute_one):
    mock_conn = object()

    # First query returns None → book not found
    mock_book_execute_one.return_value = None

    data = BookUpdate(
        title="New",
        author="New",
        total_copies=5
    )

    with pytest.raises(HTTPException) as exc:
        book_service.update_book(mock_conn, 1, data)

    assert exc.value.status_code == 404

