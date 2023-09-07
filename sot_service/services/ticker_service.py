from typing import List

import pydash as pydash
from sqlalchemy.engine import Connection

from sot_service.daos import ticker_dao
from sot_service.models.ticker import Ticker
from sot_service.services import price_history_service


def upsert_ticker(conn: Connection, ticker: Ticker) -> None:
    request = {
        'symbol': ticker.symbol,
        'cusip': pydash.get(ticker.quote, 'cusip'),
        'asset_type': pydash.get(ticker.quote, 'assetType'),
        'description': pydash.get(ticker.quote, 'description'),
        'exchange_name': pydash.get(ticker.quote, 'exchangeName')
    }
    ticker_dao.upsert(conn, request)


def delete_ticker(conn: Connection, symbol: str) -> None:
    request = {
        'symbol': symbol
    }
    ticker_dao.delete(conn, request)
    price_history_service.delete_price_history(conn, symbol)


def get_ticker(conn: Connection, symbol: str) -> dict:
    request = {'symbol': symbol}
    return ticker_dao.get(conn, request)


def get_all_tickers(conn: Connection) -> List[dict]:
    return ticker_dao.get_all(conn)
