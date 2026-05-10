"""
Risk System — Main entry point.
Run: python src/main.py
"""
import numpy as np
import sys
sys.path.insert(0, "src")

from pricing.stock_pricer import calibrate_gbm
from pricing.option_pricer import bs_price
from risk.monte_carlo_var import monte_carlo_stock_var, monte_carlo_option_var, monte_carlo_portfolio_var
from risk.expected_shortfall import cvar_from_pnl
from risk.backtesting import kupiec_pof_test, christoffersen_test
from config import DEFAULT_CONFIDENCE, DEFAULT_HORIZON_DAYS, DEFAULT_N_SIM


def main():
    print("=" * 60)
    print("RISK SYSTEM — DEMO")
    print("=" * 60)

    # --- Stock VaR ---
    print("\n[1] Stock Monte Carlo VaR (AAPL proxy)")
    np.random.seed(0)
    sim_prices = 200 * np.exp(np.cumsum(np.random.normal(0.0003, 0.015, 252)))
    cal = calibrate_gbm(sim_prices)
    print(f"  Calibrated: mu={cal['mu']:.4f}, sigma={cal['sigma']:.4f}")

    stock_res = monte_carlo_stock_var(
        mu=cal["mu_daily"], sigma=cal["sigma_daily"],
        current_price=sim_prices[-1], shares=100,
        n_sim=DEFAULT_N_SIM, confidence=DEFAULT_CONFIDENCE,
        horizon=DEFAULT_HORIZON_DAYS
    )
    stock_cvar = cvar_from_pnl(stock_res["pnl"], DEFAULT_CONFIDENCE)
    print(f"  VaR (99%, 10d):  ${stock_res['var']:,.2f}")
    print(f"  CVaR (99%, 10d): ${stock_cvar['cvar']:,.2f}")

    # --- Option VaR ---
    print("\n[2] Option Monte Carlo VaR (SPY ATM Call)")
    opt_res = monte_carlo_option_var(
        S0=530, K=530, T=30/365, r=0.05, sigma=0.18,
        option_price=12.5, option_type="call",
        n_sim=DEFAULT_N_SIM, confidence=DEFAULT_CONFIDENCE,
        horizon_days=DEFAULT_HORIZON_DAYS
    )
    opt_cvar = cvar_from_pnl(opt_res["pnl"], DEFAULT_CONFIDENCE)
    print(f"  VaR (99%, 10d):  ${opt_res['var']:,.2f}")
    print(f"  CVaR (99%, 10d): ${opt_cvar['cvar']:,.2f}")
    print(f"  CVaR/VaR Ratio:  {opt_cvar['cvar_var_ratio']:.3f}")

    # --- Combined Portfolio ---
    print("\n[3] Combined Stock + Option Portfolio")
    stocks = [{"S0": sim_prices[-1], "mu": cal["mu_daily"], "sigma": cal["sigma_daily"], "shares": 100}]
    options = [{"S0": 530, "K": 530, "T": 30/365, "sigma": 0.18, "option_price": 12.5, "option_type": "call", "contracts": 1}]
    port = monte_carlo_portfolio_var(stocks, options, n_sim=DEFAULT_N_SIM, confidence=DEFAULT_CONFIDENCE)
    port_cvar = cvar_from_pnl(port["portfolio_pnl"], DEFAULT_CONFIDENCE)

    print(f"  Portfolio VaR:   ${port['portfolio_var']:,.2f}")
    print(f"  Portfolio CVaR:  ${port_cvar['cvar']:,.2f}")
    print(f"  Stock VaR:       ${port['stock_var']:,.2f}")
    print(f"  Option VaR:      ${port['option_var']:,.2f}")
    print(f"  Div Ratio:       {port['diversification_ratio']:.3f}")

    print("\n" + "=" * 60)
    print("Done. For full analysis with live data, run the notebook.")


if __name__ == "__main__":
    main()
