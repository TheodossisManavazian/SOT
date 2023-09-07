from typing import List, Union, Optional

import numpy
import numpy as np
from pandas import DataFrame, Series

from sot_service.models.internal_ticker import InternalTicker
from sot_service.models.ticker import Ticker
import talib


class TechnicalAnalysis:
    ticker: Union[Ticker, InternalTicker]
    rsi: float
    sma_200: float
    sma_50: float
    ema_15: float
    macd_value: float
    macd_signal: float
    vwap: float
    momentum_10: float
    stddev: float

    resistances: list
    support: float
    resistance: float
    percent_away_from_support: float
    percent_away_from_resistance: float

    risk_assessment: int
    technicals: dict
    forecast: list

    # hammer: int
    # engulf: int

    def __init__(self, ticker: Union[Ticker, InternalTicker]):
        self.ticker = ticker
        self.rsi = self.calculate_rsi(ticker)
        self.sma_200 = self.calculate_moving_average(ticker, 200)
        self.sma_50 = self.calculate_moving_average(ticker, 50)
        self.ema_15 = self.calculate_exponential_moving_average(ticker, 15)
        # self.momentum_10 = self.get_momentum(ticker, 10)
        # self.stddev = self.get_stddev(ticker, 5, 2)
        # self.forecast = self.get_forecast(ticker, 10)
        if ticker.intraday:
            self.vwap = self.calculate_vwap(ticker)
        else:
            self.vwap = -1

        self.resistances = self.calculate_support_and_resistance(ticker)
        self.support, self.resistance = self.get_next_set_of_resistances(ticker, self.resistances)
        self.percent_away_from_support, self.percent_away_from_resistance = self.calculate_percent_off_resistances(ticker, self.support, self.resistance)
        self.macd_value, self.macd_signal = self.calculate_macd_vals(ticker)
        self.technicals = self._technicals_to_dict()
        self.risk_assessment = self._evaluate_risk()

        # self.hammer = self.hammer(ticker)
        # self.engulf = self.engulf(ticker)


    def _technicals_to_dict(self):
        return {
            'rsi': self.rsi,
            'sma_200': self.sma_200,
            'sma_50': self.sma_50,
            'ema_15': self.ema_15,
            'resistance': {
                'support': self.support,
                'percent_away_from_support': self.percent_away_from_support,
                'resistance': self.resistance,
                'percent_away_from_resistance': self.percent_away_from_resistance
            },
            'macd': {
                'value': self.macd_value,
                'signal': self.macd_signal
            }
        }

    @staticmethod
    def calculate_moving_average(ticker: Ticker, time: int) -> float:
        CLOSE = 'Close'
        if 'close' in ticker.price_history.columns:
            CLOSE = 'close'

        close_prices = ticker.price_history[CLOSE].to_frame()
        close_prices[f'moving_average_{time}'] = close_prices[CLOSE].rolling(time).mean()
        return round(float(close_prices[f'moving_average_{time}'].iloc[-1]), 4)

    # @staticmethod
    # def get_momentum(ticker: Ticker, time: int) -> float:
    #     closes = ticker.price_history['close']
    #     return talib.MOM(closes, time).iloc[-1]
    #
    # @staticmethod
    # def get_stddev(ticker: Ticker, time: int, num_dev: int) -> float:
    #     closes = ticker.price_history['close']
    #     return talib.STDDEV(closes, time, nbdev=num_dev).iloc[-1]
    #
    # @staticmethod
    # def get_forecast(ticker: Ticker, time: int) -> list:
    #     closes = ticker.price_history['close']
    #     return talib.TSF(closes, time)

    @staticmethod
    def calculate_vwap(ticker: Ticker) -> float:
        VOLUME, CLOSE, HIGH, LOW = 'Volume', 'Close', 'High', 'Low'
        if 'close' in ticker.price_history.columns:
            VOLUME, CLOSE, HIGH, LOW = 'volume', 'close', 'high', 'low'

        df = ticker.price_history
        v = df[VOLUME].values
        tp = (df[LOW] + df[CLOSE] + df[HIGH]).div(3).values
        return df.assign(vwap=(tp * v).cumsum() / v.cumsum()).iloc[-1]['vwap']

    @staticmethod
    def calculate_rsi(ticker: Ticker, periods: int = 14) -> float:
        CLOSE = 'Close'
        if 'close' in ticker.price_history.columns:
            CLOSE = 'close'

        close_diff = ticker.price_history[CLOSE].diff()

        change_up = close_diff.clip(lower=0)
        change_down = -1 * close_diff.clip(upper=0)

        up = change_up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
        down = change_down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

        rsi = up / down
        rsi = 100 - (100 / (1 + rsi))
        return round(float(rsi.iloc[-1]), 4)

    @staticmethod
    def calculate_support_and_resistance(ticker: Ticker) -> List[tuple]:
        price_history = ticker.price_history
        OPEN, HIGH, LOW, CLOSE = 'Open', 'High', 'Low', 'Close'
        if 'close' in price_history.columns:
            OPEN, HIGH, LOW, CLOSE = 'open', 'high', 'low', 'close'

        def is_support(df, i):
            support = df[LOW][i] < df[LOW][i - 1] < df[LOW][i - 2] and \
                      df[LOW][i] < df[LOW][i + 1] < df[LOW][i + 2]
            return support

        def is_resistance(df, i):
            resistance = df[HIGH][i] > df[HIGH][i - 1] > df[HIGH][i - 2] and \
                         df[HIGH][i] > df[HIGH][i + 1] > df[HIGH][i + 2]
            return resistance

        s = np.mean(price_history[HIGH] - price_history[LOW])

        def is_far_from_level(level):
            return np.sum([abs(level - x[1]) < s for x in levels]) == 0

        levels = []
        for index in range(2, price_history.shape[0] - 2):
            if is_support(price_history, index):
                price = float(price_history[LOW][index])
                if is_far_from_level(price):
                    levels.append((index, price))
            elif is_resistance(price_history, index):
                price = float(price_history[HIGH][index])
                if is_far_from_level(price):
                    levels.append((index, price))

        return sorted(levels, key=lambda x: x[1])

    @staticmethod
    def calculate_exponential_moving_average(ticker: Ticker, period: int = 15) -> float:
        CLOSE = "Close"
        if 'close' in ticker.price_history.columns:
            CLOSE = 'close'
        return round(float(ticker.price_history[CLOSE].ewm(span=period, adjust=False).mean().iloc[-1]), 4)

    @staticmethod
    def calculate_macd_lines(ticker: Ticker) -> tuple:
        CLOSE = "Close"
        if 'close' in ticker.price_history.columns:
            CLOSE = 'close'
        exp1 = ticker.price_history[CLOSE].ewm(span=12, adjust=False).mean()
        exp2 = ticker.price_history[CLOSE].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
        return macd, exp3

    @staticmethod
    def calculate_macd_vals(ticker: Ticker) -> tuple:
        macd_lines = TechnicalAnalysis.calculate_macd_lines(ticker)
        return round(macd_lines[0].iloc[-1], 3), round(macd_lines[1].iloc[-1], 3)

    def _evaluate_risk(self) -> int:
        price = self.ticker.last_price
        score = 0
        if price > self.sma_50:
            score += 1
        else:
            score -= 1
        if price > self.sma_200:
            score += 1
        else:
            score -= 1
        if self.sma_50 > self.sma_200:
            score += 1
        else:
            score -= 1
        if self.rsi <= 30:
            score += 1
        if self.rsi >= 70:
            score -= 1

        if self.macd_value > 0:
            score += 1
        else:
            score -= 1

        if self.macd_value > self.macd_signal:
            score += 1
        else:
            score -= 1
        return score

    @staticmethod
    def get_next_set_of_resistances(ticker: Ticker, resistances: List[tuple]) -> Optional[tuple]:
        high, low = 'High', 'Low'
        if 'high' in ticker.price_history.columns:
            high, low = 'high', 'low'

        nearest_supp = 0
        nearest_res = 0
        for level in resistances:
            if ticker.last_price >= level[1]:
                nearest_supp = level[1]
            if ticker.last_price <= level[1]:
                nearest_res = level[1]
                break

        if nearest_res == 0.0:
            nearest_res = max(ticker.price_history[high])
        if nearest_supp == 0.0:
            nearest_supp = min(ticker.price_history[low])

        return round(nearest_supp, 2), round(nearest_res, 2)

    @staticmethod
    def calculate_percent_off_resistances(ticker: Ticker, nearest_support: float, nearest_resistance: float) -> tuple:
        percent_off_resist = round((abs(ticker.last_price - nearest_resistance) /
                                    ((ticker.last_price + nearest_resistance) / 1)) * 100, 2)

        percent_off_supp = round((abs(ticker.last_price - nearest_support) /
                                  ((ticker.last_price + nearest_support) / 1)) * 100, 2)

        return round(percent_off_supp, 2), round(percent_off_resist, 2)


    # @staticmethod
    # def hammer(ticker: Ticker) -> int:
    #     close = ticker.price_history.close
    #     open = ticker.price_history.open
    #     high = ticker.price_history.high
    #     low = ticker.price_history.low
    #
    #     return talib.CDLHAMMER(open, high, low, close).iloc[-1]
    #
    # @staticmethod
    # def engulf(ticker: Ticker) -> int:
    #     close = ticker.price_history.close
    #     open = ticker.price_history.open
    #     high = ticker.price_history.high
    #     low = ticker.price_history.low
    #
    #     return talib.CDLENGULFING(open, high, low, close).iloc[-1]