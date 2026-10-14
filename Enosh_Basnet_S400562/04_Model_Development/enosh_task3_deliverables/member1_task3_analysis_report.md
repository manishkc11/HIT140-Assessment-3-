# Member 1 – Task 3: Correlation, multicollinearity and outlier diagnostics

## Purpose, input and boundaries

This is **descriptive and diagnostic analysis**, not a fitted goal-difference prediction model. The only observations are 104 matches from the `Master_104_Matches` worksheet of the supplied XLSX; eight features (X1–X8) and `goal_difference` (Y) retain Team A minus Team B orientation.

- Original input: `FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting(1).xlsx` (read-only; cached numeric formula values); SHA-256: `71da963689f5c79e08c4375114665b2388e72d219d58a2294a7afa6dda660d88`.
- Main analyses: **104/104** observations, complete numeric columns, no missing input, no rows omitted, no duplicate IDs or full rows, all target arithmetic verified.
- Figure files: 320 DPI PNG. Pearson and Spearman are *marginal* associations; VIF concerns redundancy **among predictors**, not association with Y.
- No scaling, imputation, winsorisation, outlier deletion, feature selection, test-data optimisation, final model training, or prediction is performed.

## Methods

**Pearson correlation (r)** measures linear association between two numerical variables. Its sign indicates direction and its magnitude, from 0 to 1, shows the strength of the observed linear association. **Spearman rank correlation (ρ)** is Pearson correlation applied to the ranked values; it measures monotonic association and uses *average ranks for tied observations*. Correlation does not show causation, adjusted effects, model predictive performance, or statistical significance. No p-values or significance claims are made.

**VIF:** For each predictor, regress it on the other seven predictors **with an intercept**, calculate the auxiliary R², then use `VIF = 1 / (1 − R²)`. Results are generated with `statsmodels` and independently checked using NumPy least-squares. No regression involving the target is trained. Guidelines: near 1 low dependence, >5 investigate, >10 potentially serious; these are screening conventions, not removal rules.

**IQR:** For each feature use Q1 and Q3 computed with linear interpolation; flag observations outside `[Q1 − 1.5×IQR, Q3 + 1.5×IQR]`. All 18 flags are preserved. A flag alone is **not a data error**. If the original dataset is later used for predictive development, any data-driven preprocessing or model-selection decision must use training data only.

## Figure 6 – Pearson correlation heatmap

The 9×9 heatmap includes the eight predictors and Y on a fixed scale of −1 to +1, with 2-decimal coefficients. The correlation matrix is symmetric, its diagonal equals 1 and all coefficients are within the expected range.

### Predictor correlations with goal difference

| Predictor | Pearson r | Spearman ρ | Pearson direction and approximate magnitude |
|---|---:|---:|---|
| X1 – FIFA ranking difference | -0.621 | -0.630 | strong negative association |
| X2 – Elo rating difference | +0.627 | +0.642 | strong positive association |
| X3 – Last-5 average goals scored difference | +0.436 | +0.498 | moderate positive association |
| X4 – Last-5 average goals conceded difference | -0.357 | -0.339 | weak negative association |
| X5 – Last-5 win-rate difference | +0.486 | +0.499 | moderate positive association |
| X6 – Last-5 clean-sheet-rate difference | +0.193 | +0.164 | very weak positive association |
| X7 – Rest-days difference | +0.042 | +0.069 | very weak positive association |
| X8 – Last-5 opponent-strength difference | -0.209 | -0.176 | weak negative association |

In this sample, the largest absolute *marginal* Pearson correlations with Y are **X2 (+0.627)** and **X1 (-0.621)**, while the smallest absolute correlation is **X7 (+0.042)**. Neither ranking constitutes a decision to select features nor evidence of independent predictive contribution.

### Prespecified predictor-pair checks

- **X1–X2:** Pearson r = **-0.898**; FIFA rank and Elo use opposite numerical strength conventions. This measures predictor–predictor association, not their adjusted effects on Y.
- **X3–X5:** Pearson r = **+0.735**; goals scored and win rate can encode overlapping recent form. This measures predictor–predictor association, not their adjusted effects on Y.
- **X4–X6:** Pearson r = **-0.732**; goals conceded and clean-sheet rates describe related defensive history. This measures predictor–predictor association, not their adjusted effects on Y.

FIFA ranking difference requires sign care: lower ranking numbers mean stronger teams, so negative X1 can legitimately associate with positive goal difference. Elo's direction is the opposite. Negative r values are not errors.

**Suggested caption:** *Figure 6. Pearson correlation matrix for all eight pre-match explanatory variables and observed goal difference across 104 World Cup matches. Cells display r to two decimal places; colours use a common −1 to +1 scale.*

## Figure 7 – Pearson versus Spearman

The two methods agree on the correlation direction for **8 of eight** variables. The largest absolute method difference is **X3** (Pearson +0.436, Spearman +0.498; absolute difference 0.062). Differences can result from nonlinear monotonic patterns, ties, or the influence of extreme values; the plot alone does not identify the cause.

X5 and X6 are differences of rates based on five matches, so ties and discrete increments are expected. X7 contains many identical zero observations: **62/104** are exactly zero, plus the unusually negative Match 13. Spearman accounts for tied ranks but is not immune to small samples or measurement problems.

Neither Spearman coefficients nor their relative size justify replacing, removing or rescaling any predictor here.

**Suggested caption:** *Figure 7. Side-by-side Pearson and Spearman correlation coefficients between each original explanatory variable and goal difference (N = 104); paired markers compare linear and rank-based associations without significance testing.*

## Figure 8 – Variance inflation factors

| Predictor | VIF (with intercept) | Auxiliary R² | Interpretation |
|---|---:|---:|---|
| X1 – `fifa_rank_diff` | 5.625 | 0.822 | Elevated (>5); investigate |
| X2 – `elo_rating_diff` | 6.275 | 0.841 | Elevated (>5); investigate |
| X3 – `last5_avg_goals_scored_diff` | 4.264 | 0.765 | Moderate dependence; monitor |
| X4 – `last5_avg_goals_conceded_diff` | 3.031 | 0.670 | Moderate dependence; monitor |
| X5 – `last5_win_rate_diff` | 6.134 | 0.837 | Elevated (>5); investigate |
| X6 – `last5_clean_sheet_rate_diff` | 3.117 | 0.679 | Moderate dependence; monitor |
| X7 – `rest_days_diff` | 1.049 | 0.047 | Low dependence |
| X8 – `last5_opponent_strength_diff` | 1.306 | 0.234 | Low dependence |

**Screening results:** 3 features exceed VIF 5 (X1, X2, X5); 0 exceed 10 (none). All eight remain included. The intercept's own VIF is intentionally excluded.

When explanatory variables share substantial information, their individual regression coefficients can become sensitive to minor changes in the training dataset, inflating standard errors and complicating interpretation. This does not necessarily prevent the model from producing predictions. The later modelling team should investigate on *training data only*, rather than delete variables solely on these full-dataset screening statistics.

Independent validation computed each auxiliary R² using an intercept and NumPy least squares, then reconstructed each VIF; maximum absolute difference from `statsmodels` was **3.55e-15**.

**Suggested caption:** *Figure 8. Variance inflation factors for the eight candidate predictors from auxiliary regressions containing an intercept. Dashed guides at 5 and 10 denote conventional investigation thresholds, not automatic removal criteria.*

## IQR screening and detailed outlier investigation

Across all eight feature columns, the independent 1.5×IQR screen identified **18 feature-level flags** involving **14 distinct matches**. These agree with Task 1's 18 feature-level flags. Every flagged record, team, date, value, lower/upper fence and recommended follow-up appears in `member1_task3_outlier_investigation.csv`.

| Case | Observed value | IQR screen (lower, upper) | Investigation rationale |
|---|---:|---|---|
| Match 13 / X7 | -70.00 | (-1.500, 2.500) | Large rest-day imbalance: verify predecessor dates and calendar-day convention; value is not impossible by its definition. |
| Match 18 / X8 | +57.20 | (-57.925, 55.075) | Large average-ranking difference: verify five previous opponents, their applicable publication dates and arithmetic; possible but unusual. |
| Match 70 / X5 | -1.00 | (-0.875, 0.925) | −1 is a mathematically possible rate difference; check all five win results for each team. |
| Match 70 / X6 | -1.00 | (-0.800, 0.800) | −1 is a mathematically possible clean-sheet-rate difference; check five conceded-goal records for each team. |

In particular, X7 has no fixed maximum or minimum mathematical bound, so −70 is an extreme observation, **not a mathematically invalid input**. X8 is a difference of FIFA ranking averages, and +57.20 is similarly possible. X5/X6 are bounded differences of proportions and −1 is valid at the boundary. None has been excluded or edited. External historical fixture/ranking verification was outside the scope of this workbook-only task.

## X7 sensitivity – visual/diagnostic comparison only

- Main sample (104): X7 mean = **-0.490**; sample SD = **7.015**.
- Excluding Match 13 for sensitivity only (103): mean = **+0.184**; sample SD = **1.363**. **All 104 remain in the official analysis.**

| X7 paired with | Pearson 104 | Pearson 103 | Change (103−104) | Spearman 104 | Spearman 103 | Change (103−104) |
|---|---:|---:|---:|---:|---:|---:|
| X1 – fifa_rank_diff | -0.143 | +0.039 | +0.182 | +0.047 | +0.079 | +0.033 |
| X2 – elo_rating_diff | +0.136 | -0.062 | -0.198 | -0.058 | -0.090 | -0.032 |
| X3 – last5_avg_goals_scored_diff | -0.007 | +0.001 | +0.008 | +0.004 | +0.002 | -0.001 |
| X4 – last5_avg_goals_conceded_diff | -0.055 | -0.145 | -0.090 | -0.109 | -0.100 | +0.009 |
| X5 – last5_win_rate_diff | +0.043 | +0.140 | +0.097 | +0.043 | +0.038 | -0.005 |
| X6 – last5_clean_sheet_rate_diff | +0.044 | +0.220 | +0.176 | +0.193 | +0.193 | +0.000 |
| X8 – last5_opponent_strength_diff | -0.130 | +0.002 | +0.132 | -0.015 | +0.010 | +0.026 |
| Y – goal_difference | +0.042 | +0.098 | +0.056 | +0.069 | +0.064 | -0.005 |

The Pearson X7–Y correlation changes from **+0.042 to +0.098** (Δ +0.056); Spearman changes from **+0.069 to +0.064** (Δ -0.005). X7 has a very extreme left-tail value; Pearson depends on the actual magnitudes and can be influenced by such a point, whereas Spearman uses ranks with ties. The direction of individual X7 correlations with other predictors may also change; see table rather than interpreting sensitivity as a new primary dataset.

Removing Match 13 from a descriptive *comparison* does not demonstrate corruption, justify exclusion, or establish performance effects in a fitted regression. Any later model diagnostics and treatment decisions belong to training-set-based analysis and require documented rationale.

## Limitations and implications for the regression stage

1. The complete 104-match sample was used for descriptive reporting. If these statistics inform feature selection, transformations, or parameter tuning before a train/test split, that would risk test-data leakage. **Make data-dependent modelling choices on training data only** after the split; reserve test matches for the final evaluation.
2. Pairwise correlations assess one relationship at a time; they do not estimate the independent effect of a feature holding others fixed. VIF diagnoses overlap among the Xs; neither test proves causation or out-of-sample predictability.
3. Spearman and Pearson are descriptive coefficients. No significance testing or multiple-comparisons inference has been performed, so no p-value or statistical significance claim is made.
4. The dataset includes tied discrete predictors, an influential-looking X7 value, and interrelated measures of team strength and form. Later model developers should test assumptions and stability on their training partition.
5. Correlation magnitude is not comparable to regression coefficient magnitude, and a negative sign can be meaningful because of Team A−B feature definitions. Do not interpret the marginal coefficient ranking as feature importance in the multivariable model.
6. The Excel worksheet was read through stored/cached values. The script does not recalculate spreadsheet formulas; it confirms that goal_difference matches the cached team-goal columns and checks complete numerical inputs.
7. This study does not perform external historical research. Source-quality questions for previously collected football statistics remain separate from the validated workbook arithmetic.

## Reproducibility and quality checks

- Input shape: 104 records × 20 worksheet columns; all nine numerical modelling columns complete.
- Pearson 9×9 matrix: symmetric, diagonal exactly 1 (within numerical precision), all values bounded by [−1,+1].
- VIF: `statsmodels` auxiliary regressions (with intercept) independently agree with NumPy OLS reconstruction; no VIF for intercept is presented.
- IQR: 18 flagged feature observations, including Match 13 X7, Match 18 X8, and Match 70 X5/X6.
- X7 sensitivity: all 104 cases for main metrics and 103 only for comparison; no stored data removal.
- Each figure saves as a 320-DPI PNG; the script saves the correlation matrix, correlation summary, VIF, IQR and X7 sensitivity CSVs automatically.

## Academic-integrity disclosure

Generative AI assisted with script design, Python implementation, mathematical validations, plotting, draft interpretations and report construction. Coefficients, VIF values, case flags, summary statistics and charts were computed directly from the user's supplied `Master_104_Matches` sheet. External source verification, final model fitting, predictions, tests of statistical significance, and causal analysis were not performed. Programmatic agreement establishes internal arithmetic consistency, not historical football-data authenticity.
