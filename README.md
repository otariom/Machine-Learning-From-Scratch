# Markowitz Portfolio Optimization – Global Minimum Variance (GMV)

This project implements Markowitz portfolio theory to construct a **Global Minimum Variance (GMV)** portfolio using historical equity data.
The goal is to demonstrate how diversification and covariance between assets can reduce overall portfolio risk.


## Motivation

Modern Portfolio Theory shows that portfolio risk depends not only on individual asset volatility, but also on how assets move relative to each other.
This project focuses on the **risk-minimization problem**, independent of expected returns.

---

# Data
- Source: Yahoo Finance (`yfinance`)
- Assets: AAPL, JPM, JNJ, XOM, PG, NEE
- Frequency: Daily adjusted prices
- Period: 2018 – Present
---

## Methodology
1. Download adjusted closing prices
2. Compute **log returns**
3. Estimate the **covariance matrix**
4. Compute Global Minimum Variance weights
5. Construct portfolio returns
6. Compare portfolio volatility with individual assets
---

## Results
- The GMV portfolio exhibits lower annualized volatility than any single asset
- Risk reduction confirms diversification benefits predicted by theory
- Portfolio cumulative returns are visualized for interpretability
---

## Tech Stack
- Python
- NumPy
- Pandas
- Matplotlib
- yFinance
