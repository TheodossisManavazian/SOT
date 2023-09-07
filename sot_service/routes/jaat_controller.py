from fastapi import APIRouter, Depends
from sot_service import engine
from sot_service.models.ticker import Ticker
from sot_service.services import current_positions_service
from sot_service.utils.auth import requires_auth
from sot_service.utils.jaat import jaat_utils

router = APIRouter(prefix='/jaat')


@router.post('/insert_position', dependencies=[Depends(requires_auth)])
def insert_position():
    with engine.connect() as conn:
        ticker = Ticker('AMD')
        strategy = "123"
        quantity = 100
        jaat_utils.add_to_position(conn, ticker, quantity, strategy)


@router.post('/remove_position', dependencies=[Depends(requires_auth)])
def remove_position():
    with engine.connect() as conn:
        ticker = "AMD"
        strategy = "123"
        current_position = jaat_utils.remove_from_position(conn, Ticker(ticker), strategy)
        return current_position


@router.get('/get_position', dependencies=[Depends(requires_auth)])
def get_position():
    with engine.connect() as conn:
        ticker = "AMD"
        strategy = "123"
        current_position = current_positions_service.get_positions_by_symbol(conn, ticker)
        return current_position


