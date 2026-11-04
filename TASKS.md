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
9. [ ] Push to GitHub — needs the user: create an empty GitHub repo, then
       `git remote add origin <url> && git push -u origin main`, then replace `REPO_URL` in
       `scripts/build_notebook.py` (setup cell), rebuild + re-execute the notebook, commit, push.
10. [ ] Test the notebook in real Colab (fresh runtime) after step 9; fix anything Colab-specific.
11. [ ] Optional upgrades (pick with the user; see README §15). Best value first:
       a. [codex] Quarterly-return robustness table (should remove the −0.3 residual autocorrelation).
       b. Hedged vs unhedged pair (HEFA vs EFA) to measure currency hedging directly.
       c. Add the user's home-country ETF and more EM countries (INDA, FXI, EWW, EZA).

## Handoff notes
(Updated by the agent that stops working. Read this first.)

- Active claim (Codex, 2026-11-04): task 11a. Editing `scripts/build_notebook.py`,
  `intl_factors/models.py`, `tests/test_models.py`, `README.md`, the generated notebook,
  and generated reports for the quarterly robustness check.
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
  - Residual lag-1 autocorrelation (≈ −0.35) is a month-end close-time mismatch, documented in
    README finding 6; it is not a bug. HAC errors handle inference.
  - If any number in README changes after a data refresh, update the README table and §14.
