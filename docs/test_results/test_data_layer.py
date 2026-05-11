# test_data_layer.py

from pathlib import Path
import pandas as pd
from data.data_loader.loader import load_all

# ---------------------------------------------------
# Test 1 — Raw Data File Generation Test
# ---------------------------------------------------

def test_raw_data_files_exist():
    raw_path = Path("data/raw")

    assert (raw_path / "stock_prices.csv").exists()
    assert (raw_path / "portfolio_positions.csv").exists()
    assert (raw_path / "option_data.csv").exists()
    assert (raw_path / "rates.csv").exists()

    print("Test 1 Passed — Raw data files exist")


# ---------------------------------------------------
# Test 2 — Returns Matrix Processing Test
# ---------------------------------------------------

def test_returns_matrix():
    processed_path = Path("data/processed")

    returns = pd.read_csv(
        processed_path / "returns_matrix.csv"
    )

    assert not returns.empty
    assert returns.isna().sum().sum() == 0

    print("Test 2 Passed — Returns matrix valid")


# ---------------------------------------------------
# Test 3 — Loader Integration Test
# ---------------------------------------------------

def test_loader():
    data = load_all()

    assert "prices" in data
    assert "returns" in data
    assert "portfolio" in data
    assert "options" in data
    assert "rates" in data

    assert not data["prices"].empty
    assert not data["returns"].empty

    print("Test 3 Passed — Loader working correctly")


# ---------------------------------------------------
# Run Tests
# ---------------------------------------------------

if __name__ == "__main__":
    test_raw_data_files_exist()
    test_returns_matrix()
    test_loader()

    print("\nAll Data Layer tests passed.")