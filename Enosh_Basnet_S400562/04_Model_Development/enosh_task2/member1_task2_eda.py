#!/usr/bin/env python3
"""FIFA World Cup 2026 | Member 1, Task 2: univariate and bivariate EDA.

AI-use disclosure: Generative AI assisted with the Matplotlib code, EDA text,
chart-design choices, and programmatic validation. All plotted points and
reported statistics are calculated directly from the supplied workbook.
No external match sources are read, no models are fitted, and the original
workbook is never written to.

Example (macOS):
  python3 member1_task2_eda.py \
    --input 'FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting.xlsx' \
    --output-dir .

Dependencies: pandas, openpyxl, numpy, matplotlib (requirements file).
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Generate files without a graphical display.
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

SHEET = "Master_104_Matches"
FEATURES = [
    ("X1", "fifa_rank_diff", "FIFA rank difference", "FIFA ranking positions"),
    ("X2", "elo_rating_diff", "Elo rating difference", "Elo points"),
    ("X3", "last5_avg_goals_scored_diff", "Last-five average goals scored difference", "Goals per match"),
    ("X4", "last5_avg_goals_conceded_diff", "Last-five average goals conceded difference", "Goals per match"),
    ("X5", "last5_win_rate_diff", "Last-five win-rate difference", "Proportion (−1 to +1)"),
    ("X6", "last5_clean_sheet_rate_diff", "Last-five clean-sheet-rate difference", "Proportion (−1 to +1)"),
    ("X7", "rest_days_diff", "Rest-days difference", "Calendar days"),
    ("X8", "last5_opponent_strength_diff", "Last-five opponent-strength difference", "FIFA ranking positions"),
]
TARGET = "goal_difference"
NAVY = "#23395B"
TEAL = "#127F80"
CORAL = "#C46C49"
GREY = "#777D86"
AMBER = "#BB7830"
GRID = "#DBE2EA"
MUTED = "#526072"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def style_charts() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 10,
        "axes.titlesize": 12, "axes.titleweight": "semibold",
        "axes.labelsize": 10, "axes.edgecolor": GRID,
        "axes.labelcolor": NAVY, "text.color": NAVY,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "grid.color": GRID, "grid.alpha": 0.7,
        "axes.spines.top": False, "axes.spines.right": False,
        "figure.facecolor": "white", "axes.facecolor": "white",
        "savefig.facecolor": "white", "savefig.dpi": 320,
    })


def finish(fig: plt.Figure, destination: Path) -> None:
    fig.savefig(destination, dpi=320, bbox_inches="tight", pad_inches=0.24)
    plt.close(fig)


def load_and_check(workbook: Path) -> tuple[pd.DataFrame, pd.DataFrame, list[dict]]:
    # The workbook is opened read-only by pandas. There is no Excel writer.
    df = pd.read_excel(workbook, sheet_name=SHEET, engine="openpyxl")
    required = {"match_id", "match_date", "team_a", "team_b", "team_a_goals", "team_b_goals", TARGET}
    required.update(name for _, name, _, _ in FEATURES)
    absent = sorted(required - set(df.columns))
    if absent:
        raise ValueError(f"Missing required workbook columns: {absent}")
    if len(df) != 104:
        raise ValueError(f"Expected 104 records; found {len(df)}")
    ids = pd.to_numeric(df["match_id"], errors="raise")
    if ids.isna().any() or len(set(ids)) != 104 or set(ids) != set(range(1, 105)):
        raise ValueError("Match IDs are not a complete unique set from 1 to 104")
    modelling_columns = [name for _, name, _, _ in FEATURES] + [TARGET]
    clean_numeric = df[modelling_columns].apply(pd.to_numeric, errors="coerce")
    if clean_numeric.isna().any().any():
        raise ValueError(f"Modelling values are missing or nonnumeric: {clean_numeric.isna().sum().to_dict()}")
    if not np.isfinite(clean_numeric.to_numpy(dtype=float)).all():
        raise ValueError("Non-finite modelling values were encountered")
    actual = pd.to_numeric(df["team_a_goals"], errors="raise") - pd.to_numeric(df["team_b_goals"], errors="raise")
    if not (df[TARGET].to_numpy() == actual.to_numpy()).all():
        raise ValueError("Target does not equal Team A goals minus Team B goals")
    dates = pd.to_datetime(df["match_date"], errors="raise")
    if dates.isna().any() or not dates.between("2026-06-11", "2026-07-19").all():
        raise ValueError("Invalid or out-of-tournament match date")
    for col in ("last5_win_rate_diff", "last5_clean_sheet_rate_diff"):
        if not df[col].between(-1, 1).all():
            raise ValueError(f"Invalid rate difference in {col}")
    if df.duplicated().any():
        raise ValueError("Complete duplicate workbook rows found")
    m13 = df.loc[ids == 13, "rest_days_diff"]
    if len(m13) != 1 or float(m13.iloc[0]) != -70:
        raise ValueError("Expected Match 13 to have X7 = −70, but it differs in the input")
    vcounts = df[TARGET].value_counts()
    pos = int(df[TARGET].gt(0).sum())
    neg = int(df[TARGET].lt(0).sum())
    zero = int(df[TARGET].eq(0).sum())
    if (pos, neg, zero) != (50, 30, 24) or vcounts.sum() != 104:
        raise ValueError(f"Unexpected target frequencies: {pos} positive, {neg} negative, {zero} zero")
    outliers = []
    for code, col, label, unit in FEATURES:
        values = df[col].astype(float)
        q1, q3 = values.quantile([.25, .75])
        low, high = q1 - 1.5 * (q3 - q1), q3 + 1.5 * (q3 - q1)
        flagged = df.loc[(values < low) | (values > high), ["match_id", col]]
        for _, row in flagged.iterrows():
            outliers.append(dict(match_id=int(row["match_id"]), feature=code,
                                 column=col, value=float(row[col]), lower=float(low), upper=float(high)))
    if len(outliers) != 18:
        raise ValueError(f"Expected 18 feature-specific IQR flags, found {len(outliers)}")
    return df, clean_numeric, outliers


def integer_bins(values: np.ndarray) -> np.ndarray:
    return np.arange(int(np.floor(values.min())) - .5, int(np.ceil(values.max())) + 1.5, 1)


def figure1(df: pd.DataFrame, dest: Path) -> None:
    frequencies = df[TARGET].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(12, 5.8), constrained_layout=True)
    colors = [CORAL if v < 0 else GREY if v == 0 else TEAL for v in frequencies.index]
    bars = ax.bar(frequencies.index.astype(int), frequencies.values, width=.79,
                  color=colors, edgecolor="white", linewidth=.9, zorder=3)
    for bar, freq in zip(bars, frequencies.values):
        ax.annotate(str(int(freq)), (bar.get_x()+bar.get_width()/2, bar.get_height()),
                    xytext=(0, 4), textcoords="offset points", ha="center",
                    va="bottom", fontsize=10, fontweight="semibold")
    ax.set_title("Figure 1  |  Actual goal-difference distribution", loc="left", fontsize=16, pad=19)
    ax.set_xlabel("Actual goal difference (Team A goals − Team B goals)")
    ax.set_ylabel("Number of matches")
    ax.set_xticks(frequencies.index.astype(int))
    ax.set_ylim(0, max(frequencies.values) + 6)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.grid(axis="y", zorder=0)
    ax.legend(handles=[Patch(facecolor=CORAL,label="Negative: Team B scored more (30)"),
                       Patch(facecolor=GREY,label="Zero: Equal goals (24)"),
                       Patch(facecolor=TEAL,label="Positive: Team A scored more (50)")],
              loc="upper center", bbox_to_anchor=(.5,1.02), ncol=3, frameon=False, fontsize=9)
    ax.text(1.0, -0.17, "N = 104  |  Outcome values, not model predictions",
            transform=ax.transAxes, ha="right", fontsize=9, color=MUTED)
    finish(fig, dest)


def bins_for(code: str, values: np.ndarray) -> np.ndarray:
    if code == "X7":
        return integer_bins(values)
    if code in {"X5", "X6"}:
        return np.arange(-1.1, 1.10001, .2)
    raw = np.histogram_bin_edges(values, bins="fd")
    # Bounded bin counts keep small panels legible and comparable as figures.
    count = max(8, min(18, len(raw)-1))
    return np.linspace(float(values.min()), float(values.max()), count+1)


def figure2(df: pd.DataFrame, dest: Path) -> None:
    fig, axs = plt.subplots(4, 2, figsize=(15, 16), constrained_layout=True)
    fig.suptitle("Figure 2  |  Distributions of the eight explanatory variables",
                 x=.02, ha="left", fontsize=17, fontweight="bold")
    for ax, (code, col, label, unit) in zip(axs.flat, FEATURES):
        values = df[col].to_numpy(dtype=float)
        ax.hist(values, bins=bins_for(code, values), color=TEAL, edgecolor="white",
                linewidth=.65, alpha=.9, zorder=2)
        ax.axvline(0, color=GREY, linestyle="--", linewidth=1, alpha=.85,
                   label="Zero difference")
        ax.set_title(f"{code}  ·  {label}", loc="left", fontsize=11, pad=10)
        ax.set_xlabel(f"Difference ({unit})", fontsize=9)
        ax.set_ylabel("Matches", fontsize=9)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=5))
        ax.grid(axis="y", alpha=.55, zorder=0)
        ax.tick_params(labelsize=9)
        if code == "X7":
            ax.annotate("Match 13: −70", xy=(-70, 1), xytext=(-61, 15),
                        arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.3),
                        fontsize=9, color=CORAL, fontweight="semibold")
            inset = ax.inset_axes([.28, .24, .60, .44])
            inset.hist(values, bins=np.arange(-8.5, 7.5, 1), color=TEAL,
                       edgecolor="white", linewidth=.4)
            inset.set_xlim(-8.7, 7)
            inset.set_title("Detail: −8 to +6 days", fontsize=8)
            inset.tick_params(labelsize=7)
            for spine in inset.spines.values():
                spine.set_color(GRID)
    finish(fig, dest)


def figure3(df: pd.DataFrame, outliers: list[dict], dest: Path) -> None:
    fig, axs = plt.subplots(4, 2, figsize=(15, 14), constrained_layout=True)
    fig.suptitle("Figure 3  |  Feature boxplots with separate numerical scales",
                 x=.02, ha="left", fontsize=17, fontweight="bold")
    for ax, (code, col, label, unit) in zip(axs.flat, FEATURES):
        vals = df[col].to_numpy(dtype=float)
        ax.boxplot([vals], vert=False, widths=.36, patch_artist=True,
                   boxprops=dict(facecolor="#D0E9E7", edgecolor=TEAL, linewidth=1.4),
                   medianprops=dict(color=NAVY, linewidth=2),
                   whiskerprops=dict(color=TEAL, linewidth=1.2),
                   capprops=dict(color=TEAL, linewidth=1.2),
                   flierprops=dict(marker="o", markerfacecolor=CORAL,
                                   markeredgecolor="white", markersize=6, alpha=.95))
        ax.axvline(0, color=GREY, linestyle="--", linewidth=1, alpha=.75)
        ax.set_yticks([])
        ax.set_title(f"{code}  ·  {label}", loc="left", fontsize=11, pad=8)
        ax.set_xlabel(f"Difference ({unit})", fontsize=9)
        ax.grid(axis="x", alpha=.58)
        nflags = sum(z["column"] == col for z in outliers)
        ax.text(.99, .91, f"{nflags} IQR flag{'s' if nflags!=1 else ''}  |  n = 104",
                transform=ax.transAxes, ha="right", va="top", fontsize=8, color=MUTED)
        if code == "X7":
            ax.annotate("ID 13: −70", xy=(-70, 1), xytext=(-48, 1.23),
                        color=CORAL, fontsize=9, fontweight="semibold",
                        arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.25))
    finish(fig, dest)


def figure4(df: pd.DataFrame, dest: Path) -> tuple[float, float, float, float]:
    full = df["rest_days_diff"].to_numpy(dtype=float)
    visual_only = df.loc[df["match_id"] != 13, "rest_days_diff"].to_numpy(dtype=float)
    m1, s1 = float(np.mean(full)), float(np.std(full, ddof=1))
    m2, s2 = float(np.mean(visual_only)), float(np.std(visual_only, ddof=1))
    fig, axs = plt.subplots(1, 2, figsize=(15, 6.1), constrained_layout=True)
    fig.suptitle("Figure 4  |  X7 rest days: visual sensitivity to Match 13",
                 fontsize=16, fontweight="bold")
    a, b = axs
    a.hist(full, bins=integer_bins(full), color=TEAL, edgecolor="white", linewidth=.5)
    a.annotate("Match 13: X7 = −70", xy=(-70, 1), xytext=(-57, 23),
               arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.7),
               fontsize=11, color=CORAL, fontweight="bold")
    a.set_xlim(-74, 9)
    a.set_xticks([-70, -8, -4, 0, 4, 6])
    a.set_title("A. All 104 matches", loc="left", pad=12)
    b.hist(visual_only, bins=integer_bins(visual_only), color=NAVY,
           edgecolor="white", linewidth=.65)
    b.set_title("B. Visual comparison only: 103 matches (ID 13 hidden)", loc="left", pad=12)
    b.set_xlim(-9, 7)
    b.set_xticks([-8,-6,-4,-2,0,2,4,6])
    for ax in axs:
        ax.set_xlabel("Rest-days difference (calendar days)")
        ax.set_ylabel("Number of matches")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True, nbins=6))
        ax.grid(axis="y", zorder=0)
    a.text(.03, .92, f"Mean = {m1:+.3f}  |  SD = {s1:.3f}", transform=a.transAxes,
           fontsize=10, color=NAVY, va="top", bbox=dict(facecolor="white",edgecolor=GRID,boxstyle="round,pad=.4"))
    b.text(.03, .92, f"Mean = {m2:+.3f}  |  SD = {s2:.3f}", transform=b.transAxes,
           fontsize=10, color=NAVY, va="top", bbox=dict(facecolor="white",edgecolor=GRID,boxstyle="round,pad=.4"))
    b.text(.5, .08, "Not an exclusion for analysis or modelling",
           transform=b.transAxes, ha="center", fontsize=9, color=CORAL,
           bbox=dict(facecolor="white",edgecolor=GRID,boxstyle="round,pad=.35"))
    finish(fig, dest)
    return m1, s1, m2, s2


def figure5(df: pd.DataFrame, dest: Path) -> None:
    fig, axs = plt.subplots(4, 2, figsize=(15, 16), constrained_layout=True)
    fig.suptitle("Figure 5  |  Explanatory variables versus actual goal difference",
                 x=.02, ha="left", fontsize=17, fontweight="bold")
    for ax, (code, col, label, unit) in zip(axs.flat, FEATURES):
        vals = df[col].to_numpy(dtype=float)
        goals = df[TARGET].to_numpy(dtype=float)
        if len(vals) != 104 or len(goals) != 104:
            raise AssertionError(f"Incorrect scatter sample count for {code}")
        ax.scatter(vals, goals, s=28, alpha=.48, color=TEAL, edgecolors="none")
        ax.axvline(0, color=GREY, linestyle="--", lw=.9, alpha=.75)
        ax.axhline(0, color=GREY, linestyle="--", lw=.9, alpha=.75)
        ax.set_title(f"{code}  ·  {label}", loc="left", fontsize=11, pad=8)
        ax.set_xlabel(f"{code} difference ({unit})", fontsize=9)
        ax.set_ylabel("Actual goal difference (goals)", fontsize=9)
        ax.set_ylim(-4.7, 6.7)
        ax.set_yticks([-4,-2,0,2,4,6])
        ax.grid(alpha=.42)
        if code == "X7":
            ax.annotate("ID 13 (−70)", xy=(-70, 0), xytext=(-53, 4.2),
                        arrowprops=dict(arrowstyle="->", color=CORAL, lw=1.2),
                        fontsize=9, color=CORAL, fontweight="semibold")
    finish(fig, dest)


def describe_shape(skew: float) -> str:
    if skew <= -1:
        return "strongly left-skewed"
    if skew >= 1:
        return "strongly right-skewed"
    if skew < -.5:
        return "moderately left-skewed"
    if skew > .5:
        return "moderately right-skewed"
    return "roughly balanced in skewness"


def render_report(df: pd.DataFrame, outliers: list[dict], x7_stats: tuple[float,float,float,float], digest: str) -> str:
    cols = [*FEATURES, ("Y", TARGET, "Actual goal difference", "Goals")]
    stats_lines = ["| Variable | N | Mean | Median | SD | Min | Q1 | Q3 | Max | Skewness |",
                   "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for code, col, _, unit in cols:
        s = df[col].astype(float)
        stats_lines.append(f"| {code} `{col}` | {s.count()} | {s.mean():+.2f} | {s.median():+.2f} | {s.std(ddof=1):.2f} | {s.min():+.2f} | {s.quantile(.25):+.2f} | {s.quantile(.75):+.2f} | {s.max():+.2f} | {s.skew():+.2f} |")
    outlier_lines=["| Match ID | Variable | Observed value | IQR lower | IQR upper |",
                   "|---:|---|---:|---:|---:|"]
    for o in sorted(outliers, key=lambda x:(x["match_id"],x["feature"])):
        outlier_lines.append(f"| {o['match_id']} | {o['feature']} `{o['column']}` | {o['value']:+.2f} | {o['lower']:+.2f} | {o['upper']:+.2f} |")
    freqs=df[TARGET].value_counts().sort_index()
    freqtext=", ".join(f"{int(k):+d}: {int(v)}" for k,v in freqs.items())
    m1,s1,m2,s2=x7_stats
    npos=int(df[TARGET].gt(0).sum()); nneg=int(df[TARGET].lt(0).sum()); nzero=int(df[TARGET].eq(0).sum())
    x7flags=sum(o['feature']=='X7' for o in outliers)
    x4flags=sum(o['feature']=='X4' for o in outliers)
    x8flags=sum(o['feature']=='X8' for o in outliers)
    rateflags=sum(o['feature'] in ('X5','X6') for o in outliers)
    return f"""# FIFA World Cup 2026 — Multiple Linear Regression
## Member 1, Task 2: Exploratory Data Analysis and Visualisations

### Purpose and data provenance
This exploratory analysis describes the eight *pre-match* differences (X1–X8) and actual goal difference (Y) for the **104** fixtures in the supplied Excel worksheet `Master_104_Matches`. It is descriptive work for the written university report, not a regression model or test of statistical significance. Every figure is generated by `member1_task2_eda.py` directly from the original workbook. No external football records are consulted.

- Input sheet: `Master_104_Matches`; **104** records; nine numerical modelling columns complete; no records removed, modified, scaled, winsorised, or imputed.
- Predictor direction: each feature retains the input workbook's **Team A minus Team B** definition. For X1 (ranking difference) and X4 (goals conceded), lower values may have a different substantive interpretation from other feature differences.
- Target Y: Team A's actual match goals minus Team B's actual match goals, **not** an explanatory variable or model prediction.
- Source file SHA-256 (read-only input): `{digest}`.
- Sample standard deviations use `ddof=1`; quartiles are pandas quantiles (25th and 75th percentiles); skewness is a descriptive pandas sample skewness coefficient.

### Figure 1 — Distribution of actual goal difference
![Figure 1](figures/fig01_goal_difference_distribution.png)

**Suggested caption:** *Figure 1. Frequency of observed Team A minus Team B goal difference across all 104 World Cup matches. Negative, zero and positive outcomes are differentiated.*

The distribution includes **{npos} positive**, **{nneg} negative** and **{nzero} zero** goal differences. Positive means Team A scored more goals, negative means Team B scored more, and zero means equal goals in the recorded match score (a knockout tie can still be decided by penalties). Goal differences range from **{int(df[TARGET].min()):+d}** to **{int(df[TARGET].max()):+d}**, with median **{df[TARGET].median():.0f}** and mean **{df[TARGET].mean():+.2f}** goals. The most common result is **0**, recorded in **{nzero}** matches. The individual difference frequencies are {freqtext}. This plot describes the target spread; it does not establish whether a predictor will explain it.

### Figure 2 — Histograms of all eight explanatory variables
![Figure 2](figures/fig02_explanatory_variable_histograms.png)

**Suggested caption:** *Figure 2. Eight separate histograms showing distributions of X1–X8. Each panel uses its own original unit and axis, with a vertical reference line at zero. X7 includes an inset showing its central range.*

The features have **different measurement units**, so a numerically larger range does not itself imply greater statistical importance. For example, X1 ranges from **{int(df.fifa_rank_diff.min())} to {int(df.fifa_rank_diff.max())} ranking places**, whereas X2 ranges from **{int(df.elo_rating_diff.min())} to {int(df.elo_rating_diff.max())} Elo points**. Their spreads should be interpreted within their own scales, not compared directly. X3 and X4 reflect goals-per-match differences; X5 and X6 are discrete proportion differences with medians **{df.last5_win_rate_diff.median():+.2f}** and **{df.last5_clean_sheet_rate_diff.median():+.2f}**. X7 has median **{df.rest_days_diff.median():+.0f}** and is **{describe_shape(float(df.rest_days_diff.skew()))}** (skewness **{df.rest_days_diff.skew():+.2f}**) largely because of Match 13. Apart from X7, all other feature skewness magnitudes are below 0.5 in the supplied data; that does not prove normality. X8 ranges from **{df.last5_opponent_strength_diff.min():+.2f}** to **{df.last5_opponent_strength_diff.max():+.2f}** FIFA-ranking places. Skewness is descriptive and, alone, cannot establish predictive usefulness.

### Figure 3 — Boxplots with independent feature scales
![Figure 3](figures/fig03_explanatory_variable_boxplots.png)

**Suggested caption:** *Figure 3. Individual horizontal boxplots for X1–X8 (N = 104 per panel). Boxes show Q1–Q3, the centre line shows the median, whiskers use the conventional 1.5 × IQR rule, and plotted points beyond whiskers indicate screening flags.*

Across the eight feature columns, the conventional **1.5 × IQR** rule flags **{len(outliers)} feature–match observations**, not necessarily {len(outliers)} different matches and not confirmed errors. These comprise **{x4flags} X4**, **{rateflags} X5/X6**, **{x7flags} X7**, and **{x8flags} X8** flags; X1, X2 and X3 have no IQR flags. Match **13 (X7 = −70)** is the most pronounced rest-days observation. Match **18 (X8 = +57.20)** is also beyond X8's upper fence. A statistical flag requires a source or modelling review; it is not a reason to delete, cap or edit data automatically.

### Figure 4 — Focused X7 visual sensitivity comparison
![Figure 4](figures/fig04_x7_outlier_sensitivity.png)

**Suggested caption:** *Figure 4. X7 rest-days differences for (A) all 104 matches and (B) the remaining 103 after hiding Match 13 for visual sensitivity only. Panel B is not the analysis or modelling dataset; Match 13 remains retained in the original data.*

| X7 statistic | All 104 matches | Visual-only comparison (103 matches) |
|---|---:|---:|
| Mean (days) | {m1:+.3f} | {m2:+.3f} |
| Sample standard deviation (days) | {s1:.3f} | {s2:.3f} |
| Match 13 retained in calculation | Yes | No, panel only |

The extreme value of **−70** for Match 13 pulls the overall X7 mean below zero and makes its sample standard deviation much larger than it is in the 103-match view. The 103-match view reveals central rest-day intervals obscured by the full-range plot; it is *not* a recommendation to remove the observation. A high-leverage predictor value could affect later regression coefficients and diagnostics, depending on its relationship with the target and other features. Appropriate later checks include source verification, influence diagnostics and model sensitivity analysis using a principled analysis plan. **All 104 matches remain in this task.**

### Figure 5 — Each feature versus actual goal difference
![Figure 5](figures/fig05_features_vs_goal_difference.png)

**Suggested caption:** *Figure 5. Eight scatter plots of X1–X8 against recorded goal difference for 104 matches per panel, with transparent markers to reveal overlaps and zero-reference guides. No regression or trend lines are fitted.*

The y-values lie on **integer goal differences**, so repeated horizontal bands and some overplotting are expected, especially for discrete X5, X6 and X7 values near zero. The panels show a range of goal differences across both positive and negative feature values; Match 13 occupies an extreme negative X7 position but has **Y = {int(df.loc[df.match_id.eq(13),TARGET].iloc[0]):+d}**. This graphic can motivate questions about functional form, influential observations, and later predictor interrelationships, but it cannot establish statistical significance, independent predictive contribution, or causality. No correlations, regression fits, coefficients or prediction metrics were calculated.

### Descriptive statistical summary
The following statistics are from the source workbook. Units vary by column, so cross-variable numerical magnitudes are not directly comparable.

{chr(10).join(stats_lines)}

### Full IQR screening log — observations retained
For each feature, Q1 − 1.5 × IQR and Q3 + 1.5 × IQR define the screening fences. Flags are **not** assumed data errors.

{chr(10).join(outlier_lines)}

### Implications, limitations and subsequent analysis
1. **Target shape:** The outcome spans {int(df[TARGET].min())} to +{int(df[TARGET].max())} goals, with **{nzero}** recorded zero goal differences. Retain the full target distribution when later defining validation metrics.
2. **Different units:** X1/X8 use FIFA rank positions, X2 Elo points, X3/X4 goals per match, X5/X6 proportions, and X7 days. Descriptive magnitude alone does not rank their usefulness. No scaling is carried out here.
3. **Extreme X7:** Retain Match 13 and confirm provenance or physical plausibility before considering any later model diagnostics. The omission in Figure 4B is *visual only*.
4. **Evidence boundaries:** These analyses establish internal patterns of the provided workbook. They do not independently verify upstream historical fixture or ranking sources, nor do they test pre-kickoff availability of every input.
5. **No test-set-guided feature choice:** These full-data plots are for descriptive reporting. Once a train/test split is defined, choices learned from data, including imputation, scaling, feature selection and model tuning, should be fitted or chosen using training data only, rather than using held-out test data to drive decisions.
6. **Task boundaries:** No outliers removed; no transformations; no correlations/VIF; no train/test split; no EDA-based feature selection; no regression model, line, coefficients or predictions.

### Verification and reproducibility
- Worksheet loaded with pandas from the supplied workbook (read-only).
- Confirmed 104 rows, IDs 1–104 unique, nine modelling columns numeric/nonmissing, rate differences within [−1, 1], and `goal_difference = team_a_goals − team_b_goals` on every row.
- Verified target category frequencies 50 positive, 30 negative, 24 zero; X7 for Match 13 equals −70; and 18 IQR feature-level flags.
- Every histogram, boxplot and scatter panel is derived from exactly 104 original observations, except the *clearly labelled* Figure 4B with 103; the workbook itself remains untouched.
- Five PNG files are rendered at **320 DPI**. Figures use original data units, separate feature scales and descriptive annotations only.

### AI-assistance disclosure
Generative AI assisted in authoring the Python code, choosing the figure layout, and drafting descriptions and validation assertions. Numerical findings and images are calculated directly from the supplied workbook using pandas, NumPy and Matplotlib. Code-level checks verify consistency with that workbook; **they do not authenticate the football sources underlying the original data**. The work should be inspected and explained by the submitting student.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate descriptive EDA PNGs and report; no model fitting")
    parser.add_argument("--input", default="FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting.xlsx",
                        help="Path to original Excel workbook (read-only)")
    parser.add_argument("--output-dir", default=".", help="Folder for report and figures")
    args = parser.parse_args()
    workbook = Path(args.input).expanduser().resolve()
    if not workbook.is_file():
        parser.error(f"Input workbook not found: {workbook}")
    output_dir = Path(args.output_dir).expanduser().resolve()
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    before = sha256(workbook)
    df, numeric, outliers = load_and_check(workbook)
    style_charts()
    figure1(df, figures_dir / "fig01_goal_difference_distribution.png")
    figure2(df, figures_dir / "fig02_explanatory_variable_histograms.png")
    figure3(df, outliers, figures_dir / "fig03_explanatory_variable_boxplots.png")
    x7_stats = figure4(df, figures_dir / "fig04_x7_outlier_sensitivity.png")
    figure5(df, figures_dir / "fig05_features_vs_goal_difference.png")
    report = render_report(df, outliers, x7_stats, before)
    (output_dir / "member1_task2_eda_report.md").write_text(report, encoding="utf-8")
    if before != sha256(workbook):
        raise RuntimeError("Input Excel workbook checksum changed unexpectedly")
    saved = sorted(figures_dir.glob("*.png"))
    if len(saved) != 5:
        raise AssertionError(f"Expected five PNGs, found {len(saved)}")
    print(f"PASS: 104 matches; 9 complete numeric modelling columns; 18 feature-IQR flags.")
    print("PASS: goal difference frequencies +50 / −30 / 0=24; Match 13 X7=−70.")
    print(f"X7 all: mean={x7_stats[0]:+.6f}, sample SD={x7_stats[1]:.6f}")
    print(f"X7 visual-only 103: mean={x7_stats[2]:+.6f}, sample SD={x7_stats[3]:.6f}")
    print(f"PASS: generated {len(saved)} PNG figures at 320 DPI and an EDA report.")
    print("PASS: input Excel SHA-256 unchanged; no modelling or feature transformations.")
    print(f"Outputs: {output_dir}")


if __name__ == "__main__":
    main()
