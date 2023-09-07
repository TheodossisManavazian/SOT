import pydash
from sqlalchemy.engine import Connection

from sot_service import engine
from sot_service.daos import current_positions_dao
from sot_service.models.technical_analysis import TechnicalAnalysis, Ticker
from sot_service.services import current_positions_service
from sot_service.utils.jaat import jaat_utils
from sot_service.models.constants.strategies import EMA_15_CROSSES_SMA_50

ema_above_sma = None


def check_conditions(conn: Connection, ta: TechnicalAnalysis, current_positions: dict):
    current_position = pydash.get(current_positions, EMA_15_CROSSES_SMA_50)
    global ema_above_sma
    if ema_above_sma is None:
        ema_above_sma = False
        if ta.ema_15 > ta.sma_50:
            ema_above_sma = True

    # Buy Stock
    # print(f"{ta.ticker.price_history.iloc[-1]['datetime']} --- {ta.ticker.symbol} -- ${ta.ticker.last_price} || EMA_15 -- {ta.ema_15} , SMA_50 -- {ta.sma_50}")
    if current_position is None:
        if ta.ema_15 > ta.sma_50 and ema_above_sma is False:
            ema_above_sma = True
            jaat_utils.add_to_position(conn, ta.ticker, 100, EMA_15_CROSSES_SMA_50)

    elif current_position:
        # Sell Stock
        if ta.ema_15 < ta.sma_50:

            jaat_utils.remove_from_position(conn, ta.ticker, EMA_15_CROSSES_SMA_50)

    if ta.ema_15 < ta.sma_50:
        ema_above_sma = False
