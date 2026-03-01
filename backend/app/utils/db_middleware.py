from fastapi import Request
from app.utils.db import get_connection, release_connection

async def db_session_middleware(request: Request, call_next):
    conn = get_connection()
    request.state.db = conn

    try:
        response = await call_next(request)
        conn.commit()
        return response

    except Exception:
        conn.rollback()
        raise

    finally:
        release_connection(conn)