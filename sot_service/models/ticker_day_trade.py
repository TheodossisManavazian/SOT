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

    price_history_weekly: DataFrame
    price_history_daily: DataFrame
    price_history_intraday: DataFrame

    ema_8_daily: float
    ema_8_weekly: float
    ema_8_intraday_5: float
    ema_8_intraday_30: float

    def __init__(self, symbol):
        self.symbol = symbol.upper()
        self.quote = self.try_get_quote(self.symbol)
        self.last_price = float(pydash.get(self.quote, 'lastPrice'))

        self.price_history_daily = self._get_price_history(client.PriceHistory.PeriodType.YEAR, client.PriceHistory.Period.ONE_YEAR, client.PriceHistory.FrequencyType.DAILY, client.PriceHistory.Frequency.DAILY)
        self.price_history_weekly = self._get_price_history(client.PriceHistory.PeriodType.YEAR, client.PriceHistory.Period.ONE_YEAR, client.PriceHistory.FrequencyType.WEEKLY, client.PriceHistory.Frequency.DAILY)

        # Probably makes more sense to get a 15 min chart and use it for both intraday 15 and 60 -- will change later
        self.price_history_intraday_5 = self._get_price_history(client.PriceHistory.PeriodType.DAY, client.PriceHistory.Period.ONE_DAY, client.PriceHistory.FrequencyType.MINUTE, client.PriceHistory.Frequency.EVERY_FIVE_MINUTES)
        self.price_history_intraday_30 = self._get_price_history(client.PriceHistory.PeriodType.DAY, client.PriceHistory.Period.ONE_DAY, client.PriceHistory.FrequencyType.MINUTE, client.PriceHistory.Frequency.EVERY_THIRTY_MINUTES)

        # Calc EMA
        self.ema_8_daily = self.calculate_exponential_moving_average(self.price_history_daily, 8)
        self.ema_8_weekly = self.calculate_exponential_moving_average(self.price_history_weekly, 8)
        self.ema_8_intraday_5 = self.calculate_exponential_moving_average(self.price_history_intraday_5, 8)
        self.ema_8_intraday_30 = self.calculate_exponential_moving_average(self.price_history_intraday_30, 8)

        self.fundamentals = pydash.get(client.search_instruments([symbol], client.Instrument.Projection.FUNDAMENTAL).json(), f'{symbol}.fundamental')


    @staticmethod
    def try_get_quote(symbol) -> Optional[dict]:
        quote = client.get_quote(symbol).json()
        if not quote:
            raise InvalidTickerException()
        return pydash.get(quote, symbol)

    @staticmethod
    def calculate_exponential_moving_average(df: DataFrame, period: int) -> float:
        return round(float(df.Close.ewm(span=period, adjust=False).mean().iloc[-1]), 4)

    def _get_price_history(self,
                           period_type: client.PriceHistory.PeriodType,
                           period: client.PriceHistory.Period,
                           frequency_type: client.PriceHistory.FrequencyType,
                           frequency: client.PriceHistory.Frequency
    ):
        col_names = {'close' : 'Close', 'high': 'High', 'low': 'Low', 'open': 'Open', 'volume': 'Volume', 'datetime': 'Datetime'}
        frame = pd.DataFrame(client.get_price_history(
            self.symbol,
            period_type=period_type,
            period=period,
            frequency_type=frequency_type,
            frequency=frequency,
            start_datetime=None,
            end_datetime=datetime.datetime.today(),
            need_extended_hours_data=None
        ).json()['candles'])

        frame.rename(columns= col_names, inplace=True)
        return frame
