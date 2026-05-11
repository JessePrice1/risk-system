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

# Group B — Core System Test Plan (main + config)

## Purpose of Testing
The purpose of testing the Core System is to verify that the full risk pipeline executes correctly using global configuration parameters. This includes validating that the system orchestrates pricing, simulation, risk measurement, and portfolio aggregation in a consistent and stable manner.

The tests validate:
- Correct execution of the main risk pipeline
- Correct usage of configuration parameters (confidence, horizon, simulations)
- Stability of Monte Carlo outputs under fixed seeds
- Consistency of portfolio aggregation outputs

---

# Test 1 — Main Pipeline Execution Test

## Purpose
Verify that `main.py` runs end-to-end without runtime errors.

## Validation
- Script executes successfully
- All three sections run:
  - Stock VaR
  - Option VaR
  - Portfolio aggregation
- No import or runtime failures

## Expected Result
System completes full risk workflow and prints results.

---

# Test 2 — Config Parameter Propagation Test

## Purpose
Verify that configuration values are correctly used in the system.

## Validation
- `DEFAULT_CONFIDENCE` used in:
  - Stock VaR
  - Option VaR
  - Portfolio VaR
- `DEFAULT_HORIZON_DAYS` used in Monte Carlo functions
- `DEFAULT_N_SIM` used consistently across all simulations

## Expected Result
All risk outputs reflect configuration settings consistently.

---

# Test 3 — Portfolio Risk Consistency Test

## Purpose
Verify that portfolio aggregation produces logically consistent risk outputs.

## Validation
- Portfolio VaR ≥ individual component VaRs (or logically consistent aggregation)
- CVaR ≥ VaR for all outputs
- Diversification ratio is finite and positive
- No NaN or infinite values

## Expected Result
Portfolio risk metrics are stable, finite, and consistent.

---

# Summary of Results

The Core System tests demonstrate that:
- The full risk pipeline executes successfully
- Configuration parameters correctly control system behavior
- Portfolio aggregation produces stable and meaningful outputs
- Monte Carlo simulation results are consistent and reproducible

The Core System is therefore considered operationally stable and correctly integrated.