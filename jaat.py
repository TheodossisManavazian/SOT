import pydash
import finnhub

# This will not run on online IDE
import requests
from bs4 import BeautifulSoup

import json

import config
from client import client
from sot_service.models.ticker_day_trade import Ticker

if __name__ == "__main__":
    pass



    # OPTIONS LOGIC
    # account = client.get_account(config.keys['account_number']).json()
    # available_trading_funds = pydash.get(account, 'securitiesAccount.initialBalances.cashAvailableForTrading')
    #
    # options = client.get_option_chain('TSLA').json()
    #
    # date = '2023-08-18:38'
    # call_strike = '325.0'
    # put_strike = '230.0'
    #
    # call = pydash.get(options, ['callExpDateMap', date, call_strike])[0]
    # put = pydash.get(options, ['putExpDateMap', date, put_strike])[0]
    # call_open_interest = pydash.get(call, 'openInterest')
    # put_open_interest = pydash.get(put, 'openInterest')
    # call_price = pydash.get(call, 'last')
    # put_price = pydash.get(put, 'last')
    #
    # # print(date)
    # # print(f"Calls: \nStrike: ${call_strike}\nPrice: ${call_price} \nOpenInterest: {call_open_interest}\nMoneyIn: ${call_open_interest*call_price*100}")
    # # print("\n\n")
    # # print(f"Puts: \nStrike: ${put_strike}\nPrice: ${put_price} \nOpenInterest: {put_open_interest}\nMoneyIn: ${put_open_interest*put_price*100}")
    # #
    #
    # all_calls = pydash.get(options, ['callExpDateMap', date])
    # all_puts = pydash.get(options, ['putExpDateMap', date])
    #
    # money_on_calls = 0
    # for key, val in all_calls.items():
    #     open_interest = pydash.get(val[0], 'openInterest')
    #     price = pydash.get(val[0], 'last')
    #     money_on_calls += (open_interest * price * 100)
    #
    # money_on_puts = 0
    # for key, val in all_puts.items():
    #     open_interest = pydash.get(val[0], 'openInterest')
    #     price = pydash.get(val[0], 'last')
    #     money_on_puts += (open_interest * price * 100)
    #
    # money_on_calls = '{:,}'.format(money_on_calls)
    # money_on_puts = '{:,}'.format(money_on_puts)
    #
    # print("="*20, date)
    # print(f"Money on calls: ${money_on_calls}")
    # print(f"Money on puts: ${money_on_puts}")


    #
    # finnhub_client = finnhub.Client(api_key="<redacted>")
    #
    # url_tesla = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0001318605.json'
    # url_apple = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000320193.json'
    # url_amd = 'https://data.sec.gov/api/xbrl/companyfacts/CIK0000002488.json'
    #
    # headers = {'User-Agent': 'theomanavazian@gmail.com'}
    # req = requests.get(url_tesla, headers=headers).json()
    # req1 = requests.get(url_apple, headers=headers).json()
    # req2 = requests.get(url_amd, headers=headers).json()

    # with open('chains.json', 'w') as f:
    #     json.dump(options, f)

    # gross_profit_tesla = pydash.get(req, 'facts.us-gaap.GrossProfit.units.USD')
    # gross_profit_apple = pydash.get(req1, 'facts.us-gaap.GrossProfit.units.USD')
    # gross_profit_amd = pydash.get(req2, 'facts.us-gaap.GrossProfit.units.USD')
    #
    # print(gross_profit_tesla)
    # print(gross_profit_amd)
    # print(gross_profit_apple)

    # print(finnhub_client.financials('AAPL', 'bs', 'annual'))
    # apple_reports = finnhub_client.filings(symbol='AAPL', _from="2023-01-01", to="2023-07-03")
    # amd_reports = finnhub_client.filings(symbol='AMD', _from="2023-01-01", to="2023-07-03")
    # tsla_reports = finnhub_client.filings(symbol='TSLA', _from="2023-01-01", to="2023-07-03")
    # rcl_reports = finnhub_client.filings(symbol='RCL', _from="2023-01-01", to="2023-07-03")
    #
    # ten_q_apple = [x for x in apple_reports if x['form'] == '10-Q']
    # ten_q_amd = [x for x in amd_reports if x['form'] == '10-Q']
    # ten_q_tsla = [x for x in tsla_reports if x['form'] == '10-K']
    # ten_q_rcl = [x for x in rcl_reports if x['form'] == '10-Q']
    #
    # print(ten_q_apple)
    # print(ten_q_amd)
    # print(ten_q_tsla)
    # print(ten_q_rcl)

    # print(T.symbol)
    # print(T.quote)
    # print(T.last_price)
    #
    # print(T.ema_8_weekly)
    # print(T.ema_8_daily)
    # print(T.ema_8_intraday_30)
    # print(T.ema_8_intraday_5)
    #
    # print(T.fundamentals)
