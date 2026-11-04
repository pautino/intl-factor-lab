"""Charts. Every function returns a matplotlib Figure so callers can show or save it."""
from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams.update({"figure.dpi": 110, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.3, "font.size": 9})
COLORS = plt.get_cmap("tab10").colors


def exposure_bars(tables: dict[str, pd.DataFrame], title: str = "Factor exposures (95% CI)"):
    """Grouped bars: one group per factor, one bar per ETF, HAC 95% confidence intervals."""
    factors = [f for f in next(iter(tables.values())).index if f != "const"]
    width = 0.8 / len(tables)
    fig, ax = plt.subplots(figsize=(10, 4))
    x = np.arange(len(factors))
    for i, (name, t) in enumerate(tables.items()):
        t = t.loc[factors]
        err = [t["coef"] - t["ci_low"], t["ci_high"] - t["coef"]]
        ax.bar(x + i * width, t["coef"], width, yerr=err, capsize=2, label=name, color=COLORS[i])
    ax.axhline(0, color="black", lw=0.8)
    ax.set_xticks(x + width * (len(tables) - 1) / 2, factors)
    ax.set_ylabel("Beta")
    ax.set_title(title)
    ax.legend(ncol=len(tables), fontsize=8)
    fig.tight_layout()
    return fig


def rolling_beta_grid(betas: dict[str, pd.DataFrame], factors: list[str], window: int):
    """One panel per factor, one line per ETF."""
    fig, axes = plt.subplots(len(factors), 1, figsize=(10, 2.2 * len(factors)), sharex=True)
    axes = np.atleast_1d(axes)
    for ax, f in zip(axes, factors):
        for i, (name, b) in enumerate(betas.items()):
            ax.plot(b.index.to_timestamp(), b[f], label=name, color=COLORS[i], lw=1.2)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_ylabel(f)
    axes[0].set_title(f"Rolling {window}-month betas")
    axes[0].legend(ncol=len(betas), fontsize=8)
    fig.tight_layout()
    return fig


def fitted_vs_realized(fits: dict[str, tuple], title: str = "Fitted vs realized excess returns"):
    """fits: name -> (result, df). Scatter with 45-degree line, one panel per ETF."""
    n = len(fits)
    cols = min(3, n)
    rows = int(np.ceil(n / cols))
    fig, axes = plt.subplots(rows, cols, figsize=(3.6 * cols, 3.3 * rows), squeeze=False)
    for ax, (name, (res, df)) in zip(axes.flat, fits.items()):
        ax.scatter(res.fittedvalues, df["y"], s=8, alpha=0.6)
        lim = np.abs(df["y"]).max() * 1.05
        ax.plot([-lim, lim], [-lim, lim], color="black", lw=0.8)
        ax.set_title(f"{name}  (R² {res.rsquared:.2f})")
        ax.set_xlabel("Fitted")
        ax.set_ylabel("Realized")
    for ax in list(axes.flat)[n:]:
        ax.set_visible(False)
    fig.suptitle(title)
    fig.tight_layout()
    return fig


def cumulative_residuals(fits: dict[str, tuple], title: str = "Cumulative alpha + residual"):
    """Cumulative unexplained return (alpha + residual): drift = persistent mispricing
    relative to the model, breaks = changing exposures."""
    fig, ax = plt.subplots(figsize=(10, 4))
    for i, (name, (res, df)) in enumerate(fits.items()):
        unexplained = res.params["const"] + res.resid
        ax.plot(df.index.to_timestamp(), unexplained.cumsum(), label=name, color=COLORS[i])
    ax.axhline(0, color="black", lw=0.8)
    ax.set_ylabel("Cumulative sum (decimal)")
    ax.set_title(title)
    ax.legend(ncol=len(fits), fontsize=8)
    fig.tight_layout()
    return fig


def attribution_bars(attr: pd.DataFrame, title: str = "Return attribution (annualized)"):
    """attr: rows = ETFs, columns = components. Stacked bars + dot for the total."""
    fig, ax = plt.subplots(figsize=(10, 4))
    pos = np.zeros(len(attr))
    neg = np.zeros(len(attr))
    for i, c in enumerate(attr.columns):
        v = attr[c].to_numpy()
        base = np.where(v >= 0, pos, neg)
        ax.bar(attr.index, v, bottom=base, label=c, color=COLORS[i % 10])
        pos += np.where(v >= 0, v, 0)
        neg += np.where(v < 0, v, 0)
    ax.scatter(attr.index, attr.sum(axis=1), color="black", zorder=3, label="Total excess return")
    ax.axhline(0, color="black", lw=0.8)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.1%}"))
    ax.set_title(title)
    ax.legend(ncol=5, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.08))
    fig.tight_layout()
    return fig


def correlation_heatmap(df: pd.DataFrame, title: str = "Factor correlations"):
    """Multicollinearity check: high |corr| between factors inflates beta standard errors."""
    c = df.corr()
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    im = ax.imshow(c, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(c)), c.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(c)), c.columns)
    for i in range(len(c)):
        for j in range(len(c)):
            ax.text(j, i, f"{c.iat[i, j]:.2f}", ha="center", va="center", fontsize=7)
    fig.colorbar(im, ax=ax, shrink=0.8)
    ax.set_title(title)
    ax.grid(False)
    fig.tight_layout()
    return fig


def global_vs_local_bars(table: pd.DataFrame, title: str = "Adjusted R²: global vs local factors"):
    """table: rows = ETFs, columns = ['global', 'local'] adjusted R^2."""
    fig, ax = plt.subplots(figsize=(8, 3.5))
    x = np.arange(len(table))
    ax.bar(x - 0.2, table["global"], 0.4, label="Global (Developed) factors", color=COLORS[0])
    ax.bar(x + 0.2, table["local"], 0.4, label="Local (regional) factors", color=COLORS[1])
    ax.set_xticks(x, table.index)
    ax.set_ylim(0, 1.15)
    ax.set_title(title)
    ax.legend(fontsize=8, ncol=2, loc="upper center")
    fig.tight_layout()
    return fig
