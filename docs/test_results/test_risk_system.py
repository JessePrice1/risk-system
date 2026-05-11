import numpy as np

from src.risk.historical_var import historical_var
from src.risk.parametric_var import parametric_var
from src.risk.expected_shortfall import cvar_from_pnl
from src.risk.monte_carlo_var import monte_carlo_stock_var, monte_carlo_portfolio_var


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
# RUN ALL TESTS
# =========================================================
if __name__ == "__main__":
    test_historical_var()
    test_parametric_var_sensitivity()
    test_monte_carlo_portfolio()

    print("\n✔ All Group D Risk Model tests passed.")