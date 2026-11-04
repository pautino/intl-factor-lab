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
10. [x] Tested in real Colab by the user (fresh runtime): all cells pass.
11. [ ] Optional upgrades (pick with the user; see README §15). Best value first:
       a. [x] Quarterly-return robustness table (Codex; residual autocorrelation persists).
       b. [codex] Hedged vs unhedged pair (HEFA vs EFA) to measure currency hedging directly.
       c. [x] Russia section (user's choice, not home country): MOEX MCFTR via ISS API in USD
          (RUB=X), Brent oil factor, 2014 sanctions break, ruble decomposition, post-2022 segmentation.
12. [x] Closing-time test: regress residuals on S&P 500 last-trading-day return (t, t-1);
       add to data.py/models.py/tests/notebook §9; fix README finding 6 and resume line.

13. [ ] Codex explains the project to the user (read-only: no file changes). Paste this into Codex:

```
Read AGENTS.md, TASKS.md and README.md, then the notebook builder scripts/build_notebook.py
and the result tables in reports/tables/. Do not change any files. You are my tutor for this
project. I study International Economic Relations (international finance). Explain it in
plain language, one part at a time, and wait for me to type "next" before moving on:
1. The question and the data: what an ETF, an excess return and a Fama-French factor are,
   where each dataset comes from (Ken French, Yahoo, FRED, Moscow Exchange) and why.
2. How a factor regression works: beta, alpha, R², t-stat and Newey-West errors, using real
   rows from reports/tables/model_summary.csv and coefficients_ff6_usd.csv as examples.
3. README findings 1 to 9, one at a time: the number, what it means economically, and the
   theory it connects to (market integration vs segmentation, the global financial cycle,
   covered interest parity, sanctions and capital controls).
4. How the code is organised: intl_factors/data.py, models.py, plots.py, the notebook builder.
After each part, ask me two short questions to check I understood, and correct my answers.
Finish with five questions a professor or interviewer would likely ask, with model answers.
```

14. [x] Remove Claude co-author credit from published commit messages; prepare a local
    backup and cleaned branch, verify file trees are preserved, then publish the history rewrite.

## Handoff notes
(Updated by the agent that stops working. Read this first.)

- Status (Claude Code, 2026-11-04): task 14 COMPLETE, per the user's choice. Published history has
  no Claude/Anthropic co-author trailers AND every commit is authored "Alexander Papoyan
  <73597411+pautino@users.noreply.github.com>" (repo git config set to this too). This SUPERSEDES
  Codex's `cleanup/remove-claude-coauthors` branch (which kept the old "dot tot" author):
  do not push that branch or any backup branch. Files are byte-identical to before. Backups stay local only.

- Active claim (Codex, 2026-11-04): task 14. Editing only `AGENTS.md` / `TASKS.md` for
  attribution policy and coordination, and preparing Git metadata on a separate cleanup branch.
  Prepared `cleanup/remove-claude-coauthors`: removes 11 Claude/Anthropic co-author trailers;
  every historical file tree, author, committer, and timestamp is preserved. Local backup:
  `backup/before-claude-credit-removal-20261104`; audit map: `.git/claude-credit-rewrite.json`.
  AGENTS.md now prevents future Claude co-author trailers. Current main retains its original
  history. Publishing requires a force push with an explicit lease on the old remote main;
  GitHub DNS remains unavailable in this shell, so the public repository is unchanged.
  Task 14 stays open until the cleaned history is published and contributor credit is checked.
- Status (Claude Code, 2026-11-04): task 11c COMPLETE as a Russia case study (user's choice).
  Notebook §13, README finding 9 + resume bullet. Data: MOEX ISS (MCFTR, IMOEX, RTSI, USD/RUB traded
  close <Jun 2013 then evening fixing "mc"), FRED Brent. All cached + committed. Do NOT use Yahoo
  RUB=X (wrong after 2022) or RSX/ERUS (deleted). Ruble series validated vs RTSI/IMOEX implied rate
  (corr 0.9994 since Jul 2013, excl. Feb-Mar 2022 market closure); the notebook asserts this.
  14/14 tests pass; notebook executes end to end. No open tasks; no active claims.

- Status (Claude Code, 2026-11-04): task 11b COMPLETE (Codex's code, run on the HEFA cache that was
  already in `data/cache/`). README finding 8: HEFA 10.3% vs EFA 6.6% p.a. compound; gap β on raw
  USD 1.02 (t 16, R² 0.78); 3.11% mean gap = 2.16 dollar appreciation + 0.95 intercept (t 1.2).
  Also: `data/cache/` is now COMMITTED (Colab could not reach FRED); Colab setup cell now refreshes
  a stale clone (fetch + reset) and only pip-installs missing packages. 13/13 tests pass; notebook
  executes end to end. No active claims. Remaining: 10 (user re-tests Colab), 11c (home country).

- Active claim (Codex, 2026-11-04): task 11b. Editing `intl_factors/models.py`,
  `intl_factors/plots.py`, `tests/test_models.py`, `scripts/build_notebook.py`, `README.md`,
  the generated notebook, and new hedged/unhedged comparison reports. No rate-data addition planned.
  Implementation ready: matched-sample EFA/HEFA metrics, FF6+USD fits, raw-USD-only gap fit,
  CIP explanation, one two-panel chart, and CSV export in new notebook §12. 13/13 tests pass.
  Pending external dependency: this shell cannot resolve Yahoo or GitHub. The required new cache
  `data/cache/etf_close_EFA_HEFA.csv` is absent; no real-data results have been fabricated.
  To populate it in a network-enabled terminal, run from the repo root:
  `.venv/bin/python -c 'from intl_factors import data; data.etf_returns(["EFA", "HEFA"])'`.
  Then add the actual README finding (and update deliverable/test counts), rebuild the notebook,
  execute all cells, inspect `08_hedged_vs_unhedged.png` / `hedged_vs_unhedged.csv`, and push.
  The previously executed notebook has been preserved until the new input data are available.
  Task 11b remains claimed, not done; the source implementation is committed separately.
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
