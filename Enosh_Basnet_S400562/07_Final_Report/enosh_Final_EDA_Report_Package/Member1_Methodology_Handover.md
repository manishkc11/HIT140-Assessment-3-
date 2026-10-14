# Member 1 — Methodology handover to Member 2

## Scope and authoritative input

- Use only the verified **104** rows of `Master_104_Matches` in `FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting(1).xlsx` for Objective 2.1 modelling.
- Outcome: `goal_difference = team_a_goals - team_b_goals` (penalty shootout goals excluded from the recorded target); actual scores are **not predictors**.
- Model candidate features in established order: `fifa_rank_diff`, `elo_rating_diff`, `last5_avg_goals_scored_diff`, `last5_avg_goals_conceded_diff`, `last5_win_rate_diff`, `last5_clean_sheet_rate_diff`, `rest_days_diff`, `last5_opponent_strength_diff`.
- Preserve `match_id`, `match_date`, `team_a` and `team_b`, and the **Team A minus Team B** sign convention; X1 and X4 sign interpretations differ from other features.
- Keep the original workbook unmodified. Maintain a scriptable, separately saved modelling workflow and documented output versions.

## Established workbook-level facts (Member 1 Tasks 1–3)

| Check | Confirmed finding |
|---|---|
| Records and identifiers | 104 records, `match_id` 1–104 each once; 20 worksheet columns |
| Modelling columns | Nine numeric columns, no missing or invalid values |
| Target audit | 104/104 rows match goals A minus goals B |
| Recorded date range | 11 June–19 July 2026 |
| Target distribution | 50 positive, 30 negative, 24 zero; range −4 to +6 |
| IQR flags | 18 feature-level flags across 14 distinct matches; none excluded |
| X7 extreme | Match 13: `rest_days_diff = -70` |
| Strong X–X associations | X1–X2 Pearson −0.898; X3–X5 +0.735; X4–X6 −0.732 |
| VIF with intercept | X1 5.625; X2 6.275; X5 6.134 (each exceeds 5; none exceeds 10) |
| X7 vs target | Pearson +0.042 and Spearman +0.069 using all 104 |

## Pre-modelling safeguards

1. Specify and document a valid **train/test strategy before estimating performance**. Consider the temporal structure of a single tournament and repeated team appearances when selecting a split; justify the final choice rather than choosing it after viewing test outcomes.
2. Keep outcome information (`team_a_goals`, `team_b_goals`, `result_note`, and `goal_difference` except as Y) out of X. Ensure each historical feature is measured only with pre-kickoff data; source completeness remains a separate provenance issue.
3. Compute any data-learned preprocessing (such as scaling, imputation or data-derived transformations) **on the training portion only** and apply the learned settings to the test portion. All nine modelling columns are currently complete; do not add unnecessary imputation.
4. Treat the correlation and VIF results from all 104 matches **only as descriptive context**, not as training-only evidence for feature deletion or hyperparameter decisions.
5. Retain all eight features as the agreed baseline initially. Multicollinearity in X1/X2/X5 warrants **training-only coefficient-stability and VIF diagnostics**; VIF alone is not a reason to remove features.
6. Retain Match 13 as the default. If further source checks or training-only influence analyses suggest alternatives, state the rationale and compare sensitivities transparently. The previously analysed 103-match view was **not** a proposed modelling dataset.
7. Report regression assumptions and diagnostics in the modelling section: linearity, residual behaviour, heteroscedasticity, independence considerations, influential observations, and overfitting risk. Do not assert satisfaction before testing.
8. Fit the final model and compute any MAE, RMSE or R² **only in Member 2's authorised workflow**. Do not infer model performance from marginal correlations or from VIF.

## Evidence, reproducibility and integrity

- Task 1: `member1_task1_data_validation.py`, `member1_task1_descriptive_statistics.csv`, `member1_task1_validation_report.md`.
- Task 2: `member1_task2_eda.py`, five original report figures, `member1_task2_eda_report.md`.
- Task 3: `member1_task3_correlation_analysis.py`, correlation/VIF/outlier/sensitivity CSVs, three figures, `member1_task3_analysis_report.md`.
- Values are internally validated from the workbook. Separate football-source and ranking provenance caveats remain; code-level reproducibility does not establish external-source authenticity.
- Generative AI assisted with historical-source work in upstream stages, Python generation, diagnostic checks, visualisations and report drafting. The team should review scripts and be able to explain every operation for its academic-integrity declaration.

**Handover boundary:** No split, final regression, prediction or evaluation is performed or authorised by these Member 1 deliverables.
