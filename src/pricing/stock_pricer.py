"""
Stock GBM calibration and pricing utilities.
"""
import numpy as np
import pandas as pd


def calibrate_gbm(prices, method="mle"):
    """
    Calibrate GBM parameters (mu, sigma) from historical prices.

    Parameters
    ----------
    prices : array-like — historical closing prices (oldest first)
    method : str — 'mle' or 'moment'

    Returns
    -------
    dict with annualized mu, sigma, and diagnostics
    """
    prices = np.array(prices, dtype=float)
    log_returns = np.diff(np.log(prices))

    if method == "mle":
        sigma_daily = np.std(log_returns, ddof=1)
    else:
        sigma_daily = np.std(log_returns, ddof=0)

    mu_daily = np.mean(log_returns) + 0.5 * sigma_daily**2

    return {
        "mu": mu_daily * 252,
        "sigma": sigma_daily * np.sqrt(252),
        "mu_daily": mu_daily,
        "sigma_daily": sigma_daily,
        "n_obs": len(log_returns),
        "log_returns": log_returns,
        "skewness": float(pd.Series(log_returns).skew()),
        "kurtosis": float(pd.Series(log_returns).kurtosis()),
        "method": method,
    }


def calibrate_from_ticker(ticker, start, end, method="mle"):
    """Fetch price data via yfinance and calibrate GBM."""
    import yfinance as yf

    df = yf.download(ticker, start=start, end=end, progress=False)
    if len(df) < 30:
        raise ValueError(f"Insufficient data for {ticker}: {len(df)} rows")

    prices = df["Close"].values.flatten()
    cal = calibrate_gbm(prices, method=method)
    cal["ticker"] = ticker
    cal["start"] = start
    cal["end"] = end
    cal["prices_df"] = df
    return cal
