import datetime
from time import sleep

from sot_service import engine
from sot_service.daos import ticker_dao
from sot_service.models.ticker import Ticker
from sot_service.services import ticker_service, price_history_service


def upsert_initial_tickers():
    with engine.connect() as conn:
        tickers = ticker_dao.get_all(conn)
        for s in tickers:
            symbol = s['symbol']
            if price_history_service.is_updated_today(conn, symbol):
                continue
            ticker = Ticker(symbol)
            ticker_service.upsert_ticker(conn, ticker)
            price_history_service.upsert_price_history(conn, ticker)
            sleep(1)


if __name__ == '__main__':
    upsert_initial_tickers()
