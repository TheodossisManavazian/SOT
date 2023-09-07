from typing import Optional, List

from sqlalchemy import text
from sqlalchemy.engine import Connection

from sot_service.utils import db_utils


def insert_new_position(conn: Connection, request: dict) -> None:
    sql = """
        INSERT INTO jaat.current_positions(
            symbol,
            strategy,
            quantity,
            price_per_share,
            equity
        ) VALUES (
            :symbol,
            :strategy,
            :quantity,
            :price_per_share,
            :equity
        )
    """
    conn.execute(text(sql), request)


def delete_position(conn: Connection, request: dict) -> dict:
    sql = """
        DELETE FROM jaat.current_positions as t
        WHERE symbol = :symbol AND strategy = :strategy
        RETURNING 
            symbol,
            strategy,
            quantity,
            price_per_share,
            equity
    """
    result = conn.execute(text(sql), request).fetchone()
    return db_utils.single_nullable_result(result)


def get_position_by_symbol_and_strategy(conn: Connection, request: dict) -> Optional[dict]:
    sql = """
        SELECT 
            symbol,
            strategy,
            quantity,
            price_per_share,
            equity
        FROM jaat.current_positions
        WHERE symbol = :symbol
        AND strategy = :strategy
    """

    results = conn.execute(text(sql), request).fetchone()
    return db_utils.single_nullable_result(results)


def get_position_by_symbol(conn: Connection, request: dict) -> Optional[dict]:
    sql = """
        SELECT 
            symbol,
            strategy,
            quantity,
            price_per_share,
            equity
        FROM jaat.current_positions
        WHERE symbol = :symbol
    """

    results = conn.execute(text(sql), request).fetchall()
    return db_utils.list_results(results)


def get_all_positions(conn: Connection) -> Optional[List[dict]]:
    sql = """
        SELECT * FROM jaat.current_positions
    """
    results = conn.execute(text(sql)).fetchall()
    return db_utils.list_results(results)
