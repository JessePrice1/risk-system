"""
Historical VaR — non-parametric VaR from historical returns.
"""
import numpy as np


def historical_var(returns, confidence=0.99):
    """
    Historical simulation VaR.

    Parameters
    ----------
    returns : array-like — historical P&L or returns
    confidence : float

    Returns
    -------
    dict with var, cvar
    """
    losses = -np.array(returns)
    var = np.percentile(losses, confidence * 100)
    tail = losses[losses >= var]
    cvar = np.mean(tail) if len(tail) > 0 else var

    return {
        "var": var,
        "cvar": cvar,
        "n_obs": len(returns),
        "confidence": confidence,
    }
