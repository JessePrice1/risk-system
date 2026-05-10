"""
Statistical utilities.
"""
import numpy as np
import pandas as pd


def return_statistics(returns):
    """Compute summary statistics for a return series."""
    r = np.array(returns)
    return {
        "mean": np.mean(r),
        "std": np.std(r, ddof=1),
        "skewness": float(pd.Series(r).skew()),
        "kurtosis": float(pd.Series(r).kurtosis()),
        "min": np.min(r),
        "max": np.max(r),
        "sharpe": np.mean(r) / np.std(r, ddof=1) * np.sqrt(252) if np.std(r) > 0 else 0,
        "n": len(r),
    }


def jarque_bera_test(returns, sig_level=0.05):
    """Jarque-Bera normality test."""
    from scipy.stats import jarque_bera
    stat, p_value = jarque_bera(returns)
    return {
        "statistic": stat,
        "p_value": p_value,
        "reject_normal": p_value < sig_level,
    }
