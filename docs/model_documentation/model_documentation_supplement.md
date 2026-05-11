# Model Documentation — Supplement
## CVaR, Backtesting & Market Regime Analysis

**Author:** Sangwon Park (swp0569)

---

## 1. Expected Shortfall (CVaR)

### 1.1 Definition
CVaR at confidence level α is defined as:

    CVaR_α = E[Loss | Loss > VaR_α]

It represents the average loss in the tail beyond the VaR threshold.

### 1.2 Motivation
VaR is not a coherent risk measure — it violates subadditivity for portfolios with nonlinear payoffs (options). This means diversifying a portfolio can paradoxically increase VaR. CVaR satisfies all four coherence axioms (monotonicity, subadditivity, positive homogeneity, translation invariance), making it a more reliable risk measure for option portfolios.

### 1.3 Implementation
CVaR is computed from Monte Carlo simulated P&L arrays:
1. Sort losses (negative P&L) in descending order
2. Identify the VaR threshold at the α percentile
3. Average all losses exceeding VaR

The `expected_shortfall.py` module provides:
- `cvar_from_pnl()` — single position CVaR from P&L array
- `portfolio_cvar()` — multi-position CVaR with subadditivity verification

### 1.4 Subadditivity Verification
For each portfolio run, we verify:

    CVaR(Portfolio) ≤ Σ CVaR(Individual positions)

This inequality must always hold for CVaR (coherent) but may be violated for VaR (not coherent).

---

## 2. Backtesting Framework

### 2.1 Kupiec Proportion of Failures (POF) Test
Tests whether the observed VaR violation rate matches the expected rate.

**Hypotheses:**
- H0: p_observed = p_expected = (1 - α)
- H1: p_observed ≠ p_expected

**Test statistic:**

    LR_POF = -2 * [log L(p_expected) - log L(p_observed)]

Distributed as χ²(1) under H0.

**Interpretation:**
- p-value > 0.05 → PASS (model is well-calibrated)
- p-value < 0.05 → FAIL (model underestimates or overestimates risk)

### 2.2 Christoffersen Independence Test
Tests whether VaR violations are independent (not clustered in time).

**Hypotheses:**
- H0: violations are independent (P(violation today | violation yesterday) = P(violation today))
- H1: violations are clustered

**Test statistic:**

    LR_IND = -2 * [log L(restricted) - log L(unrestricted)]

Based on transition counts between violation/no-violation states.

**Interpretation:**
- PASS → violations are randomly distributed (model captures regime changes adequately)
- FAIL → violations cluster (model is slow to adapt to volatility shifts)

### 2.3 Rolling Backtest Procedure
1. At each date t, calibrate GBM parameters using trailing 252-day window
2. Compute 1-day VaR via Monte Carlo simulation (10,000 paths)
3. Compare predicted VaR against actual next-day loss
4. Record violation (1 if actual loss > VaR, 0 otherwise)
5. After full period, run Kupiec and Christoffersen tests on violation sequence

---

## 3. Market Regime Analysis

### 3.1 Regime Definitions
We define five market regimes using the dataset's date range (2020-2025):

| Regime | Period | Characteristics |
|--------|--------|-----------------|
| COVID Crash | Feb 2020 - Jun 2020 | Sharp drawdown, vol spike > 50% |
| Post-COVID Rally | Jul 2020 - Jun 2021 | V-shaped recovery, declining vol |
| Rate Hikes 2022 | Jan 2022 - Dec 2022 | Sustained drawdown, elevated vol ~30% |
| Recovery 2023 | Jan 2023 - Dec 2023 | Gradual recovery, normalizing vol |
| Normal 2024 | Jan 2024 - Dec 2024 | Low vol, steady returns |

### 3.2 Methodology
For each regime:
1. Calibrate GBM parameters (mu, sigma) from regime-specific price data
2. Price an ATM call option using Black-Scholes with calibrated sigma
3. Run Monte Carlo VaR/CVaR (50,000 paths, 99% confidence, 10-day horizon)
4. Compare VaR, CVaR, and CVaR/VaR ratio across regimes

### 3.3 Expected Findings
- VaR and CVaR scale with realized volatility across regimes
- CVaR/VaR ratio increases during stress periods (fatter tails)
- GBM calibration shows excess kurtosis in stress periods, indicating model limitations

---

## 4. Horizon Scaling Analysis

### 4.1 sqrt(t) Rule
Under GBM assumptions, VaR scales as:

    VaR_h = VaR_1 × √h

where h is the horizon in days.

### 4.2 Deviation for Options
For option positions, sqrt(t) scaling underestimates multi-day VaR because:
- **Gamma effect**: option delta changes as underlying moves, creating nonlinear P&L
- **Theta decay**: time value erodes over the horizon
- **Vega risk**: implied vol may change across the horizon

We compare MC-simulated VaR at 1d, 5d, and 10d horizons against sqrt(t)-scaled 1d VaR to quantify this deviation.

---

## 5. Combined Portfolio Analysis

### 5.1 Stock + Option Portfolio
The `monte_carlo_portfolio_var()` function simulates correlated GBM paths for all underlyings simultaneously using Cholesky decomposition of the correlation matrix.

### 5.2 Diversification Ratio
Defined as:

    Div_Ratio = Portfolio_VaR / Σ Individual_VaR

Values < 1 indicate diversification benefit. We compute this for both VaR and CVaR to show that CVaR always captures diversification correctly.

---

## References
- Artzner, P. et al. (1999). Coherent Measures of Risk. Mathematical Finance.
- Kupiec, P. (1995). Techniques for Verifying the Accuracy of Risk Measurement Models. Journal of Derivatives.
- Christoffersen, P. (1998). Evaluating Interval Forecasts. International Economic Review.
- Basel Committee on Banking Supervision (2019). Minimum Capital Requirements for Market Risk.
