from typing import Optional, List
from sqlalchemy.engine import Connection
from sqlalchemy import text

from sot_service.utils import db_utils


def upsert(conn: Connection, ticker: dict) -> None:
    sql = """
        INSERT INTO ticker.ticker(
            symbol,
            cusip,
            asset_type,
            description,
            exchange_name
        ) values (
            :symbol,
            :cusip,
            :asset_type,
            :description,
            :exchange_name
        ) ON CONFLICT (symbol)
        DO UPDATE
        SET
            symbol = EXCLUDED.symbol,
            cusip = EXCLUDED.cusip,
            asset_type = EXCLUDED.asset_type,
            description = EXCLUDED.description,
            exchange_name = EXCLUDED.exchange_name
    """
    conn.execute(text(sql), ticker)


def get(conn: Connection, request: dict) -> Optional[dict]:
    sql = """
        SELECT
            symbol,
            cusip,
            asset_type,
            description,
            exchange_name
        FROM ticker.ticker
        WHERE symbol = :symbol
    """

    result = conn.execute(text(sql), request).fetchone()
    return db_utils.single_nullable_result(result)


def get_all(conn: Connection) -> List[dict]:
    sql = """
        SELECT
            symbol
        FROM ticker.ticker
    """
    result = conn.execute(text(sql)).fetchall()
    return db_utils.list_results(result)


def delete(conn: Connection, request: dict) -> None:
    sql = """
        DELETE FROM ticker.ticker
        WHERE symbol = :symbol
    """

    conn.execute(text(sql), request)
