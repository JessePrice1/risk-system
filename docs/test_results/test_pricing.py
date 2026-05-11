import numpy as np
from src.pricing.option_pricer import bs_price
from src.pricing.stock_pricer import calibrate_gbm


# ---------------------------------------------------
# Test 1 — Black-Scholes validity test
# ---------------------------------------------------

def test_bs_price_validity():
    call = bs_price(100, 100, 1, 0.05, 0.2, "call")
    put = bs_price(100, 100, 1, 0.05, 0.2, "put")

    assert call > 0
    assert put > 0
    assert np.isfinite(call)
    assert np.isfinite(put)

    print("Test 1 Passed — Black-Scholes validity")


# ---------------------------------------------------
# Test 2 — GBM calibration stability test
# ---------------------------------------------------

def test_gbm_calibration():
    prices = 100 * np.exp(np.cumsum(np.random.normal(0.001, 0.02, 252)))

    result = calibrate_gbm(prices)

    assert result["sigma"] > 0
    assert np.isfinite(result["mu"])
    assert np.isfinite(result["sigma"])

    print("Test 2 Passed — GBM calibration valid")


# ---------------------------------------------------
# Test 3 — Volatility sensitivity test
# ---------------------------------------------------

def test_volatility_sensitivity():
    low_vol = bs_price(100, 100, 1, 0.05, 0.1, "call")
    high_vol = bs_price(100, 100, 1, 0.05, 0.5, "call")

    assert high_vol > low_vol

    print("Test 3 Passed — Volatility sensitivity correct")


# ---------------------------------------------------
# Run all tests
# ---------------------------------------------------

if __name__ == "__main__":
    test_bs_price_validity()
    test_gbm_calibration()
    test_volatility_sensitivity()

    print("\nAll Group C Pricing tests passed.")