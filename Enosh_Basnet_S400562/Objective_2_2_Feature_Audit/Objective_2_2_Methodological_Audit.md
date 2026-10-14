# Objective 2.2 — Targeted EDA, Feature Selection and Methodological Audit

**Decision: REVISION REQUIRED.** Source files inspected read-only. All quantitative calculations below are derived from the supplied 208-row dataset, source master, model outputs and Part 3 evaluation files. No model was retrained.

## 1. Confirmed dataset and construction

- Team-match observations: **208**, representing **104 unique football matches**, two linked team rows per match; not 208 independent fixtures.
- Exactly **8 explanatory variables** and one non-negative whole-number goal target. All model input columns contain numeric, nonmissing values. Duplicate match-side records: **0**.
- Team names, opponents, sides, dates and actual goals are consistent with the supplied master workbook: **0** mismatches. Uploaded master matches model's source master on all compared modelling fields: **yes**.
- X1–X4 team-level data match supporting X1_X2_Inputs and X3_X5_Detail sheets: **0 mismatches**. For cumulative features X7–X8, the source scores reconstruct each prior-day historical count/total exactly: **0 mismatches**.
- Previous-five detailed evidence has **1040 records**. Of 208 team histories, **208** have exactly five source observations; historical date-order failures: **0**; reconstructed goals-average mismatches: **0**; win-rate mismatches: **0**.
- Stage flag matches recorded group/knockout stage, and host flag equals Mexico/Canada/USA: **passed**. The host feature identifies team nationality, not confirmed venue-based home advantage.
- **Source verification boundary:** spreadsheet reconciliation and chronology are computationally verified. Federation/FIFA ranking releases, Elo-provider history and third-party international-results records are documented inputs, **not externally authenticated in this audit**.

## 2. Feature-reuse requirement — CRITICAL

The four explicitly reused concepts are FIFA ranking, Elo rating, previous-five average goals scored, and previous-five win rate (X1–X4). The new *knockout*, *host*, and *World Cup matches played* features are distinct. However, **X8 cumulative World Cup goals conceded uses the same substantive goals-conceded defensive statistic as Objective 2.1's X4 (previous-five average goals conceded difference)**. Different windows (World Cup cumulative vs last five), and differences versus team-level measurement, do not automatically make the concepts distinct. On a strict maximum-four-shared-*concepts* reading, this creates a **potential fifth overlap** and prevents unqualified certification of the requirement. **Required action:** confirm acceptance with lecturer/rubric; if counted as shared, the model owner must propose a different genuinely distinct pre-kickoff eighth feature and rerun only the necessary future modelling/review stages with training-only selection. No feature was changed here.

## 3. Descriptive EDA (208 team-match observations)

- Goals scored distribution: 0: 55 (26.4%), 1: 71 (34.1%), 2: 39 (18.8%), 3: 25 (12.0%), 4: 10 (4.8%), 5: 5 (2.4%), 6: 2 (1.0%), 7: 1 (0.5%).
- Mean goals: **1.481**, sample SD: **1.393**, range: **0–7**. For grouped stage breakdown, the observed mean is **1.493** for group-stage team rows (n=144) and **1.453** for knockout team rows (n=64). This is descriptive, not a causal stage effect.
- Host observations: **15/208 (7.2%)**. The host indicator and stage indicator are binary; zero-heavy early cumulative histories and 0.2-step last-five win rates have limited/discrete variation.
- All predictor means, SDs and quantiles are in `Objective_2_2_EDA_Summary.csv`; frequency counts in `Goals_Scored_Frequency.csv`.
- Training-only IQR flags for numerical candidate features (binary flags excluded): **4 feature-row flags**. IQR flags indicate candidates for checking, not bad data or automatic removals. They are recorded in `Training_IQR_Flags.csv`. Full-sample EDA is descriptive only.
- All-data Pearson correlations with goals scored: X1 = -0.367, X2 = +0.329, X3 = +0.222, X4 = +0.206, X5 = -0.013, X6 = +0.104, X7 = +0.026, X8 = -0.081. These are marginal associations, not significance tests, causation or guaranteed incremental effects.

## 4. Train/test distribution and generalisation — MODERATE

The existing date boundary is **2026-07-02**, with 164 training rows (82 matches) and 44 test rows (22 matches). Both sides of every match remain in the same partition. Training has **144 group and 20 knockout** team rows; testing has **0 group and 44 knockout** rows. The knockout indicator does vary in training, but only 12.2% of training rows are knockout compared with 100% in testing.

Host nation rows: **12 train** and **3 test**; this small sample limits a stable separate host effect. World Cup matches played before the fixture range **0–3 in training** versus **3–7 in testing**, leaving **32 test rows outside the training range**. Elo additionally has **7 test rows beyond the observed training range**. This is direct evidence of covariate shift/extrapolation risk, not proof any single variable caused poor performance. See `Train_Test_Feature_Shift.csv`.

## 5. Correlation, redundancy and VIF (training only)

Predictor correlations from 164 train rows: rank vs Elo **-0.899**, goals-scored form vs win rate **+0.764**, prior WC matches vs cumulative WC conceded **+0.622**; knockout vs prior WC matches **+0.650**. VIF from auxiliary least-squares regressions **with an intercept**: X2 6.17, X1 5.70, X4 3.10, X7 2.91, X3 2.57, X8 2.22, X5 1.81, X6 1.13. VIF was independently cross-checked against the diagonal of the inverse training predictor-correlation matrix. Interpret thresholds above 5 as a prompt for investigation, not an instruction to delete any predictor. Neither pairwise correlation nor VIF establishes independent predictive contribution.

## 6. Saved model results — MODERATE limitation

From saved `Predictions.csv` and `Metrics.csv` (no new fitting): **test MAE 0.982 goals**, **RMSE 1.266 goals**, and **R² 0.084**. Training R² is **0.188**. The saved mean-predictor baseline has test MAE **1.065** and RMSE **1.324**. Recomputed saved-prediction metric discrepancies are below **1.11e-16**.

Part 3 evaluation reports the supplied OLS test MAE/RMSE/R² as **0.982/1.266/0.084**. Its saved Ridge result is **MAE 1.003, RMSE 1.275, R² 0.070** and Lasso **MAE 1.035, RMSE 1.288, R² 0.052**; Part 3 reports a training-CV-selected **Lasso alpha 0.1**. These are **existing evaluation outputs**, not newly fitted or selected models in this audit. Avoid using final test performance to select explanatory variables.

## 7. Recommendations by severity

- **CRITICAL — Shared-feature rule:** Obtain written clarification of whether cumulative prior WC goals conceded counts as the same goals-conceded concept as Objective 2.1. A strict reading implies five shared concepts. Affected: Objective 2.2 predictor definition, `Regression_2_2.py`, dataset and saved fitted model **if** replacement is needed; no changes made here.
- **MODERATE — Distribution shift:** Training covers only 10 knockout matches (20 team rows), while test covers 22 knockout matches. 32 test rows exceed the training experience range. Report this and interpret performance as later-stage generalisation, not uniform performance across the tournament. Affected: final 4-page Word report/methodology language, not current data.
- **MODERATE — Provenance:** X1–X4 rolling historical source data are computationally reconciled but official date-specific publications and every source match were not independently authenticated here. Affected: dataset methodology/evidence statement and source documentation; investigate records if independent audit finds conflict.
- **MINOR — Observational dependence and count outcome:** Each fixture contributes two related team rows; goals are discrete and non-negative while ordinary linear regression is unbounded. Avoid treating 208 rows as independent matches or interpreting coefficients causally. Affected: final report limitations and later statistical inference.

## 8. Recommended illustration and academic disclosure

Prefer **Figure D (Training vs Testing Feature Distributions)** in the four-page report: it conveys the large knockout/experience shift underlying limited generalisation. Figure A is a good alternative when the section emphasises the outcome distribution. Figure B is training-only by design; Figure C is descriptive and uses all 208 observations. All at 320 DPI.

**AI assistance:** A generative AI system assisted in inspecting the provided source files, drafting auditing code and source classifications, carrying out calculations, generating graphics and preparing the written interpretation. Source-book numerical reconciliation and script tests are independently reproducible; **external publication authenticity and every historical entry were not independently verified by those tests**. No original workbook, source ZIP, model output or past project file was altered. No model was retrained, tuned or replaced.
