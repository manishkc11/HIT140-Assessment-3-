# X7 – Rest Days Difference: Independent Validation of Matches 51–70

**Project:** FIFA World Cup 2026, Linear Regression Objective 2.1  
**Batch:** Match IDs 51–70 (20 matches; 40 team observations)  
**Review date:** 12 October 2026  
**Input archive:** `matches_51_70.zip`

## Summary of outcome

**Status: calculations validated; individual source-link verification outstanding.**

- All four expected deliverables were present: master extract CSV, previous-matches CSV, calculated-results CSV, and Python reproduction script.
- The supplied script ran successfully using Python's standard library and generated a byte-for-byte identical results CSV.
- The reproduced `X7_Matches51_70_Calculated_Results.csv` has SHA-256 `4bc5fa5919e04434c7a39192d03f2c3a410174df8c33a83ce622b75cf9b7e9dc`.
- All 20 match IDs are unique, contiguous and ordered from 51 to 70. There are 40 team-side historical observations.
- All 20 X7 values equal zero. In every fixture the two previous-match dates are identical, so both teams have equal calendar-date rest intervals (4–6 days).
- The 40 previous-match selections were independently compared against the *actual earlier 50 match records* in the prior three supplied master-extract CSV files (batches 1–10, 11–30, and 31–50). All 40 align with the latest available earlier World Cup fixture, including match ID, opponent and date.
- The JSON historical fixture sequences embedded in this batch's previous-matches CSV were also compared against the independent earlier master extracts: 40/40 sequences matched.

## Method verified

`rest_days = (current_match_local_date - previous_match_local_date).days`  
`X7 = rest_days_team_a - rest_days_team_b`

The script checks all expected match IDs and participant sides, prevents selecting previous fixtures on or after the current date, preserves match ordering, and checks the consistency of reused prior fixture references. Calculations use *local match dates*, not article publication dates.

### Example

**Match 61, Norway vs France (26 June 2026):** Norway last played Senegal on 22 June; France last played Iraq on 22 June. Each side has four calendar days between matches, yielding **X7 = 4 − 4 = 0**.

## Results distribution

| X7 | Number of matches |
|---:|---:|
| 0 | 20 |

Rest intervals for both teams ranged from **4 to 6 calendar days**. They are not missing values or zero-day rest periods.

## Source-quality audit and limitations

1. All 40 historical observations carry an `https://www.fifa.com/` URL. There are **20 distinct source URLs**, representing 20 earlier World Cup fixtures; reused links do **not** constitute independent corroboration.
2. The source classifications in the file are 28 `MATCH_SPECIFIC`, 8 `MATCH_SPECIFIC_VIDEO`, 2 `MATCH_SPECIFIC_FEATURE`, and 2 `MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION` observations. These classifications are claims made by the supplied research file, not independent certifications that the pages contain the relevant fixture evidence.
3. The common `chronology_url` is a single general FIFA tournament-results page, *not* an independent source for each match.
4. The official FIFA tournament schedule independently supports the dates and fixtures reviewed. Source: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums .
5. Several individual URLs could be opened as opaque/empty HTML in web retrieval, and exact-path searches did not conclusively confirm those pages. **Do not claim all 20 individual links have been independently verified.** Use the official tournament schedule as a grounded overarching reference and replace unverifiable per-match links before final submission where appropriate.
6. Checking earlier World Cup matches does not prove that no intervening senior international took place outside the World Cup; in this tournament context, the preceding World Cup fixture is well supported, but the script itself cannot establish universal absence of other fixtures.
7. The supplied script reads its extracted CSVs and does not independently read the original full 104-match Excel file or authenticate websites. This review used earlier archived extracts supplied in separate batches for cross-batch verification.

## Cumulative progress

| Batch | Match IDs | Matches | Nonzero X7 | Zero X7 |
|---|---|---:|---:|---:|
| 1 | 1–10 | 10 | 7 | 3 |
| 2 | 11–30 | 20 | 15 | 5 |
| 3 | 31–50 | 20 | 2 | 18 |
| 4 | 51–70 | 20 | 0 | 20 |
| **Total** | **1–70** | **70** | **24** | **46** |

**Implication for modelling:** Through match 70, 46/70 values are zero. The final 104-row feature needs to be assessed for its overall variation, and for possible sensitivity to outliers (notably match 13's X7 = −70), before model specification. A zero difference does not mean zero preparation or recovery time.

## Academic-integrity record

Historical match selections, source choices, and the Python reproduction script were prepared with AI assistance. The researcher should retain the full chat history, original exports, independently checked summaries, any source corrections, and notes explaining the method and its limitations. The work should not be represented as wholly independently researched or programmed.

## File handling

Save the four AI-generated Batch 4 files together under `02_X7_Rest_Days/Matches_51_70/`. Save this review under `05_Evidence_and_AI_Declaration/`. Do not overwrite the untouched original master workbook.
