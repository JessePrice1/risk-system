print("FILE IS RUNNING")
import pandas as pd
from pathlib import Path

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"

# ---------------------------------------------------
# Load functions
# ---------------------------------------------------

def load_prices():
    prices = pd.read_csv(
        RAW_PATH / "stock_prices.csv",
        index_col=0,
        parse_dates=True
    )
    prices = prices.sort_index().dropna()
    return prices


def load_returns():
    returns = pd.read_csv(
        PROCESSED_PATH / "returns_matrix.csv",
        index_col=0,
        parse_dates=True
    )
    return returns


def load_portfolio():
    return pd.read_csv(RAW_PATH / "portfolio_positions.csv")


def load_options():
    return pd.read_csv(RAW_PATH / "option_data.csv")


def load_rates():
    return pd.read_csv(RAW_PATH / "rates.csv")


# ---------------------------------------------------
# Optional: master loader (VERY IMPORTANT FOR YOUR PROJECT)
# ---------------------------------------------------

def load_all():
    return {
        "prices": load_prices(),
        "returns": load_returns(),
        "portfolio": load_portfolio(),
        "options": load_options(),
        "rates": load_rates()
    }

if __name__ == "__main__":
    data = load_all()

    print("\nLOADED DATA SUMMARY")
    print("--------------------")

    print("Prices shape:", data["prices"].shape)
    print("Returns shape:", data["returns"].shape)
    print("Portfolio:\n", data["portfolio"].head())
    print("Options:\n", data["options"].head())
    print("Rates:\n", data["rates"].head())