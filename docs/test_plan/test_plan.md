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

# Group C — Pricing Models Test Plan  
## Modules: stock_pricer.py + option_pricer.py  

---

# Objective

This test suite validates the correctness, stability, and financial realism of:

- Black-Scholes European option pricing model
- GBM (Geometric Brownian Motion) calibration model

The goal is to ensure that both models are mathematically correct and behave consistently under realistic market conditions.

---

# Test 1 — Black-Scholes Output Validity (Component Test)

## Purpose
Ensure the Black-Scholes formula produces valid and non-negative option prices.

## What is tested
- Call and put prices are positive
- Call and put differ appropriately
- No NaN or infinite values

## Expected Result
- Valid financial prices
- No numerical instability

---

# Test 2 — GBM Calibration Validity (Robustness Test)

## Purpose
Check that GBM calibration produces stable and finite estimates of volatility and drift.

## What is tested
- σ (volatility) > 0
- μ is finite
- Model works on simulated market data

## Expected Result
- Stable parameter estimates
- No crashes or invalid outputs

---

# Test 3 — Volatility Sensitivity (Model Behavior Test)

## Purpose
Ensure option prices behave correctly under changes in volatility.

## What is tested
- Higher volatility leads to higher option price
- Monotonic relationship preserved

## Expected Result
- Consistent financial intuition
- No inverted or unstable pricing behavior

---

# Overall Validation Criteria

The pricing system is valid if:

- ✔ Black-Scholes outputs are finite and positive
- ✔ GBM calibration produces realistic parameters
- ✔ Option prices increase with volatility
- ✔ No numerical instability across tests

---

# Model Limitations

- Assumes log-normal returns (GBM assumption)
- Constant volatility in Black-Scholes model
- No jumps or fat tails
- Calibration depends on quality of historical data

# Group D — Risk Models Test Plan

## Models Covered
This test plan validates the correctness and robustness of the following risk models:

- historical_var
- parametric_var
- monte_carlo_stock_var
- monte_carlo_option_var
- monte_carlo_portfolio_var
- cvar_from_pnl / portfolio_cvar

---

# 1. Test Objective

The objective is to ensure that the Group D risk models:

- Produce mathematically correct risk measures (VaR and CVaR)
- Behave consistently under controlled inputs
- Are robust across different market scenarios (low/high volatility, different distributions)
- Maintain logical relationships between risk measures (e.g., higher volatility → higher VaR)

---

# 2. Test Design Overview

We implement **three core test cases**:

### Test 1 — Historical VaR Consistency
Checks:
- VaR is positive
- CVaR ≥ VaR (loss tail behavior is correct)
- Increasing losses increase VaR

---

### Test 2 — Parametric VaR Volatility Sensitivity
Checks:
- Higher volatility increases VaR
- VaR is finite and positive
- Model reacts correctly to risk scaling

---

### Test 3 — Monte Carlo Portfolio Coherence
Checks:
- Portfolio VaR ≥ individual VaR (diversification effect is bounded)
- P&L arrays are correctly generated
- VaR is finite and stable under simulation

---

# 3. Robustness Coverage

The tests also indirectly validate:

- Extreme loss scenarios (tail risk behavior)
- Sensitivity to volatility and return distributions
- Stability under Monte Carlo randomness
- Consistency between analytical and simulation-based models

---

# 4. Limitations Acknowledged

- Assumes normality in parametric model
- Monte Carlo results depend on seed and number of simulations
- Historical VaR depends on sample size and past relevance

# Group F — Volatility / Statistics Test Plan

## Overview
This test plan validates the correctness, stability, and statistical soundness of the Group F volatility and statistical models:

- EWMA volatility (`ewma_volatility`)
- GARCH(1,1) volatility (`garch_11_volatility`)
- Implied volatility solver (`implied_vol`)
- Statistical utilities (`return_statistics`, `jarque_bera_test`)
- Covariance estimation (`covariance_matrix`)

The goal is to ensure:
- Mathematical correctness of implementations
- Stability under realistic and extreme inputs
- Statistical consistency with expected financial behavior

---

# Test 1 — Volatility Positivity & Stability (EWMA + GARCH)

## Purpose
Ensure volatility models produce:
- Positive volatility values
- Finite outputs
- Stable behavior under random return inputs

## Design
We simulate random returns and verify:
- EWMA volatility is positive and non-NaN
- GARCH volatility is positive and non-NaN

## Expected Result
- No negative or NaN volatility values
- Volatility reacts to randomness but remains stable

---

# Test 2 — Implied Volatility Consistency

## Purpose
Validate that implied volatility solver:
- Produces a finite solution
- Produces a volatility consistent with Black-Scholes pricing

## Design
- Generate synthetic option price using known volatility
- Recover implied volatility
- Compare recovered vs true volatility

## Expected Result
- |σ_implied − σ_true| is small (within tolerance)
- No convergence failure (NaN)

---

# Test 3 — Statistical & Covariance Consistency

## Purpose
Validate statistical correctness of:
- Return statistics (mean, std, skew, kurtosis)
- Covariance matrix structure

## Design
- Generate correlated synthetic returns
- Compute:
  - statistics summary
  - covariance matrix
- Validate:
  - covariance matrix is symmetric
  - diagonal entries are positive
  - statistics are finite

## Expected Result
- Covariance matrix is symmetric and positive diagonal
- All statistics are finite and well-defined

---

# Test Coverage Summary

| Area | Coverage |
|------|----------|
| EWMA Volatility | ✔ |
| GARCH Volatility | ✔ |
| Implied Volatility | ✔ |
| Statistical Metrics | ✔ |
| Covariance Matrix | ✔ |

---

# Limitations

- No real market data stress testing included
- No regime-switching volatility tested
- Covariance assumes clean returns (no microstructure noise)