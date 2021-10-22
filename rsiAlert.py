import pprint
import ccxt
import pandas as pd
from ta.volatility import BollingerBands, AverageTrueRange
import ta
import schedule
import datetime
import config
import time
import asyncio
from ta import add_all_ta_features
from ta import momentum
from ta.utils import dropna
from notifypy import Notify

pd.set_option("display.max_rows", None, "display.max_columns", None)

exchange_id = 'binance'
exchange = ccxt.binance({
    'options': {
        'defaultType': 'future',  # ←-------------- quotes and 'future'
    },
})

inPosition: bool = False
order = 0


def check():
    markets = exchange.load_markets()
    for i in markets:
        # every symbol taken here
        if i =="BTCSTUSDT":
            i="BTC/USDT"
        bars = exchange.fetch_ohlcv(i, timeframe='5m', limit=50)
        data = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data['rsi'] = momentum.rsi(data['close'])
        data["symbol"] =i

        rsivalue=data['rsi'].iloc[len(data['rsi'])-1]
        print(f'Fecthing {i} {datetime.datetime.now().isoformat()} RSI: {rsivalue}')
        if rsivalue >= 80.0:
            print(data['symbol']+" Overbought RSI: "+str(rsivalue))
            notification = Notify()
            notification.title = i +" Overbought"
            notification.message = "look for an entry"
            notification.send()
        elif rsivalue<20:
            print(data['symbol']+" Oversold RSI: "+str(rsivalue))
            notification = Notify()
            notification.title = i +" Oversold"
            notification.message = "LooK for an entry."
            notification.send()


print('wait!')


def run_bot():
    check()


run_bot()
while True:
    schedule.run_pending()
    time.sleep(5)
