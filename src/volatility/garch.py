"""
GARCH(1,1) volatility estimation.
"""
import numpy as np
import pandas as pd


def garch_11_volatility(returns, omega=1e-6, alpha=0.1, beta=0.85):
    """
    GARCH(1,1): sigma_t^2 = omega + alpha * r_{t-1}^2 + beta * sigma_{t-1}^2

    Parameters
    ----------
    returns : array-like — log returns
    omega, alpha, beta : GARCH parameters

    Returns
    -------
    pd.Series of GARCH volatility estimates (annualized)
    """
    returns = np.array(returns)
    n = len(returns)
    var = np.zeros(n)
    var[0] = np.var(returns[:min(20, n)])

    for i in range(1, n):
        var[i] = omega + alpha * returns[i-1]**2 + beta * var[i-1]

    return pd.Series(np.sqrt(var * 252), name="GARCH_Vol")
