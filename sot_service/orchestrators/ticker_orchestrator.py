from sot_service.services import ticker_service, price_history_service
from sqlalchemy.engine import Connection
from sot_service.models.ticker import Ticker


def upsert_ticker(conn: Connection, ticker: Ticker) -> None:
    with conn.begin():
        ticker_service.upsert_ticker(conn, ticker)
        price_history_service.upsert_price_history(conn, ticker)


def delete_ticker(conn: Connection, symbol: str) -> None:
    with conn.begin():
        price_history_service.delete_price_history(conn, symbol)
        ticker_service.delete_ticker(conn, symbol)

