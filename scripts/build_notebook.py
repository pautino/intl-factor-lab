"""Builds notebooks/international_factor_lab.ipynb (run from repo root)."""
import nbformat as nbf

cells = []
md = lambda s: cells.append(nbf.v4.new_markdown_cell(s.strip()))
code = lambda s: cells.append(nbf.v4.new_code_cell(s.strip()))

md("""
# International Factor Exposure & Return Attribution Lab

Which risks drive the returns of international equity ETFs, and are those risks **global** or **local**?

**Research questions**
1. How much of each ETF's return do Fama–French 5 + momentum factors explain?
2. Integration vs segmentation: do *regional* factors explain returns better than *global* (developed-market) factors?
3. Currency: does exposure to the broad US dollar add explanatory power?
4. Stability: did exposures change after 2016?

**Data**: Kenneth French international factor library (USD, monthly), Yahoo Finance total returns, FRED broad dollar index.
**Method**: OLS with Newey–West (HAC) standard errors, rolling 36-month betas, return attribution, Chow-type Wald stability test.
""")

md("## 0. Setup (Colab or local)")
code('''
import os, sys, subprocess
from pathlib import Path

REPO_URL = "https://github.com/YOUR_USER/intl-factor-lab.git"  # <- set after pushing to GitHub

if "google.colab" in sys.modules and not Path("intl_factors").exists():
    if not Path("intl-factor-lab").exists():
        subprocess.run(["git", "clone", "-q", REPO_URL, "intl-factor-lab"], check=True)
    os.chdir("intl-factor-lab")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-U", "yfinance", "statsmodels"], check=True)

ROOT = Path.cwd() if Path("intl_factors").exists() else Path.cwd().parent
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

from intl_factors import data, models, plots

pd.set_option("display.float_format", "{:.3f}".format)
''')

md("## 1. Configuration")
code('''
ETFS = data.ETFS                 # ticker -> (description, local Ken French region)
GLOBAL_REGION = "Developed"      # benchmark "global" factor set
SINGLE_COUNTRY = ["EWZ"]         # country funds explained by a broader regional factor set
SPLIT = "2016-01"                # subperiod break for the stability test
WINDOW = 36                      # months for rolling betas
FIG_DIR = ROOT / "reports" / "figures"
TAB_DIR = ROOT / "reports" / "tables"
FIG_DIR.mkdir(parents=True, exist_ok=True)
TAB_DIR.mkdir(parents=True, exist_ok=True)

def save(fig, name):
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=150)

pd.DataFrame(ETFS, index=["description", "local region"]).T
''')

md("""
## 2. Data collection
Downloads are cached in `data/cache/`. Set `refresh=True` to pull the latest vintage
(record the date: French factors are revised when Bloomberg data are updated).
""")
code('''
rets, factors, usd = data.load_all(ETFS, refresh=False)
print("ETF returns:", rets.index.min(), "->", rets.index.max())
for region, f in factors.items():
    print(f"{region:<24} factors: {f.index.min()} -> {f.index.max()}")
print("USD factor:", usd.index.min(), "->", usd.index.max())
''')

md("""
## 3. Cleaning checks and descriptive statistics
- Returns are monthly decimals in USD; ETF returns include reinvested dividends (Yahoo adjusted close).
- No prices are filled before inception or across gaps; the current, incomplete month is dropped.
- The factor correlation matrix checks multicollinearity (high correlations widen beta confidence intervals).
""")
code('''
coverage = pd.DataFrame({
    "first": rets.apply(lambda s: s.first_valid_index()),
    "last": rets.apply(lambda s: s.last_valid_index()),
    "months": rets.notna().sum(),
    "missing_inside": rets.apply(lambda s: s.loc[s.first_valid_index():s.last_valid_index()].isna().sum()),
})
assert coverage["missing_inside"].eq(0).all(), "gap inside an ETF's history"
display(coverage)

stats = pd.DataFrame({
    "ann_return": rets.mean() * 12,
    "ann_vol": rets.std() * np.sqrt(12),
    "worst_month": rets.min(),
    "best_month": rets.max(),
})
stats["sharpe_like"] = stats["ann_return"] / stats["ann_vol"]
display(stats)

em = models.align(rets["EEM"], factors["Emerging"], usd, orthogonalize_usd=False)
fig = plots.correlation_heatmap(em[models.FF6 + ["USD"]], "Emerging-market factors + raw USD: correlations")
save(fig, "01_factor_correlations_emerging")
print(f"corr(EM Mkt-RF, USD) = {em['Mkt-RF'].corr(em['USD']):.2f}")
''')

md("""
**Why USD is orthogonalized below.** EM equity returns measured in USD fall when the dollar
strengthens, so the raw dollar factor is strongly correlated with the regional market factor.
In the models we replace USD with the part of the dollar move *not* explained by Mkt-RF.
This leaves the USD beta and R² unchanged, but the Mkt-RF beta now also carries the dollar
move that travels with the market, and the two betas stop trading off in rolling windows.
""")

md("""
## 4. Full-sample factor models (local factors)
Each ETF is regressed on its **own region's** factors. All three models use the same months
(the USD series starts in 2006), so adjusted R² and alphas are comparable across models.
Alpha is annualized (×12); t-stats use Newey–West standard errors.
""")
code('''
aligned, fits = {}, {}
for t, (_, region) in ETFS.items():
    aligned[t] = models.align(rets[t], factors[region], usd)
    fits[t] = models.fit_models(aligned[t])

summary = pd.concat({t: models.model_summary(r) for t, r in fits.items()}, names=["ETF", "model"])
display(summary)
''')

md("## 5. Factor exposures with 95% confidence intervals (FF6 + USD)")
code('''
coefs = {t: models.coef_table(r["FF6+USD"]) for t, r in fits.items()}
display(pd.DataFrame({t: c["coef"] for t, c in coefs.items()}).T)
fig = plots.exposure_bars(coefs, "Factor exposures, FF6 + USD on local factors (95% HAC CI)")
save(fig, "02_exposures")
''')

md("""
## 6. Global vs local factors (integration vs segmentation)
Same FF6 specification and months; only the factor region changes. If local factors explain
returns much better, the market behaves as if partly **segmented** from global risk pricing.
""")
code('''
gvl = pd.concat({t: models.global_vs_local(rets[t], factors[region], factors[GLOBAL_REGION])
                 for t, (_, region) in ETFS.items()}, names=["ETF", "factors"])
display(gvl)
fig = plots.global_vs_local_bars(gvl["adj_r2"].unstack())
save(fig, "03_global_vs_local")
''')

md("""
## 7. Rolling 36-month exposures
Each point uses only the trailing 36 months, i.e. what an analyst could have measured at that date.
""")
code('''
rolling = {t: models.rolling_betas(aligned[t], models.FF6 + ["USD"], WINDOW).dropna() for t in ETFS}
broad = {t: b for t, b in rolling.items() if t not in SINGLE_COUNTRY}
save(plots.rolling_beta_grid(broad, ["Mkt-RF", "HML", "MOM", "USD"], WINDOW), "04_rolling_betas_regional")
# single-country funds vs a broad regional factor set: much noisier, so plotted on their own scale
single = {t: b for t, b in rolling.items() if t in SINGLE_COUNTRY}
save(plots.rolling_beta_grid(single, ["Mkt-RF", "HML", "MOM", "USD"], WINDOW), "04b_rolling_betas_single_country")
''')

md("""
## 8. Return attribution
Average annualized excess return split into alpha + Σ beta × factor premium. Components sum to the
ETF's annualized mean excess return (arithmetic, ×12); the in-sample residual averages to zero.
""")
code('''
attr = pd.DataFrame({t: models.attribution(fits[t]["FF6+USD"], aligned[t]) for t in ETFS}).T
attr = attr.drop(columns="residual")
assert np.allclose(attr.sum(axis=1), pd.Series({t: aligned[t]["y"].mean() * 12 for t in ETFS}))
display(attr)
fig = plots.attribution_bars(attr, "Annualized excess return attribution (FF6 + USD, local factors)")
save(fig, "05_attribution")
''')

md("""
## 9. Residual diagnostics
- **Fitted vs realized**: how close points lie to the 45° line.
- **Cumulative alpha + residual**: a steady downward drift is a cost the factors do not capture
  (expense ratio, dividend withholding tax, index differences).
- **Residual autocorrelation**: negative lag-1 autocorrelation means a one-day timing mismatch (ETFs
  are priced at the New York close; local factors at local market closes) that reverses next month.
  A lagged market term tests the alternative explanation of slow price adjustment.
""")
code('''
best = {t: (fits[t]["FF6+USD"], aligned[t]) for t in ETFS}
save(plots.fitted_vs_realized(best), "06_fitted_vs_realized")
save(plots.cumulative_residuals(best), "07_cumulative_residuals")

rows = {}
for t in ETFS:
    res, d = best[t]
    lagged = d.assign(Mkt_lag=d["Mkt-RF"].shift(1)).dropna()
    r_lag = models.fit(lagged, models.FF6 + ["USD", "Mkt_lag"])
    rows[t] = {"resid_ac1": res.resid.autocorr(1), "resid_ac2": res.resid.autocorr(2),
               "lagged_mkt_beta": r_lag.params["Mkt_lag"], "lagged_mkt_t": r_lag.tvalues["Mkt_lag"]}
diag = pd.DataFrame(rows).T
display(diag)
''')

md(f"""
## 10. Stability: did exposures change?
HAC Wald test that alpha and all betas are equal before and after the split month (Chow-type test).
""")
code('''
stab_rows, stab_tables = {}, {}
for t in ETFS:
    table, stat, p = models.stability_test(aligned[t], models.FF6 + ["USD"], SPLIT)
    stab_tables[t] = table
    stab_rows[t] = {"wald_chi2": stat, "p_value": p,
                    "mkt_beta_pre": table.loc["Mkt-RF", "pre"], "mkt_beta_post": table.loc["Mkt-RF", "post"],
                    "usd_beta_pre": table.loc["USD", "pre"], "usd_beta_post": table.loc["USD", "post"]}
stability = pd.DataFrame(stab_rows).T
display(stability)
''')

md("## 11. Export tables")
code('''
summary.to_csv(TAB_DIR / "model_summary.csv")
pd.concat(coefs, names=["ETF", "term"]).to_csv(TAB_DIR / "coefficients_ff6_usd.csv")
gvl.to_csv(TAB_DIR / "global_vs_local.csv")
attr.to_csv(TAB_DIR / "attribution.csv")
diag.to_csv(TAB_DIR / "residual_diagnostics.csv")
stability.to_csv(TAB_DIR / "stability.csv")
print("Saved tables to", TAB_DIR, "and figures to", FIG_DIR)
''')

md("""
## 12. Limitations
- French factors are built from Bloomberg stock data and are not the MSCI indices the ETFs track
  (e.g. `Developed_ex_US` includes Canada, MSCI EAFE does not). Part of each alpha is index mismatch.
- ETF returns are net of fees and foreign dividend withholding taxes; factor returns are not.
- The USD factor is a non-traded index change, so its coefficient is a sensitivity, not a priced premium.
- Survivorship is not an issue for the fixed ETF list, but the list itself was chosen today.
- Alphas and betas are conditional on the model and the 2006–2026 sample.
""")

nb = nbf.v4.new_notebook(cells=cells, metadata={
    "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
    "colab": {"provenance": []}})
nbf.write(nb, "notebooks/international_factor_lab.ipynb")
print("wrote", len(cells), "cells")
