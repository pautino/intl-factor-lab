# Tasks

Legend: `[ ]` open, `[claude]`/`[codex]` claimed, `[x]` done.

1. [x] Repo skeleton: git, AGENTS.md, TASKS.md, .gitignore, requirements.txt
2. [x] `intl_factors/data.py`: Ken French international factor download + parser, ETF monthly total returns (yfinance), USD dollar factor (FRED broad dollar index), caching
3. [x] `intl_factors/models.py`: CAPM / FF5+Mom / +USD regressions with HAC errors, rolling betas, return attribution, global-vs-local comparison, subperiod stability
4. [x] `intl_factors/plots.py`: exposure bars with CIs, rolling betas, fitted vs realized, cumulative residuals, attribution bars
5. [x] `tests/`: synthetic-data test that regressions recover known betas; parser test on a sample French CSV
6. [x] `notebooks/international_factor_lab.ipynb`: Colab notebook with section headers, runs end to end
7. [x] `README.md`: the 15 sections + key results + limitations + references
8. [x] Run notebook end to end on real data, save figures to `reports/figures/`, write findings into README
9. [x] Pushed to https://github.com/pautino/intl-factor-lab (public). Original steps:
       `git remote add origin <url> && git push -u origin main`, then replace `REPO_URL` in
       `scripts/build_notebook.py` (setup cell), rebuild + re-execute the notebook, commit, push.
10. [ ] Test the notebook in real Colab (fresh runtime) after step 9; fix anything Colab-specific.
11. [ ] Optional upgrades (pick with the user; see README §15). Best value first:
       a. [x] Quarterly-return robustness table (Codex; residual autocorrelation persists).
       b. [codex] Hedged vs unhedged pair (HEFA vs EFA) to measure currency hedging directly.
       c. Add the user's home-country ETF and more EM countries (INDA, FXI, EWW, EZA).
12. [x] Closing-time test: regress residuals on S&P 500 last-trading-day return (t, t-1);
       add to data.py/models.py/tests/notebook §9; fix README finding 6 and resume line.

## Handoff notes
(Updated by the agent that stops working. Read this first.)

- Active claim (Codex, 2026-11-04): task 11b. Editing `intl_factors/models.py`,
  `intl_factors/plots.py`, `tests/test_models.py`, `scripts/build_notebook.py`, `README.md`,
  the generated notebook, and new hedged/unhedged comparison reports. No rate-data addition planned.
- Status (Claude Code, 2026-11-04, after Codex 11a): task 12 COMPLETE. The closing-time cause is
  now CONFIRMED, not tentative: residuals load +0.2…+0.6 on the S&P 500 last-trading-day return
  of month t and −0.3…−0.6 on month t−1 (|t| 5–9, 27–44% of residual variance), scaling with
  time-zone gap; EWZ ≈ 0. Quarterly persistence (11a) is expected: the mismatch recurs at every
  quarter-end. `data.last_day_returns`, `models.closing_time_test`, notebook §9, README findings
  6–7 and §14 updated. 12/12 tests pass; notebook executes end to end.
  Remaining: tasks 9 (user pushes to GitHub), 10, 11b, 11c.

- Status (Codex, 2026-11-04): task 11a COMPLETE. New notebook §10 compares local FF6+USD
  fits on 246 months / 82 complete quarters (2006Q2–2026Q3); results are exported to
  `reports/tables/quarterly_robustness.csv`. Quarterly residual AC(1) remains −0.33 to −0.20,
  so aggregation does not remove the reversal. README finding 7 records this result.
  11/11 tests pass; all 13 notebook code cells execute with 8 embedded figures and no errors.
  Standard nbconvert was blocked by sandbox local-port binding; executed and saved outputs
  in-process with IPython InteractiveShell, capture_output, and the matplotlib inline backend.
  Existing figures and CSV tables are unchanged. No active Codex file claims remain.
  Remaining: tasks 9, 10, 11b, and 11c.
- Status (Claude Code, 2026-11-04): core project COMPLETE. 7/7 tests pass, notebook executes
  end to end, README results match `reports/tables/*.csv`. Remaining: tasks 9–11.
- How to verify: `.venv/bin/python -m pytest -q`, then
  `.venv/bin/jupyter nbconvert --to notebook --execute --inplace notebooks/international_factor_lab.ipynb`.
  (In a sandbox, Jupyter needs local port binding; data downloads need network to
  mba.tuck.dartmouth.edu, fred.stlouisfed.org, query1/query2.finance.yahoo.com. Cached data
  in `data/cache/` lets it run offline.)
- Edit the notebook through `scripts/build_notebook.py`, not the .ipynb JSON.
- Design decisions to keep:
  - USD factor is orthogonalized against each region's Mkt-RF inside `models.align`
    (EM Mkt vs USD corr = −0.78). USD beta and R² are unchanged by this; Mkt beta absorbs the
    market-correlated dollar move. Use `orthogonalize_usd=False` for the raw correlation chart.
  - Monthly residual lag-1 autocorrelation (≈ −0.35) is consistent with a month-end close-time
    mismatch, but task 11a shows quarterly aggregation does not eliminate it; treat that causal
    explanation as tentative. HAC errors account for serial dependence in inference.
  - If any number in README changes after a data refresh, update the README table and §14.
