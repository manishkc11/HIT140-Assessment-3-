#!/usr/bin/env python3
"""Member 1 / Task 3: exploratory correlation, VIF and IQR diagnostics.

Source: the *cached values* in Master_104_Matches of the specified XLSX.
Read-only OOXML parsing (Python standard library; does not recalculate formulas).
The supplied workbook has cached numeric results for formula cells.

AI-assistance disclosure: generative AI assisted with the design, code,
visualisation formatting, validation logic and academic report text. All
numerical outputs are calculated from the supplied workbook. No external
historical football facts are independently authenticated by this script.

Statistical boundary: VIF uses auxiliary regressions of each X on other Xs
plus an intercept, NOT a final regression of goal_difference on X1..X8.
No row or variable is dropped from the main analysis, no predictive models,
predictions, scaling, imputation, train/test splitting or feature selection.
The 103-row case is a sensitivity calculation only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np
from scipy.stats import rankdata, spearmanr
from statsmodels.stats.outliers_influence import variance_inflation_factor

FEATURES = [
    ("X1", "fifa_rank_diff", "FIFA ranking difference"),
    ("X2", "elo_rating_diff", "Elo rating difference"),
    ("X3", "last5_avg_goals_scored_diff", "Last-5 average goals scored difference"),
    ("X4", "last5_avg_goals_conceded_diff", "Last-5 average goals conceded difference"),
    ("X5", "last5_win_rate_diff", "Last-5 win-rate difference"),
    ("X6", "last5_clean_sheet_rate_diff", "Last-5 clean-sheet-rate difference"),
    ("X7", "rest_days_diff", "Rest-days difference"),
    ("X8", "last5_opponent_strength_diff", "Last-5 opponent-strength difference"),
]
TARGET = "goal_difference"
NUMERIC = [f[1] for f in FEATURES] + [TARGET]
PRETTY = ["X1 · FIFA ranking", "X2 · Elo rating", "X3 · Goals scored",
          "X4 · Goals conceded", "X5 · Win rate", "X6 · Clean sheets",
          "X7 · Rest days", "X8 · Opponent strength", "Y · Goal difference"]
COLORS = {"navy": "#213A56", "teal": "#007D89", "coral": "#B85F4E",
          "blue": "#5475AA", "grey": "#738093", "light": "#E9EDF2"}
XMLNS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
         "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
         "p": "http://schemas.openxmlformats.org/package/2006/relationships"}


def cell_col(cell_ref: str) -> int:
    match = re.match(r"([A-Z]+)\d+$", cell_ref)
    if not match:
        raise ValueError(f"Unexpected cell address: {cell_ref}")
    col = 0
    for ch in match.group(1):
        col = col * 26 + ord(ch) - ord("A") + 1
    return col - 1


def read_master_xlsx(path: Path) -> list[dict]:
    """Extract values from the named worksheet, retaining cached formula values.

    XLSX is a ZIP of XML files. This reader requires only Python's stdlib,
    avoiding re-evaluating workbook formulae or modifying the original.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Workbook not found: {path}")
    with zipfile.ZipFile(path) as archive:
        book = ET.fromstring(archive.read("xl/workbook.xml"))
        props = book.find("m:workbookPr", XMLNS)
        date1904 = props is not None and props.get("date1904", "false").lower() in ("1", "true")
        matching = [s for s in book.findall("m:sheets/m:sheet", XMLNS)
                    if s.get("name") == "Master_104_Matches"]
        if len(matching) != 1:
            raise ValueError("Exactly one Master_104_Matches worksheet is required")
        relationship_id = matching[0].get("{%s}id" % XMLNS["r"])
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {r.get("Id"): r.get("Target") for r in rels.findall("p:Relationship", XMLNS)}
        target = targets[relationship_id].lstrip("/")
        from posixpath import normpath
        sheet_path = normpath(target if target.startswith("xl/") else "xl/" + target)
        shared = []
        if "xl/sharedStrings.xml" in archive.namelist():
            xml = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = ["".join(t.text or "" for t in si.findall(".//m:t", XMLNS))
                      for si in xml.findall("m:si", XMLNS)]
        worksheet = ET.fromstring(archive.read(sheet_path))
        raw_rows = []
        for row in worksheet.findall("m:sheetData/m:row", XMLNS):
            values = {}
            for c in row.findall("m:c", XMLNS):
                index = cell_col(c.get("r", ""))
                kind = c.get("t", "n")
                val = c.find("m:v", XMLNS)
                if kind == "e":
                    raise ValueError(f"Excel formula/error at {c.get('r')}: {val.text if val is not None else ''}")
                if kind == "inlineStr":
                    text = "".join(t.text or "" for t in c.findall("m:is//m:t", XMLNS))
                    out = text
                elif val is None or val.text is None:
                    if c.find("m:f", XMLNS) is not None:
                        raise ValueError(f"Formula without cached value at {c.get('r')}")
                    out = None
                elif kind == "s":
                    out = shared[int(val.text)]
                elif kind in ("str", "d"):
                    out = val.text
                elif kind == "b":
                    out = val.text == "1"
                else:
                    out = float(val.text)
                values[index] = out
            raw_rows.append(values)
    if not raw_rows:
        raise ValueError("The master worksheet has no data")
    header = [raw_rows[0].get(i) for i in range(max(raw_rows[0]) + 1)]
    if any(not isinstance(h, str) for h in header):
        raise ValueError("Invalid header row")
    result = []
    epoch = datetime(1904, 1, 1) if date1904 else datetime(1899, 12, 30)
    for raw in raw_rows[1:]:
        if not any(x is not None for x in raw.values()):
            continue
        record = {h: raw.get(i) for i, h in enumerate(header)}
        value = record.get("match_date")
        if isinstance(value, (int, float)):
            record["match_date"] = (epoch + timedelta(days=value)).date().isoformat()
        elif isinstance(value, str):
            try:
                record["match_date"] = date.fromisoformat(value[:10]).isoformat()
            except ValueError as exc:
                raise ValueError(f"Unparseable match_date: {value}") from exc
        result.append(record)
    return result


def validate_and_matrices(records):
    if len(records) != 104:
        raise ValueError(f"Expected exactly 104 match rows, received {len(records)}")
    required = ["match_id", "match_date", "team_a", "team_b"] + NUMERIC
    for i, row in enumerate(records, start=2):
        missing = [name for name in required if name not in row]
        if missing:
            raise ValueError(f"Missing columns {missing} at worksheet row {i}")
    ids = [r["match_id"] for r in records]
    if any(isinstance(x, bool) or not isinstance(x, (float, int)) or int(x) != x for x in ids):
        raise ValueError("Noninteger match ID found")
    if sorted(int(x) for x in ids) != list(range(1, 105)):
        raise ValueError("match_id must be exactly 1..104 with no duplicates")
    for row in records:
        dt = date.fromisoformat(row["match_date"])
        if not date(2026, 6, 11) <= dt <= date(2026, 7, 19):
            raise ValueError(f"Match {int(row['match_id'])} date outside tournament: {dt}")
        for col in NUMERIC:
            val = row[col]
            if val is None or isinstance(val, (str, bool)) or not np.isfinite(val):
                raise ValueError(f"Invalid modelling input for match {int(row['match_id'])}: {col}={val}")
        if not np.isclose(row[TARGET], row["team_a_goals"] - row["team_b_goals"], atol=1e-9):
            raise ValueError(f"Goal difference does not match score at match {int(row['match_id'])}")
    for name in ("last5_win_rate_diff", "last5_clean_sheet_rate_diff"):
        for row in records:
            if abs(row[name]) > 1.0 + 1e-12:
                raise ValueError(f"Invalid difference outside [-1,1] at match {row['match_id']}, {name}")
    if Counter(tuple(sorted((k, str(v)) for k, v in row.items())) for row in records).most_common(1)[0][1] > 1:
        raise ValueError("Duplicate complete rows found")
    matrix = np.asarray([[float(r[col]) for col in NUMERIC] for r in records], dtype=float)
    match13 = next(r for r in records if int(r["match_id"]) == 13)
    if float(match13["rest_days_diff"]) != -70.0:
        raise ValueError("Expected Task 1 anchor: Match 13 X7 = -70")
    return matrix[:, :8], matrix[:, 8]


def fmt(val, digits=3):
    return f"{float(val):.{digits}f}"


def write_csv(path, headers, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(headers)
        writer.writerows(rows)


def vip_interpret(v):
    if v > 10:
        return "Potentially serious; investigate"
    if v > 5:
        return "Elevated (>5); investigate"
    if v >= 2:
        return "Moderate dependence; monitor"
    return "Low dependence"


def get_analysis(records, X, y):
    matrix = np.column_stack([X, y])
    pearson = np.corrcoef(matrix, rowvar=False)
    spearman_values = np.array([float(spearmanr(X[:, i], y).statistic) for i in range(8)])
    # Include intercept in *every* auxiliary VIF regression.
    with_const = np.column_stack((np.ones(len(X)), X))
    vifs = np.array([float(variance_inflation_factor(with_const, i+1)) for i in range(8)])
    independent = []
    aux_r2 = []
    for i in range(8):
        others = np.delete(X, i, axis=1)
        design = np.column_stack((np.ones(len(X)), others))
        betas, *_ = np.linalg.lstsq(design, X[:, i], rcond=None)
        residuals = X[:, i] - design @ betas
        rss = float(np.dot(residuals, residuals))
        centered = X[:, i] - X[:, i].mean()
        tss = float(np.dot(centered, centered))
        r2 = 1.0 - rss / tss
        independent.append(1.0 / (1.0 - r2))
        aux_r2.append(r2)
    independent = np.asarray(independent)
    if not np.allclose(vifs, independent, atol=1e-8, rtol=1e-8):
        raise AssertionError(f"Independent VIF disagrees: {vifs} vs {independent}")
    flags = []
    fences = {}
    for i, (code, col, title) in enumerate(FEATURES):
        q1, q3 = np.quantile(X[:, i], [0.25, 0.75], method="linear")
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        fences[col] = (lower, upper)
        for j, record in enumerate(records):
            val = float(X[j, i])
            if val < lower or val > upper:
                side = "below lower" if val < lower else "above upper"
                reason = f"{side} 1.5×IQR fence; statistical screening flag, not a demonstrated error"
                if col == "rest_days_diff":
                    follow = "Recheck previous-fixture dates and rest-day definition against documented source history; retain pending review"
                elif col == "last5_opponent_strength_diff":
                    follow = "Recheck five opponents, published ranking editions, source evidence and averaging; retain pending review"
                elif col in ("last5_win_rate_diff", "last5_clean_sheet_rate_diff"):
                    follow = "Within possible difference range [-1,+1]; verify previous-five match counts and rates; retain pending review"
                else:
                    follow = "Recheck source results, previous-five matches and Team A−B ordering; retain pending review"
                flags.append([int(record["match_id"]), record["match_date"], record["team_a"],
                             record["team_b"], code, col, fmt(val, 6), fmt(lower, 6), fmt(upper, 6),
                             reason, follow])
    if len(flags) != 18:
        raise AssertionError(f"Expected exactly 18 feature-level IQR flags, got {len(flags)}")
    mask = np.array([int(r["match_id"]) != 13 for r in records])
    assert np.count_nonzero(mask) == 103
    sens = []
    for i in [0, 1, 2, 3, 4, 5, 7, 8]:
        second = X[:, i] if i != 8 else y
        first_full, first_trim = X[:, 6], X[mask, 6]
        pear_all = float(np.corrcoef(first_full, second)[0, 1])
        pear_trim = float(np.corrcoef(first_trim, second[mask])[0, 1])
        spear_all = float(spearmanr(first_full, second).statistic)
        spear_trim = float(spearmanr(first_trim, second[mask]).statistic)
        # Independently verify that scipy's Spearman = Pearson on average ranks (tie aware).
        independent_spearman = np.corrcoef(rankdata(first_full), rankdata(second))[0, 1]
        if not np.isclose(spear_all, independent_spearman, atol=1e-12):
            raise AssertionError("Spearman/tie rank validation failed")
        code = "Y" if i == 8 else FEATURES[i][0]
        col = TARGET if i == 8 else FEATURES[i][1]
        sens.append([code, col, 104, 103, pear_all, pear_trim, pear_trim-pear_all,
                     spear_all, spear_trim, spear_trim-spear_all])
    # Main-dataset-only integrity of the 9x9 matrix.
    if pearson.shape != (9,9) or not np.allclose(pearson, pearson.T, atol=1e-12):
        raise AssertionError("Pearson 9×9 matrix not symmetric")
    if not np.allclose(np.diag(pearson), np.ones(9), atol=1e-12):
        raise AssertionError("Correlation diagonal is not 1")
    if np.any(np.abs(pearson) > 1 + 1e-12):
        raise AssertionError("Correlation out of [-1,1]")
    return pearson, spearman_values, vifs, independent, np.asarray(aux_r2), flags, fences, sens


def style_plots():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                         "axes.titlesize": 15, "axes.titleweight": "semibold",
                         "axes.labelsize": 11, "xtick.labelsize": 10,
                         "ytick.labelsize": 10, "figure.facecolor": "white",
                         "axes.facecolor": "white", "savefig.facecolor": "white",
                         "axes.spines.top": False, "axes.spines.right": False,
                         "axes.edgecolor": "#D3DAE2", "grid.color": "#E6E9EF"})


def save_figure(fig, path):
    fig.savefig(path, dpi=320, facecolor="white", bbox_inches="tight", pad_inches=0.25,
                metadata={"Software": "Member1 Task3 Matplotlib"})
    plt.close(fig)


def make_figures(outdir, pear, spear, vifs):
    style_plots()
    figs = outdir / "figures"
    figs.mkdir(parents=True, exist_ok=True)
    # Fig 06: 9×9, visibly distinct negative and positive coefficients.
    fig, ax = plt.subplots(figsize=(12.7, 10.5))
    cmap = plt.get_cmap("RdBu_r")
    im = ax.imshow(pear, cmap=cmap, norm=TwoSlopeNorm(vmin=-1, vcenter=0, vmax=1))
    labels = ["X1 FIFA rank", "X2 Elo rating", "X3 Goals scored", "X4 Goals conceded",
              "X5 Win rate", "X6 Clean sheets", "X7 Rest days",
              "X8 Opponent strength", "Y Goal difference"]
    ax.set_xticks(np.arange(9), labels=labels, rotation=37, ha="right", rotation_mode="anchor")
    ax.set_yticks(np.arange(9), labels=labels)
    ax.set_xticks(np.arange(-.5, 9, 1), minor=True)
    ax.set_yticks(np.arange(-.5, 9, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", bottom=False, left=False)
    for i in range(9):
        for j in range(9):
            v = pear[i,j]
            ax.text(j, i, f"{v:+.2f}" if i!=j else "1.00",
                    ha="center", va="center", fontsize=10, fontweight="semibold" if i==j else "normal",
                    color="white" if abs(v) > .58 else COLORS["navy"])
    ax.set_title("Figure 6  |  Pearson correlations across nine modelling variables", loc="left", pad=18, color=COLORS["navy"])
    cb = fig.colorbar(im, ax=ax, shrink=.82, pad=.025, ticks=[-1,-.5,0,.5,1])
    cb.set_label("Pearson r  (−1 to +1)")
    fig.text(.12, .015, "N = 104 matches  •  Full-sample descriptive correlations, not modelling decisions", color=COLORS["grey"], fontsize=10)
    fig.subplots_adjust(left=.20, bottom=.23, right=.93, top=.91)
    save_figure(fig, figs/"fig06_pearson_correlation_heatmap.png")

    # Fig 07: paired marks on a common correlation scale.
    fig, ax = plt.subplots(figsize=(11.7, 7.4))
    p = pear[:8, -1]
    for i in range(8):
        ypos = 7-i  # Match label/point row; X1 is at top, X8 at bottom.
        ax.plot([p[i], spear[i]], [ypos, ypos], color="#CED7E1", lw=3, zorder=1)
    positions = np.arange(8)[::-1]
    ax.scatter(p, positions + .085, s=91, label="Pearson r (linear)", color=COLORS["navy"], marker="o", zorder=3)
    ax.scatter(spear, positions - .085, s=104, label="Spearman ρ (rank/monotonic)", color=COLORS["coral"], marker="D", zorder=3)
    ax.axvline(0, color=COLORS["grey"], linewidth=1.1)
    ax.set_yticks(positions, [f"{FEATURES[i][0]}   {['FIFA ranking','Elo rating','Goals scored','Goals conceded','Win rate','Clean sheets','Rest days','Opponent strength'][i]}" for i in range(8)])
    ax.set_xlim(-1.02, 1.02)
    ax.set_xticks(np.arange(-1, 1.01, .25))
    ax.grid(axis="x", alpha=.75)
    ax.set_axisbelow(True)
    ax.set_xlabel("Correlation with actual goal difference (Y)")
    ax.set_title("Figure 7  |  Pearson versus Spearman correlations", loc="left", pad=24, color=COLORS["navy"])
    ax.legend(loc="upper center", bbox_to_anchor=(.51, 1.055), ncol=2, frameon=False, fontsize=10)
    fig.text(.15,.02,"N = 104  •  Discrete variables contain ties  •  No significance tests or predictions",fontsize=10,color=COLORS["grey"])
    fig.subplots_adjust(left=.27,right=.98,top=.87,bottom=.12)
    save_figure(fig, figs/"fig07_pearson_spearman_comparison.png")

    # Fig 08 VIF bar plot incl threshold markers.
    fig, ax = plt.subplots(figsize=(11.5, 7.2))
    order = np.argsort(vifs)  # sorted ascending makes larger appear near top
    ys = np.arange(8)
    bars = ax.barh(ys, vifs[order], height=.67,
                   color=[COLORS["coral"] if vifs[k] > 5 else COLORS["teal"] for k in order])
    ax.set_yticks(ys, [f"{FEATURES[i][0]}   {['FIFA ranking','Elo rating','Goals scored','Goals conceded','Win rate','Clean sheets','Rest days','Opponent strength'][i]}" for i in order])
    ax.axvline(5, color=COLORS["coral"], ls="--", lw=1.5, label="Investigate above 5")
    ax.axvline(10, color=COLORS["grey"], ls=":", lw=1.4, label="Potential concern above 10")
    ax.set_xlim(0, max(10.7, float(max(vifs))+1.4))
    for bar, i in zip(bars, order):
        ax.text(bar.get_width()+.15, bar.get_y()+bar.get_height()/2, f"{vifs[i]:.2f}", va="center", fontsize=10, color=COLORS["navy"])
    ax.set_xlabel("Variance inflation factor (VIF), with auxiliary-regression intercept")
    ax.set_title("Figure 8  |  Predictor multicollinearity diagnostics", loc="left", pad=20, color=COLORS["navy"])
    ax.grid(axis="x", alpha=.75)
    ax.set_axisbelow(True)
    ax.legend(loc="lower right", frameon=False, fontsize=10)
    fig.text(.12,.02,"Thresholds are screening guides, not automatic feature-exclusion rules  •  N = 104", fontsize=10,color=COLORS["grey"])
    fig.subplots_adjust(left=.29,right=.97,top=.89,bottom=.14)
    save_figure(fig, figs/"fig08_vif_diagnostics.png")


def strength(r):
    # Explicitly descriptive and heuristic only, no inferential significance.
    a = abs(r)
    if a < .20: return "very weak"
    if a < .40: return "weak"
    if a < .60: return "moderate"
    if a < .80: return "strong"
    return "very strong"


def make_report(path, source, sha, records, X, y, pear, spear, vifs, independent, aux_r2, flags, fences, sens):
    lines = []
    add = lines.append
    add("# Member 1 – Task 3: Correlation, multicollinearity and outlier diagnostics")
    add("")
    add("## Purpose, input and boundaries")
    add("")
    add("This is **descriptive and diagnostic analysis**, not a fitted goal-difference prediction model. The only observations are 104 matches from the `Master_104_Matches` worksheet of the supplied XLSX; eight features (X1–X8) and `goal_difference` (Y) retain Team A minus Team B orientation.")
    add("")
    add(f"- Original input: `{source.name}` (read-only; cached numeric formula values); SHA-256: `{sha}`.")
    add("- Main analyses: **104/104** observations, complete numeric columns, no missing input, no rows omitted, no duplicate IDs or full rows, all target arithmetic verified.")
    add("- Figure files: 320 DPI PNG. Pearson and Spearman are *marginal* associations; VIF concerns redundancy **among predictors**, not association with Y.")
    add("- No scaling, imputation, winsorisation, outlier deletion, feature selection, test-data optimisation, final model training, or prediction is performed.")
    add("")
    add("## Methods")
    add("")
    add("**Pearson correlation (r)** measures linear association between two numerical variables. Its sign indicates direction and its magnitude, from 0 to 1, shows the strength of the observed linear association. **Spearman rank correlation (ρ)** is Pearson correlation applied to the ranked values; it measures monotonic association and uses *average ranks for tied observations*. Correlation does not show causation, adjusted effects, model predictive performance, or statistical significance. No p-values or significance claims are made.")
    add("")
    add("**VIF:** For each predictor, regress it on the other seven predictors **with an intercept**, calculate the auxiliary R², then use `VIF = 1 / (1 − R²)`. Results are generated with `statsmodels` and independently checked using NumPy least-squares. No regression involving the target is trained. Guidelines: near 1 low dependence, >5 investigate, >10 potentially serious; these are screening conventions, not removal rules.")
    add("")
    add("**IQR:** For each feature use Q1 and Q3 computed with linear interpolation; flag observations outside `[Q1 − 1.5×IQR, Q3 + 1.5×IQR]`. All 18 flags are preserved. A flag alone is **not a data error**. If the original dataset is later used for predictive development, any data-driven preprocessing or model-selection decision must use training data only.")
    add("")
    add("## Figure 6 – Pearson correlation heatmap")
    add("")
    add("The 9×9 heatmap includes the eight predictors and Y on a fixed scale of −1 to +1, with 2-decimal coefficients. The correlation matrix is symmetric, its diagonal equals 1 and all coefficients are within the expected range.")
    add("")
    add("### Predictor correlations with goal difference")
    add("")
    add("| Predictor | Pearson r | Spearman ρ | Pearson direction and approximate magnitude |")
    add("|---|---:|---:|---|")
    for i, (code, col, descr) in enumerate(FEATURES):
        r = pear[i,-1]
        direction = "negative" if r<0 else "positive" if r>0 else "zero"
        add(f"| {code} – {descr} | {r:+.3f} | {spear[i]:+.3f} | {strength(r)} {direction} association |")
    add("")
    order = np.argsort(-np.abs(pear[:8,-1]))
    add(f"In this sample, the largest absolute *marginal* Pearson correlations with Y are **{FEATURES[order[0]][0]} ({pear[order[0],-1]:+.3f})** and **{FEATURES[order[1]][0]} ({pear[order[1],-1]:+.3f})**, while the smallest absolute correlation is **{FEATURES[order[-1]][0]} ({pear[order[-1],-1]:+.3f})**. Neither ranking constitutes a decision to select features nor evidence of independent predictive contribution.")
    add("")
    add("### Prespecified predictor-pair checks")
    add("")
    for a,b,explanation in [(0,1,"FIFA rank and Elo use opposite numerical strength conventions"),
                             (2,4,"goals scored and win rate can encode overlapping recent form"),
                             (3,5,"goals conceded and clean-sheet rates describe related defensive history")]:
        add(f"- **{FEATURES[a][0]}–{FEATURES[b][0]}:** Pearson r = **{pear[a,b]:+.3f}**; {explanation}. This measures predictor–predictor association, not their adjusted effects on Y.")
    add("")
    add("FIFA ranking difference requires sign care: lower ranking numbers mean stronger teams, so negative X1 can legitimately associate with positive goal difference. Elo's direction is the opposite. Negative r values are not errors.")
    add("")
    add("**Suggested caption:** *Figure 6. Pearson correlation matrix for all eight pre-match explanatory variables and observed goal difference across 104 World Cup matches. Cells display r to two decimal places; colours use a common −1 to +1 scale.*")
    add("")
    add("## Figure 7 – Pearson versus Spearman")
    add("")
    deltas = np.abs(spear - pear[:8,-1])
    largest = int(np.argmax(deltas))
    add(f"The two methods agree on the correlation direction for **{int(np.sum(np.sign(spear)==np.sign(pear[:8,-1])))} of eight** variables. The largest absolute method difference is **{FEATURES[largest][0]}** (Pearson {pear[largest,-1]:+.3f}, Spearman {spear[largest]:+.3f}; absolute difference {deltas[largest]:.3f}). Differences can result from nonlinear monotonic patterns, ties, or the influence of extreme values; the plot alone does not identify the cause.")
    add("")
    add("X5 and X6 are differences of rates based on five matches, so ties and discrete increments are expected. X7 contains many identical zero observations: " + f"**{int(np.count_nonzero(X[:,6] == 0))}/104** are exactly zero, plus the unusually negative Match 13. Spearman accounts for tied ranks but is not immune to small samples or measurement problems.")
    add("")
    add("Neither Spearman coefficients nor their relative size justify replacing, removing or rescaling any predictor here.")
    add("")
    add("**Suggested caption:** *Figure 7. Side-by-side Pearson and Spearman correlation coefficients between each original explanatory variable and goal difference (N = 104); paired markers compare linear and rank-based associations without significance testing.*")
    add("")
    add("## Figure 8 – Variance inflation factors")
    add("")
    add("| Predictor | VIF (with intercept) | Auxiliary R² | Interpretation |")
    add("|---|---:|---:|---|")
    for i,(code,col,_) in enumerate(FEATURES):
        add(f"| {code} – `{col}` | {vifs[i]:.3f} | {aux_r2[i]:.3f} | {vip_interpret(vifs[i])} |")
    add("")
    hi = [FEATURES[i][0] for i,v in enumerate(vifs) if v>5]
    high10 = [FEATURES[i][0] for i,v in enumerate(vifs) if v>10]
    add(f"**Screening results:** {len(hi)} features exceed VIF 5 ({', '.join(hi) if hi else 'none'}); {len(high10)} exceed 10 ({', '.join(high10) if high10 else 'none'}). All eight remain included. The intercept's own VIF is intentionally excluded.")
    add("")
    add("When explanatory variables share substantial information, their individual regression coefficients can become sensitive to minor changes in the training dataset, inflating standard errors and complicating interpretation. This does not necessarily prevent the model from producing predictions. The later modelling team should investigate on *training data only*, rather than delete variables solely on these full-dataset screening statistics.")
    add("")
    add("Independent validation computed each auxiliary R² using an intercept and NumPy least squares, then reconstructed each VIF; maximum absolute difference from `statsmodels` was " + f"**{np.max(np.abs(vifs-independent)):.2e}**.")
    add("")
    add("**Suggested caption:** *Figure 8. Variance inflation factors for the eight candidate predictors from auxiliary regressions containing an intercept. Dashed guides at 5 and 10 denote conventional investigation thresholds, not automatic removal criteria.*")
    add("")
    add("## IQR screening and detailed outlier investigation")
    add("")
    unique_matches = len(set(int(row[0]) for row in flags))
    add(f"Across all eight feature columns, the independent 1.5×IQR screen identified **{len(flags)} feature-level flags** involving **{unique_matches} distinct matches**. These agree with Task 1's 18 feature-level flags. Every flagged record, team, date, value, lower/upper fence and recommended follow-up appears in `member1_task3_outlier_investigation.csv`.")
    add("")
    add("| Case | Observed value | IQR screen (lower, upper) | Investigation rationale |")
    add("|---|---:|---|---|")
    for target_id, code, col in [(13,"X7","rest_days_diff"),(18,"X8","last5_opponent_strength_diff"),
                                  (70,"X5","last5_win_rate_diff"),(70,"X6","last5_clean_sheet_rate_diff")]:
        value = next(r[col] for r in records if int(r['match_id']) == target_id)
        lo, hi2 = fences[col]
        msg = {"X7":"Large rest-day imbalance: verify predecessor dates and calendar-day convention; value is not impossible by its definition.",
               "X8":"Large average-ranking difference: verify five previous opponents, their applicable publication dates and arithmetic; possible but unusual.",
               "X5":"−1 is a mathematically possible rate difference; check all five win results for each team.",
               "X6":"−1 is a mathematically possible clean-sheet-rate difference; check five conceded-goal records for each team."}[code]
        add(f"| Match {target_id} / {code} | {float(value):+.2f} | ({lo:.3f}, {hi2:.3f}) | {msg} |")
    add("")
    add("In particular, X7 has no fixed maximum or minimum mathematical bound, so −70 is an extreme observation, **not a mathematically invalid input**. X8 is a difference of FIFA ranking averages, and +57.20 is similarly possible. X5/X6 are bounded differences of proportions and −1 is valid at the boundary. None has been excluded or edited. External historical fixture/ranking verification was outside the scope of this workbook-only task.")
    add("")
    add("## X7 sensitivity – visual/diagnostic comparison only")
    add("")
    mask = np.array([int(row['match_id'])!=13 for row in records])
    add(f"- Main sample (104): X7 mean = **{np.mean(X[:,6]):+.3f}**; sample SD = **{np.std(X[:,6],ddof=1):.3f}**.")
    add(f"- Excluding Match 13 for sensitivity only (103): mean = **{np.mean(X[mask,6]):+.3f}**; sample SD = **{np.std(X[mask,6],ddof=1):.3f}**. **All 104 remain in the official analysis.**")
    add("")
    add("| X7 paired with | Pearson 104 | Pearson 103 | Change (103−104) | Spearman 104 | Spearman 103 | Change (103−104) |")
    add("|---|---:|---:|---:|---:|---:|---:|")
    for row in sens:
        add(f"| {row[0]} – {row[1]} | {row[4]:+.3f} | {row[5]:+.3f} | {row[6]:+.3f} | {row[7]:+.3f} | {row[8]:+.3f} | {row[9]:+.3f} |")
    add("")
    target_sens = next(s for s in sens if s[0] == "Y")
    add(f"The Pearson X7–Y correlation changes from **{target_sens[4]:+.3f} to {target_sens[5]:+.3f}** (Δ {target_sens[6]:+.3f}); Spearman changes from **{target_sens[7]:+.3f} to {target_sens[8]:+.3f}** (Δ {target_sens[9]:+.3f}). X7 has a very extreme left-tail value; Pearson depends on the actual magnitudes and can be influenced by such a point, whereas Spearman uses ranks with ties. The direction of individual X7 correlations with other predictors may also change; see table rather than interpreting sensitivity as a new primary dataset.")
    add("")
    add("Removing Match 13 from a descriptive *comparison* does not demonstrate corruption, justify exclusion, or establish performance effects in a fitted regression. Any later model diagnostics and treatment decisions belong to training-set-based analysis and require documented rationale.")
    add("")
    add("## Limitations and implications for the regression stage")
    add("")
    add("1. The complete 104-match sample was used for descriptive reporting. If these statistics inform feature selection, transformations, or parameter tuning before a train/test split, that would risk test-data leakage. **Make data-dependent modelling choices on training data only** after the split; reserve test matches for the final evaluation.")
    add("2. Pairwise correlations assess one relationship at a time; they do not estimate the independent effect of a feature holding others fixed. VIF diagnoses overlap among the Xs; neither test proves causation or out-of-sample predictability.")
    add("3. Spearman and Pearson are descriptive coefficients. No significance testing or multiple-comparisons inference has been performed, so no p-value or statistical significance claim is made.")
    add("4. The dataset includes tied discrete predictors, an influential-looking X7 value, and interrelated measures of team strength and form. Later model developers should test assumptions and stability on their training partition.")
    add("5. Correlation magnitude is not comparable to regression coefficient magnitude, and a negative sign can be meaningful because of Team A−B feature definitions. Do not interpret the marginal coefficient ranking as feature importance in the multivariable model.")
    add("6. The Excel worksheet was read through stored/cached values. The script does not recalculate spreadsheet formulas; it confirms that goal_difference matches the cached team-goal columns and checks complete numerical inputs.")
    add("7. This study does not perform external historical research. Source-quality questions for previously collected football statistics remain separate from the validated workbook arithmetic.")
    add("")
    add("## Reproducibility and quality checks")
    add("")
    add("- Input shape: 104 records × 20 worksheet columns; all nine numerical modelling columns complete.")
    add("- Pearson 9×9 matrix: symmetric, diagonal exactly 1 (within numerical precision), all values bounded by [−1,+1].")
    add("- VIF: `statsmodels` auxiliary regressions (with intercept) independently agree with NumPy OLS reconstruction; no VIF for intercept is presented.")
    add("- IQR: 18 flagged feature observations, including Match 13 X7, Match 18 X8, and Match 70 X5/X6.")
    add("- X7 sensitivity: all 104 cases for main metrics and 103 only for comparison; no stored data removal.")
    add("- Each figure saves as a 320-DPI PNG; the script saves the correlation matrix, correlation summary, VIF, IQR and X7 sensitivity CSVs automatically.")
    add("")
    add("## Academic-integrity disclosure")
    add("")
    add("Generative AI assisted with script design, Python implementation, mathematical validations, plotting, draft interpretations and report construction. Coefficients, VIF values, case flags, summary statistics and charts were computed directly from the user's supplied `Master_104_Matches` sheet. External source verification, final model fitting, predictions, tests of statistical significance, and causal analysis were not performed. Programmatic agreement establishes internal arithmetic consistency, not historical football-data authenticity.")
    path.write_text("\n".join(lines)+"\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Member 1 Task 3: correlations, VIF and exploratory outlier checks only")
    parser.add_argument("--input", required=True, type=Path, help="Path to original FIFA master XLSX (read-only)")
    parser.add_argument("--output-dir", type=Path, default=Path("."), help="Folder for generated outputs")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    sha_before = hashlib.sha256(args.input.read_bytes()).hexdigest()
    rows = read_master_xlsx(args.input)
    X, y = validate_and_matrices(rows)
    pear, spear, vifs, independent, aux_r2, flags, fences, sens = get_analysis(rows, X, y)

    write_csv(args.output_dir/"member1_task3_correlation_matrix.csv",
              ["variable"] + NUMERIC,
              [[name] + [fmt(pear[i,j], 9) for j in range(9)] for i,name in enumerate(NUMERIC)])
    write_csv(args.output_dir/"member1_task3_correlation_summary.csv",
              ["variable_code", "column_name", "description", "pearson_r_with_goal_difference", "spearman_rho_with_goal_difference", "n_observations"],
              [[code,col,desc,fmt(pear[i,-1],9),fmt(spear[i],9),104] for i,(code,col,desc) in enumerate(FEATURES)])
    write_csv(args.output_dir/"member1_task3_vif_results.csv",
              ["variable_code", "column_name", "vif_with_intercept", "interpretation", "auxiliary_r_squared", "independent_numpy_vif"],
              [[code,col,fmt(vifs[i],9),vip_interpret(vifs[i]),fmt(aux_r2[i],9),fmt(independent[i],9)]
               for i,(code,col,_) in enumerate(FEATURES)])
    write_csv(args.output_dir/"member1_task3_outlier_investigation.csv",
              ["match_id", "match_date", "team_a", "team_b", "variable_code", "explanatory_variable", "observed_value", "lower_iqr_fence", "upper_iqr_fence", "reason_for_flag", "recommended_follow_up"],
              flags)
    write_csv(args.output_dir/"member1_task3_x7_sensitivity.csv",
              ["paired_variable_code", "paired_variable", "n_all", "n_without_match13", "pearson_all", "pearson_without_match13", "pearson_change_without_minus_all", "spearman_all", "spearman_without_match13", "spearman_change_without_minus_all"],
              [[*row[:4]] + [fmt(x, 9) for x in row[4:]] for row in sens])
    make_figures(args.output_dir, pear, spear, vifs)
    make_report(args.output_dir/"member1_task3_analysis_report.md", args.input, sha_before, rows, X, y,
                pear, spear, vifs, independent, aux_r2, flags, fences, sens)
    sha_after = hashlib.sha256(args.input.read_bytes()).hexdigest()
    if sha_after != sha_before:
        raise AssertionError("Original workbook modified unexpectedly!")
    print(f"PASS: {len(rows)} rows, 9 modelling columns, {len(flags)} IQR flags; clean dates and goal differences")
    print(f"PASS: correlation symmetry, bounds and diagonal; VIF NumPy check; X7 104/103 sensitivity")
    print(f"PASS: workbook unchanged (SHA-256 {sha_after})")
    print(f"Output directory: {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
