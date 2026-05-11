import numpy as np
import pandas as pd

from src.volatility.ewma import ewma_volatility
from src.volatility.garch import garch_11_volatility
from src.volatility.implied_vol import implied_vol
from src.utils.statistics import return_statistics
from src.utils.covariance import covariance_matrix
from src.pricing.option_pricer import bs_price


# ---------------------------------------------------
# TEST 1 — EWMA + GARCH stability
# ---------------------------------------------------

def test_volatility_models():
    np.random.seed(42)
    returns = np.random.normal(0, 0.01, 500)

    ewma = ewma_volatility(returns)
    garch = garch_11_volatility(returns)

    assert np.all(np.isfinite(ewma))
    assert np.all(np.isfinite(garch))
    assert np.all(ewma > 0)
    assert np.all(garch > 0)

    print("Test 1 Passed — Volatility models stable")


# ---------------------------------------------------
# TEST 2 — Implied volatility recovery
# ---------------------------------------------------

def test_implied_vol():
    S, K, T, r = 100, 100, 1, 0.05
    true_sigma = 0.2

    market_price = bs_price(S, K, T, r, true_sigma, "call")

    est_sigma = implied_vol(market_price, S, K, T, r, "call")

    assert np.isfinite(est_sigma)
    assert abs(est_sigma - true_sigma) < 0.05

    print("Test 2 Passed — Implied volatility accurate")


# ---------------------------------------------------
# TEST 3 — Statistics + covariance consistency
# ---------------------------------------------------

def test_stats_and_covariance():
    np.random.seed(42)

    r1 = np.random.normal(0, 0.01, 300)
    r2 = 0.5 * r1 + np.random.normal(0, 0.01, 300)

    df = pd.DataFrame({"asset1": r1, "asset2": r2})

    stats = return_statistics(r1)
    cov = covariance_matrix(df)

    assert np.isfinite(stats["mean"])
    assert np.isfinite(stats["std"])

    assert cov.shape == (2, 2)
    assert np.allclose(cov, cov.T)  # symmetry
    assert cov[0, 0] > 0 and cov[1, 1] > 0

    print("Test 3 Passed — Stats and covariance valid")


# ---------------------------------------------------
# RUN ALL TESTS
# ---------------------------------------------------

if __name__ == "__main__":
    test_volatility_models()
    test_implied_vol()
    test_stats_and_covariance()

    print("\nAll Group F tests passed.")