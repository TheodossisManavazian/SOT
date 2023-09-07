from typing import Optional

from fastapi import APIRouter, Depends
from sot_service import engine
from sot_service.models.routes.ticker_controller_request import AddDeleteTickersRequest
from sot_service.models import ticker as t
from sot_service.orchestrators import ticker_orchestrator
from sot_service.utils.auth import requires_auth

router = APIRouter(prefix='/ticker')


@router.post("/add/{symbol}", dependencies=[Depends(requires_auth)])
def add_symbol(symbol: Optional[str] = None):
    ticker = t.try_create_ticker(symbol)
    if ticker is None:
        return {"message": f"Invalid Ticker: {symbol}"}
    with engine.connect() as conn:
        ticker_orchestrator.upsert_ticker(conn, ticker)
    return {"message": "OK"}


@router.post("/add", dependencies=[Depends(requires_auth)])
def add_symbols(request: AddDeleteTickersRequest):
    symbols = request.symbols
    with engine.connect() as conn:
        for symbol in symbols:
            ticker = t.try_create_ticker(symbol)
            if ticker:
                ticker_orchestrator.upsert_ticker(conn, ticker)
    return {"message": "OK"}


@router.post("/delete/{symbol}", dependencies=[Depends(requires_auth)])
def delete_symbol(symbol: str):
    with engine.connect() as conn:
        ticker_orchestrator.delete_ticker(conn, symbol)
    return {"message": "OK"}


@router.post("/delete", dependencies=[Depends(requires_auth)])
def delete_symbols(request: AddDeleteTickersRequest):
    symbols = request.symbols
    with engine.connect() as conn:
        for symbol in symbols:
            ticker_orchestrator.delete_ticker(conn, symbol)
    return {"message": "OK"}



