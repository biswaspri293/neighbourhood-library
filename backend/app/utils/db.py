from psycopg2 import pool
from app.utils.config import DATABASE_CONFIG

connection_pool = None


def get_pool():
    global connection_pool

    if connection_pool is None:
        connection_pool = pool.SimpleConnectionPool(
            1,
            10,
            **DATABASE_CONFIG
        )

    return connection_pool


def get_connection():
    return get_pool().getconn()


def release_connection(conn):
    get_pool().putconn(conn)


def close_pool():
    if connection_pool:
        connection_pool.closeall()


# -------------------------------------------------------
# Execute INSERT/UPDATE/DELETE returning single row
# -------------------------------------------------------
def execute_and_return_one(conn, query: str, params=None):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            result = cursor.fetchone()

            if not result:
                return None

            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))


# -------------------------------------------------------
# Execute query returning multiple rows
# -------------------------------------------------------
def execute_and_return_many(conn, query: str, params=None):
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in rows]