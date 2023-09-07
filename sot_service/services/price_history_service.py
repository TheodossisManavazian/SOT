import datetime
from typing import Optional

import pydash
import pandas as pd
from sqlalchemy.engine import Connection

from sot_service.daos import price_history_dao
from sot_service.models.ticker import Ticker
from sot_service.utils import datetime_utils
from sot_service.utils.datetime_utils import days_between_dates


def upsert_price_history(conn: Connection, ticker: Ticker) -> None:
    for index, date in ticker.price_history.iterrows():
        request = {
            'open': date['open'],
            'high': date['high'],
            'low': date['low'],
            'close': date['close'],
            'volume': date['volume'],
        }
        epoch = pydash.get(date, 'datetime')
        request.update(
            {
                "datetime": datetime_utils.epoch_to_date(epoch),
                "symbol": ticker.symbol
            }
        )
        price_history_dao.upsert(conn, request)


def delete_price_history(conn: Connection, symbol: str) -> None:
    request = {
        'symbol': symbol
    }
    price_history_dao.remove_symbol_set(conn, request)


def remove_price_history_set(conn: Connection, symbol: str) -> None:
    request = {'symbol': symbol}
    price_history_dao.remove_symbol_set(conn, request)


def get_price_history_dataframe(conn: Connection, symbol: str) -> Optional[pd.DataFrame]:
    request = {'symbol': symbol}
    price_history = price_history_dao.get_price_history(conn, request)
    if len(price_history) == 0:
        return None
    dataframe = pd.DataFrame(price_history)
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
    dataframe.index = dataframe.pop("datetime")
    return dataframe


def get_close_prices_dataframe(conn: Connection, symbol: str) -> Optional[pd.DataFrame]:
    request = {'symbol': symbol}
    price_history = price_history_dao.get_close_prices(conn, request)
    if len(price_history) == 0:
        return None
    dataframe = pd.DataFrame(price_history)
    dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
    dataframe.index = dataframe.pop("datetime")
    return dataframe


# fix logic for this, last_updated is always at 12:00 am
def is_updated_today(conn: Connection, symbol: str) -> bool:
    df = get_price_history_dataframe(conn, symbol)
    if df.empty:
        return False
    last_updated = df.iloc[-1].name.to_pydatetime()
    current_date_time = datetime.datetime.today()
    if days_between_dates(current_date_time.date(), last_updated.date()) > 1:
        return False
    if days_between_dates(current_date_time.date(), last_updated.date()) == 1 and 0 <= current_date_time.hour < 8:
        return True
    if current_date_time.date() == last_updated.date():
        return True
    return False
