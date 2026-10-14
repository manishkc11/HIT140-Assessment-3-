HIT140 Assessment 3 — Objective 2.1
Member 2: Multiple Linear Regression Model

CONTENTS
- FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting.xlsx: input data
- Task_2_1_Member_2_Regression_Model.ipynb: guided Jupyter notebook
- Task_2_1_Member_2_Regression_Model.py: stand-alone Python script for the repository
- Member2_Model_Outputs/Member2_predictions_for_evaluation.csv: actual/predicted values + train/test split for Member 3
- Member2_Model_Outputs/Member2_regression_coefficients.csv: model coefficients for Member 4
- Member2_Model_Outputs/Member2_linear_regression_model.joblib: fitted model
- Member2_Model_Outputs/Member2_model_settings.json: split details and predictors


SPLIT USED
- Chronological, approximately 80% training / 20% test (82 training, 22 testing).
- Training through 1 July 2026; testing from 2 July 2026.
- The split keeps all matches played on the same day in one set.

MODEL
- Target: goal_difference
- Exactly 8 predictors: fifa_rank_diff, elo_rating_diff, last5_avg_goals_scored_diff,
  last5_avg_goals_conceded_diff, last5_win_rate_diff, last5_clean_sheet_rate_diff,
  rest_days_diff, last5_opponent_strength_diff
- scikit-learn LinearRegression, fit_intercept=True
