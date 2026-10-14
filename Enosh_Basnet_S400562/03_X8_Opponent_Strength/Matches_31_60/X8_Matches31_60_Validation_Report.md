# X8 – Matches 31–60: Research, Calculation and Validation

**Review status:** 30 computed results available; three have additional historical-source/eligibility flags. Other rows still depend partly on secondary ranking archives, so “calculated” is not synonymous with direct FIFA row-level verification.

## Scope and input provenance

- Original match IDs, dates, Team A/B ordering: read from the unchanged `Master Dataset(1).xlsx`, rows for match IDs 31–60.
- Existing historical team histories: reused **corrected** `X8_Matches6_30_Historical_Research_v2.csv` and reviewed `X8_Matches1_5_Historical_Opponents_Rankings_v2_verified.csv`, not original 6–30 v1.
- A reusable cache contained **240 distinct pre-World Cup team-fixture records (48 teams × five matches)**. The current 300-row output uses **216 observations of those prior team histories**, plus **84 earlier World Cup observations**. These are observation counts, so repeated references to the same historic fixture are intentional.
- Earlier World Cup fixture dates/opponents were derived from the master match chronology and checked against the official FIFA tournament results page. The latest predecessor was cross-checked with the existing X7 records for all 60 target team entries.
- The first **11 June 2026** FIFA ranking was released before the first World Cup kickoff, according to FIFA’s official announcement. All prior World Cup opponents are ranked using the **11 June 2026** published edition; older previous fixtures retain the earlier published ranking edition appropriate to their date.
- Data source classification is deliberately conservative: FIFA’s tournament-wide results page is used as the primary **GENERAL** evidence for earlier World Cup games. Previously collected match-specific links are retained in `reused_match_specific_url_unverified` and are not claimed to be fresh independent verifications.

## Equation and interpretation

`X8 = (sum of A previous-five opponent FIFA ranks / 5) − (sum of B previous-five opponent FIFA ranks / 5)`

Negative X8: Team A’s previous opponents had a lower numerical FIFA rank (stronger-ranked opponents on this metric). Positive X8: Team B’s previous opponents had the lower mean rank. This measures past opposition, not match winner or goals.

## All calculated results

| ID | Team A | Team B | A sum | A avg | B sum | B avg | X8 | Calculation status |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 31 | Türkiye | Paraguay | 271 | 54.20 | 216 | 43.20 | **11.00** | Secondary evidence |
| 32 | USA | Australia | 80 | 16.00 | 182 | 36.40 | **-20.40** | Secondary evidence |
| 33 | Germany | Côte d'Ivoire | 261 | 52.20 | 119 | 23.80 | **28.40** | Secondary evidence |
| 34 | Ecuador | Curaçao | 205 | 41.00 | 362 | 72.40 | **-31.40** | Secondary evidence |
| 35 | Netherlands | Sweden | 151 | 30.20 | 187 | 37.40 | **-7.20** | Secondary evidence |
| 36 | Tunisia | Japan | 183 | 36.60 | 201 | 40.20 | **-3.60** | Secondary evidence |
| 37 | Uruguay | Cabo Verde | 123 | 24.60 | 337 | 67.40 | **-42.80** | Manual review |
| 38 | Spain | Saudi Arabia | 247 | 49.40 | 248 | 49.60 | **-0.20** | Secondary evidence |
| 39 | Belgium | IR Iran | 115 | 23.00 | 330 | 66.00 | **-43.00** | Secondary evidence |
| 40 | New Zealand | Egypt | 237 | 47.40 | 113 | 22.60 | **24.80** | Secondary evidence |
| 41 | Norway | Senegal | 128 | 25.60 | 249 | 49.80 | **-24.20** | Secondary evidence |
| 42 | France | Iraq | 138 | 27.60 | 331 | 66.20 | **-38.60** | Secondary evidence |
| 43 | Argentina | Austria | 375 | 75.00 | 276 | 55.20 | **19.80** | Secondary evidence |
| 44 | Jordan | Algeria | 133 | 26.60 | 195 | 39.00 | **-12.40** | Secondary evidence |
| 45 | England | Ghana | 183 | 36.60 | 120 | 24.00 | **12.60** | Secondary evidence |
| 46 | Panama | Croatia | 347 | 69.40 | 90 | 18.00 | **51.40** | Secondary evidence |
| 47 | Portugal | Uzbekistan | 157 | 31.40 | 186 | 37.20 | **-5.80** | Secondary evidence |
| 48 | Colombia | Congo DR | 178 | 35.60 | 318 | 63.60 | **-28.00** | Secondary evidence |
| 49 | Scotland | Brazil | 285 | 57.00 | 163 | 32.60 | **24.40** | Secondary evidence |
| 50 | Morocco | Haiti | 325 | 65.00 | 260 | 52.00 | **13.00** | Manual review |
| 51 | Switzerland | Canada | 242 | 48.40 | 276 | 55.20 | **-6.80** | Secondary evidence |
| 52 | Bosnia and Herzegovina | Qatar | 162 | 32.40 | 248 | 49.60 | **-17.20** | Manual review |
| 53 | Czechia | Mexico | 280 | 56.00 | 225 | 45.00 | **11.00** | Secondary evidence |
| 54 | South Africa | Korea Republic | 289 | 57.80 | 280 | 56.00 | **1.80** | Secondary evidence |
| 55 | Curaçao | Côte d'Ivoire | 292 | 58.40 | 94 | 18.80 | **39.60** | Secondary evidence |
| 56 | Ecuador | Germany | 279 | 55.80 | 276 | 55.20 | **0.60** | Secondary evidence |
| 57 | Japan | Sweden | 170 | 34.00 | 165 | 33.00 | **1.00** | Secondary evidence |
| 58 | Tunisia | Netherlands | 118 | 23.60 | 157 | 31.40 | **-7.80** | Secondary evidence |
| 59 | Türkiye | USA | 263 | 52.60 | 98 | 19.60 | **33.00** | Secondary evidence |
| 60 | Paraguay | Australia | 224 | 44.80 | 154 | 30.80 | **14.00** | Secondary evidence |

## Worked example: match ID 31 (Türkiye vs Paraguay)

For Türkiye, the five most recent opponents (with historical ranking values) are Australia **27** (World Cup on 13 Jun), Venezuela **49** (6 Jun), North Macedonia **67** (1 Jun), Kosovo **79** (31 Mar), and Romania **49** (26 Mar). Sum = **271**, average = **54.20**.
For Paraguay, the previous five opponents are USA **17** (World Cup on 12 Jun), Nicaragua **131** (5 Jun), Morocco **8** (31 Mar), Greece **46** (27 Mar), and Mexico **14** (18 Nov 2025). Sum = **216**, average = **43.20**.
**X8 = 54.20 − 43.20 = +11.00.** The first opponent in each list played in the World Cup, so the June 11 ranking applies; earlier games use their own historical editions.

## Verification checks

| Check | Finding |
|---|---|
| Total research observations | **300**, corresponding to 30 × 2 × 5 |
| Match IDs | Exactly **31–60**, 30 distinct IDs |
| Team histories | Exactly **60**, each with five different previous fixtures |
| Duplicate recency keys / fixture pairs | None; two matches against same opponent on different dates are allowed |
| Original Team A/B order and target dates | Matched to embedded master match control table in script |
| Previous fixture chronology | All preceding dates are strictly before target fixture dates |
| World Cup opponent and earlier match ID | Matched against the corresponding master fixture (84 team observations, 36 distinct WC matches) |
| Most recent earlier World Cup fixture | Matched to X7 for all **60/60** team entries |
| Ranking edition selection | Publication precedes fixture, or 11 June same-day has confirmed pre-kickoff official statement; approved editions tested |
| Missing dates, ranks, ranking/fixture source URL fields | **0** in selected baseline data |
| Official FIFA row-level verification for every ranking | **NOT established**; dated secondary archives and previously researched ranking evidence remain material |
| Rank release policy tests | **9/9 passed** including accepted/rejected same-day cases |
| Mutation tests | Missing pre-kickoff evidence rejected; tampered WC predecessor rejected; missing rank produces blank X8, never substituted with 0 |
| Isolated reproduction | Python script rerun in a separate temporary folder, with only exported historical research CSV: **byte-for-byte identical** CSV |
| Original workbook / earlier batch files | Read-only; never modified |

## Ranking publication editions present in selected observations

| Edition | Observations | Evidence |
|---|---:|---|
| 2025-10-17 | 5 | Previously reviewed historical ranking archive; direct individual FIFA ranking verification not guaranteed |
| 2025-11-19 | 1 | Previously reviewed historical ranking archive; direct individual FIFA ranking verification not guaranteed |
| 2025-12-22 | 1 | Previously reviewed historical ranking archive; direct individual FIFA ranking verification not guaranteed |
| 2026-01-19 | 93 | Previously reviewed historical ranking archive; direct individual FIFA ranking verification not guaranteed |
| 2026-04-01 | 116 | Previously reviewed historical ranking archive; direct individual FIFA ranking verification not guaranteed |
| 2026-06-11 | 84 | FIFA official publication statement + Wildstat 11 Jun table + MLS 11 Jun list |

## Unresolved and unusual records

### Match 37 – Uruguay vs Cabo Verde (X8 = −42.80)
- Cabo Verde’s match against Bermuda dated **6 June 2026** is included in its previous five. Prior X8 research marked the fixture `PARTIALLY_DOCUMENTED_FRIENDLY`. Its rank (**166**, 1 April edition) is a reused research baseline, **not a claim of fresh official match-by-match verification**.
- Calculation is arithmetically valid using the cited baseline; confirm the friendly and ranking from primary records if higher assurance is required.

### Match 50 – Morocco vs Haiti (X8 = +13.00)
- **Cross-batch discrepancy:** the earlier X8 v2 batch for match IDs 6–30 used **Scotland rank 41** for a June 11 World Cup opponent. The dated **11 June** Wildstat ranking and independently published MLS ranking list show Scotland **42**. This new batch uses **42** in both team histories and flags the difference; earlier v2 files are unchanged.
- Scotland appears once in Morocco’s five opponents and once in Haiti’s. Using 41 instead of 42 in **both** histories would reduce **both averages by 0.20** and leave **X8 unchanged at +13.00**. Nevertheless the ranking discrepancy should be resolved across batches before the final 104-match master is populated.
- Sources: https://wildstat.com/p/7001/ddate/2026-06-11 and https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup

### Match 52 – Bosnia and Herzegovina vs Qatar (X8 = −17.20)
- Qatar’s 7 December 2025 fixture against Tunisia appears as its fifth previous match. The prior verified work still flags FIFA Arab Cup **senior-A international eligibility**. The prior fixture/ranking values were **carried forward without changing their verification status**.
- Check official team data centre and match classification if the group requires only FIFA-recognised senior-A matches. If the fixture is excluded, the five-match history must be rebuilt and X8 recalculated; do not merely delete the row.

### Large absolute differences
- Match 46 (Panama vs Croatia) **+51.40**, match 39 (Belgium vs IR Iran) **−43.00**, and match 37 **−42.80** are large. They result from different recent opposition strength rather than obvious arithmetic errors. They deserve an exploratory outlier check during model development, **not automatic removal**.

### General source-quality limitation
- **Most individual historical ranking positions were inherited from previously reviewed third-party historical FIFA-ranking archives.** Programmatic validation establishes correct arithmetic and date logic for the **supplied records**, not proof that each ranking number exactly matches FIFA’s official record.
- FIFA’s official tournament chronology is a single general source; repeating it in rows does **not** constitute independent verification. Legacy match-specific links are explicitly labelled as unverified in the research file and source log.
- No gaps or missing ranks were encountered in the selected baseline, so all 30 numerical values could be calculated. Review flags should be resolved before approval for final regression training.

## Reproducibility

Files: `X8_Matches31_60_Historical_Research.csv`, `X8_Matches31_60_Calculated_Results.csv`, `X8_Matches31_60_Reproduce.py`, `X8_Matches31_60_Source_Log.csv`, this report.

Place the research CSV and script in the same directory, then run:

```bash
python X8_Matches31_60_Reproduce.py --test
python X8_Matches31_60_Reproduce.py
```

The script uses only Python’s standard library. It carries an embedded read-only fixture control extracted from the master workbook. It does not fetch websites and does not change the master spreadsheet or earlier batches.

SHA-256 of the reproduced calculated-results CSV:

`8a3e185ca2876e40ac2bd3e5c3b70c0b9210bbac6016db466445398f3ddaa270`

## Source references (primary versus secondary)

- **Official FIFA tournament results (GENERAL chronology):** https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums
- **Official FIFA 11 June ranking release (publication sequence, not all individual ranks):** https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola
- **Dated historical 11 June secondary ranking archive:** https://wildstat.com/p/7001/ddate/2026-06-11
- **Independent dated list of World Cup participants’ June 11 ranking positions:** https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup
- **Historical pre-World Cup editions, individual fixture sources, flagged cases:** see research CSV and source log. Old source evidence is carried forward with its original verification limitations.

## Academic integrity – truthful disclosure

Generative AI helped extract and reconcile historical research from earlier team datasets, select and classify official versus secondary source evidence, transcribe 11 June ranking positions, build the 300-row historical research CSV, generate the Python script, and design/run validation and regression tests. The student/team should independently inspect the supporting records and understand the Python code. The script verifies date ordering, grouping, match IDs, team ordering, no duplicate fixtures, applicable ranking publication periods, arithmetic, and output reproducibility; it cannot independently establish the factual authenticity or complete coverage of every external historical record.

**Approval boundary:** Only match IDs 31–60 were processed for X8. The original master workbook and existing batches remain unchanged. Do not automatically incorporate review-flagged values into the final model without the team’s review.
