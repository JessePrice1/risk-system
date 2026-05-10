"""
Parametric (Variance-Covariance) VaR.
"""
import numpy as np
from scipy.stats import norm


def parametric_var(mu, sigma, portfolio_value, confidence=0.99, horizon=1):
    """
    Parametric VaR assuming normal returns.

    Parameters
    ----------
    mu : float — mean return (daily)
    sigma : float — volatility (daily)
    portfolio_value : float
    confidence : float
    horizon : int — days

    Returns
    -------
    dict with var, cvar
    """
    z = norm.ppf(confidence)
    var = portfolio_value * (z * sigma * np.sqrt(horizon) - mu * horizon)

    # Parametric CVaR (normal)
    es_z = norm.pdf(z) / (1 - confidence)
    cvar = portfolio_value * (es_z * sigma * np.sqrt(horizon) - mu * horizon)

    return {
        "var": var,
        "cvar": cvar,
        "z_score": z,
        "confidence": confidence,
        "horizon": horizon,
    }
