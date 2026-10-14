# X8 — Final Batch (Match IDs 91–104): Research and Validation Report

**Assessment:** FIFA World Cup 2026, HIT140 Objective 2.1.  
**Scope:** Match IDs 91–104 only; no full 104-match consolidation.  
**As-of date:** 13 October 2026.  
**Original input:** `Master Dataset(1).xlsx` (read only).  
**Calculation input:** `X8_Matches91_104_Historical_Research.csv`.  
**Output:** `X8_Matches91_104_Calculated_Results.csv`.

## 1. Method

For each target match, read its exact `match_id`, local `match_date`, `team_a`, `team_b` from the original master workbook. For each team, select the five latest eligible completed senior internationals **before** the match, ordered newest first. FIFA World Cup 2026 fixtures were reconstructed programmatically from all earlier match IDs in the 104-match master dataset, then checked against FIFA’s published general schedule and knockout results. For the first six matches in this batch (IDs 91–96), each side had four earlier World Cup matches, so the fifth entry is the team's latest pre-tournament international, reused from reviewed earlier X8 research. IDs 97–104 have five or more earlier World Cup fixtures; use only the five most recent.

The preceding opponent's FIFA ranking is taken from the **latest officially published edition available before that historical fixture**:
- FIFA World Cup 2026 earlier fixtures: **11 June 2026** edition, which FIFA announced was published before kickoff of the opening match. This includes first-day fixtures under the previously approved same-day rule.
- Pre-tournament fixtures selected here (June 4–10): **1 April 2026** edition.
- Never use 20 July 2026 or current/live FIFA rankings retrospectively.

Compute the **unrounded arithmetic means**, then subtract Team B’s mean from Team A’s mean:

`X8 = sum(A previous 5 opponent ranks) / 5 - sum(B previous 5 opponent ranks) / 5`

Calculations use `Decimal` integers, with display rounded to two decimals only at export. Lower historical FIFA ranking number indicates stronger-ranked prior opposition; the sign is **not** a predicted goal difference.

## 2. Research and evidence, separate from arithmetic

- Exactly **140** selected historical observations: **128** World Cup fixtures and **12** pre-tournament internationals. Distinct earlier World Cup fixtures are linked by original master `previous_wc_match_id`.
- FIFA’s official tournament results and knockout bracket were opened to verify the date and opponents of the relevant World Cup matches. A general results URL is labelled **general chronology**, not misrepresented as a match-specific report. Match-specific FIFA reports were also checked for #90 (Canada–Morocco), #97 (France–Morocco) and #100 (Argentina–Switzerland).
- The 11 June **ranking edition date** is directly established by FIFA's official pre-tournament announcement. The individual ranks are from the previously reviewed dated Wildstat archive and were also compared with a *separate* published 11 June list from MLSsoccer.com for all World Cup opponent observations (45 distinct opponent countries).
- The 12 April-edition positions were compared against the archived 1 April Wildstat edition. They remain **secondary ranking evidence**; no claim is made that those positions were individually read from FIFA’s own original downloadable database.
- Matching opponent + identical ranking edition pairs were compared across prior batches 1–5 v2, 6–30 corrected v3, 31–60, and 61–90. No cross-batch rank contradictions were found for the selected observations. Scotland is ranked **42**, not 41, in both of its applicable June-edition occurrences.
- Pre-tournament fixtures were reused with their existing source labels; links from earlier batches are not claimed to have been independently reopened in this stage. The known published-edition vs live-calculator disagreement for **Serbia (1 April: rank 39)** is noted in earlier v2 research and remains documented; no live ranking is substituted.
- The previously flagged December 2025 FIFA Arab Cup *senior-A international eligibility* question does not affect this batch's selected 140 observations, all of which date from April-ranking-era June friendlies or the World Cup. The earlier flags remain unchanged in earlier batches.

### Main sources

- FIFA World Cup 2026 full match results (official general chronology): https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums
- FIFA knockout stage results (official general chronology): https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/knockout-stage-match-schedule-bracket
- FIFA 11 June official ranking announcement (publication time ordering): https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola
- MLSsoccer 11 June ranking positions (dated secondary list): https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup
- Wildstat official-ranking reproduction, 11 June edition: https://wildstat.com/p/7001/ddate/2026-06-11
- Wildstat official-ranking reproduction, 1 April edition: https://wildstat.com/p/7001/ddate/2026-04-01
- FIFA France–Morocco quarter-final match report: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/france-morocco-match-report-highlights?searchOverlay=1
- FIFA Argentina–Switzerland quarter-final match report: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/argentina-switzerland-match-report-highlights?gsid=e7fc2e4a-e5a2-4ab7-8a6f-44714b86ea48

All observation-level sources and classifications are in the Historical Research CSV; distinct URLs and their evidence roles are in the Source Log CSV. Multiple mentions of the same URL are **not** counted as independent sources.

## 3. Results

| Match ID | Team A | Team B | A rank sum | A average | B rank sum | B average | X8 | Status |
|---:|---|---|---:|---:|---:|---:|---:|---|
| 91 | Brazil | Norway | 179 | 35.80 | 116 | 23.20 | **12.60** | Calculated; published-edition secondary rank evidence |
| 92 | Mexico | England | 187 | 37.40 | 215 | 43.00 | **-5.60** | Calculated; published-edition secondary rank evidence |
| 93 | Portugal | Spain | 146 | 29.20 | 221 | 44.20 | **-15.00** | Calculated; published-edition secondary rank evidence |
| 94 | USA | Belgium | 164 | 32.80 | 193 | 38.60 | **-5.80** | Calculated; published-edition secondary rank evidence |
| 95 | Argentina | Egypt | 257 | 51.40 | 147 | 29.40 | **22.00** | Calculated; published-edition secondary rank evidence |
| 96 | Switzerland | Colombia | 205 | 41.00 | 237 | 47.40 | **-6.40** | Calculated; published-edition secondary rank evidence |
| 97 | France | Morocco | 182 | 36.40 | 169 | 33.80 | **2.60** | Calculated; published-edition secondary rank evidence |
| 98 | Spain | Belgium | 173 | 34.60 | 166 | 33.20 | **1.40** | Calculated; published-edition secondary rank evidence |
| 99 | Norway | England | 114 | 22.80 | 178 | 35.60 | **-12.80** | Calculated; published-edition secondary rank evidence |
| 100 | Argentina | Switzerland | 211 | 42.20 | 191 | 38.20 | **4.00** | Calculated; published-edition secondary rank evidence |
| 101 | France | Spain | 174 | 34.80 | 115 | 23.00 | **11.80** | Calculated; published-edition secondary rank evidence |
| 102 | England | Argentina | 198 | 39.60 | 202 | 40.40 | **-0.80** | Calculated; published-edition secondary rank evidence |
| 103 | France | England | 119 | 23.80 | 126 | 25.20 | **-1.40** | Calculated; published-edition secondary rank evidence |
| 104 | Spain | Argentina | 57 | 11.40 | 182 | 36.40 | **-25.00** | Calculated; published-edition secondary rank evidence |

## 4. Worked example — Match 104 (final)

Spain vs Argentina, 19 July 2026. The five most recent opponents before kickoff, all from earlier World Cup fixtures, are:

- **Spain:** France (#101, ranking 3), Belgium (#98, ranking 9), Portugal (#93, ranking 5), Austria (#84, ranking 24), Uruguay (#66, ranking 16). Sum = 57, mean = 57 / 5 = **11.40**.
- **Argentina:** England (#102, ranking 4), Switzerland (#100, ranking 19), Egypt (#95, ranking 29), Cabo Verde (#86, ranking 67), Jordan (#70, ranking 63). Sum = 182, mean = 182 / 5 = **36.40**.

**X8 = 11.40 − 36.40 = −25.00.** This means Spain faced stronger-ranked opponents on average (lower FIFA rank), **not** that Spain was expected to win by 25 goals. The prior semi-finals are included as the most recent fixture, rather than ignoring knockout matches.

## 5. Validation results

| Check | Outcome |
|---|---|
| Target IDs 91–104, exactly 14 | PASS |
| Historical observations | PASS: 140 |
| Five unique fixtures per Team A / Team B | PASS: 28 team histories |
| Historical fixture dates before target dates | PASS |
| Correct recency and no duplicated historical fixture | PASS |
| Ranking edition before historical match, or verified 11 June same-day exception | PASS |
| Latest eligible official publication edition | PASS |
| Earlier World Cup fixtures linked to original master ID, date, opponent | PASS: 128 |
| Latest previous fixture consistent with independently reviewed X7 | PASS: 28 of 28 |
| Identical opponent+edition rankings consistent with earlier research | PASS |
| Scotland 11 June historical rank = 42 | PASS: 2 occurrences |
| June ranks compared against dated independent MLSsoccer list | PASS: 128 observations (45 distinct opponents) |
| April rank records checked against dated historical archive | PASS: 12 |
| Nine ranking-edition policy test cases | PASS |
| Essential missing historical rankings | NONE in supplied research |
| Claim all rank positions directly verified against official FIFA row-level database | NOT CLAIMED |
| Independent clean-directory reproduction from CSV/script alone | PASS: byte-for-byte identical |
| Earlier files or master workbook changed | NO |

## 6. Unusual values, source limitations and review decisions

- **Match 104 (Spain–Argentina): X8 = −25.00**, the largest absolute X8 in this batch. Check the opponent sequence in the historical CSV, including semi-finals; it is a meaningful strength-of-schedule contrast, not an arithmetic error.
- **Matches 91–96:** One pre-tournament friendly each per team is required. Its published April rank must not be replaced with that opponent's June position. In particular, Serbia's April position is 39, although a previously assessed live calculator conflicted; the published dated-edition baseline is retained.
- **FIFA news publication date vs match date:** all World Cup observations use the actual local fixture date stored in the master, never the date a follow-up news story appeared.
- All X8 values are numerically complete with no row-specific missing-ranking or senior-A eligibility flags. However **every match retains the general qualification that secondary published FIFA-ranking reproductions, rather than direct FIFA row-level database exports, support many individual opponent positions**.
- A Python reproduction pass proves that these results follow from the supplied research CSV; it cannot prove that every external historical source is complete or accurate.
- The 11 June edition release **preceded the tournament opener according to FIFA's official text**. The timezone of FIFA's displayed publication clock is not independently certified and is not invented.

## 7. Reproduce and academic-integrity disclosure

Copy `X8_Matches91_104_Historical_Research.csv` and `X8_Matches91_104_Reproduce.py` to an otherwise empty directory. Run:

```bash
python X8_Matches91_104_Reproduce.py --test
python X8_Matches91_104_Reproduce.py
```

The standalone script has an embedded **read-only reference snapshot** of the original master chronology and previously reviewed opponent ranking pairs/X7 latest fixtures. It reads the exported historical research CSV and reproduces the calculated-results CSV without any previous batch files or Excel workbook.

**AI disclosure:** Generative AI contributed to historic fixture research reuse, source selection, opponent-ranking transcription, the Python implementation, document production and validation tests. Research claims and their source classes are recorded separately from programmatic calculations. The user and group should review the evidence and understand and run the script before submitting work. The original master workbook and previously reviewed batches are unchanged, and **no full 104-match X8 consolidation has been performed**.

**Clean-directory results SHA-256:** `2fa17f9b23f11c15a454116d12ef12f2b35cac8a9b895ca68e87129dbc4418f4`  
**Reproduction run:** `VALIDATED: 140 observations; 128 prior World Cup fixtures; 28 latest-X7 checks; Scotland rank 42 references: 2`  
**Policy tests:** `PASSED 9 ranking edition and same-day publication tests`
