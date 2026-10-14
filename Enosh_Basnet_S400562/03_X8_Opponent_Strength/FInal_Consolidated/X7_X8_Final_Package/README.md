# FIFA World Cup 2026 — Consolidated X7 + X8

This is the reproducible working dataset for two explanatory variables from 104 matches:

- **X7** (`rest_days_diff`): calendar-date interval since Team A's latest completed match, minus that of Team B.
- **X8** (`last5_opponent_strength_diff`): average FIFA ranking of Team A's five previous opponents minus the same average for Team B; lower FIFA ranking number means stronger-ranked previous opposition.

## Files to give your team

- `outputs/X7_X8_104_Merge_Ready.csv` — **PRIMARY**; unique `match_id`, X7 and X8, ready to merge into your original master sheet.
- `outputs/X7_X8_104_With_Match_Info.csv` — same values plus dates, teams, component values, review status and source batch.
- `outputs/X8_104_Merge_Ready.csv` — X8 alone when X7 has already been added to your group's master dataset.
- `FIFA_2026_X7_X8_Consolidated.xlsx` — workbook with 104 model rows, linked calculation formulas, all 1040 research observations, X7 evidence, review notes and a batch manifest.

## Reproduce the calculations

From this folder:

```bash
python3 Consolidate_X7_X8.py
```

Uses Python standard library only, reads the 13 archived CSVs in `inputs/`, and regenerates all CSVs and the validation report in `outputs/`. It never changes the source input files.

The prebuilt `.xlsx` is provided for spreadsheet review and can be reconciled with the reproduced CSVs. The script regenerates CSV outputs, not the Excel workbook.

## Evidence and audit

- `outputs/X8_104_Historical_Evidence.csv` — all 1040 research observations with historical dates, opponents, ranking editions and source URLs.
- `outputs/X7_X8_Source_Review_Log.csv` — unresolved historical verification issues and legacy correction notes.
- `outputs/X7_X8_Consolidation_Validation_Report.md` — internal validation checks, version controls, caveats, and academic-integrity disclosure.

**Version control:** Use `x8_6_30_v3_results.csv` and `x8_6_30_v3_history.csv`. Match 29 X8 is **-43.60**, corrected from -43.40 when Scotland's 11 June 2026 published FIFA rank was revised from 41 to 42. Older v1/v2 results must not be merged.

**Important limitation:** The Python checks demonstrate internal consistency and arithmetic reproducibility, but do not independently authenticate every ranking or fixture webpage. Some rankings rely on dated secondary archives, and Arab Cup senior-international classification questions remain flagged.

**Original master file:** The original group's 20-column `Master Dataset.xlsx` was not provided as an editable source in this consolidation, so this package does not modify it. Use `match_id` to populate the master `rest_days_diff` and `last5_opponent_strength_diff` columns after team review.

## Academic integrity

Data collection, ranking transcription, historical verification support, Python coding, correction logging, consolidation, and internal auditing were AI-assisted. The user should review code and independently check cited sources and sample calculations, disclosing the assistance in the assignment's required AI declaration.
