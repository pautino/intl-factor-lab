import numpy as np
import pandas as pd
import pytest

from intl_factors.data import parse_french_csv
from intl_factors.models import (FF6, align, attribution, contributions, fit,
                                 nw_lags, quarterly_returns, quarterly_robustness,
                                 rolling_betas, stability_test)

SAMPLE = """This file was created using the 202609 Bloomberg database.

Missing data are indicated by -99.99.

,Mkt-RF,SMB,HML,RMW,CMA,RF
199007    ,0.77    ,0.60   ,-0.36    ,0.21    ,1.35    ,0.68
199008    ,-10.00  ,-99.99 ,1.00     ,0.00    ,0.00    ,0.66

 Annual Factors: January-December
,Mkt-RF,SMB,HML,RMW,CMA,RF
1991   ,10.0   ,1.0  ,1.0  ,1.0  ,1.0  ,5.0
"""

TRUE_BETAS = np.array([1.1, 0.3, -0.2, 0.15, 0.1, -0.05])


def synthetic(n=480, seed=0, break_at=None):
    rng = np.random.default_rng(seed)
    idx = pd.period_range("1985-01", periods=n, freq="M")
    f = pd.DataFrame(rng.normal(0.005, 0.04, (n, 6)), index=idx, columns=FF6)
    f["RF"] = 0.002
    betas = np.tile(TRUE_BETAS, (n, 1))
    if break_at is not None:
        betas[break_at:, 0] = 0.5  # market beta halves after the break
    ret = 0.002 + (f[FF6].to_numpy() * betas).sum(1) + rng.normal(0, 0.01, n) + f["RF"]
    return pd.Series(ret, index=idx), f


def test_parse_french_csv_monthly_block_only():
    df = parse_french_csv(SAMPLE)
    assert list(df.columns) == ["Mkt-RF", "SMB", "HML", "RMW", "CMA", "RF"]
    assert len(df) == 2  # annual block excluded
    assert df.index[0] == pd.Period("1990-07", "M")
    assert df.loc["1990-07", "Mkt-RF"] == pytest.approx(0.0077)  # percent -> decimal
    assert np.isnan(df.loc["1990-08", "SMB"])  # -99.99 -> NaN


def test_fit_recovers_known_betas_and_alpha():
    ret, f = synthetic()
    res = fit(align(ret, f), FF6)
    np.testing.assert_allclose(res.params[FF6], TRUE_BETAS, atol=0.05)
    assert res.params["const"] == pytest.approx(0.002, abs=0.001)


def test_contributions_sum_to_excess_return_and_attribution_to_mean():
    ret, f = synthetic()
    df = align(ret, f)
    res = fit(df, FF6)
    np.testing.assert_allclose(contributions(res, df).sum(axis=1), df["y"], atol=1e-12)
    assert attribution(res, df).sum() == pytest.approx(df["y"].mean() * 12)


def test_rolling_betas_track_true_value():
    ret, f = synthetic()
    b = rolling_betas(align(ret, f), FF6, window=60).dropna()
    assert b["Mkt-RF"].mean() == pytest.approx(1.1, abs=0.05)


def test_stability_test_detects_break_and_not_absent_one():
    ret, f = synthetic(break_at=240)
    table, stat, p = stability_test(align(ret, f), FF6, "2005-01")
    assert p < 0.001
    assert table.loc["Mkt-RF", "post"] == pytest.approx(0.5, abs=0.1)
    ret, f = synthetic(seed=1)
    assert stability_test(align(ret, f), FF6, "2005-01")[2] > 0.01


def test_orthogonal_usd_keeps_usd_beta_and_fit():
    ret, f = synthetic()
    rng = np.random.default_rng(5)
    usd = pd.Series(-0.6 * f["Mkt-RF"] + rng.normal(0, 0.02, len(f)), index=f.index, name="USD")
    raw = fit(align(ret, f, usd, orthogonalize_usd=False), FF6 + ["USD"])
    d = align(ret, f, usd)
    orth = fit(d, FF6 + ["USD"])
    assert abs(d["USD"].corr(d["Mkt-RF"])) < 1e-10
    assert orth.params["USD"] == pytest.approx(raw.params["USD"])
    assert orth.rsquared == pytest.approx(raw.rsquared)


def test_closing_time_test_recovers_reversal_loadings():
    from intl_factors.models import closing_time_test
    rng = np.random.default_rng(3)
    idx = pd.period_range("2000-01", periods=300, freq="M")
    gap = pd.Series(rng.normal(0, 0.01, 300), index=idx)
    resid = 0.5 * gap - 0.5 * gap.shift(1) + rng.normal(0, 0.002, 300)
    out = closing_time_test(resid.dropna(), gap)
    assert out["gap_t"] == pytest.approx(0.5, abs=0.05)
    assert out["gap_t-1"] == pytest.approx(-0.5, abs=0.05)
    assert out["ac1_before"] < -0.3 and abs(out["ac1_after"]) < 0.15


def test_nw_lags():
    assert nw_lags(100) == 4
    assert nw_lags(240) == 4


def test_quarterly_returns_compounds_total_returns_before_subtracting_rf():
    idx = pd.period_range("2020-01", periods=8, freq="M")
    df = pd.DataFrame(0.0, index=idx, columns=FF6 + ["RF", "USD", "y"])
    df["RF"], df["Mkt-RF"], df["SMB"] = 0.01, 0.02, 0.1
    df.loc["2020-01":"2020-03", "y"] = [0.09, -0.06, 0.01]
    df.loc["2020-01":"2020-03", "USD"] = [0.1, -0.05, 0.02]
    q = quarterly_returns(df)
    assert list(q.index) == list(pd.period_range("2020Q1", "2020Q2", freq="Q-DEC"))
    assert q.loc["2020Q1", "RF"] == pytest.approx(1.01 ** 3 - 1)
    assert q.loc["2020Q1", "y"] == pytest.approx(1.10 * 0.95 * 1.02 - 1.01 ** 3)
    assert q.loc["2020Q1", "Mkt-RF"] == pytest.approx(1.03 ** 3 - 1.01 ** 3)
    assert q.loc["2020Q1", "USD"] == pytest.approx(1.10 * 0.95 * 1.02 - 1)
    assert q.loc["2020Q1", "SMB"] == pytest.approx(0.3)  # fixed-notional spread payoffs


def test_quarterly_returns_drops_quarters_with_missing_months_or_inputs():
    ret, factors = synthetic(n=12)
    usd = pd.Series(0.01, index=ret.index, name="USD")
    raw = align(ret, factors, usd, orthogonalize_usd=False)
    raw.loc["1985-05", "HML"] = np.nan
    raw = raw.drop(pd.Period("1985-08", "M"))
    q = quarterly_returns(raw.iloc[::-1])  # input order must not change calendar grouping
    assert list(q.index) == [pd.Period("1985Q1", "Q-DEC"), pd.Period("1985Q4", "Q-DEC")]


def test_quarterly_robustness_matches_calendar_samples_and_annualization():
    ret, factors = synthetic()
    rng = np.random.default_rng(7)
    usd = pd.Series(-0.6 * factors["Mkt-RF"] + rng.normal(0, 0.02, len(ret)),
                    index=ret.index, name="USD")
    ret = ret.iloc[1:-1]  # leave both boundary quarters incomplete
    table = quarterly_robustness(ret, factors, usd)
    monthly, quarterly = table.loc["monthly"], table.loc["quarterly"]
    assert monthly["n_obs"] == 3 * quarterly["n_obs"] == 474
    assert monthly["start"] == "1985-04" and monthly["end"] == "2024-09"
    assert quarterly["start"] == "1985Q2" and quarterly["end"] == "2024Q3"
    assert monthly["ljung_box_lags"] == 12 and quarterly["ljung_box_lags"] == 4
    q = quarterly_returns(align(ret, factors, usd, orthogonalize_usd=False))
    d = align(q["y"] + q["RF"], q[FF6 + ["RF"]], q["USD"])
    assert abs(d["USD"].corr(d["Mkt-RF"])) < 1e-10
    res = fit(d, FF6 + ["USD"])
    assert quarterly["alpha_ann"] == pytest.approx(res.params["const"] * 4)
    assert quarterly["alpha_t"] == pytest.approx(res.tvalues["const"])
    assert quarterly["resid_ac1"] == pytest.approx(res.resid.autocorr(1))


def test_quarterly_returns_rejects_duplicate_months_and_no_complete_quarters():
    ret, factors = synthetic(n=3)
    usd = pd.Series(0.01, index=ret.index, name="USD")
    raw = align(ret, factors, usd, orthogonalize_usd=False)
    with pytest.raises(ValueError, match="unique months"):
        quarterly_returns(pd.concat([raw, raw.iloc[:1]]))
    with pytest.raises(ValueError, match="No complete calendar quarters"):
        quarterly_returns(raw.iloc[:2])
