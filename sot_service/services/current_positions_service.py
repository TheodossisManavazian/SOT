from typing import Optional, List

from sqlalchemy.engine import Connection

from sot_service.daos import current_positions_dao

from sot_service.models.ticker import Ticker


def insert_position(conn: Connection, ticker: Ticker, quantity: int, strategy: str)-> None:
    equity = ticker.last_price * quantity
    request = {
        'symbol': ticker.symbol,
        'strategy': strategy,
        'quantity': quantity,
        'price_per_share': ticker.last_price,
        'equity': equity
    }
    current_positions_dao.insert_new_position(conn, request)


def get_position_by_symbol_and_strategy(conn: Connection, symbol: str, strategy: str) -> Optional[dict]:
    request = {
        'symbol': symbol,
        'strategy': strategy
    }
    return current_positions_dao.get_position_by_symbol_and_strategy(conn, request)


def get_positions_by_symbol(conn: Connection, symbol: str) -> Optional[dict]:
    request = {
        'symbol': symbol,
    }
    positions = current_positions_dao.get_position_by_symbol(conn, request)
    formatted_positions = {}
    for position in positions:
        formatted_positions[position['strategy']] = position
    return formatted_positions


def remove_position(conn: Connection, symbol: str, strategy: str) -> dict:
    request = {
        'symbol': symbol,
        'strategy': strategy
    }

    return current_positions_dao.delete_position(conn, request)


def get_all_positions(conn: Connection) -> Optional[List[dict]]:
    return current_positions_dao.get_all_positions(conn)
