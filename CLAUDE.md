# CLAUDE.md — Time Series Analysis (TSA) Project

## Context
Academic project (EPF Montpellier, Data & AI). Goal: forecast a univariate time series **and interpret every step**, both technically and in business terms. Deliverable: a structured report, written as a Jupyter notebook.

**Before starting any task, read the files in `Contexte/`** (assignment brief, course material). They define the requirements; if they conflict with this file, `Contexte/` wins — flag the conflict.

## Dataset
- File: `MRTSSM4453USN.csv` (project root — do not move or modify it)
- Series: **Retail Sales: Beer, Wine, and Liquor Stores (US)** — millions of dollars, **not seasonally adjusted**
- Source: U.S. Census Bureau, retrieved from FRED: https://fred.stlouisfed.org/series/MRTSSM4453USN
- Download (no API key needed): https://fred.stlouisfed.org/graph/fredgraph.csv?id=MRTSSM4453USN
- Frequency: **monthly**, 1992-01 → 2026-07 (~415 observations, no missing values)
- CSV columns: `observation_date`, `MRTSSM4453USN` → parse dates, set a monthly DatetimeIndex (`freq="MS"`).
- Report citation: "U.S. Census Bureau, Retail Sales: Beer, Wine, and Liquor Stores [MRTSSM4453USN], retrieved from FRED, Federal Reserve Bank of St. Louis."

### Implications for the methods
- **Strong yearly seasonality (period = 12)** with a December peak, plus a strong upward trend.
- **Additive vs multiplicative**: seasonal amplitude grows with the level → test both, or log-transform then additive. Justify the choice.
- **ETS**: seasonal decomposition (`seasonal_decompose` / STL, period=12) + ETS model with seasonal term (Holt-Winters).
- **SARIMA** (not plain ARIMA): seasonal differencing (D) and seasonal orders (P,D,Q,12).
- **Prophet**: yearly seasonality on (weekly/daily off), `seasonality_mode` additive vs multiplicative.
- **Test horizon**: last 12–24 months. Seasonal naive baseline is mandatory.
- **Structural events** (verify before citing): 2008–09 recession, COVID-19 shock in 2020, post-COVID inflation. Link anomalies and changepoints to these events.

### Business context
Retail planning for alcohol retailers and distributors: inventory and supply-chain planning ahead of holiday peaks, staffing, cash-flow forecasting, excise tax revenue estimates for public authorities. Every interpretation should connect to at least one of these.

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
├── MRTSSM4453USN.csv     # raw data (read-only)
├── tsa_report.ipynb      # main deliverable
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
Maintain `AI_USAGE_LOG.md` at project root. After each significant contribution (generated code, methodological choice, interpretation help, debugging), append:
- Date
- Prompt (verbatim if short, otherwise summarized)
- What was produced
- How the student used or modified it

Minor edits (typos, formatting) are not logged.

## How Claude should work
- Explain every choice (decomposition type, SARIMA orders, Prophet parameters…) so the student can defend it orally.
- For key methodological decisions, present options and trade-offs before implementing.
- Never invent data, results, dates or historical facts. If unsure, say so or ask.
- Interpretations are drafts for the student to validate, not final text.