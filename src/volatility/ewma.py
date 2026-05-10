"""
EWMA (Exponentially Weighted Moving Average) volatility.
"""
import numpy as np
import pandas as pd


def ewma_volatility(returns, lam=0.94):
    """
    EWMA volatility estimation (RiskMetrics standard lambda=0.94).

    Parameters
    ----------
    returns : array-like — log returns
    lam : float — decay factor

    Returns
    -------
    pd.Series of EWMA volatility estimates
    """
    returns = np.array(returns)
    n = len(returns)
    var = np.zeros(n)
    var[0] = returns[0]**2

    for i in range(1, n):
        var[i] = lam * var[i-1] + (1 - lam) * returns[i]**2

    return pd.Series(np.sqrt(var * 252), name="EWMA_Vol")
