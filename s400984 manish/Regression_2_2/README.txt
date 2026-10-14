HIT140 | OBJECTIVE 2 | LINEAR REGRESSION 2.2
==============================================

PURPOSE
Predict the number of goals scored by one team in a 2026 FIFA World Cup match.
104 actual matches -> 208 team-match observations; exactly 8 pre-match explanatory variables.

START HERE
1. Extract this ZIP in full; do not open individual files directly inside the ZIP.
2. Open Regression_2_2.ipynb in Jupyter Notebook from this extracted folder.
3. Saved outputs and graphs are already visible in the notebook.
4. To reproduce all calculations select Kernel -> Restart & Run All.
5. The notebook reads data/Source_104_Matches.xlsx. Do not move that workbook without updating the code path.

WHICH FILE IS WHICH
Regression_2_2.ipynb            Executed Jupyter notebook; primary code + visible results.
Regression_2_2.py               Equivalent Python script (run from this folder).
data/Source_104_Matches.xlsx    Original source workbook (104 matches + supporting sheets).
data/Regression_2_2_208_Team_Rows.csv
                               FINAL DATASET: 208 observations with X1-X8 and goal target.
outputs/Predictions.csv         Actual and predicted goals, with train/test labels.
outputs/Coefficients.csv        Eight fitted model coefficients.
outputs/Metrics.csv             Training/testing regression scores and baseline comparison.
outputs/Actual_vs_Predicted.png Diagnostic figure generated in Python.
outputs/Test_Residuals.png      Residuals figure generated in Python.
outputs/Trained_Model.joblib    Serialized binary model, load through joblib in Python.
outputs/Model_Settings.json    Model configuration, counts, predictor names and metrics.

PREDICTORS (THESE ARE THE ONLY EIGHT REGRESSION X VARIABLES)
X1 team_fifa_rank                  Team pre-match FIFA rank. Shared underlying concept with 2.1.
X2 team_elo_rating_before          Team pre-match Elo rating. Shared underlying concept with 2.1.
X3 team_last5_avg_goals_scored     Five-match scoring form. Shared underlying concept with 2.1.
X4 team_last5_win_rate             Five-match win rate. Shared underlying concept with 2.1.
X5 is_knockout                     1 for knockout, 0 for group stage. New.
X6 is_host_nation                  1 for host team, 0 otherwise. New.
X7 wc_matches_played_before        Prior completed WC matches. New.
X8 wc_goals_conceded_before        Goals conceded in earlier WC matches. New.
Target Y: goals_scored             Actual number of match goals scored by the team.

The extra match_id, match_date, team, opponent, side, and stage columns are
identifiers or descriptors: they are NOT features in the fitted regression.

SOURCE WORKBOOK NOTES
The workbook has multiple TABS, not multiple Excel workbooks. Only these
three tabs are directly read by Python: Master_104_Matches, X1_X2_Inputs,
X3_X5_Detail. Other tabs (Last5_Evidence, Used_Source_Matches, X3_X5_Methodology,
X4_X6_Audit, Merge_Notes, Data_Rules) preserve provenance/working evidence.
Keep them for reproducibility; only one Excel workbook is included.

CHECKED MODEL RUN (time-ordered split)
104 matches / 208 team rows; 82 training matches (164 team rows),
22 testing matches (44 team rows).
Test MAE ~0.982 goals; Test RMSE ~1.266 goals; Test R-squared ~0.084.
Accuracy is modest. Do not overclaim predictive power.

SUBMISSION AND ACADEMIC INTEGRITY
Upload code/dataset to your group's ONE approved repository and include its
URL in the group's required text file. The final assignment ZIP also needs
the ONE group Word report, Turnitin originality report, and fully signed AI
Usage Declaration form. The report must be written by the group in its own
words; AI support for code must be declared. Verify all pre-match statistics
and sources independently before the deadline.

BINARY MODEL NOTE
Do not double-click outputs/Trained_Model.joblib in Jupyter's text editor;
it is not UTF-8 text. View training results in the .ipynb notebook or load
it with joblib.load() in a trusted Python environment.

Python libraries: numpy, pandas, matplotlib, scikit-learn, joblib, ipython,
openpyxl (used by pandas to read the source XLSX), jupyter, nbclient (optional).
