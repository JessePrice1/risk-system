import yfinance as yf
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_PATH = BASE_DIR / "data" / "raw"
RAW_PATH.mkdir(parents=True, exist_ok=True)

print("NEWLY UPDATED FILE")

tickers = ["AAPL", "MSFT", "TSLA"]

prices = yf.download(
    tickers,
    start="2020-01-01",
    end="2025-01-01",
    auto_adjust=True
)

prices = prices["Close"]

prices.to_csv(RAW_PATH / "stock_prices.csv")

print("Saved stock_prices.csv")

# ---------------------------------------------------
# Example portfolio positions
# ---------------------------------------------------

portfolio = pd.DataFrame({
    "ticker": ["AAPL", "MSFT", "TSLA"],
    "quantity": [100, 50, 25],
    "asset_type": ["stock", "stock", "stock"]
})

portfolio.to_csv(
    RAW_PATH / "portfolio_positions.csv",
    index=False
)

print("Saved portfolio_positions.csv")


# ---------------------------------------------------
# Example option data
# ---------------------------------------------------

options = pd.DataFrame({
    "ticker": ["AAPL", "MSFT"],
    "type": ["call", "put"],
    "strike": [200, 350],
    "maturity": [0.5, 1.0],
    "market_price": [12.5, 18.0]
})

options.to_csv(
    RAW_PATH / "option_data.csv",
    index=False
)

print("Saved option_data.csv")


# ---------------------------------------------------
# Example risk-free rates
# ---------------------------------------------------

rates = pd.DataFrame({
    "date": ["2024-01-01"],
    "rate": [0.05]
})

rates.to_csv(
    RAW_PATH / "rates.csv",
    index=False
)

print("Saved rates.csv")