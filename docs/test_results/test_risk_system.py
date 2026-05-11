import numpy as np

from src.risk.historical_var import historical_var
from src.risk.parametric_var import parametric_var
from src.risk.expected_shortfall import cvar_from_pnl
from src.risk.monte_carlo_var import monte_carlo_stock_var, monte_carlo_portfolio_var


from src.risk.backtesting import kupiec_pof_test, christoffersen_test, backtest_var


# =========================================================
# TEST 1 — Historical VaR Consistency
# =========================================================
def test_historical_var():
    returns = np.random.normal(0.001, 0.02, 1000)

    result = historical_var(returns, confidence=0.99)

    var = result["var"]
    cvar = result["cvar"]

    assert var > 0, "VaR should be positive (loss measure)"
    assert cvar >= var, "CVaR should be at least as large as VaR"
    assert np.isfinite(var), "VaR must be finite"
    assert np.isfinite(cvar), "CVaR must be finite"

    print("✔ Test 1 Passed — Historical VaR consistency")


# =========================================================
# TEST 2 — Parametric VaR Sensitivity to Volatility
# =========================================================
def test_parametric_var_sensitivity():
    low_risk = parametric_var(mu=0.0005, sigma=0.01, portfolio_value=10000)
    high_risk = parametric_var(mu=0.0005, sigma=0.05, portfolio_value=10000)

    assert high_risk["var"] > low_risk["var"], "Higher volatility must increase VaR"
    assert np.isfinite(high_risk["var"])
    assert np.isfinite(low_risk["var"])

    print("✔ Test 2 Passed — Parametric VaR volatility sensitivity")


# =========================================================
# TEST 3 — Monte Carlo Portfolio Coherence
# =========================================================
def test_monte_carlo_portfolio():

    stock_positions = [
        {"S0": 100, "mu": 0.01, "sigma": 0.2, "shares": 100}
    ]

    option_positions = [
        {
            "S0": 100,
            "K": 100,
            "T": 1,
            "sigma": 0.2,
            "option_price": 10,
            "option_type": "call",
            "contracts": 5
        }
    ]

    result = monte_carlo_portfolio_var(
        stock_positions,
        option_positions,
        n_sim=5000,
        horizon_days=5
    )

    portfolio_var = result["portfolio_var"]
    stock_var = result["stock_var"]
    option_var = result["option_var"]

    assert np.isfinite(portfolio_var)
    assert portfolio_var >= 0

    # diversification check (portfolio should not explode beyond sum excessively)
    assert portfolio_var <= stock_var + option_var * 1.5

    print("✔ Test 3 Passed — Monte Carlo portfolio coherence")


# =========================================================
# TEST 4 — Backtesting (Kupiec POF + Christoffersen)
# =========================================================
def test_backtesting():
    np.random.seed(42)
    n = 1000
    returns = np.random.normal(0.001, 0.02, n)
    # Simulate a VaR series that should have ~1% violation rate at 99%
    var_series = np.full(n, np.percentile(-returns, 99))

    # Kupiec test
    violations = int(np.sum(-returns > var_series))
    kupiec = kupiec_pof_test(violations, n, confidence=0.99)
    assert kupiec["p_value"] >= 0, "p-value must be non-negative"
    assert kupiec["p_value"] <= 1, "p-value must be at most 1"
    assert np.isfinite(kupiec["LR_statistic"]), "LR statistic must be finite"
    assert kupiec["conclusion"] in ["PASS", "FAIL"], "Must have valid conclusion"

    # Christoffersen test
    violation_seq = (-returns > var_series).astype(int).tolist()
    christ = christoffersen_test(violation_seq, confidence=0.99)
    assert christ["p_value"] >= 0, "p-value must be non-negative"
    assert np.isfinite(christ["LR_statistic"]), "LR statistic must be finite"

    # backtest_var wrapper
    bt = backtest_var(returns, var_series, confidence=0.99)
    assert bt["violation_rate"] >= 0, "Violation rate must be non-negative"
    assert bt["violation_rate"] <= 1, "Violation rate must be at most 1"
    assert bt["n_obs"] == n, "Observation count must match"

    print("✔ Test 4 Passed — Backtesting (Kupiec + Christoffersen)")


# =========================================================
# RUN ALL TESTS
# =========================================================
if __name__ == "__main__":
    test_historical_var()
    test_parametric_var_sensitivity()
    test_monte_carlo_portfolio()
    test_backtesting()

    print("\n✔ All Group D Risk Model tests passed.")