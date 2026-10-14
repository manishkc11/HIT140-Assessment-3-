# X7 – Matches 71–90: Independent Validation Record

**Assignment:** FIFA World Cup 2026 — Linear Regression Objective 2.1  
**Reviewed batch:** Match IDs 71–90, 20 matches, 40 team-level previous-match observations  
**Scope of validation:** reproducibility, date arithmetic, cross-batch previous-match matching, and selected external source corroboration  
**Disposition:** ACCEPTED AS REPRODUCIBLE WORKING DATA, subject to full source-link audit before final submission.

## 1. Files inspected

- `X7_Matches71_90_Master_Extract.csv` — 20 rows and 6 columns.
- `X7_Matches71_90_Previous_Matches.csv` — 40 rows and 12 columns.
- `X7_Matches71_90_Calculated_Results.csv` — 20 rows and 16 columns.
- `X7_Matches71_90_Reproduce.py` — standard-library Python reproduction script.

Ignored operating-system metadata (`__MACOSX`) in the uploaded ZIP.

## 2. Checks and outcomes

| Check | Result |
| --- | --- |
| Batch IDs unique and ordered 71–90 | PASS |
| 20 matches, 40 team-history records | PASS |
| No blank calculation dates | PASS |
| Recalculated Python calendar-date differences | PASS — all 20 |
| Python script executed in an isolated temporary folder | PASS — exit code 0 |
| Reproduced output exactly matches supplied CSV | PASS — same SHA-256 hash |
| Prior dates/opponents match earlier batch master extracts | PASS — all 40 |
| Selected prior match latest in the combined matches 1–90 history | PASS — all 40 |
| Embedded earlier fixture-history JSON matches independently recomputed master history | PASS — all 40 |
| Unique prior World Cup match IDs | 30 |
| Unique match-specific or feature source URLs provided | 30 (not all content independently audited) |
| General FIFA chronology URLs | 1, reused across all observations |
| Direct live verification of all 30 source webpages | NOT COMPLETE |

**Reproduction SHA-256 (`X7_Matches71_90_Calculated_Results.csv`):**

`06858858e31d4f647bb1902b0c17cb5df69651b99442ae439a5d47d54ce75a2e`

## 3. Result table

| Match ID | Fixture | Team A rest | Team B rest | X7 |
| ---: | --- | ---: | ---: | ---: |
| 71 | Colombia vs Portugal | 4 | 4 | 0 |
| 72 | Congo DR vs Uzbekistan | 4 | 4 | 0 |
| 73 | South Africa vs Canada | 4 | 4 | 0 |
| 74 | Germany vs Paraguay | 4 | 4 | 0 |
| 75 | Netherlands vs Morocco | 4 | 5 | -1 |
| 76 | Brazil vs Japan | 5 | 4 | 1 |
| 77 | France vs Sweden | 4 | 5 | -1 |
| 78 | Côte d'Ivoire vs Norway | 5 | 4 | 1 |
| 79 | Mexico vs Ecuador | 6 | 5 | 1 |
| 80 | England vs Congo DR | 4 | 4 | 0 |
| 81 | USA vs Bosnia and Herzegovina | 6 | 7 | -1 |
| 82 | Belgium vs Senegal | 5 | 5 | 0 |
| 83 | Portugal vs Croatia | 5 | 5 | 0 |
| 84 | Spain vs Austria | 6 | 5 | 1 |
| 85 | Switzerland vs Algeria | 8 | 5 | 3 |
| 86 | Argentina vs Cabo Verde | 6 | 7 | -1 |
| 87 | Colombia vs Ghana | 6 | 6 | 0 |
| 88 | Australia vs Egypt | 8 | 7 | 1 |
| 89 | Paraguay vs France | 5 | 4 | 1 |
| 90 | Canada vs Morocco | 6 | 5 | 1 |

### Distribution and interpretation

Counts: -1: 4, +0: 8, +1: 7, +3: 1.
12 of the 20 values are non-zero; the largest absolute difference is **+3 (match ID 85, Switzerland vs Algeria)**.
Match 85: Switzerland last played Canada on 24 June; Algeria last played Austria on 27 June; target match 2 July. Therefore 8 − 5 = +3 calendar days.

## 4. External corroboration performed

- FIFA official 2026 knockout-stage results page: confirms 29 June–4 July match IDs/fixtures/dates, including 74–90: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/knockout-stage-match-schedule-bracket
- FIFA official schedule corroborates the 27 June group-stage fixtures and 28 June match 73: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums
- FIFA Germany vs Paraguay official 29 June match report (relevant to match 89 previous Paraguay fixture): https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/germany-paraguay-review-highlights
- FIFA France vs Sweden match report corroborates their 30 June fixture (relevant to match 89 previous France fixture): https://ppr-www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/france-sweden-review-highlights?searchOverlay=1
- Scottish FA match report explicitly records Scotland vs Brazil as played **24 June 2026**, even though the article header displays 23 June: https://www.scottishfa.co.uk/en/news/match-report-or-scotland-v-brazil

These external checks support the reviewed examples and official tournament chronology. They do **not** constitute a completed independent content audit of every one of the 30 individual recorded URLs.

## 5. Caveats and validation boundaries

1. **Reproduction is not source authentication.** The Python script checks URL format and exported histories; it cannot determine whether an external webpage actually contains the claimed fixture.
2. **Avoid circular verification.** The embedded fixture-history JSON comes from the same master workbook as prior extracts. This reviewer also reconstructed independent chronology from the *earlier saved batch master extracts*, which verifies consistent processing but is not a separate FIFA history database.
3. **Date convention.** Rest days are elapsed *local calendar-date intervals*; no kickoff-time or time-zone precision is claimed.
4. **Source count.** 40 historical team observations correspond to 30 distinct prior fixtures, with 30 unique source links and one reused FIFA general schedule link. Repeated links are not independent confirmations.
5. **Unexpected publication dates.** Scotland FA report displays an article date of 23 June but explicitly lists the fixture date as 24 June. Use fixture date, not the publication header; document the discrepancy.
6. **Model interpretation.** X7 equals the *difference* between teams’ rest intervals. X7=0 means equal intervals, not that neither team rested. More non-zero X7 values appear in this knockout batch than in the third-group batch.

## 6. AI declaration notes

The user employed generative AI for fixture research, source gathering and Python code preparation. The reviewer reran the generated script, independently recomputed rest-day arithmetic and cross-checked the selection of preceding fixtures against previously saved master extracts; selected external FIFA and Scottish FA material was checked separately. Final source verification and interpretation remain the student’s responsibility. Do not state that all URLs have been independently audited.

## 7. Next action

Keep the four original agent files under `02_X7_Rest_Days/Matches_71_90/`; save this report under `05_Evidence_and_AI_Declaration/`. Proceed to match IDs 91–104 using the same methodology, then consolidate and audit all 104 X7 values without overwriting the raw research files.
