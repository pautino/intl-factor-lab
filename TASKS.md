# Tasks

Legend: `[ ]` open, `[claude]`/`[codex]` claimed, `[x]` done.

1. [x] Repo skeleton: git, AGENTS.md, TASKS.md, .gitignore, requirements.txt
2. [x] `intl_factors/data.py`: Ken French international factor download + parser, ETF monthly total returns (yfinance), USD dollar factor (FRED broad dollar index), caching
3. [x] `intl_factors/models.py`: CAPM / FF5+Mom / +USD regressions with HAC errors, rolling betas, return attribution, global-vs-local comparison, subperiod stability
4. [x] `intl_factors/plots.py`: exposure bars with CIs, rolling betas, fitted vs realized, cumulative residuals, attribution bars
5. [x] `tests/`: synthetic-data test that regressions recover known betas; parser test on a sample French CSV
6. [x] `notebooks/international_factor_lab.ipynb`: Colab notebook with section headers, runs end to end
7. [claude] `README.md`: the 15 sections (overview, use case, architecture, data, libraries, structure, build guide, pipeline, cleaning, models, visuals, metrics, deliverables, resume text, upgrades)
8. [claude] Run notebook end to end on real data, save figures to `reports/figures/`, write findings into README "Results"
9. [ ] Push to GitHub (user must create the repo; then set REPO_URL in notebook cell 1)

## Handoff notes
(Updated by the agent that stops working. Read this first.)

- Status: in progress (Claude Code started 2026-11-04).
