1. System Architecture
2. Module Descriptions
3. System Design Details
* 3.1 Purpose
* 3.2 Assumptions
* 3.3 Interfaces
* 3.4 Limitations

## 1. System Architecture

```text
risk_system/
│
├── Implemented/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── data_loader/
│   │   └── loader.py
│   │   └── download_data.py
│   │   └── process_data.py
│
├── docs/
│   ├── model_documentation/
│   ├── software_design/
│   ├── test_plan/
│   └── test_results/
│
├── src/
│   ├── main.py
│   ├── config.py
│   │
│   ├── pricing/
│   │   ├── stock_pricer.py
│   │   ├── option_pricer.py
│   │   └── greeks.py
│   │
│   ├── risk/
│   │   ├── historical_var.py
│   │   ├── parametric_var.py
│   │   ├── monte_carlo_var.py
│   │   ├── expected_shortfall.py
│   │   └── backtesting.py
│   │
│   ├── volatility/
│   │   ├── ewma.py
│   │   ├── garch.py
│   │   └── implied_vol.py
│   │
│   ├── utils/
│   │   ├── statistics.py
│   │   ├── covariance.py
│   │   └── plots.py
│
│
├── requirements.txt
```

**2. Data Flow**

* download_data
* Raw Data -> 
* loader.py -> 
* processed data -> 
* volatility estimation -> 
* pricing models -> 
* risk models (VaR / ES) -> 
* backtesting -> 
* reports

**3. System Design Details**

# **3. System Design Details**

---

# **Modules Overview (Purpose / Assumptions / Interfaces / Limitations)**

---

## Data Module (System Design)

## Purpose
The Data Module is responsible for sourcing, cleaning, transforming, and providing structured financial data used across the risk system. It acts as the foundational input layer for all downstream components including volatility estimation, pricing models, and risk calculations (VaR/ES). It ensures consistent and reproducible access to market data, portfolio positions, option data, and risk-free rates.

---

## Assumptions
- Market data (stock prices) is assumed to be correctly retrieved from Yahoo Finance via `yfinance`.
- Adjusted close / close prices are assumed to be sufficient proxies for tradable asset prices.
- Log returns are assumed to approximate continuously compounded returns.
- Missing data is assumed to be minimal and is handled via row-wise deletion (`dropna`).
- Portfolio positions are assumed static over the analysis period.
- Option data is assumed to be simplified (no full option chain, only representative contracts).
- Risk-free rate is assumed constant over time (simplified single-rate input).
- Data is assumed to be correctly time-aligned after sorting and preprocessing.

---

## Interface
The Data Module exposes structured datasets through a loader interface (`loader.py`).

### Inputs
- Stock tickers (e.g., AAPL, MSFT, TSLA)
- Date range for historical data extraction
- CSV files stored in:
  - `data/raw/`
  - `data/processed/`

### Outputs
- `prices` → DataFrame (T × N) of cleaned stock prices
- `returns` → DataFrame (T × N) of log returns
- `portfolio` → holdings with quantities and asset types
- `options` → simplified option contracts (strike, maturity, type)
- `rates` → risk-free rate data
- `load_all()` → dictionary containing all datasets

### Module Flow
1. `download_data.py`
   → pulls raw market + synthetic data and stores CSVs in `data/raw/`

2. `process_data.py`
   → cleans raw inputs and computes:
   - cleaned prices
   - log return matrix
   - cleaned options dataset  
   Outputs stored in `data/processed/`

3. `loader.py`
   → provides unified access layer to all datasets for model usage

---

## Limitations
- Data coverage is limited to a small set of equities (AAPL, MSFT, TSLA), which may not represent full market behavior.
- Option data is synthetic and does not reflect real option market surfaces or volatility smiles.
- Risk-free rate is static and does not vary over time (no yield curve modeling).
- No handling of survivorship bias or missing market events beyond basic `dropna`.
- No adjustment for corporate actions beyond `auto_adjust=True` in price retrieval.
- Data frequency is limited to daily observations (no intraday modeling).
- Simplified structure does not yet include alternative asset classes (bonds, FX, commodities).

---

Data Structures
* prices: DataFrame (T × N) — time-series of asset prices
* returns: DataFrame (T × N) — log return matrix
* portfolio: dict or list of dicts — asset holdings and quantities
* options: list of dicts — option contracts (strike, maturity, type)
* rates: float or time series — risk-free rate input
* load_all(): dict — aggregated dataset container for system-wide access

--

The Data Module provides a minimal but complete pipeline from raw market data acquisition to structured datasets ready for quantitative modeling. It ensures consistency across downstream risk, pricing, and volatility modules while maintaining simplicity appropriate for a prototype risk system.

---

## **Docs Module**

### Purpose
Stores all project documentation including model documentation, software design, test plans, and test code for results.

### Assumptions
- Documentation is manually maintained and updated

### Interface
- Input: markdown / text files
- Output: structured reports for submission

### Limitations
- No automated validation of documentation consistency with code

---

## **Main Module**

### Purpose
Entry point of the system that orchestrates simulation pipeline, model execution, risk computation, and result generation.

### Assumptions
- All submodules are correctly implemented
- Execution follows a predefined pipeline order

### Interface
- Input: config parameters + dataset paths
- Output: demo run of results (VaR, ES)

### Limitations
- Not designed for partial execution of pipeline components

---

## **Config Module**

### Purpose
Stores global model parameters such as confidence levels, time horizon, volatility settings, and simulation parameters.

### Assumptions
- Parameters are fixed per run
- Parameters are externally validated by user

### Interface
- Input: No runtime input; provides globally defined constants imported by other modules
- Output: parameter values used across models

### Limitations
- Does not dynamically calibrate parameters from data

---

## **Pricing Module**

### Purpose
Computes asset and option pricing, Greeks, and GBM calibration from historical prices using financial models.

**Submodules:**
- `option_pricer.py` — Black-Scholes European option pricing (call/put)
- `stock_pricer.py` — GBM parameter calibration via MLE (mu, sigma) from historical prices; includes diagnostics (skewness, kurtosis) to assess GBM fit
- `greeks.py` — Delta, Gamma, Vega, Theta for European options

### Assumptions
- Market follows GBM dynamics (lognormal returns) for stock calibration
- Options are European-style; no early exercise
- Volatility input is constant over option lifetime (no smile/skew modeling)
- Calibration window is user-specified; longer windows smooth noise but lag regime changes

### Interface
- Input: asset prices, strikes, maturities, volatility, risk-free rate
- Output: option prices, Greeks, calibration statistics (mu, sigma, skewness, kurtosis)

### Limitations
- Does not model complex market frictions or transaction costs
- No support for American options or exotic payoffs
- GBM calibration may produce misleading parameters during regime transitions

---

## **Risk Module**

### Purpose
Implements risk metrics including VaR and Expected Shortfall (CVaR), statistical backtesting, and multi-regime stress testing. The module supports multiple methodologies: historical, parametric, and Monte Carlo methods, along with model validation tests.

**Submodules:**
- `monte_carlo_var.py` — GBM-based MC simulation for stocks, options (BS repricing), and combined portfolios with correlation support
- `expected_shortfall.py` — CVaR computation from simulated P&L; portfolio-level CVaR with subadditivity verification (proving coherence vs VaR)
- `backtesting.py` — Kupiec Proportion of Failures test (unconditional coverage) and Christoffersen independence test (violation clustering detection)
- `historical_var.py` — Non-parametric VaR/CVaR from historical return distributions
- `parametric_var.py` — Variance-covariance VaR/CVaR assuming normal returns

### Assumptions
- Return distributions approximate historical behavior or assumed parametric forms
- Portfolio composition is static over risk horizon
- Monte Carlo option VaR uses risk-neutral drift (r) for GBM simulation and Black-Scholes for repricing at horizon
- Backtesting assumes daily P&L observations with rolling recalibration

### Interface
- Input: returns, portfolio weights, confidence levels, option parameters (S0, K, T, sigma), correlation matrices
- Output: VaR / CVaR estimates, backtesting statistics (LR, p-value, pass/fail), regime comparison tables

### Limitations
- Sensitive to distributional assumptions (GBM assumes lognormal; real returns exhibit fat tails and skewness)
- CVaR estimates depend on tail sample size; may be noisy at extreme confidence levels (99%+)
- Backtesting power is limited with small sample sizes
- No stochastic volatility or jump-diffusion models implemented

---

## **Volatility Module**

### Purpose
Estimates time-varying volatility using EWMA, rolling window methods, and implied volatility from market prices.

### Assumptions
- Volatility is time-varying but can be approximated using historical data
- Implied volatility reflects market expectations

### Interface
- Input: return series / option prices
- Output: volatility estimates

### Limitations
- EWMA and rolling models may lag sudden regime changes
- Implied volatility depends on model assumptions (e.g., Black-Scholes)

---

## **Utils Module**

### Purpose
Provides shared mathematical and statistical functions used across the system.

### Assumptions
- Mathematical operations assume valid numeric inputs

### Interface
- Input: numerical arrays, DataFrames, or risk metric outputs
- Output: covariance matrices, statistical dictionaries, and Matplotlib figure objects

### Limitations
- Does not validate financial meaning of inputs

---

## **Tests Module**

### Purpose
The test module checks if the implementations are correct and robust for all pricing, volatility, and risk models.

### Assumptions
- Benchmark models (e.g., NumPy covariance) are correct references
- Test datasets are representative of real market behavior

### Interface
- Input: model outputs + benchmark datasets
- Output: pass/fail results, error metrics, robustness indicators

### Limitations
- Tests validate implementation correctness, not financial truth
- Cannot guarantee predictive performance in real markets

## **Requirements Module**

### Purpose
Defines Python dependencies required to run the project.

### Assumptions
- All dependencies are compatible across system

### Interface
- Input: package list (requirements.txt)
- Output: installed environment

### Limitations
- Version conflicts may occur if environment changes
