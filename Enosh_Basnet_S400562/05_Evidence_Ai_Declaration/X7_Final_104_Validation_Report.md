# X7 – Rest Days Difference: Final Validation and Consolidation

**Project:** FIFA World Cup 2026 — Linear Regression Objective 2.1  
**Prepared:** 12 October 2026  
**Scope:** 104 match IDs, 6 batches, 208 team-level preceding-match records  
**Status:** Calculations and internal chronology verified; external-source audit is not exhaustive.

## 1. Objective and definition

For every tournament match, calculate:

- `Team A Rest Days = (current local match date – Team A's previous completed senior international match local date).days`
- `Team B Rest Days = (current local match date – Team B's previous completed senior international match local date).days`
- `X7 = Team A Rest Days – Team B Rest Days`

A value of `0` indicates that the two teams have **equal rest intervals**, not that either team had no rest. Shootouts and extra time do not affect calendar-date subtraction.

## 2. Files reviewed

- `first_10_matches.zip` — match IDs 1–10.
- `matches_11_30(1).zip` — match IDs 11–30.
- `matches_31_50.zip` — match IDs 31–50.
- `matches_51_70.zip` — match IDs 51–70.
- `matches_71_90.zip` — match IDs 71–90.
- `matches_91_104.zip` — match IDs 91–104.

Each contained a master extract, the team-level previous-match source records, the calculated results, and a Python reproduction script.

## 3. Final batch (91–104) checks

| Check | Result |
|---|---|
| Four deliverables present | Passed |
| 14 original match IDs, no duplicates | Passed |
| 28 previous team-level observations | Passed |
| 26 distinct predecessor World Cup fixtures | Passed |
| All previous fixture dates before current matches | Passed |
| Team A/B order retained | Passed |
| Date arithmetic | 14/14 passed |
| Rerun of `X7_Matches91_104_Reproduce.py` | Passed |
| Output equality | Byte-for-byte identical CSV |

SHA-256 of the original and reproduced final-batch results CSV:  
`4c2135235dc8051e7b15b128e34d14f2e069a3aa19a46f9dc8003a371e47c3df`

Six matches have X7 `+1`; eight have X7 `0`. Matches 103 (France–England on July 18) and 104 (Spain–Argentina on July 19) correctly reference semi-finals 101 (July 14) and 102 (July 15). FIFA confirms these fixtures and dates: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/knockout-stage-match-schedule-bracket

## 4. Cross-batch audit (all 104 matches)

A separate consolidation script read all six original ZIPs and performed these checks:

1. Exactly 104 match IDs, in order 1–104 with no duplicates or omissions.
2. The match date and Team A/B names in every calculated-results row matched that batch's unmodified master extract.
3. Exactly 208 team-level historical records, each matched to its appropriate current match and side.
4. Historical match dates were strictly earlier than the current match dates.
5. Recomputed Team A and Team B rest days matched every supplied value.
6. Recomputed `A rest – B rest` matched every submitted X7 result.
7. For every team with earlier World Cup fixtures in the consolidated master extracts, the chosen previous fixture matched the *latest* earlier World Cup match in that chronology. Where a predecessor match ID was recorded, that ID also matched.

**Result: All these checks passed.** Note that they establish consistency with the exported dataset and tournament records. They do not independently certify every pre-tournament friendly or exhaustively confirm every external URL.

## 5. Final distribution

| X7 value | Number of matches |
|---:|---:|
| -70 | 1 |
| -8 | 1 |
| -3 | 1 |
| -2 | 2 |
| -1 | 9 |
| 0 | 62 |
| +1 | 21 |
| +2 | 3 |
| +3 | 2 |
| +4 | 1 |
| +6 | 1 |
| **Total** | **104** |

- Zero: **62** (59.6%); positive: **28** (26.9%); negative: **14** (13.5%).
- Mean X7: approximately **-0.490** days; median: **0**.
- Minimum: **-70**, Match 13, Saudi Arabia–Uruguay.
- Maximum: **+6**, Match 20, Austria–Jordan.
- Excluding Match 13 *for an exploratory sensitivity comparison only*, the mean becomes approximately **+0.184** days. **Do not remove that row from the main dataset without methodological justification.**

### Modelling implication

X7 is heavily concentrated at zero because teams frequently played on the same dates. The -70 outlier has a substantial impact on the mean and may influence fitted linear regression coefficients. The team should inspect regression diagnostics and, where appropriate, compare results with and without this observation **as a documented sensitivity analysis**, not silently delete it.

## 6. Remaining limitations

- Reproducing calculations checks arithmetic and input consistency; it does **not** guarantee that all linked pages contain the specified evidence.
- Some records cite a tournament roundup or verified video rather than an individual match report. These source types are documented and should not be mischaracterised as independent confirmations.
- The X7 -70 value relies on the completeness of Uruguay's senior international match history; earlier validation reviewed official association chronology, but completeness remains a methodological limitation.
- FIFA's match report for Spain–Austria appears to use an unusual URL path. The retrieved search result supports the fixture; retain a stable FIFA knockout-stage listing as supporting general chronology: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/knockout-stage-match-schedule-bracket
- Results represent **calendar-date intervals**, not adjusted hours of rest, travel fatigue, or recovery quality.

## 7. Outputs for the group

- `X7_104_Consolidated_Workbook.xlsx`: standalone workbook with calculations, source URLs, a formula-driven merge tab, and a summary. **Does not edit the original master workbook.**
- `X7_104_Merge_Ready.csv`: two columns, `match_id` and `rest_days_diff`, for safely joining X7 to the original master sheet.
- `X7_104_Full_Evidence.csv`: 104 rows containing the dates, previous opponents, intervals, final values, and source URLs.
- `X7_104_Consolidate_and_Check.py`: program used for the 104-record consolidation; requires all six original ZIPs in the same directory.

### Where to save

- Consolidated workbook, both CSV files, and the program: `02_X7_Rest_Days/Final_Consolidated/`
- This report: `05_Evidence_and_AI_Declaration/`
- Retain all six original ZIPs and the AI conversation history.

## 8. AI-assistance disclosure

Generative AI assisted with the historical-fixture research, source selection, Python programming, and preparation of audit outputs. The scripts can reproduce date calculations and verify consistency with the supplied extracts. Final acceptance of the historical source selections and interpretation of regression diagnostics remain part of the student's review. This report does not assert that every linked website was manually audited.
