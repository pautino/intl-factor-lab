import numpy as np
import pandas as pd
import pytest

from intl_factors.data import parse_french_csv
from intl_factors.models import (FF6, align, attribution, contributions, fit,
                                 nw_lags, rolling_betas, stability_test)

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


def test_nw_lags():
    assert nw_lags(100) == 4
    assert nw_lags(240) == 4
