# Group A — Data Layer Test Plan

## Purpose of Testing
The purpose of testing the Data Layer is to verify that financial datasets are correctly downloaded, processed, and loaded for downstream pricing and risk models.

The tests validate:
- Correct raw data generation
- Correct processing of stock prices into returns
- Correct loading of datasets through the loader interface

---

# Test 1 — Raw Data File Generation Test

## Purpose
Verify that `download_data.py` correctly creates all required raw datasets.

## Validation
- `stock_prices.csv` exists
- `portfolio_positions.csv` exists
- `option_data.csv` exists
- `rates.csv` exists

## Expected Result
All raw data files are successfully generated in `data/raw/`.

---

# Test 2 — Returns Matrix Processing Test

## Purpose
Verify that `process_data.py` correctly computes log returns and processed datasets.

## Validation
- `returns_matrix.csv` exists
- No NaN values remain after cleaning
- Returns matrix is not empty

## Expected Result
Processed return data is mathematically valid and saved correctly.

---

# Test 3 — Loader Integration Test

## Purpose
Verify that `loader.py` correctly loads all datasets into memory.

## Validation
- `load_all()` returns:
  - prices
  - returns
  - portfolio
  - options
  - rates
- No dataset is empty

## Expected Result
All datasets load successfully and are accessible system-wide.

---

# Summary of Results

The Data Layer tests demonstrate that:
- Raw financial datasets are generated correctly
- Processed return calculations execute successfully
- Loader functions provide consistent dataset access

The Data Layer is therefore considered operationally stable and suitable for downstream financial modeling.