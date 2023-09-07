import talib

from backtesting import Strategy, Backtest
from backtesting.lib import crossover

from pandas import DataFrame


def backtest(sample_data: DataFrame) -> None:
    # print(sample_data)

    class Grid(Strategy):

        def init(self):
            self.EMA_15 = self.I(talib.MA, self.data.Close, 15)
            self.SMA_50 = self.I(talib.MA, self.data.Close, 50)

        def next(self):
            price = self.data.Close[-1]
            if crossover(price, self.EMA_15) or crossover(price, self.SMA_50) or crossover(price, self.SMA_200):
                self.position.close()
                self.buy()

            elif crossover(self.EMA_15, price) or crossover(self.SMA_50, price) or crossover(self.SMA_200, price):
                self.position.close()
                self.sell()

    bt = Backtest(sample_data, Grid, cash = 100000)
    stats = bt.run()
    print(stats)
    bt.plot()

    # print(sample_data)
    # sample_data_test = sample_data[:10000]
    # df2 = sample_data[sample_data_test.index % 60 == 0]
    # df2.reset_index(drop=True, inplace= True)
    #
    # t = InternalTicker('SPY', sample_data_test, True)
    # ta = TechnicalAnalysis(t)
    #
    #
    # for tick in sample_data[10000:]:
    #     levels = set()
    #     t = InternalTicker('SPY', sample_data[:10000+tick])
    #     ta = TechnicalAnalysis(t)
    #     last_price = t.last_price
    #     levels.add(ta.resistance)
    #     levels.add(ta.support)
    #     levels.add(ta.sma_50)
    #     levels.add(ta.sma_200)
    #     levels.add(ta.ema_15)
    #
    #
    #     for price in ta.resistances:
    #         levels.add(price[1])
    #
    #
    #
    # print(ta.resistances)



