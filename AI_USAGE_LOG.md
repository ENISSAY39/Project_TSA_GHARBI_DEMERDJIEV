# AI usage log

Tool: Claude Code (Anthropic). One entry per major step of the notebook; minor edits (typos, formatting, corrections) are not logged.

---

## 2026-10-01 — Step 1: Introduction and Section 1 (data loading and cleaning)

- **Major prompts (verbatim):**
  - "Read the CLAUDE.md lets create the .ipynb file first with the write file name Project_TSA_Gharbi_Yassine"
  - "oui renomme le et fait **Data loading & cleaning** — DatetimeIndex, frequency, missing values, outliers"
- **What was produced:**
  - The notebook `Project_TSA_Gharbi_Yassine.ipynb`: title cell, a drafted Introduction (0.1 problem and business question, 0.2 dataset, 0.3 approach and plan), the setup cells (imports, seed, constants, shared plot style) and the headings of sections 2–9, each with a "To do" list of planned content.
  - The course tools found in `Contexte/Cours` (band procedure, Buys-Ballot table and test, analysis of variance) were added to the plan of sections 2 and 4.
  - Section 1, code and draft interpretations: loading, `DatetimeIndex`, frequency and completeness checks, summary statistics, outlier screening.
  - Methodological proposals made by the AI: screening outliers on the year-over-year change with a modified z-score (after showing that the IQR rule on raw values only flags Decembers), and leaving the flagged months unmodified.
  - The AI ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_

---

## 2026-10-01 — Step 2: Section 2 (exploratory data analysis)

- **Major prompt (verbatim):** "next : 2. **EDA** — time plot, seasonal plot (month-by-year), boxplot by month, rolling mean/std"
- **What was produced:**
  - Section 2, code and draft interpretations: time plot, seasonal plot (in levels and relative to each year's average), boxplot by month, 12-month rolling mean and standard deviation with the NBER recessions shaded, train/test split, and a summary of what the exploration implies for the models.
  - Methodological proposals made by the AI: a 24-month test horizon (two Decembers) rather than 12; reading the stable rolling standard deviation as a sign of an additive structure, to be confirmed in Section 4; moving the band procedure, the Buys-Ballot table and the analysis of variance to Section 4, so that they are run on the training set.
  - The AI checked the NBER recession dates on the NBER website and ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_

---

## 2026-10-01 — Step 3: Section 3 (stationarity)

- **Major prompt (verbatim):** "okay push and next step 3. **Stationarity** — ADF + KPSS, regular and seasonal differencing"
- **What was produced:**
  - Section 3, code and draft interpretations: a helper running ADF and KPSS together, tests on the series in level (around a constant and around a linear trend), plot and tests of the three differencing candidates (d = 1, D = 1, both), a robustness check on the training data before 2020, and the conclusion d = 1, D = 1.
  - Methodological proposals made by the AI: reading the two tests jointly; adding the lag-12 autocorrelation and the standard deviation because ADF and KPSS do not detect a seasonal pattern; repeating the tests without the 2020–2021 shock, which is what separates D = 1 alone from d = 1, D = 1; keeping the series in original units (no log).
  - The AI installed `statsmodels`, created `requirements.txt` and ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_

---

## 2026-10-01 — Step 4: Section 4 (ETS: decomposition and Holt-Winters)

- **Major prompt (verbatim):** "ok push and next ETS 4- decomposition and holt-winners"
- **What was produced:**
  - Section 4, code and draft interpretations: band procedure, Buys-Ballot table and test, analysis of variance, additive and multiplicative decompositions, seasonal coefficients and conservation principle, nine ETS candidates compared by AIC and BIC, residual diagnostics, and the 24-month forecast with its prediction interval. Two helpers (`residual_diagnostics`, `plot_forecast` / `forecast_check`) are written to be reused in Sections 5 and 6.
  - Methodological proposals made by the AI: comparing nine ETS models rather than only the additive and multiplicative Holt-Winters, which led to ETS(M,A,A); expressing the residuals of that model in percent of the fitted value; judging the forecast on the two Decembers and on each year of the test period.
  - Debugging by the AI: the default estimation of the initial states converged to absurd values for the additive models, so the heuristic initialisation is used; the simulated prediction interval changed from one run to the next until the random generator was seeded.
  - The AI ran the notebook twice to check that the results are identical and that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_

---

## 2026-10-01 — Step 5: Section 5 (SARIMA)

- **Major prompt (verbatim):** "ok push and next : 5- SARIMA and 6- Prophet"
- **What was produced:**
  - Section 5, code and draft interpretations: ACF and PACF of the twice-differenced training series, comparison of 36 SARIMA models by AIC and BIC, coefficient table, residual diagnostics, and the 24-month forecast with its prediction interval.
  - Methodological proposals made by the AI: reading the correlograms first (MA(2) and seasonal MA(1)) and then checking that reading against a grid of neighbouring models, which added a seasonal AR term; leaving out the first 13 residuals and correcting the Ljung-Box test for the four ARMA terms.
  - The AI ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_

---

## 2026-10-01 — Step 6: Section 6 (Prophet)

- **Major prompt (verbatim):** "ok push and next : 5- SARIMA and 6- Prophet" (same prompt as Step 5)
- **What was produced:**
  - Section 6, code and draft interpretations: choice of the Prophet settings by a rolling-origin validation inside the training set, trend and yearly component, changepoints compared with the NBER recessions, residual diagnostics, and the 24-month forecast with its uncertainty interval.
  - Methodological proposals made by the AI: choosing the settings by rolling-origin validation, since Prophet has no AIC; extending `changepoint_range` to 0.95 as a candidate so that changepoints can be placed after 2017; comparing Prophet's yearly effect with the seasonal coefficients of the decomposition; reporting plainly that Prophet over-forecasts and that its interval covers only 15 of the 24 test months.
  - The AI installed `prophet`, silenced its log messages, fixed the random seed of the simulated interval and ran the notebook twice to check that the results are identical and that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_

---

## 2026-10-01 — Step 7: Section 7 (comparison of the forecasts)

- **Major prompt (verbatim):** "ok push and next do comparaison and conclusion"
- **What was produced:**
  - Section 7, code and draft interpretations: naive and seasonal naive baselines, metrics table (MAE, MSE, RMSE, MAPE, mean error) with a breakdown by year and by December, overlaid forecasts and forecast errors, rolling-origin evaluation of the five methods inside the training set, comparison of the prediction intervals, summary table and discussion.
  - Methodological proposals made by the AI: RMSE as the main criterion for this business case; adding the mean error to show the direction of the errors; the rolling-origin evaluation, which shows that the test ranking is partly circumstantial; recommending ETS as the main forecast with SARIMA as a second opinion and the seasonal naive as a benchmark.
  - The AI ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it:** _to be completed by the student_
