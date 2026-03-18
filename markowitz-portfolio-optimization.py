import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf  
import datetime

tickers = ['AAPL', 'JPM', 'JNJ', 'XOM', 'PG', 'NEE']
start = '2018-01-01'
end = datetime.date.today()

data = yf.download(tickers, start=start, end=end, auto_adjust=True)

prices = data['Close']
print(prices.head())
print(prices.tail())

returns = np.log(prices/prices.shift(1))
returns = returns.dropna()

returns.plot(figsize=(12,4))
plt.title("Daily log returns")
plt.show()

mu = returns.mean()
mu_annual = mu*252 
Sigma = returns.cov()
print(Sigma)
print(mu_annual)

ones = np.ones(len(Sigma))
Sigma_inv = np.linalg.inv(Sigma)

w_gmv = Sigma_inv @ ones
w_gmv = w_gmv / (ones.T @ Sigma_inv @ ones)

gmv_weights = pd.Series(w_gmv, index=Sigma.index)
print(gmv_weights)

gmv_returns = returns @ gmv_weights

gmv_vol = gmv_returns.std() * np.sqrt(252)

asset_vol = returns.std() * np.sqrt(252)

comparison = pd.concat([asset_vol, pd.Series(gmv_vol, index=['GMV'])])
comparison

gmv_returns.cumsum().plot(figsize=(12,4))
plt.title("GMV Portfolio Cumulative Log Returns")
plt.show()

plt.savefig("outputs/gmv_cumulative_returns.png")

plt.show()
