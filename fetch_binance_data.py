import ccxt
import pandas as pd
import time
from datetime import datetime, timedelta

# Initialize Binance
exchange = ccxt.binance()

# Define parameters
symbol = 'BTC/USDT'
timeframe = '1h'
# 6 months ago from June 28, 2026
start_date = datetime(2025, 12, 28)
since = int(start_date.timestamp() * 1000)

all_ohlcv = []

# Fetch data in chunks (Binance limits)
while since < int(datetime.now().timestamp() * 1000):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=1000)
        if not ohlcv:
            break
        all_ohlcv.extend(ohlcv)
        since = ohlcv[-1][0] + 1  # Move to next timestamp
        time.sleep(0.1)  # Rate limiting
    except Exception as e:
        print(f"Error: {e}")
        break

# Convert to DataFrame
df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

# Save
df.to_csv('/home/sohan/Markov_chain-Monte-carlo-on-Bitcoin/btc_hourly_ohlcv.csv', index=False)
print(f"Data saved to /home/sohan/Markov_chain-Monte-carlo-on-Bitcoin/btc_hourly_ohlcv.csv. Total rows: {len(df)}")
