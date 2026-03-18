import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf  
import statsmodels.api as sm
import datetime

market_ticker = "SPY"

stocks = [
    "NVDA", "XOM", "PG", "JPM", 
    "KO", "JNJ", "AMZN", "META"
]
tickers = stocks + [market_ticker]
start = "2019-01-01"
end = datetime.date.today()

data = yf.download(tickers, start=start, end=end)

if 'Adj Close' in data.columns:
    prices = data['Adj Close']
else:
    prices = data['Close']
prices.dropna(inplace=True)
print("Success! Data shape:", prices.shape)
print(prices.head())

log_returns = np.log(prices / prices.shift(1))
log_returns.dropna(inplace=True)

rf = yf.download("^TNX", start=start, end=end)['Close'] / 100
rf = rf.reindex(log_returns.index).ffill()
daily_rf = rf / 252

excess_returns = log_returns.sub(daily_rf, axis=0)

def run_capm(stock_returns, market_returns):
    X = sm.add_constant(market_returns)
    model = sm.OLS(stock_returns, X).fit()
    return model

rf_series = daily_rf.iloc[:, 0] 

# 2. Subtract row-by-row
excess_returns = log_returns.sub(rf_series, axis=0)

# 3. Clean and Check
clean_excess = excess_returns.dropna()
print(f"Clean Data Shape: {clean_excess.shape}")

if clean_excess.empty:
    print("Still empty. Let's check date alignment:")
    print("Log Returns Index:", log_returns.index[:2])
    print("RF Series Index:", rf_series.index[:2])
else:
    # 4. Proceed with Regression
    market_excess = clean_excess[market_ticker]
    X = sm.add_constant(market_excess)
    results = []

    for stock in stocks:
        y = clean_excess[stock]
        model = sm.OLS(y, X).fit()
        results.append({
            "Stock": stock,
            "Alpha": model.params["const"] * 252,
            "Beta": model.params[market_ticker],
            "R_squared": model.rsquared
        })

    capm_df = pd.DataFrame(results).set_index("Stock")
    print("\n--- CAPM RESULTS ---")
    print(capm_df)

equal_weights = np.array([1 / len(stocks)] * len(stocks))

portfolio_beta = np.dot(equal_weights, capm_df["Beta"])
portfolio_alpha = np.dot(equal_weights, capm_df["Alpha"])

print(f"Portfolio Beta: {portfolio_beta:.2f}")
print(f"Portfolio Alpha: {portfolio_alpha:.2%}")

plt.figure(figsize=(8,6))
plt.scatter(capm_df["Beta"], capm_df["Alpha"], s=80)

for stock in capm_df.index:
    plt.text(capm_df.loc[stock, "Beta"], capm_df.loc[stock, "Alpha"], stock)

plt.axhline(0, linestyle="--", color="gray")
plt.xlabel("Beta")
plt.ylabel("Alpha")
plt.title("Security Market Line (CAPM)")
plt.show()

window = 126
rolling_beta = (
    excess_returns["NVDA"]
    .rolling(window)
    .cov(market_excess)
    / market_excess.rolling(window).var()
)

rolling_beta.plot(figsize=(10,4))
plt.title("Rolling Beta — NVDA (6-month window)")

plt.show()
