from typing import List

from sqlalchemy.engine import Connection
from sqlalchemy import text

from sot_service.utils import db_utils


def upsert(conn: Connection, request: dict) -> None:
    sql = """
        INSERT INTO ticker.price_history (
            symbol,
            open,
            high,
            low,
            close,
            volume,
            datetime
        ) VALUES (
            :symbol,
            :open,
            :high,
            :low,
            :close,
            :volume,
            :datetime
        ) 
        ON CONFLICT (datetime, symbol) DO UPDATE
        SET 
            symbol = EXCLUDED.symbol,
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume,
            datetime = EXCLUDED.datetime 
    """

    conn.execute(text(sql), request)


def remove_symbol_set(conn: Connection, request: dict) -> None:
    sql = """
        DELETE FROM ticker.price_history
        WHERE symbol = :symbol
    """
    conn.execute(text(sql), request)


def get_price_history(conn: Connection, request: dict) -> List[dict]:
    sql = """
        SELECT
            datetime,
            symbol,
            open,
            high,
            low,
            close,
            volume
        FROM ticker.price_history
        WHERE symbol = :symbol
        ORDER BY datetime ASC
        
    """
    result = conn.execute(text(sql), request).fetchall()
    return db_utils.list_results(result)


def get_close_prices(conn: Connection, request: dict) -> List[dict]:
    sql = """
        SELECT
            datetime,
            close
        FROM ticker.price_history
        WHERE symbol = :symbol
        ORDER BY datetime ASC

    """
    result = conn.execute(text(sql), request).fetchall()
    return db_utils.list_results(result)

