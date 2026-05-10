"""
VaR Backtesting — Kupiec POF & Christoffersen Independence Tests.
"""
import numpy as np
from scipy.stats import chi2


def kupiec_pof_test(violations, n_obs, confidence=0.99, sig_level=0.05):
    """
    Kupiec Proportion of Failures (POF) test.
    H0: observed violation rate = expected violation rate.

    Returns
    -------
    dict with LR statistic, p-value, conclusion
    """
    p_expected = 1 - confidence
    p_observed = violations / n_obs if n_obs > 0 else 0

    if violations == 0 or violations == n_obs:
        lr = -2 * n_obs * np.log(1 - p_expected) if violations == 0 else np.inf
    else:
        lr = -2 * (
            np.log((1 - p_expected)**(n_obs - violations) * p_expected**violations)
            - np.log((1 - p_observed)**(n_obs - violations) * p_observed**violations)
        )

    p_value = 1 - chi2.cdf(lr, df=1)

    return {
        "test": "Kupiec POF",
        "violations": violations,
        "n_obs": n_obs,
        "expected_rate": p_expected,
        "observed_rate": p_observed,
        "LR_statistic": lr,
        "p_value": p_value,
        "reject_H0": p_value < sig_level,
        "conclusion": "FAIL" if p_value < sig_level else "PASS",
    }


def christoffersen_test(violation_sequence, confidence=0.99, sig_level=0.05):
    """
    Christoffersen conditional coverage test.
    Tests independence of violations.

    Returns
    -------
    dict with LR statistic, p-value, conclusion
    """
    v = np.array(violation_sequence, dtype=int)

    n00 = n01 = n10 = n11 = 0
    for i in range(1, len(v)):
        if v[i-1] == 0 and v[i] == 0: n00 += 1
        elif v[i-1] == 0 and v[i] == 1: n01 += 1
        elif v[i-1] == 1 and v[i] == 0: n10 += 1
        elif v[i-1] == 1 and v[i] == 1: n11 += 1

    p01 = n01 / (n00 + n01) if (n00 + n01) > 0 else 0
    p11 = n11 / (n10 + n11) if (n10 + n11) > 0 else 0
    p = (n01 + n11) / (n00 + n01 + n10 + n11) if len(v) > 1 else 0

    eps = 1e-10
    if p01 < eps or p11 < eps or p < eps or (1-p01) < eps or (1-p11) < eps or (1-p) < eps:
        lr_ind = 0
    else:
        log_u = n00*np.log(1-p01) + n01*np.log(p01) + n10*np.log(1-p11) + n11*np.log(p11)
        log_r = (n00+n10)*np.log(1-p) + (n01+n11)*np.log(p)
        lr_ind = -2 * (log_r - log_u)

    p_value = 1 - chi2.cdf(lr_ind, df=1)

    return {
        "test": "Christoffersen Independence",
        "transitions": {"n00": n00, "n01": n01, "n10": n10, "n11": n11},
        "LR_statistic": lr_ind,
        "p_value": p_value,
        "reject_H0": p_value < sig_level,
        "conclusion": "FAIL — violations clustered" if p_value < sig_level else "PASS",
    }


def backtest_var(returns, var_series, confidence=0.99, sig_level=0.05):
    """
    Full backtesting suite on a VaR time series.

    Parameters
    ----------
    returns : array-like — actual P&L
    var_series : array-like — VaR estimates (positive = loss threshold)

    Returns
    -------
    dict with Kupiec, Christoffersen, violation details
    """
    returns = np.array(returns)
    var_series = np.array(var_series)

    violations = (-returns > var_series).astype(int)
    n_violations = violations.sum()
    n_obs = len(returns)

    return {
        "kupiec": kupiec_pof_test(n_violations, n_obs, confidence, sig_level),
        "christoffersen": christoffersen_test(violations, confidence, sig_level),
        "n_violations": int(n_violations),
        "n_obs": n_obs,
        "violation_rate": n_violations / n_obs if n_obs > 0 else 0,
        "expected_rate": 1 - confidence,
    }
