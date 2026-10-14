# X8 Matches 61–90 — Independent Validation

**Review date:** 13 October 2026  
**Input:** `Archive(4).zip`  
**Scope:** FIFA World Cup 2026 match IDs 61–90; no original source files were edited.

## Verdict

**Accept as computationally reproducible working data.** No numerical corrections were identified in this batch. Do not represent the 30 X8 values as fully verified against FIFA's official individual historical ranking rows: the supplied research relies substantially on dated secondary ranking archives and project research reused from earlier batches.

## Files received

- `X8_Matches61_90_Historical_Research.csv`
- `X8_Matches61_90_Calculated_Results.csv`
- `X8_Matches61_90_Reproduce.py`
- `X8_Matches61_90_Source_Log.csv`
- `X8_Matches61_90_Validation_Report.md`

The ZIP also contained macOS metadata entries (`__MACOSX/`), which were ignored.

## Computation and consistency checks performed

| Check | Independent result |
|---|---|
| Required files present | 5/5 |
| Match IDs | 61–90: all 30 distinct IDs |
| Historical observations | 300 |
| Ranking-policy code tests | 7 passed |
| Reproduction from research CSV in a separate directory | Passed; byte-for-byte identical |
| SHA-256 of submitted and regenerated results | `59514e58dcc34ace4a2908a964b761c0185c53dfc20cbfc4327552fdde819131` |
| X8 recalculation using an independent CSV arithmetic check | 30/30 correct |
| Latest fixture against separately supplied X7 full evidence file | 60/60 matched |
| Earlier World Cup references against separately supplied X7/master chronology | 160/160 matched |
| Selected World Cup fixtures belong to each team's latest five eligible earlier tournament fixtures | 60/60 selections matched the known master history |
| Reused team/date/opponent pairs cross-checked with actual earlier X8 research files | 219 matches, 0 disagreements |
| Ranking conflicts versus the available earlier X8 research records | 0 newly introduced conflicts |
| Missing fixture or ranking source URLs in the selected research | 0 |
| Result statuses | All 30 explicitly marked as reliant partly on secondary ranking sources |

**Important nuance:** The accessible earlier Version 2 research still contains the previously identified Scotland ranking 41 error. This is not a new conflict introduced by the current batch; the current records use Scotland = 42 where applicable. The separately generated **matches 6–30 Version 3 correction files were not part of this ZIP** and have not been directly compared here.

## Batch statistics

- 18 positive X8 values, 12 negative values, no exact zero values.
- Largest absolute X8 is match 63, **Egypt vs IR Iran = -35.20**.
- Historical observations by ranking edition:
  - 11 June 2026: 160
  - 1 April 2026: 112
  - 19 January 2026: 27
  - 17 October 2025: 1
- 160 historical rows refer to previous World Cup fixtures. Their `fixture_source_url` is the **general FIFA tournament chronology** page, not match-specific independent verification.
- The historical research file includes 135 rankings classified as `SECONDARY_EDITION_REVIEW_REQUIRED`, another 160 derived from the secondary dated 11 June table, and five with other qualifications or corroboration. All 30 output statuses communicate secondary-evidence limitations.
- The source log contains 116 distinct source URLs.

## Selected external corroboration (not a full source audit)

1. The 11 June 2026 FIFA ranking was published before the opening World Cup match; see official FIFA announcement: https://tickets.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola
2. The dated 11 June 2026 rankings list Scotland at 42; see https://wildstat.com/p/7001/ddate/2026-06-11 and https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup
3. FIFA's warm-up results explicitly record Cabo Verde beating Bermuda 3–0 on 6 June: https://www.fifa.com/en/articles/pre-tournament-warm-up-results-fixtures-scorers

These sources corroborate selected dates/values and ranking methodology. They do not validate all 300 historical observations against official row-level ranking data.

## Remaining limitations

- The script's embedded master/ranking snapshots enable consistency testing, but are generated project reference data rather than independent copies of FIFA's historical records.
- The script checks recorded historical chronology and ranking editions, not that all external URLs load or that complete senior-A histories have no missing matches.
- The Qatar Arab Cup eligibility issue from earlier batches remains unresolved, although none of those flagged fixtures is among the 300 selected records in this batch.
- Preserve all original and corrected batch versions for the AI declaration; explicitly distinguish AI-assisted research/coding from manual or separately performed verification.

## Recommended next action

Store this batch in `03_X8_Opponent_Strength/Matches_61_90/` and this independent report in `05_Evidence_and_AI_Declaration/`. Proceed to match IDs 91–104 using the same two-decimal method, the 11 June 2026 ranking convention, and versioned source evidence. Before final X8 consolidation, obtain the separate matches 6–30 Version 3 correction ZIP and verify the corrected Match 29 result is -43.60.
