# AI usage log

Authors: Yassine Gharbi and Martin Demerdjiev. The project was done by the two of us, working together on one computer (Yassine's), which is why every commit comes from a single account, with Martin as co-author.

Tool: Claude Code (Anthropic). One entry per major step of the notebook; minor edits (typos, formatting, corrections) are not logged.

---

## 2026-10-01 — Step 1: Introduction and Section 1 (data loading and cleaning)

- **Major prompts (verbatim):**

Read CLAUDE.md first. Then create the notebook Project_TSA_Gharbi_DEMERDJIEV.ipynb with this structure: title, objective, imports, and one empty markdown section per step (1 Data, 2 EDA, 3 Stationarity, 4 ETS/Holt-Winters, 5 SARIMA, 6 Prophet, 7 Comparison & Conclusion). Set a global random seed and a plotting style. Don't run any analysis yet.
Load the data, parse dates, set a sorted DatetimeIndex and infer/enforce the frequency (asfreq). 
Report shape, dtypes, date range and duplicated timestamps. Detect missing values (count, position, gaps in the index) and impute with a justified method (interpolation/ffill), explaining the choice. Detect outliers (IQR or rolling z-score + visual check) and say whether you flag, cap or keep them, with reasoning. Finish with a train/test split that respects time order (no shuffle), with the horizon stated. Add a markdown comment after each step.

- **What was produced:**

  - The notebook `Project_TSA_Gharbi_Yassine.ipynb`: title cell, a drafted Introduction (0.1 problem and business question, 0.2 dataset, 0.3 approach and plan), the setup cells (imports, seed, constants, shared plot style) and the headings of sections 2–9, each with a "To do" list of planned content.
  - The course tools found in `Contexte/Cours` (band procedure, Buys-Ballot table and test, analysis of variance) were added to the plan of sections 2 and 4.
  - Section 1, code and draft interpretations: loading, `DatetimeIndex`, frequency and completeness checks, summary statistics, outlier screening.
  - Methodological proposals made by the AI: screening outliers on the year-over-year change with a modified z-score (after showing that the IQR rule on raw values only flags Decembers), and leaving the flagged months unmodified.
  - The AI ran the notebook to check that the figures quoted in the text match the outputs.

---

## 2026-10-01 — Step 2: Section 2 (exploratory data analysis)

- **Major prompt (verbatim):** 

Section 2: produce (a) a time plot with trend overlay, (b) a seasonal plot (month × year lines), (c) a boxplot by month, (d) rolling mean and std (window = seasonal period) on one chart. Add ACF/PACF plots of the raw series. After each plot, write 2-3 lines of interpretation: trend, seasonality (period, additive vs multiplicative), variance changes, anomalies. Conclude with a summary of what this implies for modelling (log transform? differencing?).
- **What was produced:**

  - Section 2, code and draft interpretations: time plot, seasonal plot (in levels and relative to each year's average), boxplot by month, 12-month rolling mean and standard deviation with the NBER recessions shaded, train/test split, and a summary of what the exploration implies for the models.
  - Methodological proposals made by the AI: a 24-month test horizon (two Decembers) rather than 12; reading the stable rolling standard deviation as a sign of an additive structure, to be confirmed in Section 4; moving the band procedure, the Buys-Ballot table and the analysis of variance to Section 4, so that they are run on the training set.
  - The AI checked the NBER recession dates on the NBER website and ran the notebook to check that the figures quoted in the text match the outputs.


---

## 2026-10-01 — Step 3: Section 3 (stationarity)

- **Major prompt (verbatim):** 

Section 3: run ADF (H0: unit root) and KPSS (H0: stationary) on the series, and present results in a table (statistic, p-value, critical values, conclusion). Then apply regular differencing (d=1), seasonal differencing (D=1, s=period), and both, re-testing each time with ADF + KPSS and plotting ACF/PACF. Interpret the ADF/KPSS combination (both agree vs. conflict). Conclude with the retained (d, D) and a first guess at SARIMA orders from the ACF/PACF.

- **What was produced:**

  - Section 3, code and draft interpretations: a helper running ADF and KPSS together, tests on the series in level (around a constant and around a linear trend), plot and tests of the three differencing candidates (d = 1, D = 1, both), a robustness check on the training data before 2020, and the conclusion d = 1, D = 1.
  - Methodological proposals made by the AI: reading the two tests jointly; adding the lag-12 autocorrelation and the standard deviation because ADF and KPSS do not detect a seasonal pattern; repeating the tests without the 2020–2021 shock, which is what separates D = 1 alone from d = 1, D = 1; keeping the series in original units (no log).
  - The AI installed `statsmodels`, created `requirements.txt` and ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it: Validated by Yassine & Martin**
---

## 2026-10-01 — Step 4: Section 4 (ETS: decomposition and Holt-Winters)

- **Major prompt (verbatim):** 

Section 4: I'm a beginner in Holt-Winters, so guide me step by step. First, classical/STL decomposition (additive vs multiplicative, justify) with plots of trend, seasonal and residual. Then explain in plain language (short markdown) level/trend/seasonal components and alpha, beta, gamma, before each code cell. Fit Simple ES → Holt → Holt-Winters (additive and multiplicative, damped or not), compare AIC and test-set RMSE/MAE/MAPE, plot forecasts vs actuals with prediction intervals, and check residuals (ACF, Ljung-Box, normality). Stop after each model and wait for my confirmation.

- **What was produced:**

  - Section 4, code and draft interpretations: band procedure, Buys-Ballot table and test, analysis of variance, additive and multiplicative decompositions, seasonal coefficients and conservation principle, nine ETS candidates compared by AIC and BIC, residual diagnostics, and the 24-month forecast with its prediction interval. Two helpers (`residual_diagnostics`, `plot_forecast` / `forecast_check`) are written to be reused in Sections 5 and 6.
  - Methodological proposals made by the AI: comparing nine ETS models rather than only the additive and multiplicative Holt-Winters, which led to ETS(M,A,A); expressing the residuals of that model in percent of the fitted value; judging the forecast on the two Decembers and on each year of the test period.
  - Debugging by the AI: the default estimation of the initial states converged to absurd values for the additive models, so the heuristic initialisation is used; the simulated prediction interval changed from one run to the next until the random generator was seeded.
  - The AI ran the notebook twice to check that the results are identical and that the figures quoted in the text match the outputs.
- **How the student used or modified it: Validated by Yassine & Martin**
---

## 2026-10-01 — Step 5: Section 5 (SARIMA)

- **Major prompt (verbatim):** 

Section 5: fit SARIMA using the (d, D, s) from section 3. Choose (p,q,P,Q) from ACF/PACF candidates and confirm with a grid search or auto_arima (AIC/BIC), showing the top 5 models. Run residual diagnostics (plot_diagnostics, Ljung-Box, Jarque-Bera, heteroskedasticity). Forecast on the test set with 95% intervals, compute RMSE/MAE/MAPE, and store the metrics in a results dict for the final comparison.

- **What was produced:**

  - Section 5, code and draft interpretations: ACF and PACF of the twice-differenced training series, comparison of 36 SARIMA models by AIC and BIC, coefficient table, residual diagnostics, and the 24-month forecast with its prediction interval.
  - Methodological proposals made by the AI: reading the correlograms first (MA(2) and seasonal MA(1)) and then checking that reading against a grid of neighbouring models, which added a seasonal AR term; leaving out the first 13 residuals and correcting the Ljung-Box test for the four ARMA terms.
  - The AI ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it: Validated by Yassine & Martin**
---

## 2026-10-01 — Step 6: Section 6 (Prophet)

- **Major prompt (verbatim):** 

Section 6: fit Prophet on the same train set (ds/y format). Set the seasonality mode (additive/multiplicative) from the EDA, then test changepoint_prior_scale and seasonality_prior_scale on a small grid with time-series cross-validation. Plot the forecast and components, evaluate on the same test set with the same metrics, and store them in the same results dict. Comment on Prophet's strengths and weaknesses for this series.

- **What was produced:**

  - Section 6, code and draft interpretations: choice of the Prophet settings by a rolling-origin validation inside the training set, trend and yearly component, changepoints compared with the NBER recessions, residual diagnostics, and the 24-month forecast with its uncertainty interval.
  - Methodological proposals made by the AI: choosing the settings by rolling-origin validation, since Prophet has no AIC; extending `changepoint_range` to 0.95 as a candidate so that changepoints can be placed after 2017; comparing Prophet's yearly effect with the seasonal coefficients of the decomposition; reporting plainly that Prophet over-forecasts and that its interval covers only 15 of the 24 test months.
  - The AI installed `prophet`, silenced its log messages, fixed the random seed of the simulated interval and ran the notebook twice to check that the results are identical and that the figures quoted in the text match the outputs.
- **How the student used or modified it: Validated by Yassine & Martin**
---

## 2026-10-01 — Step 7: Section 7 (comparison of the forecasts)

- **Major prompt (verbatim):** 

Build one comparison table (Holt-Winters, SARIMA, Prophet, plus a seasonal-naive baseline) with RMSE, MAE, MAPE, and AIC where available. Plot all forecasts against the test set on a single chart. Discuss accuracy, interpretability, residual quality, interval calibration and complexity. Conclude with the recommended model and why, the limits of the study (sample size, a single split, outliers), and future work (rolling-origin CV, exogenous variables, ensembles). Make sure the notebook runs top to bottom (Restart & Run All) with no errors.

- **What was produced:**

  - Section 7, code and draft interpretations: naive and seasonal naive baselines, metrics table (MAE, MSE, RMSE, MAPE, mean error) with a breakdown by year and by December, overlaid forecasts and forecast errors, rolling-origin evaluation of the five methods inside the training set, comparison of the prediction intervals, summary table and discussion.
  - Methodological proposals made by the AI: RMSE as the main criterion for this business case; adding the mean error to show the direction of the errors; the rolling-origin evaluation, which shows that the test ranking is partly circumstantial; recommending ETS as the main forecast with SARIMA as a second opinion and the seasonal naive as a benchmark.
  - The AI ran the notebook to check that the figures quoted in the text match the outputs.
- **How the student used or modified it: Validated by Yassine & Martin**
---

## 2026-10-01 — Step 8: Section 8 (conclusion)

Done by hand 

