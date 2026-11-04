"""Factor models for international ETF returns.

Models (monthly excess returns, plus quarterly robustness; Newey-West HAC errors):
  CAPM     : y = a + b*MKT + e
  FF6      : Fama-French 5 factors + momentum
  FF6+USD  : FF6 plus the broad-dollar factor (currency translation risk)
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.regression.rolling import RollingOLS
from statsmodels.stats.diagnostic import acorr_ljungbox

FF6 = ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "MOM"]
MODELS = {"CAPM": ["Mkt-RF"], "FF6": FF6, "FF6+USD": FF6 + ["USD"]}


def align(ret: pd.Series, factors: pd.DataFrame, usd: pd.Series | None = None,
          orthogonalize_usd: bool = True) -> pd.DataFrame:
    """Factor columns + excess return ``y`` on common periods with no missing values.

    With ``orthogonalize_usd`` the USD column is replaced by its residual from a regression
    on the regional Mkt-RF (full factor sample, descriptive). The dollar is ~-0.8 correlated
    with emerging-market returns in USD, so raw Mkt and USD betas trade off against each
    other; the residual keeps the USD beta and R^2 unchanged while Mkt-RF keeps the
    dollar move that travels with the market.
    """
    df = factors.copy()
    if usd is not None:
        df = df.join(usd, how="inner")
        if orthogonalize_usd:
            ok = df[["Mkt-RF", "USD"]].dropna().index
            proj = sm.OLS(df.loc[ok, "USD"], sm.add_constant(df.loc[ok, "Mkt-RF"])).fit()
            df.loc[ok, "USD"] = proj.resid
    df["y"] = ret.reindex(df.index) - df["RF"]
    return df.dropna()


def nw_lags(n: int) -> int:
    """Newey-West (1994) rule of thumb for the HAC lag length."""
    return max(1, int(np.floor(4 * (n / 100) ** (2 / 9))))


def fit(df: pd.DataFrame, cols: list[str]):
    """OLS of ``y`` on ``cols`` with HAC (autocorrelation & heteroskedasticity robust) errors."""
    if len(df) <= len(cols) + 1:
        raise ValueError(f"Only {len(df)} observations for {len(cols)} factors")
    X = sm.add_constant(df[cols])
    return sm.OLS(df["y"], X).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags(len(df))})


def fit_models(df: pd.DataFrame, models: dict = MODELS) -> dict:
    """Fit every model on the *same* months so R^2 and alphas are comparable."""
    return {name: fit(df, cols) for name, cols in models.items()}


def coef_table(res, level: float = 0.95) -> pd.DataFrame:
    ci = res.conf_int(1 - level)
    return pd.DataFrame({"coef": res.params, "se": res.bse, "t": res.tvalues,
                         "p": res.pvalues, "ci_low": ci[0], "ci_high": ci[1]})


def model_summary(results: dict) -> pd.DataFrame:
    """One row per model: annualized alpha, its t-stat, fit, residual diagnostics."""
    rows = {}
    for name, r in results.items():
        rows[name] = {
            "alpha_ann": r.params["const"] * 12,
            "alpha_t": r.tvalues["const"],
            "adj_r2": r.rsquared_adj,
            "resid_vol_ann": r.resid.std() * np.sqrt(12),
            "ljung_box_p12": acorr_ljungbox(r.resid, lags=[12])["lb_pvalue"].iloc[0],
            "n_months": int(r.nobs),
        }
    return pd.DataFrame(rows).T


def quarterly_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate raw aligned monthly data, retaining only complete calendar quarters.

    Pass data from ``align(..., orthogonalize_usd=False)``. Compound the ETF, RF,
    and total market separately, then subtract quarterly RF to form excess returns.
    Compound the raw dollar index changes before orthogonalizing at quarterly frequency.
    Sum SMB/HML/RMW/CMA/MOM as fixed-notional monthly long-short payoffs: monthly
    spread returns alone do not identify compounded returns of the underlying legs.
    """
    if not isinstance(df.index, pd.PeriodIndex) or df.index.freqstr != "M":
        raise ValueError("Quarterly aggregation requires a monthly PeriodIndex")
    if not df.index.is_unique:
        raise ValueError("Quarterly aggregation requires unique months")
    df = df[FF6 + ["RF", "USD", "y"]].dropna().sort_index()
    quarters = df.index.asfreq("Q-DEC")
    counts = df.groupby(quarters).size()
    complete = counts.index[counts.eq(3)]
    if complete.empty:
        raise ValueError("No complete calendar quarters in the common monthly sample")
    df = df.loc[quarters.isin(complete)]
    quarters = df.index.asfreq("Q-DEC")
    out = df.groupby(quarters).sum()
    rf_growth = (1 + df["RF"]).groupby(quarters).prod()
    out["RF"] = rf_growth - 1
    out["y"] = (1 + df["y"] + df["RF"]).groupby(quarters).prod() - rf_growth
    out["Mkt-RF"] = (1 + df["Mkt-RF"] + df["RF"]).groupby(quarters).prod() - rf_growth
    out["USD"] = (1 + df["USD"]).groupby(quarters).prod() - 1
    return out


def quarterly_robustness(ret: pd.Series, factors: pd.DataFrame,
                         usd: pd.Series) -> pd.DataFrame:
    """Monthly vs quarterly local FF6+USD fits on the same complete quarters.

    Re-estimate USD orthogonalization separately at each frequency on the matched
    sample. Annualize arithmetic alpha by 12 or 4; use HAC errors at both frequencies
    and Ljung-Box horizons of 12 months or 4 quarters. Lag-1 residual correlations
    refer to different elapsed times (one month vs one quarter).
    """
    raw = align(ret, factors, usd, orthogonalize_usd=False)
    quarterly = quarterly_returns(raw)
    monthly = raw.loc[raw.index.asfreq("Q-DEC").isin(quarterly.index)].sort_index()
    rows = {}
    for frequency, frame, annual_periods in (("monthly", monthly, 12),
                                              ("quarterly", quarterly, 4)):
        d = align(frame["y"] + frame["RF"], frame[FF6 + ["RF"]], frame["USD"])
        res = fit(d, FF6 + ["USD"])
        rows[frequency] = {
            "start": str(d.index.min()), "end": str(d.index.max()),
            "n_obs": int(res.nobs),
            "alpha_ann": res.params["const"] * annual_periods,
            "alpha_t": res.tvalues["const"],
            "beta_mkt": res.params["Mkt-RF"], "beta_usd": res.params["USD"],
            "adj_r2": res.rsquared_adj, "resid_ac1": res.resid.autocorr(1),
            "hac_lags": nw_lags(len(d)), "ljung_box_lags": annual_periods,
            "ljung_box_p": acorr_ljungbox(res.resid, lags=[annual_periods])["lb_pvalue"].iloc[0],
        }
    return pd.DataFrame.from_dict(rows, orient="index").rename_axis("frequency")


def contributions(res, df: pd.DataFrame) -> pd.DataFrame:
    """Monthly decomposition y_t = alpha + sum_k beta_k f_k,t + e_t (sums exactly to y)."""
    cols = [c for c in res.params.index if c != "const"]
    out = df[cols] * res.params[cols]
    out["alpha"] = res.params["const"]
    out["residual"] = res.resid
    return out


def attribution(res, df: pd.DataFrame) -> pd.Series:
    """Annualized (x12, arithmetic) average contribution of each component.
    Sums to the annualized mean excess return; the residual averages to zero in-sample."""
    return contributions(res, df).mean() * 12


def rolling_betas(df: pd.DataFrame, cols: list[str], window: int = 36) -> pd.DataFrame:
    """Rolling-window OLS betas (point estimates). Each value uses only the trailing
    ``window`` months, so it is the exposure an analyst could have measured at that date."""
    X = sm.add_constant(df[cols])
    return RollingOLS(df["y"], X, window=window).fit().params.drop(columns="const")


def global_vs_local(ret: pd.Series, local: pd.DataFrame, global_: pd.DataFrame,
                    cols: list[str] = FF6) -> pd.DataFrame:
    """Same months and factor set; only the factor *region* differs.

    Higher adjusted R^2 and smaller |alpha| for the local model suggest the market is
    priced by regional rather than global risk (partial segmentation)."""
    dl, dg = align(ret, local), align(ret, global_)
    idx = dl.index.intersection(dg.index)
    rows = {}
    for label, d in (("global", dg.loc[idx]), ("local", dl.loc[idx])):
        r = fit(d, cols)
        rows[label] = {"alpha_ann": r.params["const"] * 12, "alpha_t": r.tvalues["const"],
                       "beta_mkt": r.params["Mkt-RF"], "adj_r2": r.rsquared_adj,
                       "n_months": int(r.nobs)}
    return pd.DataFrame(rows).T


def stability_test(df: pd.DataFrame, cols: list[str], split: str):
    """HAC Wald (Chow-type) test that alpha and all betas are equal before/after ``split``.

    Returns (table of pre/post coefficients, Wald chi2 statistic, p-value)."""
    X = sm.add_constant(df[cols])
    post = (df.index >= pd.Period(split, "M")).astype(float)
    if post.sum() <= X.shape[1] or (1 - post).sum() <= X.shape[1]:
        raise ValueError(f"Split {split} leaves too few months on one side")
    Xfull = pd.concat([X, X.mul(post, axis=0).add_suffix("_post")], axis=1)
    res = sm.OLS(df["y"], Xfull).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags(len(df))})
    k = X.shape[1]
    w = res.wald_test(np.hstack([np.zeros((k, k)), np.eye(k)]), scalar=True)
    pre = res.params.iloc[:k].to_numpy()
    table = pd.DataFrame({"pre": pre, "post": pre + res.params.iloc[k:].to_numpy()},
                         index=X.columns)
    return table, float(np.squeeze(w.statistic)), float(np.squeeze(w.pvalue))


def closing_time_test(resid: pd.Series, gap: pd.Series) -> dict:
    """Non-synchronous close test: regress model residuals on the US last-trading-day
    return of month t and t-1 (HAC errors).

    If the US-listed ETF prices end-of-month US-hours news that the local factor only
    prices next month, the loading is positive on gap_t and negative on gap_t-1."""
    X = pd.DataFrame({"gap_t": gap, "gap_t-1": gap.shift(1)}).reindex(resid.index).dropna()
    e = resid.loc[X.index]
    r = sm.OLS(e, sm.add_constant(X)).fit(cov_type="HAC", cov_kwds={"maxlags": nw_lags(len(X))})
    return {"gap_t": r.params["gap_t"], "gap_t_t": r.tvalues["gap_t"],
            "gap_t-1": r.params["gap_t-1"], "gap_t-1_t": r.tvalues["gap_t-1"],
            "resid_r2_explained": r.rsquared,
            "ac1_before": e.autocorr(1), "ac1_after": r.resid.autocorr(1)}
