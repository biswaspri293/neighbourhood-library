import pytest
from unittest.mock import patch, MagicMock


# -------------------------------------------------
# BLOCK REAL DATABASE CONNECTION
# -------------------------------------------------

@pytest.fixture(autouse=True)
def block_real_db():
    with patch("psycopg2.connect") as mock_connect:
        mock_connect.side_effect = Exception(
            "Real database connection is blocked in unit tests"
        )
        yield


# -------------------------------------------------
# BOOK SERVICE MOCKS
# -------------------------------------------------

@pytest.fixture
def mock_book_execute_one():
    with patch("app.services.book_service.execute_and_return_one") as mock:
        yield mock


@pytest.fixture
def mock_book_execute_many():
    with patch("app.services.book_service.execute_and_return_many") as mock:
        yield mock


# -------------------------------------------------
# MEMBER SERVICE MOCKS
# -------------------------------------------------

@pytest.fixture
def mock_member_execute_one():
    with patch("app.services.member_service.execute_and_return_one") as mock:
        yield mock


@pytest.fixture
def mock_member_execute_many():
    with patch("app.services.member_service.execute_and_return_many") as mock:
        yield mock


# -------------------------------------------------
# BORROWING SERVICE MOCKS
# -------------------------------------------------

@pytest.fixture
def mock_borrow_execute_one():
    with patch("app.services.borrowing_service.execute_and_return_one") as mock:
        yield mock


@pytest.fixture
def mock_borrow_execute_many():
    with patch("app.services.borrowing_service.execute_and_return_many") as mock:
        yield mock


@pytest.fixture
def mock_db_connection():
    with patch("app.services.borrowing_service.get_connection") as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()

        mock_get_conn.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

        yield mock_cursor