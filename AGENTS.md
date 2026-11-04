# Agent rules (shared by Claude Code and Codex)

Project: **International Factor Exposure & Return Attribution Lab** (idea #02 from
`colab_finance_project_ideas.md`, adapted to international finance).

## Coordination
- Two agents work in this repo: Claude Code and Codex (GPT). Before starting work,
  read `TASKS.md`, claim a task by writing `[codex]` or `[claude]` next to it, and
  mark it `[x]` when done. Never edit a file another agent has an open claim on.
- Commit small and often (`git add -A && git commit -m "..."`) so work is never lost.
- Do not add Claude or Anthropic `Co-Authored-By` trailers to commit messages.
- Handoff notes for whoever continues live at the bottom of `TASKS.md`.

## Code conventions
- Python package lives in `intl_factors/` (data.py, models.py, plots.py). Notebooks only
  call the package; no heavy logic inside notebook cells.
- Returns are **decimals** (0.01 = 1%), monthly, indexed by `pandas.Period` freq `M`.
- Ken French factors are downloaded in percent and converted to decimals in `data.py`.
- All factor and ETF returns are in **USD**; RF is the US 1-month T-bill from the French files.
- Regressions use Newey-West (HAC) standard errors.
- Tests: `.venv/bin/python -m pytest -q` must pass before marking a task done.
- Downloaded data is cached in `data/cache/` and COMMITTED (fixed vintage; Colab often cannot reach Yahoo). Only refresh with the user's approval, then update README numbers.

## Environment
- Local: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
- Colab: open `notebooks/international_factor_lab.ipynb`; the first cell installs deps.
