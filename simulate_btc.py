import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('/home/sohan/Markov_chain-Monte-carlo-on-Bitcoin/btc_daily_ohlcv_with_log_returns.csv').dropna()

# State Mapping
def get_return_state(ret):
    if ret < -0.016536: return 'Strong Bear'
    if ret < -0.004268: return 'Bear'
    if ret < 0.003725: return 'Neutral'
    if ret < 0.013312: return 'Bull'
    return 'Strong Bull'

def get_volume_state(vol):
    return 'High' if vol >= 17372.63 else 'Low'

df['r_state'] = df['log_return_calc'].apply(get_return_state)
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
days = 7
last_price = df['close'].iloc[-1]
current_state_idx = seq[-1]

# Pre-sample returns for all states to avoid sampling in loop
sampled_returns = {s: df[df['state'] == s]['log_return_calc'].values for s in states}

prices = np.full(num_simulations, last_price, dtype=float)
current_states = np.full(num_simulations, current_state_idx, dtype=int)

for _ in range(days):
    # Vectorized transition
    new_states = np.array([np.random.choice(len(states), p=T[s]) for s in current_states])
    
    # Vectorized return application
    rets = np.array([np.random.choice(sampled_returns[idx_to_state[ns]]) for ns in new_states])
    prices *= np.exp(rets)
    current_states = new_states

print(f"Final Price Estimate (Median): {np.median(prices):.2f}")
print(f"Confidence Interval (5% - 95%): {np.percentile(prices, 5):.2f} - {np.percentile(prices, 95):.2f}")

# Plotting
plt.figure(figsize=(10, 6))
plt.hist(prices, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
plt.title('Distribution of BTC Price after 7 days')
plt.xlabel('Price ($)')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.5)
plt.savefig('price_distribution_7d.png')
print("Plot saved as price_distribution_7d.png")
