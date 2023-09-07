import datetime

from sqlalchemy import text
from sqlalchemy.engine import Connection

from sot_service.daos import completed_trades_dao
from sot_service.models.ticker import Ticker

# TODO: DEPRECATE

def insert_new_trade(conn: Connection, ticker: Ticker, bought_position: dict) -> None:
    equity = ticker.last_price * bought_position['quantity']
    request = {
        'symbol': ticker.symbol,
        'quantity': bought_position['quantity'],
        'last_price': ticker.last_price,
        'equity': equity,
        'profit': equity - bought_position['equity'],
        'strategy': bought_position['strategy'],
        'updated_at': datetime.datetime.now()
    }

    completed_trades_dao.insert_new_trade(conn, request)
