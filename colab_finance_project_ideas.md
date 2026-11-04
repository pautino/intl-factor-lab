**20 Google Colab Finance Project Ideas**

Prepared November 4, 2026. Ordered from intermediate analytics to institutional research prototypes.

Each project below contains all 13 fields requested in the reference image. Development estimates are focused hours for one developer who already knows Python and basic finance; they cover the stated notebook scope, documentation, and validation. Resume scores are my subjective assessment of a well executed project for the relevant role, rather than a hiring prediction.

“Institutional” describes the methods and research design. The proposed Colab versions use bounded datasets, simulations, and batch calculations. A production trading or risk platform would require additional infrastructure and controls.

| # | Project | Difficulty | Estimated time | Resume value |
|---|---|---|---|---|
| 01 | Multiasset Portfolio Performance and Risk Dashboard | Intermediate | 10–16 hours | 6/10 |
| 02 | Factor Exposure and Return Attribution Lab | Intermediate | 14–22 hours | 7/10 |
| 03 | Bond Pricing, Yield Curves, and Duration Lab | Intermediate | 16–26 hours | 7/10 |
| 04 | SEC Financial Statement Quality and Valuation Screener | Intermediate | 20–32 hours | 7/10 |
| 05 | Monte Carlo Wealth and Retirement Simulator | Intermediate | 14–24 hours | 6/10 |
| 06 | Macro Regime Detection and Tactical Allocation | Advanced | 30–50 hours | 8/10 |
| 07 | Earnings and SEC Filing Event Study | Advanced | 35–55 hours | 8/10 |
| 08 | Cointegration Pairs Trading Research Engine | Advanced | 35–55 hours | 8/10 |
| 09 | Black–Litterman and Robust Portfolio Optimization | Advanced | 30–50 hours | 8/10 |
| 10 | Value at Risk, Expected Shortfall, and Stress Testing | Advanced | 35–55 hours | 9/10 |
| 11 | Options Volatility Surface and Delta Hedging Lab | Advanced | 45–75 hours | 9/10 |
| 12 | Credit Default Probability and Expected Loss Model | Advanced | 35–60 hours | 8/10 |
| 13 | Machine Learning Equity Ranking with Temporal Validation | Advanced | 50–85 hours | 9/10 |
| 14 | Futures Trend Following with Volatility Targeting | Advanced | 50–85 hours | 9/10 |
| 15 | Execution Algorithms and Transaction Cost Analysis | Institutional | 70–110 hours | 10/10 |
| 16 | Limit Order Book Replay and Market Making Simulator | Institutional | 85–140 hours | 10/10 |
| 17 | Counterparty Exposure, Collateral, and CVA Engine | Institutional | 80–130 hours | 10/10 |
| 18 | Treasury Curve Relative Value and Key Rate Hedging | Institutional | 80–130 hours | 10/10 |
| 19 | Pension Asset–Liability Management and Liquidity Stress | Institutional | 70–120 hours | 9/10 |
| 20 | Backtest Overfitting and Model Validation Workbench | Institutional | 70–120 hours | 9/10 |

**Data access and Colab assumptions**

Use `numpy`, `pandas`, `scipy`, and `matplotlib` as the common stack. Each project's library field names this stack and the relevant additions. `plotly` and `ipywidgets` can add interactive charts and controls. [CVXPY](https://www.cvxpy.org/) supports the optimization projects; [QuantLib](https://www.quantlib.org/) supplies pricing and risk tools where specified.

Cache small datasets as CSV or Parquet, record retrieval dates and data definitions, and save notebook outputs outside the temporary runtime. Colab resources vary and its virtual machines have limited lifetimes, so the institutional examples use batches and checkpoints. Include installation and data loading cells so another person can rerun the notebook. [Google Colab FAQ](https://research.google.com/colaboratory/faq.html).

| Source | Appropriate use and access considerations |
|---|---|
| [Yahoo Finance through yfinance](https://github.com/ranaroussi/yfinance) | Convenient daily equity and ETF research inputs. The library is independent of Yahoo and describes the data interface as intended for personal use. Preserve adjustment settings and corporate actions; current ticker lists and current option chains do not supply a historical investment universe or historical option panels. |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Public company submissions and XBRL facts without an API key. Use filing and acceptance timestamps, accession numbers, and original filings to reconstruct information availability. The latest restated value must not silently replace what an investor knew earlier. |
| [SEC developer guidance](https://www.sec.gov/about/developer-resources) | Identify automated requests and cache downloads. The published fair access ceiling is 10 requests per second across a user's machines; a notebook should operate below it. |
| [FRED API](https://fred.stlouisfed.org/docs/api/fred/) and [ALFRED vintage parameters](https://fred.stlouisfed.org/docs/api/fred/series_observations.html) | Economic and interest rate series. API access uses a key. For historical decision rules, request the vintage available at the decision date and account for release timing. Series observation dates alone do not establish availability. |
| [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/stable/latest-financial-statements) | Optional normalized financial statements. An API key, appropriate subscription, and sufficient history are needed; coverage depends on the plan. Check financial units and filing metadata against original reports. |
| [Alpha Vantage documentation](https://www.alphavantage.co/documentation/) | Alternative market and fundamental inputs using an API key. Access depends on the endpoint; the documented daily adjusted series is a premium endpoint. Do not budget on the assumption that all adjusted history is free. |
| [Massive, formerly Polygon.io](https://massive.com/blog/polygon-is-now-massive/) | Stocks and options data subject to plan entitlements. Historical bid and ask data are relevant to execution and options research. The provider announced the name change in October 2025. Check current [options coverage](https://massive.com/docs/rest/options/overview) before choosing a dataset. |
| [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) | Downloadable factor and portfolio research returns. Match frequencies and units, and record the downloaded vintage and methodology. |
| [U.S. Treasury rate data](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve) | Public par curve nodes. They are constant maturity estimates rather than prices of specific traded bonds. Treasury explains the distinction from zero rates in its [rate FAQ](https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics/interest-rates-frequently-asked-questions). |
| [CME DataMine](https://www.cmegroup.com/datamine.html) | Licensed historical futures and options datasets, including settlements. Build returns using dated contracts, contract specifications, and explicit roll rules. |
| [LOBSTER samples](https://data.lobsterdata.com/info/DataSamples.php) | Small message and order book files for replay and microstructure exercises. Broad historical coverage requires separate access; a sample day cannot establish durable trading performance. |
| [UCI Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients) | A public credit classification dataset with 30,000 observations. It supports probability estimation and calibration exercises; it does not supply a modern, multi-cohort lending history or observed recovery data. |

---

**1. Project name:** 01 — Multiasset Portfolio Performance and Risk Dashboard

**2. Difficulty level:** Intermediate.

**3. What the project does:** Compares static, monthly rebalanced, and buy-and-hold portfolios across 6–10 ETFs using a consistent total return convention.

**4. Why it matters in real finance:** A return number is difficult to interpret without its benchmark, drawdowns, concentration, and rebalancing costs.

**5. Skills learned:** Market data cleaning, vectorized return calculations, portfolio accounting, benchmark comparison, and financial chart design.

**6. Datasets/APIs required:** Daily ETF prices and distributions from [Yahoo/yfinance](https://github.com/ranaroussi/yfinance); a risk-free series from [FRED](https://fred.stlouisfed.org/docs/api/fred/). Start with a fixed ETF universe and label the resulting selection limitation. Alpha Vantage is an optional alternative with suitable adjusted data access.

**7. Python libraries needed:** Common stack; `yfinance`, `requests`, and optionally `plotly`.

**8. Step-by-step implementation plan:** (1) Select assets, benchmark, dates, and adjustment convention. (2) Align trading dates and flag missing values without inventing prices before inception. (3) Track holdings, cash, dividends, and monthly rebalances, avoiding dividend double counting. (4) Calculate annualized return, volatility, Sharpe ratio, drawdown, turnover, and costs. (5) Reconcile a two-asset example by hand and export a portfolio report.

**9. Core quantitative concepts:** Compounding, diversification, covariance, excess returns, drawdown, turnover, and return attribution.

**10. Expected visualizations:** Wealth curves, underwater chart, rolling volatility, correlation heatmap, and portfolio weight history.

**11. How institutions use similar models:** Asset managers use comparable reporting to review mandates; wealth managers use it to explain allocation and benchmark outcomes.

**12. Resume value:** 6/10 for investment analytics; stronger with reconciled holdings and costs than with charts alone.

**13. Estimated development time:** 10–16 focused hours.

---

**1. Project name:** 02 — Factor Exposure and Return Attribution Lab

**2. Difficulty level:** Intermediate.

**3. What the project does:** Estimates a fund or ETF portfolio's exposure to market, size, value, profitability, investment, and momentum factors.

**4. Why it matters in real finance:** It helps distinguish returns associated with systematic exposures from returns unexplained by the chosen model.

**5. Skills learned:** Regression, statistical inference, rolling estimation, frequency alignment, and interpretation of model residuals.

**6. Datasets/APIs required:** Monthly factors and momentum from the [Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html), plus total returns for 3–5 ETFs from Yahoo/yfinance. Convert percentage factors to decimals and use a consistent risk-free rate.

**7. Python libraries needed:** Common stack; `statsmodels`, `yfinance`, and optionally `seaborn`.

**8. Step-by-step implementation plan:** (1) Download and document monthly return series. (2) Create excess returns and align factors. (3) Fit CAPM and multifactor models with autocorrelation and heteroskedasticity robust errors. (4) Estimate rolling exposures and contributions to fitted returns. (5) Compare model fit, residual behavior, confidence intervals, and stability across subperiods.

**9. Core quantitative concepts:** Alpha, beta, omitted variables, multicollinearity, statistical uncertainty, and factor risk. Estimated alpha is conditional on the model and sample.

**10. Expected visualizations:** Exposure bars with confidence intervals, rolling beta charts, fitted versus realized returns, and cumulative residual returns.

**11. How institutions use similar models:** Fund selectors assess manager style and asset managers monitor unintended factor concentrations.

**12. Resume value:** 7/10 for asset management or manager research roles.

**13. Estimated development time:** 14–22 focused hours.

---

**1. Project name:** 03 — Bond Pricing, Yield Curves, and Duration Lab

**2. Difficulty level:** Intermediate.

**3. What the project does:** Prices a small hypothetical bond portfolio and measures sensitivity to parallel shifts, steepening, and flattening of the yield curve.

**4. Why it matters in real finance:** Bond portfolios can have similar yields while carrying very different interest rate exposures.

**5. Skills learned:** Cash flow scheduling, discounting, numerical root finding, curve construction, and sensitivity analysis.

**6. Datasets/APIs required:** Public [Treasury par curve nodes](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve) or FRED Treasury series; synthetic bond terms. Build a pedagogical discount curve from stylized par instruments with stated interpolation and day count assumptions. Par yields are not zero rates or observed bond prices.

**7. Python libraries needed:** Common stack; `requests`, with `QuantLib` optional for schedules and independent pricing checks.

**8. Step-by-step implementation plan:** (1) Load curve nodes and choose conventions. (2) Build stylized par cash flows and bootstrap approximate discount factors. (3) Price hypothetical bonds and solve yields to maturity. (4) Compute duration, convexity, DV01, and key rate sensitivities. (5) Compare full repricing with duration approximations under small and large shocks.

**9. Core quantitative concepts:** Present value, par versus spot rates, yield to maturity, duration, convexity, and key rate risk.

**10. Expected visualizations:** Par and zero curves, price–yield curves, sensitivity ladders, and scenario profit and loss bars.

**11. How institutions use similar models:** Fixed income managers hedge rate exposure; bank treasury teams measure the sensitivity of securities holdings.

**12. Resume value:** 7/10 for fixed income analytics and treasury roles.

**13. Estimated development time:** 16–26 focused hours.

---

**1. Project name:** 04 — SEC Financial Statement Quality and Valuation Screener

**2. Difficulty level:** Intermediate.

**3. What the project does:** Builds a traceable financial history and quality screen for 15–30 nonfinancial companies, with a transparent discounted cash flow sensitivity model.

**4. Why it matters in real finance:** Valuation depends on accounting definitions, cash conversion, and assumptions about future profitability.

**5. Skills learned:** API ingestion, XBRL normalization, accounting reconciliation, financial ratio design, and valuation sensitivity analysis.

**6. Datasets/APIs required:** [SEC submissions and company facts](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), original filing references, and Yahoo prices. [Financial Modeling Prep](https://site.financialmodelingprep.com/developer/docs/stable/latest-financial-statements) is an optional normalized input. Store accession, filing time, units, and fiscal period; reconcile cash flow periods and restatements.

**7. Python libraries needed:** Common stack; `requests`, `beautifulsoup4` when inspecting filing text, `yfinance`, and optionally `plotly`.

**8. Step-by-step implementation plan:** (1) Map tickers to SEC identifiers. (2) Collect and normalize annual and quarterly facts without mixing durations or units. (3) Reconcile a sample against original filings. (4) Calculate margins, leverage, cash conversion, accruals, and comparable valuation ratios. (5) Build a cash flow valuation with explicit operating assumptions, discount rates, and terminal growth sensitivities.

**9. Core quantitative concepts:** Free cash flow, accruals, return on invested capital, enterprise value, discounting, and terminal value.

**10. Expected visualizations:** Quality score heatmap, margin and cash flow trends, peer scatterplots, and valuation sensitivity grid.

**11. How institutions use similar models:** Fundamental hedge funds and equity analysts screen businesses, investigate accounting changes, and compare valuation assumptions.

**12. Resume value:** 7/10 for equity research; provenance and accounting accuracy provide the main differentiation.

**13. Estimated development time:** 20–32 focused hours.

---

**1. Project name:** 05 — Monte Carlo Wealth and Retirement Simulator

**2. Difficulty level:** Intermediate.

**3. What the project does:** Simulates inflation adjusted wealth under contributions, withdrawals, fees, and alternative asset allocations.

**4. Why it matters in real finance:** Average returns alone do not describe the chance of exhausting capital or missing a spending goal.

**5. Skills learned:** Stochastic simulation, bootstrap resampling, cash flow modeling, scenario design, and uncertainty communication.

**6. Datasets/APIs required:** Historical stock and bond ETF returns from Yahoo; inflation from [FRED](https://fred.stlouisfed.org/docs/api/fred/); synthetic contributions and spending assumptions. The model can also run entirely from explicit hypothetical return assumptions.

**7. Python libraries needed:** Common stack; `yfinance`, `requests`, and `ipywidgets` for sliders.

**8. Step-by-step implementation plan:** (1) Define horizon, starting wealth, inflation, and cash flows. (2) Compare a parametric return model with a block bootstrap. (3) Simulate roughly 10,000 paths in batches. (4) Track shortfall, depletion time, and terminal purchasing power for several allocations. (5) Stress early losses, higher inflation, fees, and lower expected returns, and verify a zero-return cash flow example.

**9. Core quantitative concepts:** Sequence of returns risk, real versus nominal wealth, simulation error, path dependence, and shortfall probability.

**10. Expected visualizations:** Wealth fan chart, terminal wealth histogram, depletion probabilities, and allocation–spending sensitivity map.

**11. How institutions use similar models:** Wealth managers and retirement product teams assess the sensitivity of funding plans to assumptions and spending policies.

**12. Resume value:** 6/10 for wealth analytics; stronger when model risk is clearly quantified.

**13. Estimated development time:** 14–24 focused hours.

---

**1. Project name:** 06 — Macro Regime Detection and Tactical Allocation

**2. Difficulty level:** Advanced.

**3. What the project does:** Estimates economic or market regimes and evaluates whether regime probabilities improve a small ETF allocation rule.

**4. Why it matters in real finance:** Correlations and asset risks can change across growth, inflation, and financial stress environments.

**5. Skills learned:** Vintage data handling, feature scaling, hidden state estimation, recursive forecasting, and strategy evaluation.

**6. Datasets/APIs required:** Growth, inflation, policy, and labor series from [FRED/ALFRED](https://fred.stlouisfed.org/docs/api/fred/series_observations.html); daily or monthly ETF returns from Yahoo. Align each release to when it became available; use a current revised series only for a separately labeled retrospective comparison.

**7. Python libraries needed:** Common stack; `scikit-learn`, `statsmodels`, optionally `hmmlearn`, plus `requests` and `yfinance`.

**8. Step-by-step implementation plan:** (1) Construct a small vintage-aware monthly feature set. (2) Fit a transparent rule or clustering baseline. (3) Refit a regime model on expanding training windows and use filtered probabilities at each decision date. (4) Map probabilities to capped allocations with delayed execution and costs. (5) Compare against static allocation and test sensitivity to regime count and fitting period.

**9. Core quantitative concepts:** Latent regimes, nonstationarity, filtering versus smoothing, revision bias, and estimation uncertainty. Full-sample smoothed states are unsuitable for historical trading decisions.

**10. Expected visualizations:** Regime probability timeline, macro feature map, transition matrix, allocation history, and relative wealth.

**11. How institutions use similar models:** Macro funds and asset allocators use regime analysis to organize scenarios and adjust portfolio risk.

**12. Resume value:** 8/10 for macro research and allocation roles.

**13. Estimated development time:** 30–50 focused hours.

---

**1. Project name:** 07 — Earnings and SEC Filing Event Study

**2. Difficulty level:** Advanced.

**3. What the project does:** Measures abnormal returns around a clearly defined event, such as an earnings announcement or a specific category of Form 8-K filing.

**4. Why it matters in real finance:** Researchers need to determine how prices incorporate new information and whether an apparent pattern survives timing and selection checks.

**5. Skills learned:** Event collection, timestamp alignment, abnormal return estimation, clustered inference, and reproducible sampling.

**6. Datasets/APIs required:** [SEC submission metadata and filings](https://www.sec.gov/search-filings/edgar-application-programming-interfaces), benchmark and stock returns from Yahoo, and optionally FMP or Alpha Vantage earnings records with suitable access. A filing acceptance time is not necessarily the first public earnings release time; choose and document one event definition.

**7. Python libraries needed:** Common stack; `requests`, `statsmodels`, `yfinance`, and `beautifulsoup4` if parsing filings.

**8. Step-by-step implementation plan:** (1) Predefine event categories and a bounded issuer sample. (2) Map events to tradable sessions using actual availability and after-hours rules. (3) Estimate expected returns in a separate pre-event window. (4) Compute abnormal and cumulative abnormal returns, accounting for overlapping events and shared dates. (5) Bootstrap or cluster uncertainty and report robustness to window choices and confounding announcements.

**9. Core quantitative concepts:** Market model, abnormal returns, event windows, information arrival, cross-sectional dependence, and selection bias.

**10. Expected visualizations:** Average cumulative abnormal return with confidence bands, event return distributions, and grouped event comparisons.

**11. How institutions use similar models:** Event-driven funds investigate catalysts, while equity research teams study how markets respond to disclosures.

**12. Resume value:** 8/10 for event research and empirical finance roles.

**13. Estimated development time:** 35–55 focused hours.

---

**1. Project name:** 08 — Cointegration Pairs Trading Research Engine

**2. Difficulty level:** Advanced.

**3. What the project does:** Selects candidate pairs using training data and evaluates a spread trading rule on subsequent periods with explicit costs and position accounting.

**4. Why it matters in real finance:** A stationary historical spread can fail when business relationships, funding conditions, or market structure change.

**5. Skills learned:** Time series testing, hedge ratio estimation, signal design, walk-forward evaluation, and trading bookkeeping.

**6. Datasets/APIs required:** Daily prices and corporate actions from Yahoo or appropriately licensed Alpha Vantage/Massive history. Use a small predeclared ETF or stock universe; add borrow and financing assumptions explicitly. A current surviving universe limits the scope of conclusions.

**7. Python libraries needed:** Common stack; `statsmodels`, `scikit-learn`, and `yfinance` or `requests`.

**8. Step-by-step implementation plan:** (1) Define economically plausible candidate groups and chronological splits. (2) Estimate cointegration and hedge ratios using training windows only. (3) Set entry, exit, sizing, and breakdown rules before evaluation. (4) Apply lagged signals to holdings and cash, including spread, borrow, financing, and turnover. (5) Evaluate untouched periods and sensitivity to pair selection, thresholds, and relationship breaks.

**9. Core quantitative concepts:** Cointegration versus correlation, stationarity, mean reversion, half-life, multiple testing, and short sale risk. A log-price hedge coefficient must be translated into implementable holdings.

**10. Expected visualizations:** Spread and entry bands, rolling hedge ratios, position history, net profit and loss, and trade duration distributions.

**11. How institutions use similar models:** Statistical arbitrage teams research relative pricing relationships and manage the risk of structural breaks.

**12. Resume value:** 8/10 for systematic trading research when results include failed pairs and costs.

**13. Estimated development time:** 35–55 focused hours.

---

**1. Project name:** 09 — Black–Litterman and Robust Portfolio Optimization

**2. Difficulty level:** Advanced.

**3. What the project does:** Compares equal weight, minimum variance, conventional mean–variance, and Black–Litterman allocations under realistic constraints.

**4. Why it matters in real finance:** Small changes in estimated returns and covariances can cause large and costly changes in portfolio weights.

**5. Skills learned:** Convex optimization, covariance regularization, Bayesian allocation, constraint design, and optimizer diagnostics.

**6. Datasets/APIs required:** Returns for 8–15 ETFs from Yahoo; FRED cash rates; a declared policy benchmark. If reliable market capitalization weights are unavailable, call the prior a policy benchmark prior rather than a market equilibrium estimate.

**7. Python libraries needed:** Common stack; `cvxpy`, `scikit-learn`, `yfinance`, and `requests`.

**8. Step-by-step implementation plan:** (1) Define benchmark weights, bounds, and evaluation dates. (2) Estimate rolling expected returns and shrinkage covariance using available history. (3) Specify views and uncertainty before each evaluation window. (4) Optimize with concentration, turnover, and cost constraints. (5) Compare subsequent risk, turnover, constraint satisfaction, and sensitivity to inputs against simple baselines.

**9. Core quantitative concepts:** Efficient frontier, covariance shrinkage, posterior expectations, view uncertainty, regularization, and robust allocation.

**10. Expected visualizations:** Allocation comparisons, frontier curves, input sensitivity maps, turnover history, and realized risk contributions.

**11. How institutions use similar models:** Multiasset managers combine strategic allocations, investment views, and mandate constraints when setting portfolio weights.

**12. Resume value:** 8/10 for portfolio construction and quantitative allocation roles.

**13. Estimated development time:** 30–50 focused hours.

---

**1. Project name:** 10 — Value at Risk, Expected Shortfall, and Stress Testing

**2. Difficulty level:** Advanced.

**3. What the project does:** Estimates the loss distribution of a small multiasset book using historical, parametric, and volatility-filtered simulations, then evaluates forecast performance.

**4. Why it matters in real finance:** Risk estimates influence limits and capital decisions, and their reliability changes when volatility and correlations shift.

**5. Skills learned:** Distribution modeling, volatility estimation, risk forecast validation, scenario design, and risk reporting.

**6. Datasets/APIs required:** Daily ETF returns from Yahoo and optionally macro or rate series from FRED. Use 5–10 positions and a clearly defined loss sign convention. A derivatives extension requires instrument terms and full repricing inputs.

**7. Python libraries needed:** Common stack; `statsmodels`, `yfinance`, `requests`, and optionally `arch`.

**8. Step-by-step implementation plan:** (1) Reconstruct portfolio returns and define the risk horizon. (2) Fit rolling historical, normal, and filtered simulation forecasts using past information. (3) Calculate one-day VaR and expected shortfall at declared confidence levels. (4) Compare later losses with forecasts, checking exception frequency, clustering, and tail severity. (5) Add historical and hypothetical stresses, including correlation breaks, and report uncertainty at extreme quantiles.

**9. Core quantitative concepts:** Tail quantiles, expected shortfall, volatility clustering, heavy tails, exception tests, and scenario risk. VaR exception counts alone do not validate expected shortfall.

**10. Expected visualizations:** Loss distribution with tail markers, VaR exception timeline, tail loss comparison, and stress loss waterfall.

**11. How institutions use similar models:** Bank market risk teams and asset manager risk teams use related forecasts and stresses to monitor exposures and challenge limits.

**12. Resume value:** 9/10 for market risk and quantitative risk roles.

**13. Estimated development time:** 35–55 focused hours.

---

**1. Project name:** 11 — Options Volatility Surface and Delta Hedging Lab

**2. Difficulty level:** Advanced.

**3. What the project does:** Cleans option quotes, infers implied volatility, fits a small surface, and studies hedging error for a simple option position.

**4. Why it matters in real finance:** Option prices depend on strike, maturity, exercise style, and the evolution of hedging costs and volatility.

**5. Skills learned:** Numerical pricing, root finding, quote filtering, interpolation, Greeks, and self-financing hedge accounting.

**6. Datasets/APIs required:** For the historical version, dated bid/ask option quotes, underlying prices, rates, dividends, and contract terms from a suitably entitled [Massive options dataset](https://massive.com/docs/rest/options/overview) or another licensed source. The inexpensive version uses synthetic European options with a known surface. A current Yahoo chain supports a snapshot exercise, not a historical hedging backtest.

**7. Python libraries needed:** Common stack; `QuantLib`, `requests`, and optionally `plotly`.

**8. Step-by-step implementation plan:** (1) Select a consistent European-style dataset or an American pricing model matching the contracts. (2) Filter stale, crossed, illiquid, and inconsistent quotes. (3) Invert prices to volatility and fit a surface with static arbitrage diagnostics. (4) Rebalance delta hedges with documented cash interest, dividends, spreads, and exercise handling. (5) Compare hedging frequency, model assumptions, and volatility scenarios using full profit and loss reconciliation.

**9. Core quantitative concepts:** Risk-neutral valuation, implied volatility, smile and term structure, delta, gamma, vega, static arbitrage, and discrete hedging error.

**10. Expected visualizations:** Smile curves, volatility surface, pricing residuals, Greek profiles, and hedging error distributions.

**11. How institutions use similar models:** Derivatives desks mark option books and manage volatility and hedge exposures using related methods.

**12. Resume value:** 9/10 for derivatives quant research; contract conventions and accounting matter more than a smooth surface chart.

**13. Estimated development time:** 45–75 focused hours for one underlying and a bounded set of maturities.

---

**1. Project name:** 12 — Credit Default Probability and Expected Loss Model

**2. Difficulty level:** Advanced.

**3. What the project does:** Estimates calibrated default probabilities and converts them into illustrative portfolio expected losses under declared exposure and recovery assumptions.

**4. Why it matters in real finance:** A useful credit model needs reliable probabilities, since the cost of lending errors depends on exposure and loss severity.

**5. Skills learned:** Classification, calibration, imbalanced data evaluation, interpretable modeling, and credit loss scenario analysis.

**6. Datasets/APIs required:** [UCI Default of Credit Card Clients](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients). Exposure at default and loss given default are scenario inputs, since this dataset does not establish realized recoveries or complete future exposures. A later extension needs dated loan cohorts and repayment histories.

**7. Python libraries needed:** Common stack; `scikit-learn`, `openpyxl` or `xlrd` as needed for the downloaded format, and optionally `shap`.

**8. Step-by-step implementation plan:** (1) Define the prediction target, permitted predictors, and exclusions such as the record identifier. (2) Create separate stratified train, calibration, and test partitions, keeping all preprocessing inside training. (3) Compare logistic regression with a small tree model. (4) Evaluate Brier score, log loss, calibration, ROC-AUC, precision–recall, and segment stability. (5) Apply explicit PD × LGD × EAD scenarios and document the dataset's single-period validation limit.

**9. Core quantitative concepts:** Probability of default, exposure at default, loss given default, expected loss, calibration, discrimination, and threshold economics.

**10. Expected visualizations:** Calibration curve, precision–recall curve, score distribution, segment loss heatmap, and loss sensitivity chart.

**11. How institutions use similar models:** Banks and credit portfolio teams use related probability and loss models for underwriting and monitoring, with substantially richer data and validation.

**12. Resume value:** 8/10 for credit analytics and risk data science roles.

**13. Estimated development time:** 35–60 focused hours.

---

**1. Project name:** 13 — Machine Learning Equity Ranking with Temporal Validation

**2. Difficulty level:** Advanced.

**3. What the project does:** Ranks equities by forecast relative returns and evaluates whether the ranking adds value after turnover and trading costs.

**4. Why it matters in real finance:** A predictive model becomes useful only when its information timing, implementation costs, and portfolio behavior hold up on unseen periods.

**5. Skills learned:** Panel data engineering, chronological model selection, feature pipelines, ranking metrics, and portfolio construction.

**6. Datasets/APIs required:** Price, volume, corporate actions, and dated universe membership; SEC fundamentals joined by actual filing availability if used. A 50–100-stock Yahoo/SEC pilot is feasible, but an institutionally credible broad-equity result also needs delisted securities and historical membership from a licensed source. Do not describe a surviving-stock pilot as an unbiased market backtest.

**7. Python libraries needed:** Common stack; `scikit-learn`, `requests`, `yfinance`, `pyarrow`, optionally `xgboost` and `shap`.

**8. Step-by-step implementation plan:** (1) Construct monthly dated features and future return labels with explicit availability. (2) Split by dates, removing training examples whose label intervals overlap validation periods and applying gaps where needed. (3) Tune a linear baseline and a small tree model inside training folds only. (4) Form capped long-only ranking portfolios with lagged execution and costs. (5) Evaluate rank correlation, turnover, benchmark-relative returns, exposure drift, and a frozen final holdout.

**9. Core quantitative concepts:** Information coefficient, label overlap, data leakage, cross-sectional ranking, regularization, factor exposure, and net alpha.

**10. Expected visualizations:** Rank correlation over time, quantile returns, feature stability, turnover versus costs, and net relative wealth.

**11. How institutions use similar models:** Systematic equity managers combine predictive rankings with risk and trading constraints to construct portfolios.

**12. Resume value:** 9/10 for systematic equity research if data availability and evaluation are defensible.

**13. Estimated development time:** 50–85 focused hours for the bounded pilot; full universe acquisition and cleaning add substantial work.

---

**1. Project name:** 14 — Futures Trend Following with Volatility Targeting

**2. Difficulty level:** Advanced.

**3. What the project does:** Builds a small trend portfolio across equity index, rates, currency, and commodity futures while targeting risk and explicitly modeling contract rolls.

**4. Why it matters in real finance:** Futures performance depends on contract multipliers, rolls, margin, cash management, and changing volatility as well as signal direction.

**5. Skills learned:** Contract data handling, risk scaling, notional sizing, roll accounting, and portfolio profit and loss reconciliation.

**6. Datasets/APIs required:** Dated contract settlements, expiry calendars, and specifications from [CME DataMine](https://www.cmegroup.com/datamine.html) or another licensed source; cash rates from FRED. An ETF version using Yahoo is a lower-cost preliminary exercise, with no claim to reproduce futures roll or margin behavior.

**7. Python libraries needed:** Common stack; `requests`, `pyarrow`, optionally `numba`; `yfinance` for the ETF preliminary version.

**8. Step-by-step implementation plan:** (1) Select 8–12 contracts and predefine roll rules. (2) Build signal histories while calculating realized profit and loss from actual held contracts. (3) Estimate volatility using past data and size contracts within leverage and liquidity caps. (4) Apply trend rules, roll costs, commissions, collateral interest, and margin cash flows. (5) Compare risk targets, lookbacks, crisis periods, and net performance against simpler exposures.

**9. Core quantitative concepts:** Time series momentum, volatility targeting, notional exposure, futures carry and rolls, leverage, and collateral return. Back-adjusted price changes are not automatically investable portfolio returns.

**10. Expected visualizations:** Asset signals, contract positions, risk contributions, roll calendar, drawdowns, and margin utilization.

**11. How institutions use similar models:** Managed futures funds and systematic macro teams use related signals with portfolio risk scaling and contract execution rules.

**12. Resume value:** 9/10 for systematic macro and managed futures research.

**13. Estimated development time:** 50–85 focused hours with prepared contract data.

---

**1. Project name:** 15 — Execution Algorithms and Transaction Cost Analysis

**2. Difficulty level:** Institutional.

**3. What the project does:** Simulates parent order execution with TWAP, volume-based schedules, and a simple risk–impact tradeoff, then reports transaction costs against several benchmarks.

**4. Why it matters in real finance:** Implementation costs can consume forecast returns, especially when orders are large relative to available liquidity.

**5. Skills learned:** Intraday data alignment, execution simulation, cost decomposition, benchmark design, and model calibration.

**6. Datasets/APIs required:** Timestamped trades and top-of-book quotes from an appropriately entitled Massive dataset; synthetic parent orders. A bar-data version can demonstrate scheduling, but it needs assumed spreads and impact and cannot identify actual execution quality. Real desk order logs would be needed for empirical transaction cost analysis.

**7. Python libraries needed:** Common stack; `cvxpy`, `requests`, `pyarrow`, and optionally `numba`.

**8. Step-by-step implementation plan:** (1) Define parent orders, decision times, and cost sign conventions. (2) Estimate volume profiles from earlier days and specify participation limits. (3) Simulate TWAP, participation schedules, and an impact-aware optimization with explicit fills and fees. (4) Calculate arrival-price shortfall, VWAP comparison, delay cost, and unfilled-order opportunity cost. (5) Stress spreads, volume, volatility, and impact assumptions on held-out days.

**9. Core quantitative concepts:** Implementation shortfall, spread cost, market impact, execution risk, participation rate, and benchmark dependence. Historical replay alone does not reveal the counterfactual impact of a new large order.

**10. Expected visualizations:** Execution schedule over volume, cumulative fills, cost decomposition, shortfall distribution, and cost–risk frontier.

**11. How institutions use similar models:** Asset manager trading desks evaluate broker execution and order schedules; banks and prop firms research execution policies.

**12. Resume value:** 10/10 for execution research when the simulator's assumptions are explicit and tested for sensitivity.

**13. Estimated development time:** 70–110 focused hours for one asset class and a small intraday dataset.

---

**1. Project name:** 16 — Limit Order Book Replay and Market Making Simulator

**2. Difficulty level:** Institutional.

**3. What the project does:** Replays exchange events and compares simple passive quoting policies under inventory, latency, fee, and conservative fill assumptions.

**4. Why it matters in real finance:** Earning the quoted spread depends on queue position and adverse selection; attractive displayed prices do not guarantee profitable fills.

**5. Skills learned:** Event processing, state machines, order lifecycle accounting, market microstructure features, and simulation diagnostics.

**6. Datasets/APIs required:** [LOBSTER message and order book samples](https://data.lobsterdata.com/info/DataSamples.php) and its [output specification](https://php.lobsterdata.com/info/DataStructure.php). Begin with one stock and one session; use additional licensed days for meaningful evaluation. These are venue-specific data rather than a complete consolidated market.

**7. Python libraries needed:** Common stack; `numba`, `pyarrow`, and optionally `plotly`.

**8. Step-by-step implementation plan:** (1) Parse event types, price scaling, and timestamps and reconcile replay to supplied book states. (2) Build a hypothetical order manager with queue-ahead, cancel latency, and partial-fill rules. (3) Compare fixed-spread quoting with inventory-skewed quotes. (4) Track cash, inventory, fees, marked profit and loss, and post-fill price moves. (5) Re-evaluate with pessimistic queue and latency assumptions and separate development days from evaluation days where available.

**9. Core quantitative concepts:** Queue priority, order flow imbalance, adverse selection, spread capture, inventory risk, and latency. Hypothetical queue placement and reaction to new orders remain model assumptions.

**10. Expected visualizations:** Book depth heatmap, imbalance and midprice, fill markouts, inventory path, and spread versus inventory profit and loss.

**11. How institutions use similar models:** Electronic market makers and prop firms study passive execution and inventory policies through much larger replay and simulation systems.

**12. Resume value:** 10/10 for market microstructure and quantitative development roles.

**13. Estimated development time:** 85–140 focused hours for a bounded replay prototype.

---

**1. Project name:** 17 — Counterparty Exposure, Collateral, and CVA Engine

**2. Difficulty level:** Institutional.

**3. What the project does:** Simulates a small interest rate swap portfolio, aggregates trades by netting set, models collateral, and estimates unilateral credit valuation adjustment.

**4. Why it matters in real finance:** Exposure depends on future market values and contractual netting and collateral terms, rather than current notional alone.

**5. Skills learned:** Risk-neutral simulation, curve-based pricing, netting set logic, collateral cash flows, numerical integration, and convergence analysis.

**6. Datasets/APIs required:** Synthetic swap trades, collateral agreements, internally consistent discount/projection curves, model volatility parameters, and a declared default probability term structure. FRED SOFR history can provide context but cannot replace a full market calibration. A calibrated version requires licensed OIS, forward rate, swaption, and credit inputs.

**7. Python libraries needed:** Common stack; `QuantLib`, `numba`, and `pyarrow` for checkpoints.

**8. Step-by-step implementation plan:** (1) Construct and independently check a 10–20-trade swap book. (2) Simulate a small rate model under risk-neutral valuation assumptions and reprice trades on future dates. (3) Apply netting and collateral with thresholds, transfer amounts, and timing. (4) Compute expected exposure, potential future exposure, and discounted expected loss increments for unilateral CVA. (5) Check zero-risk cases, netting behavior, path convergence, and sensitivities to recovery, collateral lag, and market/default dependence.

**9. Core quantitative concepts:** Expected exposure, PFE, netting, collateral, risk-neutral versus physical measures, survival probabilities, recovery, and wrong-way risk. Label the base case's independence assumption and the exclusion of bilateral or funding adjustments.

**10. Expected visualizations:** Exposure profiles, collateral paths, netted versus gross exposure, CVA contribution by trade, and convergence plots.

**11. How institutions use similar models:** Bank counterparty risk and derivatives valuation teams use exposure simulation and collateral modeling; a related framework is described in the [Open Source Risk Engine overview](https://www.quantlib.org/slides/qlum16d/caspers.pdf).

**12. Resume value:** 10/10 for derivatives risk, counterparty risk, and pricing quant roles.

**13. Estimated development time:** 80–130 focused hours for the synthetic single-currency prototype.

---

**1. Project name:** 18 — Treasury Curve Relative Value and Key Rate Hedging

**2. Difficulty level:** Institutional.

**3. What the project does:** Decomposes yield curve moves into factors, studies curve deviations, and constructs a hedged hypothetical bond basket.

**4. Why it matters in real finance:** A position intended to express relative value may carry unintended exposure to the overall rate level, slope, or curvature.

**5. Skills learned:** Curve fitting, principal components, cash flow pricing, hedge optimization, and financing-aware scenario analysis.

**6. Datasets/APIs required:** Historical Treasury par nodes or FRED Treasury yields, plus synthetic bond cash flows for the educational version. A tradable security-level study additionally needs dated bond prices, identifiers, coupon schedules, bid/ask spreads, repo funding, and short availability. Constant maturity yields alone do not supply that evidence.

**7. Python libraries needed:** Common stack; `scikit-learn`, `QuantLib`, `cvxpy`, and `requests`.

**8. Step-by-step implementation plan:** (1) Fit consistent curves and inspect missing or stale nodes. (2) Estimate principal components on training-window yield changes. (3) Define a curve deviation signal using only information available at each date. (4) Construct a stylized basket with constrained key rate or factor exposures and explicit financing assumptions. (5) Fully reprice carry, roll-down, and rate shocks, and separate model illustration from executable market evidence.

**9. Core quantitative concepts:** Level, slope, curvature, key rate duration, factor neutrality, carry, roll-down, curve residuals, and basis risk.

**10. Expected visualizations:** Curve factor loadings, residual heatmap, key rate hedge ladder, carry decomposition, and scenario profit and loss.

**11. How institutions use similar models:** Fixed income relative value funds and rates desks isolate curve views while limiting broad interest rate exposure.

**12. Resume value:** 10/10 for rates research and fixed income portfolio construction when trade assumptions are defensible.

**13. Estimated development time:** 80–130 focused hours for the stylized basket; security-level data integration is additional.

---

**1. Project name:** 19 — Pension Asset–Liability Management and Liquidity Stress

**2. Difficulty level:** Institutional.

**3. What the project does:** Chooses an asset allocation and rate hedge against a schedule of future benefit payments while evaluating funding shortfall and near-term cash needs.

**4. Why it matters in real finance:** Strong asset returns can coincide with a worsening funded position when liabilities rise faster, and illiquid assets may not meet urgent payments.

**5. Skills learned:** Liability cash flow valuation, joint scenario generation, constrained allocation, liquidity modeling, and policy comparison.

**6. Datasets/APIs required:** Synthetic benefit payment schedule and asset holdings; FRED inflation and rate history; Yahoo ETF returns for liquid asset proxies. State the liability discount basis and synthetic mortality or inflation assumptions. Actual plan actuarial data and applicable liability valuation rules are separate inputs for a real mandate.

**7. Python libraries needed:** Common stack; `cvxpy`, `QuantLib` where useful, `yfinance`, and `requests`.

**8. Step-by-step implementation plan:** (1) Build a synthetic liability schedule and calculate its present value and rate sensitivity. (2) Generate joint asset, inflation, and interest rate scenarios with explicit assumptions. (3) Compare return-seeking, liability-hedging, and blended allocations. (4) Add contribution, payout, liquidity, and hypothetical collateral-call constraints to a bounded optimization. (5) Report funded ratio distributions, cash shortfalls, hedge costs, and sensitivity to the discount basis and correlation shifts.

**9. Core quantitative concepts:** Funding ratio, surplus risk, asset–liability duration mismatch, inflation linkage, conditional value at risk, and liquidity buffers.

**10. Expected visualizations:** Liability cash flow ladder, funding ratio fan chart, surplus risk frontier, liquidity waterfall, and allocation stress matrix.

**11. How institutions use similar models:** Pension managers, insurers, and liability-driven investment teams use related frameworks to coordinate investments with future obligations.

**12. Resume value:** 9/10 for pension, insurance, and institutional allocation roles.

**13. Estimated development time:** 70–120 focused hours for a synthetic plan with a small liquid asset universe.

---

**1. Project name:** 20 — Backtest Overfitting and Model Validation Workbench

**2. Difficulty level:** Institutional.

**3. What the project does:** Demonstrates how strategy search can create impressive backtests from noise, then applies reproducible research selection and validation procedures.

**4. Why it matters in real finance:** Capital allocation based on a selected historical winner can confuse repeated experimentation with reliable predictive evidence.

**5. Skills learned:** Experimental design, null simulation, multiple-testing adjustment, temporal validation, model documentation, and independent review.

**6. Datasets/APIs required:** Synthetic returns with known null or weak-signal properties; optional ETF and factor returns from Yahoo and the Kenneth French Data Library; a complete ledger of tested strategy variants. Simulated data allow the false discovery rate to be measured against known truth.

**7. Python libraries needed:** Common stack; `statsmodels`, `scikit-learn`, `joblib`, and `pyarrow`.

**8. Step-by-step implementation plan:** (1) Define a controlled family of roughly 100–300 strategy variants and record every trial. (2) Measure how the best training Sharpe rises under a no-signal simulation. (3) Compare selection using a single split, nested chronological validation, and a frozen final holdout. (4) Use block bootstrap uncertainty and multiplicity-aware significance checks matched to the selection process. (5) Export a model review report covering data provenance, trial history, sensitivity, net costs, and acceptance criteria fixed before final evaluation.

**9. Core quantitative concepts:** Selection bias, multiple hypotheses, dependent returns, effective sample size, confidence intervals, estimation error, and research reproducibility. Reusing the final holdout turns it into another development set.

**10. Expected visualizations:** Best Sharpe versus trial count, training versus holdout scatter, false discovery distributions, performance decay, and robustness heatmaps.

**11. How institutions use similar models:** Quant research leads, model validation teams, and investment committees use related evidence to challenge strategy claims and decide whether further testing or capital is justified.

**12. Resume value:** 9/10 for research engineering, independent validation, and senior research support roles.

**13. Estimated development time:** 70–120 focused hours for the synthetic experiment and one bounded real-data illustration.

---

**Choosing a first project**

For a broad foundation, start with Project 01 and then build Project 09 or 10. For quantitative trading research, choose Project 08 or 13 and apply the validation discipline from Project 20. For derivatives roles, start with Project 03, continue with Project 11, and then attempt Project 17. For market microstructure roles, build Project 15 before Project 16.

A strong final submission should include a notebook that runs from a fresh runtime, dated input definitions, a simple benchmark or analytical check, honest uncertainty estimates, and a short explanation of what the results establish. A negative research result can still be a strong project when its design and conclusions are sound.
