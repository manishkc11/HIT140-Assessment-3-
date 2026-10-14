# Member 1 — Task 3: Independent Audit

**Review decision: APPROVED for exploratory reporting and progression to Member 1, Task 4.**

Input: `FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting.xlsx` — SHA-256 `71da963689f5c79e08c4375114665b2388e72d219d58a2294a7afa6dda660d88`.
Submission: `member1_task3_deliverables(1).zip`.

## Validation performed

- Independently read the 104 match records from `Master_104_Matches` using a separate spreadsheet-reading tool.
- Recalculated 9 × 9 Pearson correlations from the nine modelling columns.
- Recalculated eight Spearman correlations against `goal_difference`.
- Recalculated VIF values via eight auxiliary least-squares regressions with intercept; no predictive model was fitted.
- Recalculated 18 feature-level 1.5 × IQR screening flags across 14 distinct match IDs.
- Independently checked all 8 X7 Pearson and Spearman sensitivity comparisons, with 104 matches versus 103 excluding Match 13 **for sensitivity only**.
- Reran the submitted Python program directly against the original workbook. All five CSVs and three 320-DPI figures are byte-identical to the ZIP outputs. The Markdown report differs only in the input filename (`...Formatting(1).xlsx` in the submission versus `...Formatting.xlsx` in the rerun); the underlying source-file SHA-256 is identical.
- Visually inspected the correlation heatmap, Pearson/Spearman comparison and VIF diagnostic plot. All are legible and appropriately labelled.

## Recalculated results

| Predictor | Pearson r vs Y | Spearman rho vs Y | VIF |
|---|---:|---:|---:|
| X1 FIFA ranking difference | -0.621121 | -0.630276 | 5.625298 |
| X2 Elo difference | +0.626690 | +0.642081 | 6.274925 |
| X3 Recent goals scored difference | +0.436433 | +0.498139 | 4.264087 |
| X4 Recent goals conceded difference | -0.357169 | -0.339392 | 3.030687 |
| X5 Win-rate difference | +0.486448 | +0.498500 | 6.134045 |
| X6 Clean-sheet difference | +0.192669 | +0.164359 | 3.116831 |
| X7 Rest-days difference | +0.042068 | +0.068560 | 1.048774 |
| X8 Opponent-strength difference | -0.209257 | -0.175645 | 1.305685 |

Selected predictor-pair Pearson correlations: X1–X2 = -0.898072; X3–X5 = +0.734722; X4–X6 = -0.731807.

X7–Y Pearson: all 104 +0.042068; 103-case sensitivity +0.098257.

## Conclusions and boundaries

- X1, X2 and X5 exceed VIF 5 and warrant attention in future training-partition diagnostics; none automatically warrants removal. VIF is not a measure of out-of-sample accuracy.
- The extreme Match 13 X7 = -70 is a statistically unusual observation but was not removed. The 103-case comparison is **not** a revised modelling dataset.
- Descriptive correlation rankings are not feature-importance rankings in a multiple regression, and do not imply causality or statistical significance.
- Full-dataset EDA is suitable for descriptive reporting. Any data-driven changes to model specification, preprocessing and feature selection must be made with training data only; held-out test matches must remain untouched until evaluation.
- This is verification of arithmetic and reporting **against the provided Excel workbook**. It does not independently authenticate historical FIFA fixtures, ranking editions or Elo inputs.

**No correction requested for Task 3.**
