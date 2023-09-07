from pandas import DataFrame


class InternalTicker:
    symbol: str
    price_history: DataFrame
    last_price: float
    intraday: bool

    def __init__(self, symbol: str, price_history: DataFrame, intraday: bool = False):
        self.symbol = symbol.upper()
        # self.price_history = self.format_price_history(price_history)
        self.price_history = price_history
        self.last_price = self._get_last_price()
        self.quote = self._get_quote()
        self.intraday = intraday

    def _get_last_price(self):
        CLOSE = 'Close'
        if 'close' in self.price_history.columns:
            CLOSE = 'close'
        return float(self.price_history.iloc[-1][CLOSE])

    def _get_quote(self):
        CLOSE = 'Close'
        if 'close' in self.price_history.columns:
            CLOSE = 'close'
        max_values = self.price_history.max()
        min_values = self.price_history.min()
        return {
            '52WkHigh': float(max_values[CLOSE]),
            '52WkLow': float(min_values[CLOSE]),
        }

    @staticmethod
    def format_price_history(price_history: DataFrame) -> DataFrame:
        price_history = price_history.reset_index()
        price_history['datetime'] = price_history['datetime'].view(int)//1e6
        price_history.pop('symbol')
        return price_history


