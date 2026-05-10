"""
Monte Carlo VaR for stocks and options.

- monte_carlo_stock_var: GBM-based stock VaR
- monte_carlo_option_var: BS-repricing option VaR
- monte_carlo_portfolio_var: combined stock + option portfolio
"""
import numpy as np
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from pricing.option_pricer import bs_price


def monte_carlo_stock_var(
    mu, sigma, current_price, shares,
    n_sim=10000, confidence=0.99, horizon=10, seed=42
):
    """
    Monte Carlo VaR for a single stock position.
    Compatible with Jack's function signature.

    Returns
    -------
    dict with var, pnl, simulated_prices
    """
    np.random.seed(seed)
    simulated_returns = np.random.normal(
        loc=mu * horizon, scale=sigma * np.sqrt(horizon), size=n_sim
    )
    simulated_prices = current_price * (1 + simulated_returns)
    pnl = (simulated_prices - current_price) * shares
    var = -np.percentile(pnl, (1 - confidence) * 100)

    return {"var": var, "pnl": pnl, "simulated_prices": simulated_prices}


def monte_carlo_option_var(
    S0, K, T, r, sigma, option_price, option_type="call",
    contracts=1, n_sim=50000, confidence=0.99, horizon_days=10, seed=42
):
    """
    Monte Carlo VaR for a single option position.
    Simulates GBM paths then reprices with Black-Scholes.

    Returns
    -------
    dict with var, pnl, simulated_stock_prices, future_option_values
    """
    np.random.seed(seed)
    dt = 1 / 252
    n_steps = horizon_days

    Z = np.random.standard_normal((n_sim, n_steps))
    log_ret = (r - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z
    S_T = S0 * np.exp(np.cumsum(log_ret, axis=1))[:, -1]

    T_rem = max(T - horizon_days / 252, 0)
    future_option_values = np.array([
        bs_price(s, K, T_rem, r, sigma, option_type) for s in S_T
    ])

    position_now = option_price * 100 * contracts
    position_future = future_option_values * 100 * contracts
    pnl = position_future - position_now

    var = -np.percentile(pnl, (1 - confidence) * 100)

    return {
        "var": var,
        "pnl": pnl,
        "simulated_stock_prices": S_T,
        "future_option_values": future_option_values,
    }


def monte_carlo_portfolio_var(
    stock_positions, option_positions, r=0.05,
    n_sim=50000, confidence=0.99, horizon_days=10,
    seed=42, corr_matrix=None
):
    """
    Combined stock + option portfolio Monte Carlo VaR.

    Parameters
    ----------
    stock_positions : list of dict
        Each: {S0, mu, sigma, shares}
    option_positions : list of dict
        Each: {S0, K, T, sigma, option_price, option_type, contracts}
    corr_matrix : np.array or None
        Correlation for all underlyings (stocks first, then options).

    Returns
    -------
    dict with portfolio_var, stock_var, option_var, pnl arrays
    """
    n_stocks = len(stock_positions)
    n_options = len(option_positions)
    n_total = n_stocks + n_options
    np.random.seed(seed)

    if corr_matrix is not None:
        L = np.linalg.cholesky(corr_matrix)
    else:
        L = np.eye(n_total)

    dt = 1 / 252
    Z_indep = np.random.standard_normal((n_sim, horizon_days, n_total))
    Z_corr = np.einsum("ijk,lk->ijl", Z_indep, L)

    portfolio_pnl = np.zeros(n_sim)
    stock_pnl = np.zeros(n_sim)
    option_pnl = np.zeros(n_sim)

    # Stocks
    for i, pos in enumerate(stock_positions):
        S0 = pos["S0"]
        mu = pos["mu"]
        sig = pos["sigma"]
        shares = pos.get("shares", 100)

        log_ret = (mu - 0.5 * sig**2) * dt + sig * np.sqrt(dt) * Z_corr[:, :, i]
        S_T = S0 * np.exp(np.sum(log_ret, axis=1))
        pnl_i = (S_T - S0) * shares
        stock_pnl += pnl_i
        portfolio_pnl += pnl_i

    # Options
    for j, pos in enumerate(option_positions):
        idx = n_stocks + j
        S0 = pos["S0"]
        K = pos["K"]
        T = pos["T"]
        sig = pos["sigma"]
        opt_price = pos["option_price"]
        opt_type = pos.get("option_type", "call")
        contracts = pos.get("contracts", 1)

        log_ret = (r - 0.5 * sig**2) * dt + sig * np.sqrt(dt) * Z_corr[:, :, idx]
        S_T = S0 * np.exp(np.sum(log_ret, axis=1))
        T_rem = max(T - horizon_days / 252, 0)
        fut_vals = np.array([bs_price(s, K, T_rem, r, sig, opt_type) for s in S_T])
        pnl_j = (fut_vals - opt_price) * 100 * contracts
        option_pnl += pnl_j
        portfolio_pnl += pnl_j

    port_var = -np.percentile(portfolio_pnl, (1 - confidence) * 100)
    s_var = -np.percentile(stock_pnl, (1 - confidence) * 100) if n_stocks > 0 else 0
    o_var = -np.percentile(option_pnl, (1 - confidence) * 100) if n_options > 0 else 0

    return {
        "portfolio_var": port_var,
        "stock_var": s_var,
        "option_var": o_var,
        "sum_individual_var": s_var + o_var,
        "diversification_ratio": port_var / (s_var + o_var) if (s_var + o_var) > 0 else 1.0,
        "portfolio_pnl": portfolio_pnl,
        "stock_pnl": stock_pnl,
        "option_pnl": option_pnl,
    }
