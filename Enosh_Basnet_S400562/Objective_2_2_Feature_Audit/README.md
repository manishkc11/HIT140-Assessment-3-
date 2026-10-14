# Objective 2.2 — Independent EDA / Feature Audit

This package is **an audit of supplied data and already-trained model outputs**. It does not retrain or modify Objective 2.2, Objective 2.1, or the submitted Excel workbook.

## Reproduction on macOS (Python 3)

1. Place these three user-supplied inputs alongside the audit script:
   - `Regression_2_2_Final (2(1).zip`
   - `FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting(2).xlsx`
   - `Part3_Evaluation(1).zip`
2. Create a virtual environment and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python Objective_2_2_EDA_Feature_Audit.py \
  --model-zip 'Regression_2_2_Final (2(1).zip' \
  --master-xlsx 'FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting(2).xlsx' \
  --evaluation-zip 'Part3_Evaluation(1).zip' \
  --output-dir audit_out
```

The script uses only Python standard-library ZIP/XML facilities to inspect the Excel workbook read-only. It loads the team-level CSV with pandas, calculates exploratory statistics and training-only diagnostic VIFs, compares saved predictions/metrics, and creates four 320-DPI figures.

## Primary files

- `Objective_2_2_Feature_Justification.csv`: definitions, pre-match availability and potential Objective 2.1 feature overlap.
- `Objective_2_2_EDA_Summary.csv`: descriptive statistics for eight predictors and actual goals.
- `Objective_2_2_Methodological_Audit.md`: decision, findings, validation, unresolved evidence and recommended actions.
- `Objective_2_2_Final_Report_Contribution.docx`: 321-word draft for *integration* into the group's four-page Word report (not a separate final submission).
- `figures/`: four 320-DPI publication-quality PNGs; **Figure D** is recommended for the final report.
- Supporting CSVs and `audit_checks.json` provide independent calculation evidence.

**Decision: REVISION REQUIRED (conditional on the strict conceptual-overlap reading).** Cumulative World Cup goals conceded may duplicate Objective 2.1's historical-goals-conceded concept. Ask the lecturer to clarify the maximum-four-shared-concepts rule before submission. A potential change would require the model owner to revisit the affected Objective 2.2 dataset, model and evaluation; none are altered in this audit.

**AI assistance:** AI contributed to the technical review, source inspection, code writing, chart design and academic draft. Structural/arithmetic conclusions are reproducible. External football record authenticity has **not** been independently established by the scripts.
