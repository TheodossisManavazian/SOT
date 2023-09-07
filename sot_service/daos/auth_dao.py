from sqlalchemy import text
from sqlalchemy.engine import Connection

from sot_service.utils import db_utils


def lookup_key(conn: Connection, auth_header: dict) -> dict:
    sql = """
        SELECT id
        FROM auth.users
        WHERE token = :token
    """

    result = conn.execute(text(sql), auth_header).fetchone()
    return db_utils.single_nullable_result(result)
