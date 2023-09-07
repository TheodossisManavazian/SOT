# This file handles the actual client, most of the functions here are implemented as basic GUI functionality
import pydash
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from tda.orders.common import Duration, Session
from tda.orders.equities import equity_buy_limit, equity_sell_limit

import config
from client import client

from sot_service.models.ticker_day_trade import Ticker


# Window where trades are executed

class WindowTrade(Screen):
    account = client.get_account(config.TDA_ACCOUNT_NUMBER).json()
    available_trading_funds = pydash.get(account, 'securitiesAccount.initialBalances.cashAvailableForTrading')
    symbol = ''
    ticker: Ticker

    def update(self):
        t = Ticker(self.symbol)
        if t:
            self.ids.last_price.text = f'${t.last_price}'
            self.ticker = t

    def update_ticker(self):
        self.symbol = self.ids.symbol.text.upper()
        Clock.schedule_interval(lambda dt: self.update(), 5)

    def on_pre_enter(self, *args):
        self.ids.available_funds.text = f'${self.available_trading_funds}'

    def execute_buy(self):
        qty = 1
        client.place_order(
            config.TDA_ACCOUNT_NUMBER,  # account_id
            equity_buy_limit(self.symbol, qty, self.ticker.last_price)
            .set_duration(Duration.GOOD_TILL_CANCEL)
            .set_session(Session.SEAMLESS)
            .build())

        print(f"Bought {qty} {self.symbol} @ {self.ticker.last_price}")

    def execute_sell(self):
        qty = 1
        client.place_order(
            config.TDA_ACCOUNT_NUMBER,  # account_id
            equity_sell_limit(self.symbol, qty, self.ticker.last_price)
            .set_duration(Duration.GOOD_TILL_CANCEL)
            .set_session(Session.SEAMLESS)
            .build())
        print(f"Sold {qty} {self.symbol} @ {self.ticker.last_price}")
