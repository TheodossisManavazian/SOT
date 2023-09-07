from pandas import DataFrame

from sot_service import engine
from sot_service.jaat_strategies.all_strategies import ALL_TRADING_STRATEGIES
from sot_service.models.internal_ticker import InternalTicker
from sot_service.models.technical_analysis import TechnicalAnalysis
from sot_service.models.ticker import Ticker
from sot_service.services import current_positions_service
from typing import List
import datetime
import time as t

POSITIONS_HELD = {}
ABOVE_OR_BELOW = None

# Implement proprietary trading algorithm.
def start_jaat(symbol: str, strategies: List[str]) -> None:
    while True:
        time = datetime.datetime.now()
        hour, minute, second = time.hour, time.minute, time.second

        if second % 5 == 0:
            ta = TechnicalAnalysis(Ticker(symbol, True))
            with engine.connect() as conn:
                current_positions = current_positions_service.get_positions_by_symbol(conn, ta.ticker.symbol)

                for strategy in strategies:
                    ALL_TRADING_STRATEGIES[strategy].check_conditions(conn, ta, current_positions)

            conn.close()
            if second % 60 == 0:
                print(current_positions)
                if ta.hammer == 100 or ta.hammer == -100:
                    print(symbol, "HAMMER")
                    print(time.now())
                if ta.engulf == 100 or ta.engulf == -100:
                    print(symbol, "ENGULF")
                    print(time.now())

        t.sleep(1)


def start_jaat__test_data(df: DataFrame, strategies: List[str]) -> None:
    with engine.connect() as conn:
        for i, row in df.iloc[250:].iterrows():
            time = datetime.datetime.now().second
            ta = TechnicalAnalysis(InternalTicker('SPY', df.iloc[:i]))
            current_positions = current_positions_service.get_positions_by_symbol(conn, ta.ticker.symbol)

            for strategy in strategies:
                ALL_TRADING_STRATEGIES[strategy].check_conditions(conn, ta, current_positions)

            if time % 60 == 0:
                print(i, df.iloc[i]['datetime'])
    conn.close()
    t.sleep(1)
