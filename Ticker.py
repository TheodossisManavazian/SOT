import datetime

import matplotlib.dates as mpl_dates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc

pd.set_option("display.max_rows", 1000, "display.max_columns", 10)


# these two functions are defined outside, so we can run tests on them.
def set_moving_average(df, time):
    close_prices = df.tolist()
    total = sum(close_prices[-time:])
    return float(round(total / time, 2))


# Uses Exponential moving average to calculate RSI, not Simple Moving average.
def set_rsi(df, periods=14):
    close_diff = df.diff()

    change_up = close_diff.clip(lower=0)
    change_down = -1 * close_diff.clip(upper=0)

    up = change_up.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()
    down = change_down.ewm(com=periods - 1, adjust=True, min_periods=periods).mean()

    rsi = up / down
    rsi = 100 - (100 / (1 + rsi))
    return float(round(rsi.iloc[-1], 3))


class Ticker:
    def __init__(self, client, ticker, yrs=""):

        self.symbol = (ticker.upper()).replace('/', "")

        period = client.PriceHistory.Period.ONE_YEAR

        # if yrs == "1 Month":
        #     period = client.PriceHistory.Period.ONE_MONTH
        # elif yrs == '6 Months':
        #     period = client.PriceHistory.Period.SIX_MONTHS
        if yrs == "1 Year":
            period = client.PriceHistory.Period.ONE_YEAR
        elif yrs == '2 Years':
            period = client.PriceHistory.Period.TWO_YEARS
        elif yrs == "5 Years":
            period = client.PriceHistory.Period.FIVE_YEARS
        elif yrs == '10 Years':
            period = client.PriceHistory.Period.TEN_YEARS
        elif yrs == '20 Years':
            period = client.PriceHistory.Period.TWENTY_YEARS
        else:
            period = client.PriceHistory.Period.ONE_YEAR

        # Price history for ticker
        self.priceHistoryRequest = client.get_price_history(
            self.symbol,
            period_type=client.PriceHistory.PeriodType.YEAR,
            period= period,
            frequency_type=client.PriceHistory.FrequencyType.DAILY,
            frequency=client.PriceHistory.Frequency.DAILY,
            start_datetime=None,
            end_datetime=None,
            need_extended_hours_data=None
        )
        print("REQUEST CODE:", self.priceHistoryRequest)

        self.priceHistory = pd.DataFrame(self.priceHistoryRequest.json())
        # Current Quote
        try:
            self.quote = client.get_quote(ticker).json()[self.symbol]
            print("QUOTE", self.quote)
        except Exception as e:
            print("symbol not found in quote,", e)
            self.quote = client.get_quote(ticker).json()

        # Fundamentals
        self.fundamentals = client.search_instruments(self.symbol,
                                                      projection=client.Instrument.Projection.FUNDAMENTAL).json()[
            self.symbol]['fundamental']

        # Sets dates for price history
        self.epochs = self.priceHistory['candles'].apply(pd.Series)['datetime'].tolist()
        self.dateRange = list(map(self.epoch_to_datetime, self.epochs))
        self.dateRangeDF = pd.DataFrame(self.dateRange, columns=['date'])

        # Cleans the price history
        self.candles = self.priceHistory['candles'].apply(pd.Series)
        self.cleanPriceHistory = self.set_clean_price_history()

        # Quick attributes
        self.description = f'$({self.symbol}) - {self.quote["description"]}'
        self.lastPrice = self.quote['lastPrice']
        self.volume = self.quote['totalVolume']
        self.divs = False if self.quote['divYield'] == 0.0 else True

        # Analysis
        self.movingAvg200 = set_moving_average(self.cleanPriceHistory['close'], 200)
        self.movingAvg50 = set_moving_average(self.cleanPriceHistory['close'], 50)
        self.RSI = set_rsi(self.cleanPriceHistory['close'])
        self.levels = self.get_support_and_resistance_levels()
        self.MACDLines = self.set_macd()
        self.MACDVal, self.MACDSignal = self.set_macd_vals()
        self.EMA = self.set_ema(15)
        self.Support, self.percentOffSupp, self.Resistance, self.percentOffResist = self.percent_off_levels()
        self.score = self.evaluate_score()

    def set_clean_price_history(self):
        quote = self.quote
        dates = self.dateRangeDF.apply(mpl_dates.date2num)
        df = pd.concat([self.candles, dates], axis=1, join='inner')
        clean_price_history = df.loc[:, ['date', 'open', 'high', 'low', 'close']]

        quote_today = {
            'date': mpl_dates.date2num(datetime.date.today()),
            'open': quote['openPrice'],
            'high': quote['highPrice'],
            'low': quote['lowPrice'],
            'close': quote['lastPrice']
        }

        total_rows = len(clean_price_history.index)
        q_t = pd.DataFrame(quote_today, index=[total_rows])
        clean_price_history.append(q_t)
        return clean_price_history

    @staticmethod
    def epoch_to_datetime(epoch):
        return datetime.date.fromtimestamp(round(epoch) / 1000)

    def get_support_and_resistance_levels(self):
        clean_price_history = self.cleanPriceHistory

        def is_support(df, i):
            support = df['low'][i] < df['low'][i - 1] < df['low'][i - 2] and df['low'][i] < df['low'][i + 1] < \
                      df['low'][
                          i + 2]
            return support

        def is_resistance(df, i):
            resistance = df['high'][i] > df['high'][i - 1] > df['high'][i - 2] and df['high'][i] > df['high'][i + 1] > \
                         df['high'][i + 2]
            return resistance

        s = np.mean(clean_price_history['high'] - clean_price_history['low'])

        def is_far_from_level(level):
            return np.sum([abs(level - x) < s for x in levels]) == 0

        levels = []
        for index in range(2, clean_price_history.shape[0] - 2):
            if is_support(clean_price_history, index):
                price = clean_price_history['low'][index]
                if is_far_from_level(price):
                    levels.append((index, price))
            elif is_resistance(clean_price_history, index):
                price = clean_price_history['high'][index]
                if is_far_from_level(price):
                    levels.append((index, price))

        return sorted(levels, key=lambda x: x[1])

    def show_plot(self):
        plt.rcParams['figure.figsize'] = [12, 7]
        plt.rc('font', size=14)
        df = self.cleanPriceHistory

        fig, ax = plt.subplots()
        candlestick_ohlc(ax, df.values, width=0.6,
                         colorup='green', colordown='red', alpha=0.8)
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        fig.suptitle(f'$({self.symbol}) - {self.quote["description"]}\nSupport and Resistance Levels')
        date_format = mpl_dates.DateFormatter('%d-%m-%Y')
        ax.xaxis.set_major_formatter(date_format)
        fig.autofmt_xdate()
        fig.tight_layout()

        for level in self.levels:
            plt.hlines(level[1], xmin=df['date'][level[0]],
                       xmax=max(df['date']), colors='blue')
        plt.show()

    def percent_off_levels(self):
        # TODO:
        #  change the nearest support and resistance so that it includes moving averages as well not just price levels

        nearest_supp = 0
        nearest_res = 0
        for level in self.levels:
            if self.lastPrice >= level[1]:
                nearest_supp = level[1]
            if self.lastPrice <= level[1]:
                nearest_res = level[1]
                break

        if nearest_res == 0.0:
            nearest_res = self.quote['52WkHigh']
        if nearest_supp == 0.0:
            nearest_supp = self.quote['52WkLow']

        percent_off_resist = round((abs(self.lastPrice - nearest_res) /
                                    ((self.lastPrice + nearest_res) / 2)) * 100, 2)

        percent_off_supp = round((abs(self.lastPrice - nearest_supp) /
                                  ((self.lastPrice + nearest_supp) / 2)) * 100, 2)

        return round(nearest_supp, 2), round(percent_off_supp, 2), round(nearest_res, 2), round(percent_off_resist, 2)

    def set_macd(self):
        exp1 = self.cleanPriceHistory['close'].ewm(span=12, adjust=False).mean()
        exp2 = self.cleanPriceHistory['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
        return macd, exp3

    def set_macd_vals(self):
        return round(self.MACDLines[0].iloc[-1], 3), round(self.MACDLines[1].iloc[-1], 3)

    def set_ema(self, t):
        return round(self.cleanPriceHistory['close'].ewm(span=t, adjust=False).mean().iloc[-1], 2)

    def evaluate_score(self):

        price = self.lastPrice
        score = 0
        if price > self.movingAvg50:
            score += 1
        else:
            score -= 1
        if price > self.movingAvg200:
            score += 1
        else:
            score -= 1
        if self.movingAvg50 > self.movingAvg200:
            score += 1
        else:
            score -= 1
        if self.RSI <= 30:
            score += 1
        if self.RSI >= 70:
            score -= 1

        if self.MACDVal > 0:
            score += 1
        else:
            score -= 1

        if self.MACDVal > self.MACDSignal:
            score += 1
        else:
            score -= 1

        return score

    def create_snapshot(self, days_prior):
        days_prior += 14
        temp_history = self.cleanPriceHistory.copy(deep=True)
        future_price = self.cleanPriceHistory['close'].iloc[-days_prior + 13]
        self.cleanPriceHistory.drop(self.cleanPriceHistory.tail(days_prior).index, inplace=True)
        self.MACDLines = self.set_macd()
        MACD = self.set_macd_vals()

        close_price = self.cleanPriceHistory['close'].iloc[-1]
        days_since = self.cleanPriceHistory['date'].iloc[-1]
        start_date_epoch = datetime.datetime.strptime("01/01/1970", "%m/%d/%Y")
        date = (start_date_epoch + datetime.timedelta(days=int(days_since))).date().strftime("%m/%d/%Y")

        tup = (self.symbol, date, close_price, set_rsi(self.cleanPriceHistory['close']), self.set_ema(15), set_moving_average( self.cleanPriceHistory['close'], 50),
               set_moving_average(200), MACD[0], MACD[1], future_price)
        self.cleanPriceHistory = temp_history
        return tup
