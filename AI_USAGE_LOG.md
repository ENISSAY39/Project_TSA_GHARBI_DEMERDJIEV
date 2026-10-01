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
