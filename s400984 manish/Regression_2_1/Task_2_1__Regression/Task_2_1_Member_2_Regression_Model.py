"""HIT140 Assessment 3: Member 2 multiple linear regression.
Use verified group data and disclose AI assistance as required.
"""

from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from joblib import dump

# Keep the Excel file in the same folder as this notebook.
DATA_FILE = Path("FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting.xlsx")
SHEET_NAME = "Master_104_Matches"
OUTPUT_DIR = Path("Member2_Model_Outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"{DATA_FILE} not found. Place the Excel file beside this notebook."
    )

df = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME)
print("Rows:", len(df))
print("Available columns:", df.columns.tolist())


# The ONLY eight explanatory variables in Regression 2.1.
X_COLUMNS = [
    "fifa_rank_diff",                    # X1
    "elo_rating_diff",                   # X2
    "last5_avg_goals_scored_diff",       # X3
    "last5_avg_goals_conceded_diff",     # X4
    "last5_win_rate_diff",               # X5
    "last5_clean_sheet_rate_diff",       # X6
    "rest_days_diff",                    # X7
    "last5_opponent_strength_diff",      # X8
]
Y_COLUMN = "goal_difference"
NEEDED = ["match_id", "match_date", "team_a", "team_b"] + X_COLUMNS + [Y_COLUMN]

assert len(X_COLUMNS) == len(set(X_COLUMNS)) == 8
assert len(df) == 104, f"Expected 104 matches, found {len(df)}"
assert df["match_id"].is_unique, "Duplicate match IDs found"
assert set(NEEDED).issubset(df.columns), f"Missing columns: {set(NEEDED)-set(df.columns)}"

# Validate values, never silently replace missing predictors with zero.
for col in X_COLUMNS + [Y_COLUMN]:
    df[col] = pd.to_numeric(df[col], errors="raise")
assert not df[NEEDED].isna().any().any(), "Missing values in model inputs"
assert np.isfinite(df[X_COLUMNS + [Y_COLUMN]].to_numpy(dtype=float)).all(), "Non-finite values found"
assert np.allclose(df["team_a_goals"] - df["team_b_goals"], df[Y_COLUMN]), "Goal difference mismatch"

# Date order matters because the objective is prediction before kickoff.
df["match_date"] = pd.to_datetime(df["match_date"])
df = df.sort_values(["match_date", "match_id"]).reset_index(drop=True)
print("Validated:",len(df),"matches, 8 predictors, no missing model inputs.")


# Chronological 80/20 split: no later match is used to fit earlier predictions.
# Tell Member 3 the exact split, and use the same predictions when evaluating.
desired_train_size = int(len(df) * 0.80)
# Keep every match played on the same calendar date on the same side.
possible_test_start_dates = df["match_date"].drop_duplicates().sort_values().iloc[1:]
test_start_date = min(
    possible_test_start_dates,
    key=lambda date: abs((df["match_date"] < date).sum() - desired_train_size),
)
train = df.loc[df["match_date"] < test_start_date].copy()
test = df.loc[df["match_date"] >= test_start_date].copy()
X_train, y_train = train[X_COLUMNS], train[Y_COLUMN]
X_test, y_test = test[X_COLUMNS], test[Y_COLUMN]

print(f"Training rows: {len(train)}; Testing rows: {len(test)}")
print("Last training match:", train.iloc[-1]["match_id"], train.iloc[-1]["match_date"].date())
print("First test match:", test.iloc[0]["match_id"], test.iloc[0]["match_date"].date())


# Fit ONE multiple linear regression, with all eight X variables together.
model = LinearRegression(fit_intercept=True)
model.fit(X_train, y_train)

coefs = pd.DataFrame({"variable": X_COLUMNS, "coefficient": model.coef_})
intercept = float(model.intercept_)
print("Intercept:", round(intercept, 5))
print(coefs.to_string(index=False))
print("\nEquation: Predicted goal difference = intercept + sum(coefficient_i × X_i)")


# Member 3 uses this file for R², MAE, RMSE and residual analysis.
# Member 4 uses the coefficients to discuss associations and limitations.
cols = ["match_id", "match_date", "team_a", "team_b", Y_COLUMN]
train_predictions = train[cols].copy()
test_predictions = test[cols].copy()
train_predictions["predicted_goal_difference"] = model.predict(X_train)
test_predictions["predicted_goal_difference"] = model.predict(X_test)
train_predictions["dataset_split"] = "train"
test_predictions["dataset_split"] = "test"
all_predictions = pd.concat([train_predictions, test_predictions], ignore_index=True)

all_predictions.to_csv(OUTPUT_DIR / "Member2_predictions_for_evaluation.csv", index=False)
coefs.to_csv(OUTPUT_DIR / "Member2_regression_coefficients.csv", index=False)
dump(model, OUTPUT_DIR / "Member2_linear_regression_model.joblib")

# Record model setup so teammates can reproduce it.
import json
metadata = {
    "input_file": DATA_FILE.name,
    "sheet_name": SHEET_NAME,
    "model": "scikit-learn LinearRegression(fit_intercept=True)",
    "target": Y_COLUMN,
    "features": X_COLUMNS,
    "split": "chronological by match date, approximate 80% training, no date split",
    "train_n": len(train), "test_n": len(test),
    "train_match_ids": train["match_id"].astype(int).tolist(),
    "test_match_ids": test["match_id"].astype(int).tolist(),
    "intercept": intercept,
    "note": "Evaluate the test set with Member 3; do not treat coefficients as causal effects."
}
with open(OUTPUT_DIR / "Member2_model_settings.json", "w", encoding="utf-8") as fh:
    json.dump(metadata, fh, indent=2)

print("Saved in:", OUTPUT_DIR.resolve())
print("Files:")
for p in sorted(OUTPUT_DIR.iterdir()):
    print(" -", p.name)
print("\nPreview of held-out match predictions:")
print(test_predictions.head(5).to_string(index=False))
