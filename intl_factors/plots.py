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


def hedged_comparison(common: pd.DataFrame, gap_fit):
    """Common-sample wealth and the HEFA-EFA gap versus the raw broad-dollar change."""
    fig, (wealth_ax, gap_ax) = plt.subplots(1, 2, figsize=(11, 4))
    wealth = (1 + common[["EFA", "HEFA"]]).cumprod()
    for i, ticker in enumerate(wealth):
        wealth_ax.plot(wealth.index.to_timestamp(), wealth[ticker], label=ticker, color=COLORS[i])
    wealth_ax.set_title("Growth of $1, monthly total returns")
    wealth_ax.set_ylabel("Wealth ($)")
    wealth_ax.legend()
    raw_usd = common["USD"]
    gap = common["HEFA"] - common["EFA"]
    gap_ax.scatter(raw_usd, gap, s=15, alpha=0.6, color=COLORS[1])
    x = np.linspace(raw_usd.min(), raw_usd.max(), 100)
    gap_ax.plot(x, gap_fit.params["const"] + gap_fit.params["USD"] * x, color="black", lw=1.2)
    gap_ax.axhline(0, color="black", lw=0.5)
    gap_ax.axvline(0, color="black", lw=0.5)
    gap_ax.set_xlabel("Raw broad USD change (positive = stronger dollar)")
    gap_ax.set_ylabel("HEFA − EFA monthly return")
    gap_ax.set_title(f"Gap vs raw USD: β={gap_fit.params['USD']:.2f}, R²={gap_fit.rsquared:.2f}")
    for axis in (gap_ax.xaxis, gap_ax.yaxis):
        axis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))
    fig.suptitle(f"Currency hedging: {common.index.min()}–{common.index.max()} ({len(common)} months)")
    fig.tight_layout()
    return fig


def russia_overview(ru: pd.DataFrame, r2: pd.Series, events: dict[str, str]):
    """Left: growth of 1 unit in rubles vs dollars (log scale). Right: rolling R² of Russian
    returns on the EM market factor. Shaded: not investable for foreigners after Feb 2022."""
    fig, (wealth_ax, r2_ax) = plt.subplots(1, 2, figsize=(11, 4))
    for i, (col, label) in enumerate([("RUS_rub", "In rubles"), ("RUS_usd", "In US dollars")]):
        w = (1 + ru[col]).cumprod()
        wealth_ax.plot(w.index.to_timestamp(), w, label=label, color=COLORS[i])
    wealth_ax.set_yscale("log")
    for axis_fmt in (wealth_ax.yaxis.set_major_formatter, wealth_ax.yaxis.set_minor_formatter):
        axis_fmt(plt.FuncFormatter(lambda v, _: f"{v:g}"))  # plain numbers, not 6×10^0
    wealth_ax.set_title("MOEX Russia total return index, growth of 1")
    wealth_ax.legend(fontsize=8)
    r2_ax.plot(r2.index.to_timestamp(), r2, color=COLORS[2])
    r2_ax.set_ylim(0, 1)
    r2_ax.set_title("Rolling 36-month R² on the EM market factor")
    for ax in (wealth_ax, r2_ax):
        ax.axvspan(pd.Timestamp("2022-03-01"), ru.index.max().to_timestamp(), color="grey", alpha=0.15)
        for label, date in events.items():
            ax.axvline(pd.Timestamp(date), color="black", lw=0.7, ls="--")
            ax.text(pd.Timestamp(date), ax.get_ylim()[1], f" {label}", fontsize=7, va="top", rotation=90)
    fig.suptitle("Russia: ruble drag and decoupling from emerging markets (grey = closed to foreigners)")
    fig.tight_layout()
    return fig
