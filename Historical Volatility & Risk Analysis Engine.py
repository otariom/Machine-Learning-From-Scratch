import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Define variables that were missing in the original snippet
ticker = "AAPL"  # Example ticker
start_date = dt.datetime(2020, 1, 1)
end_date = dt.datetime.now()
risk_free_rate = 0.03  # Example risk-free rate

print(f"Downloading data for {ticker}...")
df = yf.download(ticker, start=start_date, end=end_date)

# Check what columns are actually available
print("Available columns:", df.columns.tolist())

# Use 'Adj Close' if available, otherwise use 'Close'
price_col = 'Adj Close' if 'Adj Close' in df.columns else 'Close'

# 2. LOG RETURNS (The Growth Rate)
# Formula: ln(Price_t / Price_t-1)
df['Log_Returns'] = np.log(df[price_col] / df[price_col].shift(1))

# 3. ROLLING VOLATILITY (The Wiggles)
# We use a 21-day window (one trading month)
window = 21
df['Daily_Volatility'] = df['Log_Returns'].rolling(window=window).std()

# 4. ANNUALIZATION (Scaling to a Year)
# Formula: Daily_Vol * sqrt(252)
df['Annualized_Volatility'] = df['Daily_Volatility'] * np.sqrt(252)

# 5. SHARPE RATIO (The Efficiency Grade)
# We calculate the rolling return and then the Sharpe Ratio
# We assume a 252-day annualization for the mean return as well
rolling_annual_return = df['Log_Returns'].rolling(window=window).mean() * 252
df['Sharpe_Ratio'] = (rolling_annual_return - risk_free_rate) / df['Annualized_Volatility']

# 6. CLEAN UP
df.dropna(inplace=True)

# 7. VISUALIZATION
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 12), sharex=True)

# Plot 1: Price
ax1.plot(df[price_col], color='blue', label='Price')
ax1.set_title(f'{ticker} Price Performance')
ax1.legend()

# Plot 2: Volatility (Risk)
ax2.plot(df['Annualized_Volatility'], color='red', label='Annualized Volatility')
ax2.axhline(df['Annualized_Volatility'].mean(), color='black', linestyle='--', label='Average Vol')
ax2.set_title('Risk (Volatility)')
ax2.legend()

# Plot 3: Sharpe Ratio (Efficiency)
ax3.plot(df['Sharpe_Ratio'], color='green', label='Rolling Sharpe Ratio')
ax3.axhline(1, color='orange', linestyle='--', label='Good Threshold (1.0)')
ax3.set_title('Efficiency (Sharpe Ratio)')
ax3.legend()

plt.tight_layout()
plt.show()

# Final Metrics Output
current_vol = df['Annualized_Volatility'].iloc[-1]
current_sharpe = df['Sharpe_Ratio'].iloc[-1]
print("-" * 30)
print(f"ANALYSIS FOR {ticker}:")
print(f"Current Annualized Volatility: {current_vol:.2%}")
print(f"Current Rolling Sharpe Ratio: {current_sharpe:.2f}")
print("-" * 30)