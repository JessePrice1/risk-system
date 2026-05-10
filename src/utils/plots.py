"""
Visualization utilities for risk analysis.
"""
import numpy as np
import matplotlib.pyplot as plt


def plot_loss_distribution(pnl, var, cvar, confidence=0.99, title="Loss Distribution"):
    """Plot loss distribution with VaR and CVaR."""
    fig, ax = plt.subplots(figsize=(10, 6))
    losses = -np.array(pnl)

    ax.hist(losses, bins=100, density=True, alpha=0.7, color="#2C3E50", edgecolor="none")
    ax.axvline(var, color="#E74C3C", linestyle="--", lw=2,
               label=f"VaR ({confidence:.0%}) = ${var:,.0f}")
    ax.axvline(cvar, color="#E67E22", linestyle="-.", lw=2,
               label=f"CVaR ({confidence:.0%}) = ${cvar:,.0f}")

    tail = losses[losses >= var]
    if len(tail) > 0:
        ax.hist(tail, bins=50, density=True, alpha=0.5, color="#E74C3C", edgecolor="none")

    ax.set_xlabel("Loss ($)")
    ax.set_ylabel("Density")
    ax.set_title(title, fontweight="bold")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig


def plot_regime_comparison(regime_results, confidence=0.99):
    """Bar chart comparing VaR/CVaR across regimes."""
    fig, ax = plt.subplots(figsize=(12, 6))

    regimes = [r["regime"] for r in regime_results]
    vars_ = [r["var"] for r in regime_results]
    cvars = [r["cvar"] for r in regime_results]

    x = np.arange(len(regimes))
    width = 0.35

    ax.bar(x - width/2, vars_, width, label="VaR", color="#2C3E50")
    ax.bar(x + width/2, cvars, width, label="CVaR", color="#E74C3C")
    ax.set_xticks(x)
    ax.set_xticklabels(regimes, rotation=45, ha="right")
    ax.set_ylabel("Loss ($)")
    ax.set_title(f"VaR vs CVaR by Market Regime ({confidence:.0%})", fontweight="bold")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    return fig


def plot_backtest(dates, actual_losses, var_series, cvar_series=None,
                  violations=None, title="VaR Backtest"):
    """Plot backtest timeline."""
    fig, ax = plt.subplots(figsize=(14, 6))

    ax.plot(dates, actual_losses, color="#2C3E50", alpha=0.6, lw=0.8, label="Actual Loss")
    ax.plot(dates, var_series, color="#E74C3C", lw=1.5, label="VaR")
    if cvar_series is not None:
        ax.plot(dates, cvar_series, color="#E67E22", lw=1.5, ls="--", label="CVaR")
    if violations is not None:
        v_idx = np.array(violations, dtype=bool)
        ax.scatter(np.array(dates)[v_idx], np.array(actual_losses)[v_idx],
                   color="#E74C3C", s=30, zorder=5, label="Violations")

    ax.set_ylabel("Loss ($)")
    ax.set_title(title, fontweight="bold")
    ax.legend()
    ax.grid(alpha=0.3)
    plt.tight_layout()
    return fig
