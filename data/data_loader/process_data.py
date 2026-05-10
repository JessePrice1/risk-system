import numpy as np
import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

RAW_PATH = Path("data/raw")
PROCESSED_PATH = Path("data/processed")

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------
# Load stock prices
# ---------------------------------------------------

prices = pd.read_csv(
    RAW_PATH / "stock_prices.csv",
    index_col=0,
    parse_dates=True
)

# ---------------------------------------------------
# Clean prices
# ---------------------------------------------------

prices = prices.sort_index()

prices = prices.dropna()

prices.to_csv(PROCESSED_PATH / "cleaned_prices.csv")

print("Saved cleaned_prices.csv")


# ---------------------------------------------------
# Compute log returns
# ---------------------------------------------------

returns = np.log(prices / prices.shift(1))

returns = returns.dropna()

returns.to_csv(PROCESSED_PATH / "returns_matrix.csv")

print("Saved returns_matrix.csv")


# ---------------------------------------------------
# Clean option data
# ---------------------------------------------------

options = pd.read_csv(
    RAW_PATH / "option_data.csv"
)

options = options.dropna()

options.to_csv(
    PROCESSED_PATH / "cleaned_options.csv",
    index=False
)

print("Saved cleaned_options.csv")