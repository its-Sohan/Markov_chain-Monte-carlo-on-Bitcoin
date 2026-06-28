import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/home/sohan/Markov_chain-Monte-carlo-on-Bitcoin/btc_hourly_ohlcv.csv').dropna()
df['log_return'] = np.log(df['close'] / df['close'].shift(1))
df = df.dropna()

# Dynamic Bins
q20, q40, q60, q80 = df['log_return'].quantile([0.2, 0.4, 0.6, 0.8])
med_vol = df['volume'].median()

# State Mapping
def get_return_state(ret):
    if ret < q20: return 'Strong Bear'
    if ret < q40: return 'Bear'
    if ret < q60: return 'Neutral'
    if ret < q80: return 'Bull'
    return 'Strong Bull'

def get_volume_state(vol):
    return 'High' if vol >= med_vol else 'Low'

df['r_state'] = df['log_return'].apply(get_return_state)
df['v_state'] = df['volume'].apply(get_volume_state)
df['state'] = df['r_state'] + '_' + df['v_state']

states = sorted(df['state'].unique())
state_to_idx = {s: i for i, s in enumerate(states)}
idx_to_state = {i: s for s, i in state_to_idx.items()}

# Transition Matrix
seq = df['state'].map(state_to_idx).values
T = np.zeros((len(states), len(states)))
for i in range(len(seq) - 1):
    T[seq[i], seq[i+1]] += 1
T = T / T.sum(axis=1, keepdims=True)

# Optimized Simulation
num_simulations = 1000
hours = 6
last_price = df['close'].iloc[-1]
current_state_idx = seq[-1]

# Pre-sample returns for all states to avoid sampling in loop
sampled_returns = {s: df[df['state'] == s]['log_return'].values for s in states}

# Store all paths for line chart: shape (num_simulations, hours + 1)
all_paths = np.zeros((num_simulations, hours + 1))
all_paths[:, 0] = last_price
current_states = np.full(num_simulations, current_state_idx, dtype=int)

for h in range(1, hours + 1):
    new_states = np.array([np.random.choice(len(states), p=T[s]) for s in current_states])
    rets = np.array([np.random.choice(sampled_returns[idx_to_state[ns]]) for ns in new_states])
    all_paths[:, h] = all_paths[:, h-1] * np.exp(rets)
    current_states = new_states

final_prices = all_paths[:, -1]
print(f"Final Price Estimate (Median): {np.median(final_prices):.2f}")
print(f"70% Range (15th-85th Percentile): {np.percentile(final_prices, 15):.2f} - {np.percentile(final_prices, 85):.2f}")
print(f"Confidence Interval (5% - 95%): {np.percentile(final_prices, 5):.2f} - {np.percentile(final_prices, 95):.2f}")

# Plotting as Line Chart
plt.figure(figsize=(12, 6))
# Plot first 100 paths for clarity
for i in range(min(100, num_simulations)):
    plt.plot(all_paths[i], color='blue', alpha=0.1)

plt.title('Monte Carlo Simulation: BTC Price Paths (6 Hours)')
plt.xlabel('Hours from Now')
plt.ylabel('Price ($)')
plt.grid(True, alpha=0.3)
plt.savefig('price_paths_6h.png')
print("Line chart saved as price_paths_6h.png")
