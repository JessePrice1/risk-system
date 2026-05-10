"""
Implied volatility solver via Newton-Raphson.
"""
import numpy as np
from scipy.stats import norm
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pricing.option_pricer import bs_price


def implied_vol(market_price, S, K, T, r, option_type="call",
                tol=1e-6, max_iter=100):
    """
    Solve for implied volatility using Newton-Raphson.

    Parameters
    ----------
    market_price : float — observed option price
    S, K, T, r : BS parameters
    option_type : str

    Returns
    -------
    float — implied volatility, or NaN if no convergence
    """
    sigma = 0.3  # initial guess

    for _ in range(max_iter):
        price = bs_price(S, K, T, r, sigma, option_type)
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        vega = S * norm.pdf(d1) * np.sqrt(T)

        if abs(vega) < 1e-12:
            return np.nan

        sigma -= (price - market_price) / vega

        if sigma <= 0:
            sigma = 0.001

        if abs(price - market_price) < tol:
            return sigma

    return np.nan
