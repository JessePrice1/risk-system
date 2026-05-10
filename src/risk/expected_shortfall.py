"""
Expected Shortfall (CVaR) — Conditional Value at Risk.

CVaR = E[Loss | Loss > VaR]

Coherent risk measure that addresses VaR's subadditivity problem
for nonlinear payoffs (options). Recommended by TA for this project.
"""
import numpy as np


def cvar_from_pnl(pnl, confidence=0.99):
    """
    Compute CVaR from a P&L array.

    Parameters
    ----------
    pnl : array-like — simulated P&L values
    confidence : float — confidence level (e.g. 0.95, 0.99)

    Returns
    -------
    dict with var, cvar, ratio
    """
    losses = -np.array(pnl)
    var = np.percentile(losses, confidence * 100)
    tail_losses = losses[losses >= var]
    cvar = np.mean(tail_losses) if len(tail_losses) > 0 else var

    return {
        "var": var,
        "cvar": cvar,
        "cvar_var_ratio": cvar / var if var > 0 else float("nan"),
        "n_tail": len(tail_losses),
        "confidence": confidence,
    }


def portfolio_cvar(pnl_dict, confidence=0.99):
    """
    Compute CVaR for multiple P&L components and the portfolio.

    Parameters
    ----------
    pnl_dict : dict — {name: pnl_array}
    confidence : float

    Returns
    -------
    dict with individual and portfolio CVaR results
    """
    results = {}
    total_pnl = np.zeros_like(list(pnl_dict.values())[0])

    for name, pnl in pnl_dict.items():
        results[name] = cvar_from_pnl(pnl, confidence)
        total_pnl += np.array(pnl)

    results["portfolio"] = cvar_from_pnl(total_pnl, confidence)

    # Subadditivity check
    sum_individual_cvar = sum(
        r["cvar"] for name, r in results.items() if name != "portfolio"
    )
    results["subadditivity_holds"] = results["portfolio"]["cvar"] <= sum_individual_cvar
    results["sum_individual_cvar"] = sum_individual_cvar

    return results
