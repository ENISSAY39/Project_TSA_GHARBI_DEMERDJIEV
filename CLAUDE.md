# CLAUDE.md — Time Series Analysis (TSA) Project

## Context
Academic project (EPF Montpellier, Data & AI). Goal: forecast a univariate time series **and interpret every step**, both technically and in business terms. Deliverable: a structured report, written as a Jupyter notebook.

**Before starting any task, read the files in `Contexte/`** (assignment brief, course material). They define the requirements; if they conflict with this file, `Contexte/` wins — flag the conflict.

## Dataset
- File: `MRTSSM451USN.csv` (project root — do not move or modify it). Checked against the FRED download on 2026-10-01: identical.
- Series: **Retail Sales: Sporting Goods, Hobby, Musical Instrument, and Book Stores (US)** — millions of dollars, **not seasonally adjusted**
- Source: U.S. Census Bureau, retrieved from FRED: https://fred.stlouisfed.org/series/MRTSSM451USN
- Download (no API key needed): https://fred.stlouisfed.org/graph/fredgraph.csv?id=MRTSSM451USN
- Frequency: **monthly**, 1992-01 → 2026-07 (415 observations, no missing values)
- CSV columns: `observation_date`, `MRTSSM451USN` → parse dates, set a monthly DatetimeIndex (`freq="MS"`).
- Report citation: "U.S. Census Bureau, Retail Sales: Sporting Goods, Hobby, Musical Instrument, and Book Stores [MRTSSM451USN], retrieved from FRED, Federal Reserve Bank of St. Louis."

### Implications for the methods
- **Strong yearly seasonality (period = 12)**: December is the yearly maximum in all 34 complete years (1992–2025), with a secondary bump in August.
- **The trend is not a steady rise**: annual sales grow until 2007, dip in 2008–09, plateau until 2016, decline in 2017–19, then step up by about 23% in 2021 and stay flat since.
- **Additive vs multiplicative**: do not assume multiplicative. December's share of annual sales fell from about 16.5% (1992–2000) to about 12% (2021–2025), so the seasonal amplitude has not grown in proportion to the level. The EDA (Section 2.4) shows a 12-month rolling standard deviation that stays around 1,200–1,600 while the rolling mean is multiplied by 2.6: **Decided in Section 4: additive.** Buys-Ballot test on the training set: β = 0.0043, p = 0.857; the additive decomposition leaves a smaller residual (RMSE 328 vs 441).
- **ETS**: seasonal decomposition (`seasonal_decompose`, period=12) + ETS model with seasonal term (Holt-Winters). **Model retained in Section 4: ETS(M,A,A)** (lowest AIC and BIC of nine candidates), fitted with `ETSModel(..., initialization_method="heuristic")` because estimating the initial states made the optimiser fail on the additive models. Its prediction interval is simulated: pass `rng=np.random.default_rng(SEED)` to `get_prediction` to keep it reproducible. Its slope is constant (β = 0), so the 24-month forecast depends on a drift that is the 32-year average: Section 7 must include a rolling-origin evaluation inside the training set.
- **SARIMA** (not plain ARIMA): seasonal differencing (D) and seasonal orders (P,D,Q,12). Section 3 established **d = 1, D = 1** on the training set, in original units (no log): with D = 1 alone the ADF/KPSS verdict depends on whether the 2020–21 shock is included.
- **Prophet**: yearly seasonality on (weekly/daily off), `seasonality_mode` additive vs multiplicative.
- **Test horizon**: last 24 months (`TEST_HORIZON = 24`, set in Section 2.5): train = 1992-01 → 2024-07 (391 months), test = 2024-08 → 2026-07 (two Decembers). Seasonal naive baseline is mandatory.
- **Structural events** (verify before citing): 2008–09 recession, COVID-19 shock in 2020 (April 2020 = 3,264 vs 5,887 in April 2019), level shift in 2021, post-COVID inflation. Link anomalies and changepoints to these events.

### Business context
Retail planning for sporting goods, hobby, musical instrument and book retailers and their suppliers: inventory and supply-chain planning ahead of the December peak, seasonal staffing, cash-flow forecasting, sector monitoring (lenders, commercial landlords, sales-tax receipts for public authorities). Every interpretation should connect to at least one of these.

## Required methods
1. ETS decomposition + ETS / Holt-Winters forecast
2. SARIMA
3. Prophet (`prophet` package)
4. Methodological comparison of the forecasts

## Golden rule: interpret everything
After every cell producing an output (plot, test, parameter, metric), add a markdown cell with:
- **Technical reading** — what the result means statistically.
- **Business reading** — what it implies for a retailer / distributor / public authority.

Never leave a plot or test result uninterpreted. Say so explicitly when a result is inconclusive.

## Project structure
```
Project/
├── CLAUDE.md
├── Contexte/             # assignment brief & reference material (read-only)
├── MRTSSM451USN.csv      # raw data (read-only)
├── Project_TSA_Gharbi_Yassine.ipynb   # main deliverable
├── AI_USAGE_LOG.md
└── requirements.txt
```

## Notebook / report structure
0. **Introduction** — problem, dataset, business question, plan
1. **Data loading & cleaning** — DatetimeIndex, frequency, missing values, outliers
2. **EDA** — time plot, seasonal plot (month-by-year), boxplot by month, rolling mean/std
3. **Stationarity** — ADF + KPSS, regular and seasonal differencing
4. **ETS** — decomposition (additive vs multiplicative, justified), Holt-Winters fit, forecast
5. **SARIMA** — ACF/PACF, order selection (p,d,q)(P,D,Q,12), fit, residual diagnostics, forecast
6. **Prophet** — fit, trend and yearly components, changepoints vs real events, forecast
7. **Comparison** — metrics table, overlaid forecast plot, discussion
8. **Conclusion** — key findings, limits, business recommendations, improvements
9. **AI-usage policy** — major prompts and how AI was used (built from `AI_USAGE_LOG.md`)

## Evaluation protocol
- Chronological train/test split, never shuffled. Same test horizon for all models.
- Baselines: naive and seasonal naive.
- Metrics: MAE, MSE, RMSE, MAPE. Explain what each penalizes and which matters most for the business case.
- AIC/BIC for ETS/SARIMA (in-sample only, not comparable with Prophet).
- Residual diagnostics: residual plot, ACF of residuals, Ljung-Box, histogram/QQ-plot.
- Optional: rolling-origin time-series cross-validation.
- Discuss prediction intervals, not just point forecasts.

## Technical conventions
- Python 3: pandas, numpy, matplotlib/seaborn, statsmodels, prophet, scikit-learn (metrics), pmdarima (optional).
- Dependencies pinned in `requirements.txt`.
- Fixed random seeds; notebook must pass "Restart & Run All" without errors.
- Relative paths only.
- Every plot: title, axis labels with units (millions of USD), legend.
- No data leakage: anything fitted (transformations, parameters) is fitted on train only.
- One step per code cell; short, readable cells.

## AI-usage log (mandatory)
Maintain `AI_USAGE_LOG.md` at project root. **One entry per major step** (same granularity as the pushes below), not one per prompt. Each entry contains:
- Date
- Major prompts (verbatim if short, otherwise summarized)
- What was produced (generated code, methodological choices, interpretation help, debugging)
- How the student used or modified it

Minor edits (typos, formatting, corrections, follow-up fixes) are not logged; at most, amend the entry of the current step.

## Git workflow
- **One commit and one push per major step**, 9 pushes in total: the introduction and Section 1 together, then one per section from 2 to 9. No push for intermediate edits.
- Commit and push only when the student asks, on `main`.
- Before each push, make sure `AI_USAGE_LOG.md` has the entry for that step.
- **Do not add Claude as co-author**: no `Co-Authored-By` line and no "Generated with" line in commit messages.

## How Claude should work
- Explain every choice (decomposition type, SARIMA orders, Prophet parameters…) so the student can defend it orally.
- For key methodological decisions, present options and trade-offs before implementing.
- Never invent data, results, dates or historical facts. If unsure, say so or ask.
- Interpretations are drafts for the student to validate, not final text.