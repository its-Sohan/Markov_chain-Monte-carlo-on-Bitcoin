import numpy as np
import pandas as pd
from ccxt import binance

exchange = binance({
    'enableRateLimit': True
})

symbol = 'BTC/USDT'
timeframe = '1d'

ohlcvs = exchange.fetch_ohlcv(symbol, timeframe=timeframe)

df = pd.DataFrame(ohlcvs, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

df['log_return_calc'] = np.log(df['close'] / df['close'].shift(1))
df.sort_values('date').to_csv('/home/sohan/Markov_chain-Monte-carlo-on-Bitcoin/btc_daily_ohlcv_with_log_returns.csv', index=False)

print(f"Downloaded {len(df)} daily rows for BTC/USDT")
print(df.tail())
