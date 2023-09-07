# This file handles the actual client, most of the functions here are implemented as basic GUI functionality
import pydash
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

import config
from client import client
import pandas as pd

from sot_service.models.technical_analysis import TechnicalAnalysis
from sot_service.models.ticker import Ticker
from sot_service.orchestrators.sec_orchestrator import get_sec_company_facts


class WindowAnalyze(Screen):
    indices = ["$VIX.X", "$TNX.X"]
    indicesDict = {}

    for index in indices:
        instance = pd.DataFrame(client.get_price_history(
            index,
            period_type=client.PriceHistory.PeriodType.MONTH,
            period=client.PriceHistory.Period.ONE_MONTH,
            frequency_type=client.PriceHistory.FrequencyType.DAILY,
            frequency=client.PriceHistory.Frequency.DAILY,
            start_datetime=None,
            end_datetime=None,
            need_extended_hours_data=None
        ).json())

        history = instance["candles"].apply(pd.Series)
        quote = client.get_quote(index).json()[index]
        indicesDict[index] = {}
        indicesDict[index]['lastPrice'] = quote['lastPrice']
        indicesDict[index]['1MonthChange'] = history.iloc[-1]['close'] - history.iloc[0]['close']
        indicesDict[index]['Month%Change'] = indicesDict[index]['1MonthChange'] / abs(history.iloc[0]['close']) * 100

    markets = ["DBC", "SPY", "DIA", "QQQ", "GLD", "CPER", "XME", "UCO", "$TNX.X",
               "$VIX.X"]  # For some reason API doesnt like TNX or VIX
    charts = []
    for commodity in markets:
        try:
            instance = pd.DataFrame(client.get_price_history(
                commodity,
                period_type=client.PriceHistory.PeriodType.YEAR,
                period=client.PriceHistory.Period.ONE_YEAR,
                frequency_type=client.PriceHistory.FrequencyType.DAILY,
                frequency=client.PriceHistory.Frequency.DAILY,
                start_datetime=None,
                end_datetime=None,
                need_extended_hours_data=None
            ).json())
            i = instance["candles"].apply(pd.Series)

            charts.append((commodity, i['close']))
        except Exception as e:
            print(e)

    def anlz(self):
        symbol = self.ids.symbol.text
        try:
            t = Ticker(symbol)
            cf = get_sec_company_facts(symbol)
            # ===========

            # QUICK QUOTE
            # ===========

            netPercentChangeInDouble = round(t.quote['netPercentChangeInDouble'], 2)
            if netPercentChangeInDouble <= 0:
                self.ids.percentChange.color = (1, 0, 0, .8)
                self.ids.price.color = (1, 0, 0, .8)
                self.ids.netChange.color = (1, 0, 0, .8)
            else:
                self.ids.percentChange.color = (0, 1, 0, .8)
                self.ids.price.color = (0, 1, 0, .8)
                self.ids.netChange.color = (0, 1, 0, .8)

            div_date = t.quote['divDate']
            if len(div_date) > 0:
                div_date = div_date.split()[0]

            self.ids.name.text = t.quote['description']
            self.ids.price.text = f"${t.last_price}"
            self.ids.netChange.text = str(f"${t.quote['netChange']}")
            self.ids.percentChange.text = f"{netPercentChangeInDouble}%"
            self.ids.wkHigh.text = str(f"${t.quote['52WkHigh']}")
            self.ids.wkLow.text = str(f"${t.quote['52WkLow']}")
            self.ids.mktCap.text = str(f"${round(t.fundamentals['marketCap'] / 1000, 3)} B")
            self.ids.vol.text = str(t.quote['totalVolume'])
            self.ids.avgVol.text = str(f"{int(t.fundamentals['vol10DayAvg'])}")
            self.ids.divYield.text = f"{round(t.quote['divYield'], 2)}%,    {div_date}"

            # ==================
            # TECHNICAL ANALYSIS
            # ==================
            ta = TechnicalAnalysis(t)
            # account = client.get_account(config.keys['account_number']).json()
            # available_trading_funds = pydash.get(account, 'securitiesAccount.initialBalances.cashAvailableForTrading')

            self.ids.RSI.text = str(ta.rsi)
            self.ids.MACD.text = f"Val: {ta.macd_value} -- Sig: {ta.macd_signal}"
            self.ids.MA200.text = str(ta.sma_200)
            self.ids.MA50.text = str(ta.sma_50)
            self.ids.EMA15.text = str(ta.ema_15)
            self.ids.Resistance.text = str(f"{ta.resistance},    {ta.percent_away_from_resistance}%")
            self.ids.Support.text = str(f"{ta.support},    {ta.percent_away_from_support}%")
            if ta.risk_assessment >= 0:
                self.ids.Score.color = (0, 1, 0, .8)
            else:
                self.ids.Score.color = (1, 0, 0, .8)
            self.ids.Score.text = str(ta.risk_assessment)

            # ============
            # FUNDAMENTALS
            # ============

            self.ids.peRatio.text = str(t.quote['peRatio'])
            self.ids.eps.text = str(f"{round(t.fundamentals['epsTTM'], 2)},   "
                                    f"{round(t.fundamentals['epsChangePercentTTM'], 2)}%")

            self.ids.pbRatio.text = str(f"{round(t.fundamentals['pbRatio'], 3)}")
            self.ids.prRatio.text = str(f"{round(t.fundamentals['prRatio'], 3)}")
            self.ids.pcfRatio.text = str(f"{round(t.fundamentals['pcfRatio'], 3)}")
            self.ids.returnOnAssets.text = str(f"{round(t.fundamentals['returnOnAssets'], 3)}%")
            self.ids.returnOnEquity.text = str(f"{round(t.fundamentals['returnOnEquity'], 3)}%")
            self.ids.returnOnInvestment.text = str(f"{round(t.fundamentals['returnOnInvestment'], 3)}%")
            self.ids.quickRatio.text = str(f"{round(t.fundamentals['quickRatio'], 3)}")
            self.ids.currentRatio.text = str(f"{round(t.fundamentals['currentRatio'], 3)}")
            self.ids.totalDebtToEquity.text = str(f"{round((t.fundamentals['totalDebtToEquity'] / 100), 3)}")
            self.ids.beta.text = str(f"{round(t.fundamentals['beta'], 3)}")

            # =====================
            # INTER-MARKET ANALYSIS
            # =====================
            close_prices = t.price_history['close']

            correlations = {}
            charts = self.charts
            for chart in charts:
                market_close_prices = chart[1]
                correlations[chart[0]] = round(close_prices.corr(market_close_prices) * 100, 2)

            if correlations['DBC'] > 80:
                self.ids.DBC.color = (0, .4, 1, 1)
            elif 80 > correlations['DBC'] > 0:
                self.ids.DBC.color = (0, 1, 0, .8)
            elif 0 > correlations['DBC'] > -80:
                self.ids.DBC.color = (1, 0, 0, .8)
            else:
                self.ids.DBC.color = (1, .5, 0, 1)

            if correlations['SPY'] > 80:
                self.ids.SPY.color = (0, .4, 1, 1)
            elif 80 > correlations['SPY'] > 0:
                self.ids.SPY.color = (0, 1, 0, .8)
            elif 0 > correlations['SPY'] > -80:
                self.ids.SPY.color = (1, 0, 0, .8)
            else:
                self.ids.SPY.color = (1, .5, 0, 1)

            if correlations['DIA'] > 80:
                self.ids.DIA.color = (0, .4, 1, 1)
            elif 80 > correlations['DIA'] > 0:
                self.ids.DIA.color = (0, 1, 0, .8)
            elif 0 > correlations['DIA'] > -80:
                self.ids.DIA.color = (1, 0, 0, .8)
            else:
                self.ids.DIA.color = (1, .5, 0, 1)

            if correlations['QQQ'] > 80:
                self.ids.QQQ.color = (0, .4, 1, 1)
            elif 80 > correlations['QQQ'] > 0:
                self.ids.QQQ.color = (0, 1, 0, .8)
            elif 0 > correlations['QQQ'] > -80:
                self.ids.QQQ.color = (1, 0, 0, .8)
            else:
                self.ids.QQQ.color = (1, .5, 0, 1)

            if correlations['GLD'] > 80:
                self.ids.GLD.color = (0, .4, 1, 1)
            elif 80 > correlations['GLD'] > 0:
                self.ids.GLD.color = (0, 1, 0, .8)
            elif 0 > correlations['GLD'] > -80:
                self.ids.GLD.color = (1, 0, 0, .8)
            else:
                self.ids.GLD.color = (1, .5, 0, 1)

            if correlations['CPER'] > 80:
                self.ids.CPER.color = (0, .4, 1, 1)
            elif 80 > correlations['CPER'] > 0:
                self.ids.CPER.color = (0, 1, 0, .8)
            elif 0 > correlations['CPER'] > -80:
                self.ids.CPER.color = (1, 0, 0, .8)
            else:
                self.ids.CPER.color = (1, .5, 0, 1)

            if correlations['XME'] > 80:
                self.ids.XME.color = (0, .4, 1, 1)
            elif 80 > correlations['XME'] > 0:
                self.ids.XME.color = (0, 1, 0, .8)
            elif 0 > correlations['XME'] > -80:
                self.ids.XME.color = (1, 0, 0, .8)
            else:
                self.ids.XME.color = (1, .5, 0, 1)

            if correlations['UCO'] > 80:
                self.ids.UCO.color = (0, .4, 1, 1)
            elif 80 > correlations['UCO'] > 0:
                self.ids.UCO.color = (0, 1, 0, .8)
            elif 0 > correlations['UCO'] > -80:
                self.ids.UCO.color = (1, 0, 0, .8)
            else:
                self.ids.UCO.color = (1, .5, 0, 1)

            if correlations['$VIX.X'] > 80:
                self.ids.VIX.color = (0, .4, 1, 1)
            elif 80 > correlations['$VIX.X'] > 0:
                self.ids.VIX.color = (0, 1, 0, .8)
            elif 0 > correlations['$VIX.X'] > -80:
                self.ids.VIX.color = (1, 0, 0, .8)
            else:
                self.ids.VIX.color = (1, .5, 0, 1)

            if correlations['$TNX.X'] > 80:
                self.ids.TNX.color = (0, .4, 1, 1)
            elif 80 > correlations['$TNX.X'] > 0:
                self.ids.TNX.color = (0, 1, 0, .8)
            elif 0 > correlations['$TNX.X'] > -80:
                self.ids.TNX.color = (1, 0, 0, .8)
            else:
                self.ids.TNX.color = (1, .5, 0, 1)

            self.ids.DBC.text = str(f"{correlations['DBC']}%")
            self.ids.SPY.text = str(f"{correlations['SPY']}%")
            self.ids.DIA.text = str(f"{correlations['DIA']}%")
            self.ids.QQQ.text = str(f"{correlations['QQQ']}%")
            self.ids.GLD.text = str(f"{correlations['GLD']}%")
            self.ids.CPER.text = str(f"{correlations['CPER']}%")
            self.ids.XME.text = str(f"{correlations['XME']}%")
            self.ids.UCO.text = str(f"{correlations['UCO']}%")
            self.ids.TNX.text = str(f"{correlations['$TNX.X']}%")
            self.ids.VIX.text = str(f"{correlations['$VIX.X']}%")

            # Sentiment Analysis:

            if self.indicesDict['$VIX.X']['1MonthChange'] > 0:
                self.ids.VIX_last.color = (1, 0, 0, .8)
                self.ids.VIX_moChange.color = (1, 0, 0, .8)
                self.ids.VIX_moChangePercent.color = (1, 0, 0, .8)

            if self.indicesDict['$TNX.X']['1MonthChange'] < 0:
                self.ids.TNX_last.color = (1, 0, 0, .8)
                self.ids.TNX_moChange.color = (1, 0, 0, .8)
                self.ids.TNX_moChangePercent.color = (1, 0, 0, .8)

            self.ids.VIX_last.text = f"${self.indicesDict['$VIX.X']['lastPrice']}"
            self.ids.VIX_moChange.text = f"${round(self.indicesDict['$VIX.X']['1MonthChange'], 3)}"
            self.ids.VIX_moChangePercent.text = f"{round(self.indicesDict['$VIX.X']['Month%Change'], 3)}%"

            self.ids.TNX_last.text = f"${self.indicesDict['$TNX.X']['lastPrice']}"
            self.ids.TNX_moChange.text = f"${round(self.indicesDict['$TNX.X']['1MonthChange'], 3)}"
            self.ids.TNX_moChangePercent.text = f"{round(self.indicesDict['$TNX.X']['Month%Change'], 3)}%"

        except Exception as e:
            # RESET FIELDS
            self.ids.name.text = f'invalid ticker: "{symbol.upper()}"'
            self.ids.price.text = ""
            self.ids.vol.text = ""
            self.ids.netChange.text = ""
            self.ids.percentChange.text = ""
            self.ids.wkHigh.text = ""
            self.ids.wkLow.text = ""
            self.ids.peRatio.text = ""
            self.ids.divYield.text = ""
            self.ids.mktCap.text = ""
            self.ids.avgVol.text = ""
            self.ids.RSI.text = "-"
            self.ids.MACD.text = "-"
            self.ids.MA200.text = "-"
            self.ids.MA50.text = "-"
            self.ids.EMA15.text = "-"
            self.ids.Resistance.text = "-"
            self.ids.Support.text = "-"
            self.ids.Score.text = "-"
            self.ids.Score.color = (1, 1, 1, 1)
            self.ids.peRatio.text = ""
            self.ids.eps.text = ""
            self.ids.pbRatio.text = ""
            self.ids.prRatio.text = ""
            self.ids.pcfRatio.text = ""
            self.ids.returnOnAssets.text = ""
            self.ids.returnOnEquity.text = ""
            self.ids.returnOnInvestment.text = ""
            self.ids.quickRatio.text = ""
            self.ids.currentRatio.text = ""
            self.ids.totalDebtToEquity.text = ""
            self.ids.beta.text = ""
            self.ids.DBC.text = ""
            self.ids.SPY.text = ""
            self.ids.DIA.text = ""
            self.ids.QQQ.text = ""
            self.ids.GLD.text = ""
            self.ids.CPER.text = ""
            self.ids.XME.text = ""
            self.ids.UCO.text = ""
            self.ids.TNX.text = ""
            self.ids.VIX.text = ""

            print("Error when creating Ticker class,", e)

    # PLOT candle chart in new kivy window
    def plot(self):
        pass
    #     selection = self.ids.period.text
    #     symbol = self.ids.symbol.text
    #     try:
    #         t = Ticker(symbol.upper(), selection)
    #         # t.show_plot()
    #     except Exception as e:
    #         print("Invalid ticker,", e)


    def execute_trade(self):
        symbol = self.ids.symbol.text
        self.ids.name.text = f'BOUGHT {symbol}'
