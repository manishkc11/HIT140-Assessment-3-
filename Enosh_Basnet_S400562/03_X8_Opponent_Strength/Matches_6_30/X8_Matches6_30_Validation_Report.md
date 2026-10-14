# X8 – Last-5 Opponent Strength Difference: Match IDs 6–30

**Review status:** Preliminary calculated research results requiring independent source-level review; **not** certified as official FIFA row-level ranking exports. Original master Excel workbook and prior X8 batches were not changed.

## Methodology and provenance

- Each current World Cup match is identified by its original `match_id` and unchanged Team A/Team B names and order.
- For each team, select its five most recent *completed senior national-team fixtures* before the World Cup fixture. Include friendlies, qualifiers, earlier World Cup fixtures, and eligible tournament matches. Where FIFA Arab Cup roster classification is material, retain a review flag.
- Choose the latest **published historical ranking edition preceding each historical fixture**, never a subsequently recalculated live ranking. The conservative date rule excludes any same-day ranking edition where exact pre-kickoff publication time is not documented.
- Read the five integer opponent ranking positions for A and for B. Take each sum divided by exactly 5 without intermediate rounding, then X8 = A average minus B average. The final X8 is formatted to 2 decimals. A smaller average rank number means historically stronger opponents.
- Research and historic ranking transcriptions were AI-assisted and sourced from FIFA's general competition schedules, national-team year archives, FIFA publication notices and third-party *dated historical ranking editions*. The attached reproducible Python script checks dates/structure and computes arithmetic; it does **not** verify web pages or certify all 250 ranking values as FIFA's official original data.

## Machine-readable validation results

- Target matches: **25**, IDs **6–30**, 25 unique IDs.
- Historical observations: **250** = 25 × 2 teams × 5 matches.
- Each team has exactly five ordered, non-duplicate previous fixtures: **PASS**, across **50** team/target contexts.
- Ranking edition dates strictly earlier than historical match dates, and historical match dates earlier than target match dates: **PASS** for 250.
- Missing rankings, match dates, opponents and source URLs in selected rows: **0**.
- First prior fixture checked against already reviewed X7 predecessor files: **50/50 PASS**.
- Earlier World Cup predecessor fixture IDs are linked to master match records: **PASS**.
- **Independent run** of exported `X8_Matches6_30_Reproduce.py` from a new temporary directory, reading only the historical research CSV, generated a byte-for-byte identical calculated results CSV: **PASS**.
- Calculation status counts: **{'CALCULATED_SECONDARY_RANKING_EVIDENCE': 20, 'PROVISIONAL_REQUIRES_MANUAL_REVIEW': 5}**.
- Manually flagged source observations: **8**; reasons: **{'FIFA_ARAB_CUP_SENIOR_STATUS_REVIEW': 7, 'PARTIALLY_DOCUMENTED_FRIENDLY': 1}**.

## Historical ranking publication editions represented

| Publication date | Observations | Evidence status |
|---|---:|---|
| 2025-09-18 | 1 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |
| 2025-10-17 | 29 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |
| 2025-11-19 | 7 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |
| 2025-12-22 | 7 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |
| 2026-01-19 | 93 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |
| 2026-04-01 | 105 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |
| 2026-06-11 | 8 | Dated secondary historical ranking archive; not universally direct FIFA row-level verification |

## Additional manual checks before transferring to master

1. **2025 FIFA Arab Cup participation (IDs 8, 18, 20, 27):** FIFA's official tournament-wide results confirm the dates and pairings of Qatar's, Iraq's and Jordan's December matches, but an independent check is needed on whether every one counts as a senior A international under the assignment's definition, particularly for teams playing alternate selections. These affect **four distinct target match IDs (8, 18, 20 and 27)**. Their X8 calculations are explicitly provisional.
2. **Cabo Verde vs Bermuda (ID 14):** The 6 June 2026 fixture is corroborated by match-specific beIN Sports and FBref records. It remains flagged because a prior historical listing was incomplete; review final documentation.
3. **Historical FIFA ranks:** All 250 numeric entries were selected from dated historical ranking tables, but most positions are not separately confirmed within FIFA's own row-level historical tables. This is a source-quality limitation affecting the **entire batch**, not just the five flagged results. Numeric agreement within a single historical archive is not two independent sources.
4. **2025 backfill:** Some teams did not have five completed matches in 2026 before the World Cup, so the selected five extend back to 2025. These must remain in descending date order.
5. **General versus specific sources:** The FIFA World Cup master chronology and FIFA Arab Cup results pages are labelled GENERAL; national football team-year pages are dated secondary indexes, not individual FIFA match reports. Prior X7 or X8 v2 source URLs may be match-specific and are labelled by actual provenance.
6. **Same-day edition restriction:** Ranking editions on the historical match date are excluded without documented release times; all 250 chosen publication dates strictly precede fixtures.

## Reproduce locally

Keep `X8_Matches6_30_Historical_Research.csv` beside `X8_Matches6_30_Reproduce.py`, then run:

```bash
python X8_Matches6_30_Reproduce.py
```

This produces `X8_Matches6_30_Calculated_Results.csv` with standard-library Python (`csv`, `datetime`, `decimal`) and no web requests. Missing rankings generate a blank X8 with `INCOMPLETE_DO_NOT_USE`; dates on or after their target and duplicates stop the script with an error.

## Worked example: Match 6 – Australia versus Türkiye, 13 June 2026

From the research rows, Australia's five previous opponents are Switzerland (April rank 19), Mexico (15), Curaçao (January rank 81), Cameroon (January rank 45), Colombia (October 2025 rank 13): total **173**, mean **34.60**. Türkiye's five previous opponents are Venezuela (April rank 49), North Macedonia (April rank 67), Kosovo (January rank 79), Romania (January rank 49), Spain (October rank 1): total **245**, mean **49.00**. Therefore `X8 = 34.60 − 49.00 = −14.40`. Each ranking is chosen from the edition published *before that historical match*, which is why different ranking editions can appear within the same last-five window.

## Academic integrity declaration

Generative AI (ChatGPT) assisted in locating and transcribing published senior international fixture results, selecting historical ranking editions and URLs, reviewing data consistency against earlier X7 research, preparing source logs and this report, and generating the Python validation/calculation code. Python independently performed count, uniqueness, chronological-date, basic numeric-range and arithmetic checks and reproduced the CSV output. Source authenticity and each historical rank's FIFA-row accuracy require human review; the computations should not be described as universally FIFA-verified. No assumptions were substituted for missing input values.
