import pytest
from fastapi import HTTPException
from app.services import member_service
from app.utils.schemas import MemberCreate, MemberUpdate

# -------------------------------------------------
# Create member success
# -------------------------------------------------


def test_create_member_success(mock_member_execute_one):
    mock_conn = object()

    mock_member_execute_one.return_value = {
        "id": 1,
        "name": "John",
        "email": "john@test.com",
        "phone": "123",
    }

    data = MemberCreate(
        name="John",
        email="john@test.com",
        phone="123"
    )

    result = member_service.create_member(mock_conn, data)

    assert result["id"] == 1
    assert result["email"] == "john@test.com"


# -------------------------------------------------
# Create member duplicate email
# -------------------------------------------------


def test_create_member_duplicate_email(mock_member_execute_one):
    mock_conn = object()

    mock_member_execute_one.side_effect = HTTPException(
        status_code=409,
        detail="Email already exists"
    )

    data = MemberCreate(
        name="John",
        email="john@test.com",
        phone="123"
    )

    with pytest.raises(HTTPException) as exc:
        member_service.create_member(mock_conn, data)

    assert exc.value.status_code == 409

# -------------------------------------------------
# Get Member list Success
# -------------------------------------------------


def test_get_members_list(mock_member_execute_many):
    mock_conn = object()

    mock_member_execute_many.return_value = [
        {"id": 1, "name": "A"},
        {"id": 2, "name": "B"},
    ]

    result = member_service.get_members(conn=mock_conn)

    assert len(result) == 2


# -------------------------------------------------
# Get Member  by id Success
# -------------------------------------------------

def test_get_member_by_id_success(mock_member_execute_one):
    mock_conn = object()

    mock_member_execute_one.return_value = {
        "id": 1,
        "name": "John",
        "email": "john@test.com",
        "phone": None,
    }

    result = member_service.get_member_by_id(conn=mock_conn, member_id=1)

    assert result["id"] == 1

# -------------------------------------------------
# Get Member - id not found
# -------------------------------------------------

def test_get_member_by_id_not_found(mock_member_execute_one):
    mock_conn = object()

    mock_member_execute_one.return_value = None

    with pytest.raises(HTTPException) as exc:
        member_service.get_member_by_id(conn=mock_conn, member_id=1)

    assert exc.value.status_code == 404

# -------------------------------------------------
# Update Member Success
# -------------------------------------------------

def test_update_member_success(mock_member_execute_one):
    mock_conn = object()

    # First call → existing
    # Second call → updated
    mock_member_execute_one.side_effect = [
        {
            "id": 1,
            "name": "Old",
            "email": "old@test.com",
            "phone": None,
        },
        {
            "id": 1,
            "name": "New",
            "email": "new@test.com",
            "phone": "123",
        },
    ]

    data = MemberUpdate(
        name="New",
        email="new@test.com",
        phone="123"
    )

    result = member_service.update_member(mock_conn, 1, data)

    assert result["name"] == "New"
    assert result["email"] == "new@test.com"


# -------------------------------------------------
# Update Member Not Found
# -------------------------------------------------

def test_update_member_not_found(mock_member_execute_one):
    mock_conn = object()

    mock_member_execute_one.return_value = None

    data = MemberUpdate(
        name="New",
        email="new@test.com",
        phone="123"
    )

    with pytest.raises(HTTPException):
        member_service.update_member(mock_conn, 1, data)