# X8 – Independent Calculation Audit (Matches 1–5)

**Project:** FIFA World Cup 2026, Objective 2.1, Multiple Linear Regression  
**Variable:** X8 — Last-5 Opponent Strength Difference  
**Audit date:** 12 October 2026  
**Input:** `Archive.zip` with calculation CSV, historical input CSV, reproduction Python script, and agent report  
**Assessment:** Calculation-complete / reproducible. Source verification is not complete for every historical ranking or fixture.

## 1. Checks performed

- Extracted four required deliverables from the supplied ZIP (`__MACOSX` metadata ignored).
- Reviewed the reproduction script to confirm it reads its declared input and writes the calculated output.
- Ran `X8_Matches1_5_Reproduce.py` against the exported input using a separate output filename.
- Compared regenerated and submitted calculated-results CSV files byte for byte; **identical**.
- Confirmed the exported historical input CSV is **byte-for-byte identical** to the previously supplied Version 2 ranking research CSV.
- Independently regrouped all 50 historical observation rows by match ID and team side using Python's `csv` module, summed the five opponent ranking positions for each side, and recomputed X8. All five rows agreed.
- Compared each team's latest previous-match row (recency = 1) against the first-batch X7 previous-match research CSV. **10/10** dates, opponent names, and team labels matched.
- Confirmed the input's historical fixture dates and ranking publication dates pass the script's strict chronological checks. This is an **internal data-consistency check**, not independent verification of every website.

Calculated-results CSV SHA-256: `74dbd0d9c01938b7f25acd9938d69746f9b893fbfe6d361be19a6f07f21d3337`  
Historical input CSV SHA-256: `8f39ab9c732dfd1454120bf513b75a0d232a084a109acc7116fb1d51f3e2d399`

## 2. Independently reproduced results

| Match ID | Fixture | Team A rank sum | Team B rank sum | Team A mean | Team B mean | X8 |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Mexico vs South Africa | 155 | 325 | 31.00 | 65.00 | -34.00 |
| 2 | Korea Republic vs Czechia | 336 | 454 | 67.20 | 90.80 | -23.60 |
| 3 | Canada vs Bosnia and Herzegovina | 324 | 172 | 64.80 | 34.40 | +30.40 |
| 4 | USA vs Paraguay | 54 | 215 | 10.80 | 43.00 | -32.20 |
| 5 | Haiti vs Scotland | 392 | 234 | 78.40 | 46.80 | +31.60 |

Calculation: `X8 = (sum of Team A's five preceding opponents' official rank numbers / 5) – (sum of Team B's five preceding opponents' official rank numbers / 5)`. Lower rank numbers correspond to higher-ranked opponents.

## 3. Nicaragua October 2025 ranking sensitivity

- Baseline in research CSV: Nicaragua rank **133** on 17 October 2025, used for Haiti's 18 November 2025 match.
- Published contemporary evidence supports rank **133** (e.g., *La Prensa*, 19 October 2025, reporting Nicaragua at #133 with 1,106.83 points): https://www.laprensani.com/2025/10/19/deportes/3549368-nicaragua-desciende-en-el-ranking-mundial-de-la-fifa
- A dated table also gives Nicaragua #133: https://hiyun0727.blogspot.com/2025/10/fifa-mens-world-ranking-20251017.html
- A separate reported value of 132 remains documented; the dated evidence above favours the recorded 133, although the exact row was not independently retrieved from FIFA's own historical table.
- Match 5 baseline X8: **+31.60**. Replacing Nicaragua's rank with 132 would yield **+31.40** (difference **−0.20**); no source value has been changed in this audit.
- Nicaragua's April 2026 ranking (131), elsewhere in the research CSV, is for a different edition and is unaffected.

## 4. Limitations and academic integrity

- Calculations and data linkage are independently reproducible **given the input ranking values**. This does not establish that each of the 50 recorded historical ranking positions is directly authenticated against FIFA's own ranking database.
- The Python script checks that prior matches are chronological; it cannot prove from CSV data alone that there were no additional unlisted internationals. The 10 most recent fixture selections agree with the X7 source dataset, but both rely partly on research provenance.
- FIFA rank positions are ordinal; the arithmetic mean of positions is a pragmatic explanatory feature, not an official FIFA team-strength rating.
- AI assistance included historical match selection, ranking research, comparison of archives, code generation and the initial validation report. The independent CSV/code reproduction and record cross-checks are documented separately; the user should inspect and understand the process before submitting.

## 5. Conclusion and file retention

**Decision:** Accept match IDs 1–5 as **calculation-complete, reproducible working data**, retaining the historical-source limitations. Do not yet describe all 50 inputs as individually verified by FIFA. Preserve the original source CSV, Version 2 verification CSV and change log, input extract, output CSV, Python script, and all AI conversations. Keep the master workbook unchanged until approved for integration.

Recommended storage:
- `03_X8_Opponent_Strength/Matches_1_5/`: four Stage B deliverables and previous v2 source/change log.
- `05_Evidence_and_AI_Declaration/`: this independent audit report.
