import os
import threading

import mysql.connector
from mysql.connector import Error, pooling

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "MyStrongPassword123"),
    "database": os.getenv("DB_NAME", "todo_db"),
}

POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))

_connection_pool = None
_pool_lock = threading.Lock()


def _get_pool():
    global _connection_pool
    if _connection_pool is None:
        with _pool_lock:
            if _connection_pool is None:
                _connection_pool = pooling.MySQLConnectionPool(
                    pool_name="todo_pool",
                    pool_size=POOL_SIZE,
                    pool_reset_session=True,
                    **DB_CONFIG,
                )
    return _connection_pool


def get_connection():
    """Borrow a connection from the pool."""
    try:
        return _get_pool().get_connection()
    except Error as e:
        print("Database connection error:", e)
        raise


def close_db(cursor, conn):
    """Close cursor and return connection to the pool (not destroyed)."""
    if cursor:
        cursor.close()
    if conn and conn.is_connected():
        conn.close()
