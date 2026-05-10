# Introduction
## Purpose of Testing
* Validate correctness of all risk models (VaR, ES, volatility, pricing)
* Ensure statistical and mathematical consistency
* Test robustness under different market conditions
* Verify implementation matches theoretical models
## Scope of Testing
* data_loader
* covariance estimation
* volatility models (EWMA, rolling window)
* pricing models (stock & options)
* risk models (VaR, ES)
* backtesting

## Data Module

- Purpose: Ensure the data pipeline reliably produces clean, consistent, and correctly structured inputs for downstream risk and pricing models.

---

### Test 1 - Data Download Integrity Test
- Input: tickers ["AAPL", "MSFT", "TSLA"], date range (2020–2025)
- Method:
  - Run `yf.download()` pipeline
  - Save raw stock prices to CSV
- Check:
  - File `stock_prices.csv` is created
  - No empty dataset returned
- Expected:
  - Non-empty price dataset with correct tickers
  - No missing download failures

---

### Test 2 - Price Data Structure Test
- Input: raw stock price CSV
- Method:
  - Load CSV in `loader.py`
  - Inspect DataFrame shape and columns
- Check:
  - Shape = (T, N assets)
  - Columns match tickers
  - Index is datetime sorted
- Expected:
  - No missing columns or misalignment

---

### Test 3 - Return Calculation Correctness Test
- Input: cleaned price data
- Method:
  - Compute log returns:
    r_t = log(P_t / P_{t-1})
- Check:
  - No NaN explosion beyond first row
  - Output shape = (T-1, N)
- Expected:
  - Returns are finite and correctly aligned

---

### Test 4 - Data Cleaning Robustness Test
- Input: raw price dataset with potential missing values
- Method:
  - Apply `dropna()` and sorting
- Check:
  - No NaN values remain
  - Data remains time consistent
- Expected:
  - Clean monotonic time series

---

### Test 5 - Loader Consistency Test
- Input: all CSV files (prices, returns, portfolio, options, rates)
- Method:
  - Run `load_all()` function
- Check:
  - All datasets load without error
  - Returned dictionary contains all keys
- Expected:
  - Correct shapes and types for each dataset

---

### Test 6 - End-to-End Pipeline Test
- Input: full pipeline execution
- Method:
  - Run download → process → load
- Check:
  - All files generated successfully
  - Loader reads processed outputs correctly
- Expected:
  - No pipeline breakage across modules

---

### Pass Criteria
- All CSV files successfully created and readable
- No runtime errors in full pipeline execution
- Returns matrix correctly derived from prices
- All datasets are time-aligned and non-empty
- Loader returns complete dataset dictionary

## Utility Module (`utils`)
### Covariance Module
- Purpose: Validate the covariance estimation produces mathematically correct and stable correlation structure between asset returns.
- Test 1 - Symmetry Test:
    - Input: returns matrix (T×N)
    - Method: compute Σ
    - Check: Σ == Σ^(T)
    - Expected: symmetry within floating-point tolerance
- Test 2 - Benchmark Accuracy 
    - Input: historical returns dataset
    - Method: 
        - compute Σ_custom
        - compute Σ_numpy = np.cov()
    - Compare: 
        - max absolute difference < ep
- Test 3 - Positive Semi-Definite Check
    - Method: Compute eigenvalues of Σ
    - Expected: all eigenvalues > 0 (or near-tolerance)
- Test 4 - Missing Data Robustness
    - Input: returns with NaN values
    - Expected
        - no runtime error
        - output covariance remains valid
Pass Criteria:
- Symmetry error < 1e-8
- Max deviation from NumPy covariance < tolerance
- No NaN or infinite values in output
- All eigenvalues ≥ -ε (numerical tolerance)             
