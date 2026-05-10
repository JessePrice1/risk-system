# Model Documentation (Validation Report)

## 1. Executive Summary

The system is designed to compute key measures of financial risk for portfolios containing stocks and options. In particular, it estimates Value at Risk (VaR), which represents the potential maximum loss over a given time horizon at a specified confidence level, and Expected Shortfall (ES), which measures the average loss in the worst-case tail beyond the VaR threshold.

To produce these risk estimates, the system implements three different modelling approaches. The Historical method uses past observed returns directly to infer potential future losses. The Parametric method assumes returns follow a specific statistical distribution, typically normal, and derives risk measures from estimated parameters such as mean and variance. The Monte Carlo method generates a large number of simulated price paths based on stochastic processes in order to approximate the distribution of portfolio returns and compute risk metrics from these simulations.

**TO DO: Conclusion:**
- Suitable for intended risk measurement with known limitations

---

## 2. Introduction

The system, titled Risk Calculation System v1.0, is designed to support the measurement and analysis of market risk within financial portfolios.

Its primary purpose is to evaluate and quantify portfolio exposure to market movements by computing key risk metrics, specifically Value at Risk (VaR) and Expected Shortfall (ES). These measures help estimate potential losses under normal and extreme market conditions, enabling more informed risk assessment and decision-making.

The system is intended for use by individuals working in risk management and portfolio analysis. These users may include risk analysts, quantitative analysts, and portfolio managers who require systematic tools for understanding and monitoring financial risk across equity and derivative positions.

---

## 3. Product Description

The Risk Calculation System v1.0 is a modular risk analysis tool designed to estimate and support the measurement of financial risk within a portfolio containing equities and derivatives. The system is structured to process financial inputs, apply risk models, and produce key quantitative risk metrics used in portfolio analysis.

### Inputs

The system is designed to accept the following categories of input data:

* Market data, including stock prices and option-related information
* Portfolio positions, representing holdings across assets and derivatives
* Model parameters, which define assumptions used in risk calculations (e.g., time horizon, confidence levels, volatility estimates)

### Outputs

The system produces a set of risk-related outputs used for analysis and interpretation:

* Risk metrics such as Value at Risk (VaR) and Expected Shortfall (ES), which summarize potential portfolio losses under different confidence levels
* Covariance matrices, which serve as intermediate statistical outputs used in estimating portfolio risk and asset relationships

These outputs are intended to support further analysis within risk management workflows rather than serve as standalone decision-making results.

---

## 4. Model Description (Main Section)

## Core Risk Models

- Historical VaR
- Parametric VaR
- Monte Carlo VaR
- ES models

## Supporting Models

- Covariance 
- EWMA volatility
- Rolling volatility
- Implied volatility (VERY important)
- Option pricing model

## Validation-Related Models

- Backtesting

## 4.1 Data Module

The data module is responsible for sourcing, cleaning, and structuring all financial input data used across the risk modelling system. It provides the foundational datasets required for pricing, volatility estimation, and risk calculation models.

### Purpose

The purpose of the data module is to ensure that all downstream models receive:

- Consistent and correctly aligned market data
- Cleaned and validated time series inputs
- Standardised portfolio and contract specifications

It acts as the interface between raw financial data sources and model-ready datasets.

---

### Inputs

The system ingests the following raw data types:

- Equity price data (e.g. AAPL, MSFT, TSLA) sourced via market data API
- Portfolio positions (asset holdings and quantities)
- Option contract data (strike, maturity, type, market price)
- Risk-free interest rates

---

### Outputs

The data module produces structured datasets:

- Cleaned price series (sorted, missing values removed)
- Log return matrix used for statistical modelling
- Standardised portfolio dataset
- Cleaned option dataset
- Interest rate time series

These outputs are stored as CSV files and used directly by all downstream models.

---

### Assumptions

- Market data retrieved from external APIs is sufficiently accurate for academic and modelling purposes
- Missing values can be safely removed without introducing significant bias
- Historical price data is a reasonable proxy for short-term risk estimation
- Asset identifiers (tickers) are consistent across all datasets
- Time series are assumed to be correctly aligned after preprocessing

---

### Interface

The data module interacts with the system through file-based inputs and outputs:

**Inputs:**
- Raw CSV files generated from data download scripts
- External API data (Yahoo Finance)

**Outputs:**
- `cleaned_prices.csv`
- `cleaned_options.csv`
- `returns_matrix.csv`
- `portfolio_positions.csv`
- `rates.csv`

These files are loaded by the `loader.py` module and consumed by:
- Covariance estimation
- Volatility models (EWMA, rolling, implied vol)
- Risk engines (VaR / ES)
- Option pricing models

---

### Limitations

- Reliance on historical market data may not capture future structural regime changes
- Simple missing value removal may introduce information loss
- No advanced data imputation techniques are used
- Data frequency is assumed to be daily and may not capture intraday risk dynamics
- External API data availability may vary across time periods

## 4.2 Covariance Estimation Model

The covariance estimation model is a core component of the Risk Calculation System v1.0 and provides a statistical measure of how asset returns move together within a portfolio. It is primarily used as an input into the parametric Value at Risk (VaR) framework, where portfolio risk depends on both individual asset volatility and the correlation structure between assets.

---

## Model Purpose

The purpose of the covariance model is to quantify linear dependencies between asset returns in order to capture diversification effects and joint market movements. This allows the system to more accurately represent portfolio-level risk compared to treating assets independently.

---

## Model Definition and Implementation

The model computes an empirical covariance matrix from historical asset return data.

- **Input:** a returns matrix of shape *(T × N)*, where *T* represents time observations and *N* represents assets  
- **Output:** an *(N × N)* covariance matrix representing pairwise relationships between all assets  

The implementation removes missing values and computes the covariance matrix using a standard numerical estimator (`np.cov`), treating assets as columns.

---

## Assumptions

The model is based on the following assumptions:

- Asset returns exhibit linear dependence, which is sufficient to capture co-movement for risk estimation  
- Historical return data provides a reasonable approximation of near-term dependency structure  
- The covariance structure is stable over the estimation window  
- Missing observations can be removed without materially affecting results  

---

## Validation Approach

The covariance model has been validated using a structured test framework, including:

- **Symmetry check:** verifies that the covariance matrix is symmetric (Σ = Σᵀ)  
- **Benchmark comparison:** compares results against NumPy’s covariance implementation  
- **Positive semi-definite check:** ensures eigenvalues are non-negative within numerical tolerance  
- **Missing data robustness test:** confirms stable output under incomplete input data  

---

## Limitations

While the model is suitable for portfolio risk estimation, it has several limitations:

- It assumes only linear relationships between assets and does not capture nonlinear or tail dependencies  
- It does not account for time-varying volatility or changing market regimes  
- It is sensitive to outliers in historical data  
- It uses a static historical estimation window, which may not fully reflect current market conditions  


## 5. Mathematical Description
 
- Covariance matrix formula  
- Returns definition 
- EWMA model 
- Rolling volatility 
- Implied volatility 
- Option Pricing Model (pricing/option_pricer.py) 
- Historical VaR 
- Parametric VaR 
- Monte Carlo VaR 
- Expected Shortfall (ES) Models

## 5.1 Covariance Model

The covariance estimation model computes the statistical dependence between asset returns using historical data. Let \( r_{t,i} \) denote the return of asset i at time t, where t = 1,…,T and i = 1,…,N.

---

## Model Inputs

The model takes as input a returns matrix:

\[
R =
\begin{bmatrix}
r_{1,1} & r_{1,2} & \cdots & r_{1,N} \\
r_{2,1} & r_{2,2} & \cdots & r_{2,N} \\
\vdots & \vdots & \ddots & \vdots \\
r_{T,1} & r_{T,2} & \cdots & r_{T,N}
\end{bmatrix}
\]

where:

- T = number of time observations  
- N = number of assets  

---

## Covariance Definition

The covariance between two assets i and j is defined as:

\[
\Sigma_{ij} =
\frac{1}{T - 1}
\sum_{t=1}^{T}
(r_{t,i} - \bar{r}_i)(r_{t,j} - \bar{r}_j)
\]

where:

- \( \bar{r}_i \) is the mean return of asset i  
- \( \Sigma_{ij} \) measures the linear co-movement between assets i and j  

---

## Covariance Matrix

The full covariance matrix is defined as:

\[
\Sigma =
\begin{bmatrix}
\Sigma_{11} & \Sigma_{12} & \cdots & \Sigma_{1N} \\
\Sigma_{21} & \Sigma_{22} & \cdots & \Sigma_{2N} \\
\vdots & \vdots & \ddots & \vdots \\
\Sigma_{N1} & \Sigma_{N2} & \cdots & \Sigma_{NN}
\end{bmatrix}
\]

This matrix is:

- symmetric (\( \Sigma = \Sigma^T \))  
- positive semi-definite (under standard assumptions)  
- used to represent the full dependency structure between assets  

---

## Output Interpretation

Each element of \( \Sigma \):

- diagonal terms \( \Sigma_{ii} \): variance of asset i  
- off-diagonal terms \( \Sigma_{ij} \): covariance between assets i and j  

---

## Role in Risk System

The covariance matrix is a key input to the Parametric VaR model, where portfolio variance is computed as:

\[
\sigma_p^2 = w^T \Sigma w
\]

where:

- w = vector of portfolio weights  
- Σ = covariance matrix  
- \( \sigma_p^2 \) = portfolio variance  

This allows portfolio risk to incorporate diversification effects and correlations between assets.

---

## 6. Calibration Methodology

- Historical data used for:
  - Returns
  - Covariance
  - EWMA volatility  

- Implied volatility calibrated from market option prices  

---

## 7. Validation Methodology and Scope

## 7.1 Scope of Validation (Covariance Model)

The scope of validation for the covariance estimation model focuses on ensuring that the computed covariance matrix accurately captures the joint statistical relationships between asset returns and is suitable for downstream use in the Parametric Value at Risk (VaR) framework.

The validation covers:

- Correctness of covariance computation from historical returns  
- Numerical stability and matrix properties  
- Robustness to incomplete or noisy input data  
- Consistency with standard statistical benchmarks  

The model is validated at a standalone level and also in the context of its integration into portfolio risk calculations.

The following aspects are explicitly included in scope:

- Simulated Equities return datasets (multi-asset portfolios)  
- Time-series structured financial data (T × N format)  

Out of scope:

- Forecasting of future covariance dynamics (no predictive modelling)  
- Market microstructure effects  
- High-frequency intraday modelling  

---

## 7.2 Validation Methodology

The covariance model is validated using a combination of statistical, numerical, and benchmark-based testing approaches.

### A. Statistical Property Tests

To ensure mathematical correctness of the covariance matrix:

- **Symmetry Test:**  
  Verified that the covariance matrix satisfies  
  \( \Sigma = \Sigma^T \)

- **Positive Semi-Definite (PSD) Test:**  
  Eigenvalues of the covariance matrix are computed to ensure non-negativity within numerical tolerance, confirming valid variance structure  

These tests ensure the output is a valid covariance matrix in a financial sense.

---

### B. Benchmark Comparison

The model output is compared against NumPy’s built-in covariance implementation (np.cov) using identical input data.

Validation checks include:

- Maximum absolute deviation between matrices  
- Element-wise consistency across all asset pairs  
- Tolerance-based numerical agreement  

This ensures the implementation aligns with industry-standard statistical computation.

---

### C. Robustness and Data Quality Testing

The model is tested for stability under real-world data imperfections:

- Missing value (NaN) handling in return series  
- Removal of incomplete observations prior to computation  
- Verification that output remains finite and well-defined  

This ensures the model is usable in realistic financial datasets where missing data is common.

---

## 7.3 Benchmark Model

The primary benchmark used for validation is:

- NumPy covariance function (np.cov) as a reference statistical estimator  

Additional theoretical benchmarks include:

- Expected symmetry property of covariance matrices  
- Positive semi-definite property of valid covariance estimators  

---

## 7.4 Outputs Reviewed

The following outputs are reviewed during validation:

- Covariance matrix \( \Sigma \) (full N × N structure)  
- Symmetry error (Σ − Σᵀ)  
- Eigenvalue spectrum (for PSD verification)  
- Maximum deviation from benchmark covariance matrix  
- Stability under missing data conditions  

---

## 8. Validation Results


## 8.1 Covariance Validation Results

A. Symmetry Test Results  
The covariance matrix was tested for symmetry using:  
Σ − Σᵀ  

Result:  
- Maximum symmetry error observed was extremely small (e.g. < 1e-8)  
- No statistically significant deviation from symmetry was detected  

Interpretation:  
This confirms the implementation produces a mathematically valid covariance matrix consistent with theoretical requirements.  

---

B. Benchmark Comparison (NumPy Validation)  
The computed covariance matrix was compared against NumPy’s standard implementation (np.cov)

Result:  
- Maximum absolute difference between matrices was negligible (within numerical tolerance)  
- Element-wise agreement across all asset pairs was observed  

Interpretation:  
The model is numerically consistent with industry-standard covariance estimation techniques.  

---

C. Positive Semi-Definite (PSD) Check  
Eigenvalues of the covariance matrix were computed  

Result:  
- All eigenvalues were non-negative within numerical tolerance  
- No invalid negative variance structure was observed  

Interpretation:  
The covariance matrix is valid for financial use and suitable for portfolio variance calculations in Parametric VaR:  

σₚ² = wᵀ Σ w  

---

D. Missing Data Robustness  
The model was tested with simulated missing values in the returns matrix  

Result:  
- No runtime errors occurred  
- Output covariance matrix remained finite and well-defined  
- NaN/inf values were not present in final output  

Interpretation:  
The model is robust to incomplete financial datasets, which is important for real-world market data.  

---

## 9. Conclusions and Recommendations

**Overall assessment:**
- Suitable for educational and portfolio risk measurement purposes  

**Key limitations:**
- Model risk  
- Normality assumptions  
- Poor tail risk capture  

**Future improvements:**
- GARCH volatility modeling  
- Fat-tail distributions  
- Stress testing framework  

---

## 10. Bibliography

- NumPy Documentation  
- Pandas Documentation  
- Black-Scholes Model (Investopedia)