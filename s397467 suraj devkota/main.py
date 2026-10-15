
"""
PRT565 Assessment 3
FIFA World Cup 2026 - Linear Regression 2.1 and 2.2

Input files:
    data/regression_2_1.csv
    data/regression_2_2.csv

All explanatory variables must be pre-match variables.
No missing values are silently replaced.
"""

from pathlib import Path
import json
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split, GroupShuffleSplit
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

warnings.filterwarnings("default")

# --------------------------------------------------
# 1. PROJECT FOLDERS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RESULTS_DIR = BASE_DIR / "results"
FIGURES_DIR = BASE_DIR / "figures"

for folder in [DATA_DIR, RESULTS_DIR, FIGURES_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

RANDOM_STATE = 42
TEST_SIZE = 0.20

# --------------------------------------------------
# 2. VARIABLE DEFINITIONS
# --------------------------------------------------

MODEL_21_FEATURES = [
    "FIFA_Rank_Diff",
    "Elo_Diff",
    "Last5_Goals_Scored_Diff",
    "Last5_Goals_Conceded_Diff",
    "Last5_Win_Rate_Diff",
    "Last5_Clean_Sheet_Rate_Diff",
    "Rest_Days_Diff",
    "Opponent_Rank_Diff"
]

MODEL_22_FEATURES = [
    "FIFA_Rank",
    "Elo_Rating",
    "Last5_Avg_Goals_Scored",
    "Last5_Win_Rate",
    "Knockout_Stage",
    "Host_Nation",
    "Prior_WC_Matches",
    "Prior_WC_Goals_Conceded"
]

# --------------------------------------------------
# 3. DATA VALIDATION
# --------------------------------------------------

def load_and_validate(file_path, expected_rows, features, target):
    """Load data and verify its structure before modelling."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"\nMissing input file: {file_path}\n"
            "Prepare the real dataset and save it in the data folder."
        )

    df = pd.read_csv(file_path)

    required = ["Match_ID"] + features + [target]
    missing_columns = [c for c in required if c not in df.columns]

    if missing_columns:
        raise ValueError(
            f"{file_path.name}: Missing columns: {missing_columns}"
        )

    if len(df) != expected_rows:
        raise ValueError(
            f"{file_path.name}: Expected {expected_rows} rows, "
            f"but found {len(df)}."
        )

    if df["Match_ID"].isna().any():
        raise ValueError("Match_ID contains missing values.")

    if df["Match_ID"].nunique() != (
        104 if expected_rows == 104 else 104
    ):
        raise ValueError(
            f"{file_path.name}: Expected 104 unique matches."
        )

    # Keep only the ID, eight predictors, and target.
    df = df[required].copy()

    # Convert predictors and target to numeric values.
    for column in features + [target]:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    numeric_columns = features + [target]

    if df[numeric_columns].isna().any().any():
        bad_counts = df[numeric_columns].isna().sum()
        bad_counts = bad_counts[bad_counts > 0].to_dict()

        raise ValueError(
            f"{file_path.name}: Missing or non-numeric values found: "
            f"{bad_counts}. Check and document these values; "
            "do not automatically replace missing values with zero."
        )

    if not np.isfinite(df[numeric_columns].to_numpy()).all():
        raise ValueError(
            f"{file_path.name}: Infinite values found."
        )

    if df[features].nunique().eq(1).any():
        constant_columns = df[features].columns[
            df[features].nunique().eq(1)
        ].tolist()
        raise ValueError(
            f"Constant predictor(s) found: {constant_columns}"
        )

    return df


# --------------------------------------------------
# 4. MODEL TRAINING AND EVALUATION
# --------------------------------------------------

def run_regression(
    df,
    features,
    target,
    model_name,
    group_split=False
):
    """Fit a linear regression and save evaluation outputs."""

    X = df[features]
    y = df[target]

    # Chronological split: reserve the latest 22 matches for testing.
    # This also keeps both team rows together in Regression 2.2.
    if "Match_Date" not in df.columns:
        raise ValueError(
            "Match_Date is missing. Check the date merge in main()."
        )

    match_order = (
        df[["Match_ID", "Match_Date"]]
        .drop_duplicates()
        .sort_values(["Match_Date", "Match_ID"])
    )

    if len(match_order) != 104:
        raise ValueError("Expected 104 unique matches for the split.")

    test_match_ids = set(match_order.tail(22)["Match_ID"])
    test_mask = df["Match_ID"].isin(test_match_ids).to_numpy()

    train_idx = np.flatnonzero(~test_mask)
    test_idx = np.flatnonzero(test_mask)

    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model = LinearRegression()
    model.fit(X_train, y_train)

    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)

    # Evaluation metrics on held-out test data.
    r2 = r2_score(y_test, test_predictions)
    mae = mean_absolute_error(y_test, test_predictions)
    rmse = np.sqrt(mean_squared_error(y_test, test_predictions))

    n_test = len(y_test)
    p = len(features)

    if n_test > p + 1:
        adjusted_r2 = (
            1 - (1 - r2) * (n_test - 1) / (n_test - p - 1)
        )
    else:
        adjusted_r2 = np.nan

    metrics = {
        "Model": model_name,
        "Total_Rows": len(df),
        "Training_Rows": len(X_train),
        "Testing_Rows": len(X_test),
        "Number_of_Predictors": len(features),
        "Train_R2": r2_score(y_train, train_predictions),
        "Test_R2": r2,
        "Adjusted_Test_R2": adjusted_r2,
        "Test_MAE": mae,
        "Test_RMSE": rmse
    }

    # Save metrics.
    pd.DataFrame([metrics]).to_csv(
        RESULTS_DIR / f"{model_name}_metrics.csv",
        index=False
    )

    # Save coefficients and intercept.
    coefficients = pd.DataFrame({
        "Variable": features,
        "Coefficient": model.coef_
    })

    coefficients.loc[len(coefficients)] = [
        "Intercept", model.intercept_
    ]

    coefficients.to_csv(
        RESULTS_DIR / f"{model_name}_coefficients.csv",
        index=False
    )

    # Save predictions and residuals.
    predictions = pd.DataFrame({
        "Match_ID": df.iloc[test_idx]["Match_ID"].to_numpy(),
        "Actual": y_test.to_numpy(),
        "Predicted": test_predictions,
        "Residual": y_test.to_numpy() - test_predictions
    })

    predictions.to_csv(
        RESULTS_DIR / f"{model_name}_predictions.csv",
        index=False
    )

    # Graph 1: Actual versus predicted.
    plt.figure(figsize=(7, 5))
    plt.scatter(y_test, test_predictions, alpha=0.75)

    low = min(y_test.min(), test_predictions.min())
    high = max(y_test.max(), test_predictions.max())
    plt.plot([low, high], [low, high], linestyle="--")

    plt.xlabel("Actual values")
    plt.ylabel("Predicted values")
    plt.title(f"{model_name}: Actual vs Predicted")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / f"{model_name}_actual_vs_predicted.png",
        dpi=300
    )
    plt.close()

    # Graph 2: Residuals versus predicted values.
    residuals = y_test.to_numpy() - test_predictions

    plt.figure(figsize=(7, 5))
    plt.scatter(test_predictions, residuals, alpha=0.75)
    plt.axhline(0, linestyle="--")

    plt.xlabel("Predicted values")
    plt.ylabel("Residuals")
    plt.title(f"{model_name}: Residual Plot")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / f"{model_name}_residuals.png",
        dpi=300
    )
    plt.close()

    # Graph 3: Residual distribution.
    plt.figure(figsize=(7, 5))
    plt.hist(residuals, bins=12, edgecolor="black")
    plt.xlabel("Residual")
    plt.ylabel("Frequency")
    plt.title(f"{model_name}: Residual Distribution")
    plt.tight_layout()

    plt.savefig(
        FIGURES_DIR / f"{model_name}_residual_distribution.png",
        dpi=300
    )
    plt.close()

    print(f"\n{'=' * 55}")
    print(model_name)
    print(f"{'=' * 55}")

    for key, value in metrics.items():
        if isinstance(value, (float, np.floating)):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    print("Coefficients and predictions saved.")
    print("Evaluation figures saved.")

    return metrics


# --------------------------------------------------
# 5. MAIN PROGRAM
# --------------------------------------------------

def main():

    print("PRT565 Assessment 3")
    print("FIFA World Cup 2026 Regression Analysis")

    # Model 2.1: Predict match goal difference.
    data_21 = load_and_validate(
        DATA_DIR / "regression_2_1.csv",
        expected_rows=104,
        features=MODEL_21_FEATURES,
        target="Goal_Difference"
    )

    # Model 2.2: Predict one team's goals per match.
    data_22 = load_and_validate(
        DATA_DIR / "regression_2_2.csv",
        expected_rows=208,
        features=MODEL_22_FEATURES,
        target="Goals_Scored"
    )

    # Attach the actual match dates from the Excel workbook.
    date_lookup = pd.read_excel(
        BASE_DIR / "model pedition .xlsx",
        sheet_name="Master_104_Matches",
        usecols=["match_id", "match_date"]
    ).rename(columns={
        "match_id": "Match_ID",
        "match_date": "Match_Date"
    })

    date_lookup["Match_Date"] = pd.to_datetime(
        date_lookup["Match_Date"]
    )

    data_21 = data_21.merge(
        date_lookup,
        on="Match_ID",
        how="left",
        validate="one_to_one"
    )

    data_22 = data_22.merge(
        date_lookup,
        on="Match_ID",
        how="left",
        validate="many_to_one"
    )

    if data_21["Match_Date"].isna().any() or data_22["Match_Date"].isna().any():
        raise ValueError("Some matches are missing dates in the workbook.")

    # Verify that both models cover the same match IDs.
    matches_21 = set(data_21["Match_ID"])
    matches_22 = set(data_22["Match_ID"])

    if matches_21 != matches_22:
        raise ValueError(
            "The two datasets do not contain the same 104 match IDs."
        )

    # Check that each match has two team-level observations.
    rows_per_match = data_22.groupby("Match_ID").size()

    if not (rows_per_match == 2).all():
        raise ValueError(
            "Regression 2.2 must contain exactly two team rows per match."
        )

    # Verify that the two datasets use at most four shared
    # conceptual predictors.
    # Rank, Elo, recent goals scored, and recent xG are shared.
    shared_variables = {
        "FIFA ranking",
        "Elo rating",
        "Last-5 average goals scored",
        "Last-5 average xG"
    }

    if len(shared_variables) > 4:
        raise ValueError("More than four shared predictors.")

    print("\nDataset validation passed.")
    print(f"Regression 2.1 rows: {len(data_21)}")
    print(f"Regression 2.2 rows: {len(data_22)}")
    print("Eight predictors are specified for each model.")

    result_21 = run_regression(
        data_21,
        MODEL_21_FEATURES,
        "Goal_Difference",
        "Regression_2_1",
        group_split=False
    )

    result_22 = run_regression(
        data_22,
        MODEL_22_FEATURES,
        "Goals_Scored",
        "Regression_2_2",
        group_split=True
    )

    # Save a combined model comparison.
    comparison = pd.DataFrame([result_21, result_22])

    comparison.to_csv(
        RESULTS_DIR / "model_comparison.csv",
        index=False
    )

    with open(
        RESULTS_DIR / "run_summary.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            comparison.to_dict(orient="records"),
            file,
            indent=4,
            default=lambda x: (
                None if pd.isna(x) else float(x)
            )
        )

    print("\nAnalysis completed successfully.")
    print(f"Results folder: {RESULTS_DIR}")
    print(f"Figures folder: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
