import numpy as np
import pandas as pd
import os
from pathlib import Path
import yfinance as yf

from data.data_loader.loader import load_all

# ---------------------------------------------------
# Paths
# ---------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_PATH = BASE_DIR / "data" / "raw"
PROCESSED_PATH = BASE_DIR / "data" / "processed"


# ===================================================
# TEST 1 — Data Download Integrity Test
# ===================================================

def test_data_download_integrity():
    print("\nTEST 1 — Data Download Integrity")

    tickers = ["AAPL", "MSFT", "TSLA"]

    data = yf.download(
        tickers,
        start="2020-01-01",
        end="2025-01-01",
        auto_adjust=True
    )

    assert data is not None, "Download returned None"
    assert not data.empty, "Downloaded dataset is empty"

    file_exists = (RAW_PATH / "stock_prices.csv").exists()

    print("File exists:", file_exists)

    assert file_exists, "stock_prices.csv was not created"

    print("PASS: Data downloaded successfully")


# ===================================================
# TEST 2 — Price Data Structure Test
# ===================================================

def test_price_structure():
    print("\nTEST 2 — Price Structure")

    prices = pd.read_csv(RAW_PATH / "stock_prices.csv", index_col=0, parse_dates=True)

    assert prices.shape[1] == 3, "Expected 3 assets"
    assert list(prices.columns) == ["AAPL", "MSFT", "TSLA"], "Unexpected columns"
    assert prices.index.is_monotonic_increasing, "Index not sorted"

    print("Shape:", prices.shape)
    print("PASS: Price structure correct")


# ===================================================
# TEST 3 — Return Calculation Correctness
# ===================================================

def test_returns_correctness():
    print("\nTEST 3 — Returns Calculation")

    prices = pd.read_csv(RAW_PATH / "stock_prices.csv", index_col=0, parse_dates=True)

    returns = np.log(prices / prices.shift(1)).dropna()

    assert returns.shape[0] == prices.shape[0] - 1, "Incorrect return rows"
    assert not returns.isnull().values.any(), "NaN values in returns"

    print("Shape:", returns.shape)
    print("PASS: Returns computed correctly")


# ===================================================
# TEST 4 — Data Cleaning Robustness Test
# ===================================================

def test_data_cleaning():
    print("\nTEST 4 — Data Cleaning")

    prices = pd.read_csv(RAW_PATH / "stock_prices.csv", index_col=0, parse_dates=True)

    cleaned = prices.sort_index().dropna()

    assert not cleaned.isnull().values.any(), "NaN values remain"
    assert cleaned.index.is_monotonic_increasing, "Time ordering broken"

    print("PASS: Data cleaning stable")


# ===================================================
# TEST 5 — Loader Consistency Test
# ===================================================

def test_loader_consistency():
    print("\nTEST 5 — Loader Consistency")

    data = load_all()

    required_keys = ["prices", "returns", "portfolio", "options", "rates"]

    for key in required_keys:
        assert key in data, f"Missing key: {key}"
        assert data[key] is not None, f"{key} is None"

    print("Loaded keys:", data.keys())
    print("PASS: Loader consistent")


# ===================================================
# TEST 6 — End-to-End Pipeline Test
# ===================================================

def test_pipeline_integrity():
    print("\nTEST 6 — Pipeline Integrity")

    files = [
        RAW_PATH / "stock_prices.csv",
        RAW_PATH / "portfolio_positions.csv",
        RAW_PATH / "option_data.csv",
        RAW_PATH / "rates.csv",
        PROCESSED_PATH / "returns_matrix.csv"
    ]

    for f in files:
        assert f.exists(), f"Missing file: {f}"

    print("All pipeline files exist")
    print("PASS: End-to-end pipeline working")


# ===================================================
# RUN ALL TESTS
# ===================================================

if __name__ == "__main__":
    test_data_download_integrity()
    test_price_structure()
    test_returns_correctness()
    test_data_cleaning()
    test_loader_consistency()
    test_pipeline_integrity()

    print("\nALL DATA MODULE TESTS COMPLETED")