# Markov Chain Monte Carlo on Bitcoin

This project implements a price prediction model for Bitcoin (BTC) using Markov Chains and Monte Carlo simulations. By analyzing historical OHLCV (Open, High, Low, Close, Volume) data from Binance, the model simulates potential future price paths based on state transition probabilities.

## 🚀 Features

- **Multi-Timeframe Analysis**: Supports both daily and hourly data.
- **State-Based Modeling**: Categorizes market conditions into states based on log returns (Strong Bear $\rightarrow$ Strong Bull) and trading volume (High/Low).
- **Monte Carlo Simulations**: Generates thousands of possible future price trajectories to estimate the median price and confidence intervals.
- **Visualizations**: Produces price distribution histograms and price path line charts.

## 📁 Project Structure

- `binance_data.py`: Fetches daily BTC/USDT data and calculates log returns.
- `fetch_binance_data.py`: Fetches historical hourly BTC/USDT data.
- `simulate_btc.py`: Runs a 7-day price simulation using daily data.
- `simulate_btc_hourly.py`: Runs a 6-hour price simulation using hourly data.
- `btc_daily_ohlcv_with_log_returns.csv` / `btc_hourly_ohlcv.csv`: Processed historical data.

## 🛠️ Installation

```bash
pip install pandas numpy matplotlib ccxt
```

## 📈 Usage

1. **Fetch Data**:
   Run the data acquisition scripts to get the latest BTC data from Binance.
   ```bash
   python binance_data.py        # Daily data
   python fetch_binance_data.py  # Hourly data
   ```

2. **Run Simulations**:
   Execute the simulation scripts to generate price forecasts.
   ```bash
   python simulate_btc.py          # 7-day forecast
   python simulate_btc_hourly.py   # 6-hour forecast
   ```

3. **Analyze Results**:
   - Check the terminal output for the Median Price Estimate and Confidence Intervals.
   - View the generated `.png` files for price distributions and simulated paths.

## 🧠 Methodology

1. **State Definition**: The market is divided into states combining return magnitude (e.g., "Bull") and volume (e.g., "High").
2. **Transition Matrix**: A Markov transition matrix is constructed from historical data, representing the probability of moving from one state to another.
3. **Path Generation**: For each simulation, the model transitions between states according to the matrix and samples a return from the corresponding historical state to update the price.
4. **Aggregation**: The results of 1,000+ simulations are aggregated to produce a probabilistic forecast.
