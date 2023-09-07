import datetime
from typing import Optional

import pydash

import pandas as pd
from pandas import DataFrame
from client import client
from sot_service.utils.exceptions import InvalidTickerException


class Ticker:
    symbol: str
    last_price: float
    quote: Optional[dict]
    price_history: DataFrame
    fundamentals: Optional[dict]
    intraday: bool

    def __init__(self, symbol: str, intraday: bool = False):
        self.symbol = symbol.upper()
        if not intraday:
            self.quote = self.try_get_quote(self.symbol)
            self.price_history = self._get_price_history(intraday)
            self.fundamentals = pydash.get(client.search_instruments([symbol], client.Instrument.Projection.FUNDAMENTAL).json(), f'{symbol}.fundamental')
            self.last_price = float(pydash.get(self.quote, 'lastPrice'))
            self.intraday = False
        else:
            self.intraday = True
            self.price_history = self._get_price_history(intraday)
            self.last_price = self.price_history.iloc[-1]['close']


    @staticmethod
    def try_get_quote(symbol) -> Optional[dict]:
        quote = client.get_quote(symbol).json()
        if not quote:
            raise InvalidTickerException()
        return pydash.get(quote, symbol)

    def _get_price_history(self, day):
        # period_type = client.PriceHistory.PeriodType.YEAR
        # period = client.PriceHistory.Period.ONE_YEAR
        # frequency_type = client.PriceHistory.FrequencyType.DAILY
        # frequency = client.PriceHistory.Frequency.DAILY

        period = client.PriceHistory.Period.TEN_DAYS
        period_type = client.PriceHistory.PeriodType.DAY
        frequency = client.PriceHistory.Frequency.EVERY_THIRTY_MINUTES
        frequency_type = client.PriceHistory.FrequencyType.MINUTE

        if day:
            period = client.PriceHistory.Period.ONE_DAY
            period_type = client.PriceHistory.PeriodType.DAY
            frequency = client.PriceHistory.Frequency.EVERY_MINUTE
            frequency_type = client.PriceHistory.FrequencyType.MINUTE

        return pd.DataFrame(client.get_price_history(
            self.symbol,
            period_type=period_type,
            period=period,
            frequency_type=frequency_type,
            frequency=frequency,
            start_datetime=None,
            end_datetime=datetime.datetime.today(),
            need_extended_hours_data=None
        ).json()['candles'])


def try_create_ticker(symbol) -> Optional[Ticker]:
    try:
        ticker = Ticker(symbol)
        return ticker
    except InvalidTickerException:
        return None
