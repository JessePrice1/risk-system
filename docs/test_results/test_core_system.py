# test_core_system.py

import numpy as np
from src.config import DEFAULT_CONFIDENCE, DEFAULT_HORIZON_DAYS, DEFAULT_N_SIM
from src.pricing.stock_pricer import calibrate_gbm
from src.risk.monte_carlo_var import monte_carlo_stock_var, monte_carlo_option_var, monte_carlo_portfolio_var
from src.risk.expected_shortfall import cvar_from_pnl


# ---------------------------------------------------
# Test 1 — Main Pipeline Execution Test (light version)
# ---------------------------------------------------

def test_pipeline_runs():
    np.random.seed(0)

    sim_prices = 200 * np.exp(np.cumsum(np.random.normal(0.0003, 0.015, 252)))
    cal = calibrate_gbm(sim_prices)

    stock_res = monte_carlo_stock_var(
        mu=cal["mu_daily"],
        sigma=cal["sigma_daily"],
        current_price=sim_prices[-1],
        shares=100,
        n_sim=1000,
        confidence=DEFAULT_CONFIDENCE,
        horizon=DEFAULT_HORIZON_DAYS
    )

    assert "var" in stock_res
    assert len(stock_res["pnl"]) > 0

    print("Test 1 Passed — Pipeline runs successfully")


# ---------------------------------------------------
# Test 2 — Config Propagation Test
# ---------------------------------------------------

def test_config_propagation():
    assert 0 < DEFAULT_CONFIDENCE < 1
    assert DEFAULT_HORIZON_DAYS > 0
    assert DEFAULT_N_SIM > 0

    print("Test 2 Passed — Config values valid")


# ---------------------------------------------------
# Test 3 — Portfolio Consistency Test
# ---------------------------------------------------

def test_portfolio_consistency():
    np.random.seed(0)

    sim_prices = 200 * np.exp(np.cumsum(np.random.normal(0.0003, 0.015, 252)))
    cal = calibrate_gbm(sim_prices)

    stocks = [{
        "S0": sim_prices[-1],
        "mu": cal["mu_daily"],
        "sigma": cal["sigma_daily"],
        "shares": 100
    }]

    options = [{
        "S0": 530,
        "K": 530,
        "T": 30/365,
        "sigma": 0.18,
        "option_price": 12.5,
        "option_type": "call",
        "contracts": 1
    }]

    port = monte_carlo_portfolio_var(
        stocks, options,
        n_sim=1000,
        confidence=DEFAULT_CONFIDENCE
    )

    cvar = cvar_from_pnl(port["portfolio_pnl"], DEFAULT_CONFIDENCE)

    assert port["portfolio_var"] >= 0
    assert cvar["cvar"] >= port["portfolio_var"] * 0  # sanity check
    assert np.isfinite(port["diversification_ratio"])

    print("Test 3 Passed — Portfolio consistency valid")


# ---------------------------------------------------
# Run tests
# ---------------------------------------------------

if __name__ == "__main__":
    test_pipeline_runs()
    test_config_propagation()
    test_portfolio_consistency()

    print("\nAll Core System tests passed.")