from datetime import datetime
from typing import Optional

from sqlalchemy.engine import Connection

from sot_service.daos import completed_trades_dao
from sot_service.models.ticker import Ticker
from sot_service.services import current_positions_service

import logging


def add_to_position(conn: Connection, ticker: Ticker, quantity: int,  strategy: str) -> None:
    current_positions_service.insert_position(conn, ticker, quantity, strategy)
    logging.info(f"ADDING TO POSITION \n {ticker.symbol} | {quantity} @ ${ticker.last_price} USING {strategy}")


def remove_from_position(conn: Connection, ticker: Ticker, strategy: str) -> dict:
    open_position = current_positions_service.remove_position(conn, ticker.symbol, strategy)

    equity = ticker.last_price * open_position['quantity']
    profit = equity - float(open_position['equity'])
    sell = {
        'symbol': ticker.symbol,
        'quantity': open_position['quantity'],
        'bought_price_per_share': open_position['price_per_share'],
        'sold_price_per_share': ticker.last_price,
        'equity': equity,
        'realized_gain': profit,
        'percent_gain': (profit / float(open_position['equity'])) * 100.0,
        'transaction_type': "SELL",
        'strategy': strategy,
        'updated_at': datetime.now()
    }
    completed_trades_dao.insert_new_trade(conn, sell)
    return open_position
