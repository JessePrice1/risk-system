tests/
│
├── test_core_system.py — Data Layer
│ ├── data_loader
│ ├── download_data
│ └── process_data
│
├── test_data_layer.py — Core System
│ ├── main
│ └── config
│
├── test_pricing.py — Pricing Models
│ ├── stock_pricer
│ └── option_pricer
│
├── test_risk_system.py — Risk Models (VaR / ES)
│ ├── historical_var
│ ├── parametric_var
│ ├── monte_carlo_var
│ ├── historical_es
│ ├── parametric_es
│ └── monte_carlo_es
│
└── test_vol_stats.py — Volatility / Statistics
├── ewma
├── rolling_window
├── implied_vol
├── statistics
└── covariance


`test_core_system.py`

Test 1 Passed — Pipeline runs successfully
Test 2 Passed — Config values valid
Test 3 Passed — Portfolio consistency valid

All Core System tests passed.

Core system tests confirm that the full risk pipeline executes correctly, configuration parameters are valid, and portfolio-level Monte Carlo VaR/ES computations remain internally consistent and numerically stable across stock and option components.

`test_data_layer.py`

FILE IS RUNNING
Test 1 Passed — Raw data files exist
Test 2 Passed — Returns matrix valid
Test 3 Passed — Loader working correctly

All Data Layer tests passed.

`test_pricing.py`

Test 1 Passed — Black-Scholes validity
Test 2 Passed — GBM calibration valid
Test 3 Passed — Volatility sensitivity correct

All Group C Pricing tests passed.

Data layer tests confirm that all required raw and processed datasets are correctly generated, the returns matrix is clean and valid, and the data loader reliably integrates and exposes all core financial data structures for downstream use.

`test_risk_system.py`

✔ Test 1 Passed — Historical VaR consistency
✔ Test 2 Passed — Parametric VaR volatility sensitivity
✔ Test 3 Passed — Monte Carlo portfolio coherence

✔ All Group D Risk Model tests passed.

Risk system tests confirm that historical, parametric, and Monte Carlo VaR/ES implementations are mathematically consistent, correctly respond to volatility changes, and produce coherent and well-behaved portfolio-level risk estimates.

`test_vol_stats.py`

Test 1 Passed — Volatility models stable
Test 2 Passed — Implied volatility accurate
Test 3 Passed — Stats and covariance valid

All Group F tests passed.

Volatility and statistics tests confirm that EWMA/GARCH volatility models remain stable and positive, implied volatility is accurately recovered from option prices, and return statistics and covariance matrices are mathematically consistent and well-behaved.
