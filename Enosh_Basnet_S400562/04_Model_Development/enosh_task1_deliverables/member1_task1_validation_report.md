# Member 1 — Task 1: Dataset integrity and descriptive statistics

## Scope and provenance

- **Source:** `FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting.xlsx` (original workbook read-only).
- **Worksheet:** `Master_104_Matches`; supporting sheets were not used as modelling observations.
- **Observed shape:** 104 rows × 20 columns.
- **Source workbook SHA-256:** `71da963689f5c79e08c4375114665b2388e72d219d58a2294a7afa6dda660d88`.
- **Model:** eight explanatory variables (`X1`–`X8`) and `goal_difference` as target.
- **Processing:** pandas/numpy under Python 3; no historical-data lookups, feature scaling, predictive modelling, correlation analysis, transformations, value replacement, filtering, or row deletion.

### Stage counts

| Tournament stage | Matches |
| --- | --- |
| Group Stage | 72 |
| Round of 32 | 16 |
| Round of 16 | 8 |
| Quarter-finals | 4 |
| Semi-finals | 2 |
| Bronze Final | 1 |
| Final | 1 |

The workbook has 32 missing `group` labels. Of these, 32 are in knockout matches, where a group label is not expected. There are 0 group-stage records with a missing group and 0 knockout records with a filled group. The `result_note` column contains 95 blanks; it is not a predictor.

## Integrity-validation methodology and outcomes

| Integrity test | Outcome | Details |
| --- | --- | --- |
| 1. Exactly 104 match records | PASS | Read 104 rows from Master_104_Matches. |
| 2. Unique complete match IDs 1–104 | PASS | Invalid IDs: 0; duplicate rows with IDs: 0; missing IDs: none; unexpected IDs: none. |
| 3. No missing target or explanatory values | PASS | fifa_rank_diff: 0; elo_rating_diff: 0; last5_avg_goals_scored_diff: 0; last5_avg_goals_conceded_diff: 0; last5_win_rate_diff: 0; last5_clean_sheet_rate_diff: 0; rest_days_diff: 0; last5_opponent_strength_diff: 0; goal_difference: 0 |
| 4. All nine modelling columns are finite numeric data | PASS | Invalid nonnumeric/boolean/infinite values: none. All modelling columns should also have numeric storage types. |
| 5. Goal differences agree with the score columns | PASS | Correct calculations: 104/104; mismatches: 0. |
| 6. No duplicate complete rows | PASS | Rows involved in full-row duplication: 0. |
| 7. Readable match dates inside tournament period | PASS | Unreadable/out-of-range dates: 0; earliest: 2026-06-11 00:00:00; latest: 2026-07-19 00:00:00. |
| 8. X5/X6 lie between −1 and +1 | PASS | Out-of-range values: 0. |
| 9. Negative and zero values handled without coercion | PASS | Negative and zero observations are retained; counts are reported separately below. |
| 10. Unusual values identified without removal | PASS | Flagged 18 column-specific observations using 1.5×IQR; all retained. |

- IDs must be exactly 1 to 104, unique and integer-valued. Numerical data are checked for missing values, invalid text, booleans, and non-finite values.
- Match dates must parse correctly and fall between 11 June and 19 July 2026, inclusive. This checks date representation and range **within the supplied file**, not external FIFA factual accuracy.
- Goal differences are compared against `team_a_goals - team_b_goals` with a numeric tolerance of 1e-9.
- Duplicate complete rows are checked across all imported columns.
- X5 and X6 are differences of two proportions, so values outside [-1, 1] are impossible.
- Negative and zero differences are valid because signs depend on the ordered Team A/Team B subtraction. The script retains them unchanged.
- An outlier-screening flag is raised for values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR. This is **screening for review only**, not evidence of incorrect data.

## Descriptive statistics

| Variable | Valid | Mean | Median | SD | Min | Max | Q1 | Q3 | Missing |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fifa_rank_diff | 104 | -7.212 | -6.500 | 33.636 | -77.000 | 76.000 | -28.500 | 14.000 | 0 |
| elo_rating_diff | 104 | 59.952 | 76.500 | 246.464 | -512.000 | 579.000 | -114.500 | 217.500 | 0 |
| last5_avg_goals_scored_diff | 104 | 0.129 | 0.200 | 1.022 | -2.200 | 2.800 | -0.600 | 0.800 | 0 |
| last5_avg_goals_conceded_diff | 104 | -0.067 | -0.200 | 0.962 | -2.800 | 2.600 | -0.600 | 0.400 | 0 |
| last5_win_rate_diff | 104 | 0.056 | 0.000 | 0.345 | -1.000 | 0.800 | -0.200 | 0.250 | 0 |
| last5_clean_sheet_rate_diff | 104 | 0.004 | 0.000 | 0.369 | -1.000 | 0.800 | -0.200 | 0.200 | 0 |
| rest_days_diff | 104 | -0.490 | 0.000 | 7.015 | -70.000 | 6.000 | 0.000 | 1.000 | 0 |
| last5_opponent_strength_diff | 104 | -0.540 | 0.200 | 22.239 | -45.200 | 57.200 | -15.550 | 12.700 | 0 |
| goal_difference | 104 | 0.481 | 0.000 | 2.024 | -4.000 | 6.000 | -1.000 | 2.000 | 0 |

**Definitions:** SD is the sample standard deviation (`ddof=1`). Q1 and Q3 are the 25th and 75th percentiles from pandas' default linear interpolation. The downloadable CSV keeps six decimal places; the report table displays three. Statistics use all valid original observations and make no train/test split.

## Goal-difference distribution

| Outcome in recorded goals | Matches | Percentage |
| --- | ---: | ---: |
| Positive (`goal_difference > 0`) — Team A scored more goals | 50 | 48.08% |
| Negative (`goal_difference < 0`) — Team B scored more goals | 30 | 28.85% |
| Zero (`goal_difference = 0`) — Teams had equal goal totals | 24 | 23.08% |
| Missing/invalid target values | 0 | 0.00% |

A zero goal difference indicates level goals, **not necessarily that a knockout match finished undecided after a penalty shootout**. Penalty shootout goals are not part of the recorded target calculation.

### Negative and zero-value checks (all preserved)

| Variable | Negative | Zero | Positive |
| --- | --- | --- | --- |
| fifa_rank_diff | 59 | 0 | 45 |
| elo_rating_diff | 41 | 0 | 63 |
| last5_avg_goals_scored_diff | 39 | 7 | 58 |
| last5_avg_goals_conceded_diff | 55 | 9 | 40 |
| last5_win_rate_diff | 31 | 26 | 47 |
| last5_clean_sheet_rate_diff | 35 | 23 | 46 |
| rest_days_diff | 14 | 62 | 28 |
| last5_opponent_strength_diff | 52 | 0 | 52 |
| goal_difference | 30 | 24 | 50 |

## Observations requiring attention

- **Validation errors:** 0. **Review-only observations:** 18. (A single match may be flagged in several feature columns.)
- **IQR flags:** 18 feature-specific observations; these remain in the dataset without any correction.
- **Largest absolute X7 value:** Match 13, `rest_days_diff = -70`. This value is unusually distant from the typical X7 interval and merits inspection of its previous-match dates; it is *not* automatically an error.

| Match ID | Column | Observed value | Level | Explanation |
| --- | --- | --- | --- | --- |
| 20 | last5_avg_goals_conceded_diff | -2.2 | REVIEW | Outside 1.5×IQR review band [-2.1000, 1.9000]; value is below the bound. Not automatically an error. |
| 34 | last5_avg_goals_conceded_diff | -2.8 | REVIEW | Outside 1.5×IQR review band [-2.1000, 1.9000]; value is below the bound. Not automatically an error. |
| 44 | last5_avg_goals_conceded_diff | 2 | REVIEW | Outside 1.5×IQR review band [-2.1000, 1.9000]; value is above the bound. Not automatically an error. |
| 55 | last5_avg_goals_conceded_diff | 2.6 | REVIEW | Outside 1.5×IQR review band [-2.1000, 1.9000]; value is above the bound. Not automatically an error. |
| 57 | last5_avg_goals_conceded_diff | -2.2 | REVIEW | Outside 1.5×IQR review band [-2.1000, 1.9000]; value is below the bound. Not automatically an error. |
| 70 | last5_avg_goals_conceded_diff | 2.6 | REVIEW | Outside 1.5×IQR review band [-2.1000, 1.9000]; value is above the bound. Not automatically an error. |
| 70 | last5_win_rate_diff | -1 | REVIEW | Outside 1.5×IQR review band [-0.8750, 0.9250]; value is below the bound. Not automatically an error. |
| 70 | last5_clean_sheet_rate_diff | -1 | REVIEW | Outside 1.5×IQR review band [-0.8000, 0.8000]; value is below the bound. Not automatically an error. |
| 9 | rest_days_diff | 3 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is above the bound. Not automatically an error. |
| 11 | rest_days_diff | -8 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is below the bound. Not automatically an error. |
| 13 | rest_days_diff | -70 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is below the bound. Not automatically an error. |
| 14 | rest_days_diff | -2 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is below the bound. Not automatically an error. |
| 18 | rest_days_diff | -2 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is below the bound. Not automatically an error. |
| 20 | rest_days_diff | 6 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is above the bound. Not automatically an error. |
| 21 | rest_days_diff | 4 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is above the bound. Not automatically an error. |
| 22 | rest_days_diff | -3 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is below the bound. Not automatically an error. |
| 85 | rest_days_diff | 3 | REVIEW | Outside 1.5×IQR review band [-1.5000, 2.5000]; value is above the bound. Not automatically an error. |
| 18 | last5_opponent_strength_diff | 57.2 | REVIEW | Outside 1.5×IQR review band [-57.9250, 55.0750]; value is above the bound. Not automatically an error. |

## Important descriptive findings (based on calculated numbers)

- The mean recorded goal difference is **0.481**, while the median is **0.000**. The observed target ranges from **-4** to **+6** goals.
- The target has **50 positive**, **30 negative**, and **24 zero** differences; these are match outcome categories, not modelling performance measures.
- X7 (`rest_days_diff`) has median **0**, and **62/104** matches (59.62%) have equal calendar rest intervals. Its range **-70** to **+6** highlights a potentially influential extreme observation.
- `elo_rating_diff` has a standard deviation of **246.464 Elo points**, compared with **0.345** for the dimensionless `last5_win_rate_diff`. These are different units, so raw scale alone does not establish predictive importance.
- The IQR method marks **18 feature-level observations** for review. They have not been deleted, clipped, or reclassified as data errors.

## Implications for future EDA and regression

1. The supplied master worksheet has 104 rows. Its modelling variables can be described without dropping or imputing any observation. If future corrections are justified, record them transparently before modelling.
2. Team A minus Team B is the required direction for all eight features and the target. A negative value conveys direction, not an invalid measurement.
3. `goal_difference` is calculated from outcome goals, and `team_a_goals`, `team_b_goals`, and `result_note` must **not** enter the predictor matrix. They may be used solely for integrity checks or explanatory reporting.
4. The large X7 observation and other IQR flags should be investigated before model training. No outliers were removed, winsorised, or rescaled in this task. Their effect on the eventual model has not been tested.
5. Feature magnitudes differ substantially (for example Elo differences and rate differences), but no scaling has been done. Any preprocessing parameters in later stages must be learned from training data only to avoid leakage.
6. This task did **not** estimate correlations, fit regression coefficients, select variables, split train/test sets, or measure predictive performance. Completeness and arithmetic consistency alone cannot establish that all externally collected historical figures are accurate.

## Academic-integrity note

Generative AI assisted in drafting the Python script, validation checks, explanatory text, and report generation. Numerical results, counts, and flags are computed directly from the supplied worksheet by pandas and numpy. The work does **not** conduct external historical research, certify external source quality, or claim that reproducible calculations establish factual correctness of every upstream explanatory variable.
