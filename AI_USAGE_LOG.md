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
