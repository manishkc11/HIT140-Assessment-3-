# X8 — Matches 61–90: Research, Validation and Reproduction Report

**Research batch:** FIFA World Cup 2026, match IDs 61–90, inclusive.  
**Prepared:** 12 October 2026.  
**Source of original fixture order:** Read-only `Master Dataset(1).xlsx`, 104 match records.  
**Previous research reused:** `X8_Matches6_30_Historical_Research_v3.csv` (corrected Scotland), reviewed `X8_Matches31_60_Historical_Research.csv`, and reviewed match IDs 1–5 data.  
**Original project files:** Not modified.

## A. Historical research, separately from calculation

The 300 rows represent 30 World Cup fixtures × Team A and Team B × each team's five most recent *completed* senior international matches. Chronology was built using the master World Cup fixtures before each target fixture, plus the previously reviewed five-match pre-tournament history for each of the 48 teams. Entries are ordered most recent first. Earlier World Cup fixtures are preferred when more recent than the pre-tournament matches.

- World Cup historical observations: **160**. Previous match date, opponent, and World Cup match ID are checked against the embedded snapshot of the unchanged master; FIFA's official general World Cup results page provides published tournament-wide corroboration. These entries are deliberately marked **general FIFA chronology**, not individual match reports.
- Previously researched pre-tournament observations: **140**. Their fixture and historical-ranking evidence is reused with its existing classification; reuse is **not** represented as renewed independent external verification.
- Historical ranking editions in the selected records: `2025-10-17`: 1, `2026-01-19`: 27, `2026-04-01`: 112, `2026-06-11`: 160.
- Scotland's published 11 June 2026 rank is **42**, verified against the dated June ranking list. In this batch, Scotland appears as a selected previous opponent in match IDs 75, 76, 90; all use 42. Ranking consistency with prior research was checked by opponent and **ranking edition date**, not name alone.
- The official 11 June release states it was published hours before the World Cup began. Therefore its published positions were used for the first World Cup fixtures on 11 June as well as subsequent World Cup matches. A same-day release without sufficient pre-kickoff evidence is rejected by the script. The website's displayed clock timezone has not been independently established; the official before-opening textual assertion is the decisive evidence.
- The **20 July 2026 ranking** is not used.

**Improved fixture source evidence:** FIFA's official pre-tournament report states Cabo Verde beat Bermuda 3–0 on 6 June 2026. Its two selected occurrences (IDs 65 and 86) are now classified as officially confirmed *fixtures*. The ranking position in those rows still comes from the older dated ranking archive, not from that FIFA match article. Qatar's 7 December 2025 fixture with Tunisia is also confirmed by FIFA's team data centre and FIFA+ replay, but it does **not** occur among the 300 selected records in this new batch. Thus the earlier Qatar senior-A eligibility flags are not removed or retroactively modified. The existence of an Arab Cup match in FIFA's men's archive does not, by itself, resolve its official international-A classification.

### Sources and evidence classes

- **Official general World Cup results:** https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums
- **Official pre-opening ranking announcement:** https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola
- **11 June 2026 published ranks (dated secondary list):** https://www.mlssoccer.com/competitions/fifa-world-cup/news/fifa-world-rankings-every-team-at-the-world-cup
- **11 June dated historical-ranking archive:** https://wildstat.com/p/7001/ddate/2026-06-11
- **Official Cabo Verde/Bermuda fixture coverage:** https://www.fifa.com/en/articles/pre-tournament-warm-up-results-fixtures-scorers
- **Qatar/Tunisia — context only:** https://inside.fifa.com/id/data-centre/teams/qatar and https://www.plus.fifa.com/en/content/qatar-vs-tunisia/a478457d-f3b9-4ea9-944c-a88e3db82a22

See the separate `X8_Matches61_90_Source_Log.csv` for every used source URL and its role, classification, linked match IDs, and limitations. Reused match-specific X7 URLs are **not** counted as authenticated independent sources unless rechecked.

## B. Python calculation (from researched input)

For each target fixture, let `a1`–`a5` and `b1`–`b5` be the last-five opponents' FIFA ranks at the correct historical editions. The calculation is:

`A_avg = (a1 + a2 + a3 + a4 + a5) / 5`  
`B_avg = (b1 + b2 + b3 + b4 + b5) / 5`  
`X8 = A_avg - B_avg`.

Python uses integer sums and `decimal.Decimal` for averages/differences. Intermediate values are never rounded; output is formatted to two decimals only at export.

### Worked calculation — Match 61, Norway vs France

Norway's sum of opponent ranks is **136**, giving **27.20**. France's sum is **190**, giving **38.00**. Hence X8 = **-10.80**. Individual ranks, fixture dates and sources can be seen in the ten relevant input rows.

## C. Full calculated results

| Match ID | Team A | Team B | A mean rank | B mean rank | X8 | Status |
|---:|---|---|---:|---:|---:|---|
| 61 | Norway | France | 27.20 | 38.00 | -10.80 | Provisional — historic ranks partly secondary |
| 62 | Senegal | Iraq | 45.40 | 51.60 | -6.20 | Provisional — historic ranks partly secondary |
| 63 | Egypt | IR Iran | 27.40 | 62.60 | -35.20 | Provisional — historic ranks partly secondary |
| 64 | New Zealand | Belgium | 38.20 | 24.00 | 14.20 | Provisional — historic ranks partly secondary |
| 65 | Cabo Verde | Saudi Arabia | 59.60 | 42.20 | 17.40 | Provisional — historic ranks partly secondary |
| 66 | Uruguay | Spain | 35.20 | 53.80 | -18.60 | Provisional — historic ranks partly secondary |
| 67 | Panama | England | 59.60 | 47.80 | 11.80 | Provisional — historic ranks partly secondary |
| 68 | Croatia | Ghana | 22.00 | 20.00 | 2.00 | Provisional — historic ranks partly secondary |
| 69 | Algeria | Austria | 32.80 | 40.40 | -7.60 | Provisional — historic ranks partly secondary |
| 70 | Jordan | Argentina | 22.00 | 56.80 | -34.80 | Provisional — historic ranks partly secondary |
| 71 | Colombia | Portugal | 42.60 | 38.20 | 4.40 | Provisional — historic ranks partly secondary |
| 72 | Congo DR | Uzbekistan | 32.40 | 21.00 | 11.40 | Provisional — historic ranks partly secondary |
| 73 | South Africa | Canada | 56.20 | 49.60 | 6.60 | Provisional — historic ranks partly secondary |
| 74 | Germany | Paraguay | 45.40 | 41.00 | 4.40 | Provisional — historic ranks partly secondary |
| 75 | Netherlands | Morocco | 35.80 | 53.20 | -17.40 | Provisional — historic ranks partly secondary |
| 76 | Brazil | Japan | 38.80 | 34.00 | 4.80 | Provisional — historic ranks partly secondary |
| 77 | France | Sweden | 41.40 | 29.80 | 11.60 | Provisional — historic ranks partly secondary |
| 78 | Côte d'Ivoire | Norway | 30.80 | 24.20 | 6.60 | Provisional — historic ranks partly secondary |
| 79 | Mexico | Ecuador | 38.20 | 56.40 | -18.20 | Provisional — historic ranks partly secondary |
| 80 | England | Congo DR | 50.80 | 28.40 | 22.40 | Provisional — historic ranks partly secondary |
| 81 | USA | Bosnia and Herzegovina | 22.80 | 41.00 | -18.20 | Provisional — historic ranks partly secondary |
| 82 | Belgium | Senegal | 37.80 | 33.60 | 4.20 | Provisional — historic ranks partly secondary |
| 83 | Portugal | Croatia | 37.80 | 35.60 | 2.20 | Provisional — historic ranks partly secondary |
| 84 | Spain | Austria | 50.80 | 31.60 | 19.20 | Provisional — historic ranks partly secondary |
| 85 | Switzerland | Algeria | 48.00 | 34.20 | 13.80 | Provisional — historic ranks partly secondary |
| 86 | Argentina | Cabo Verde | 51.20 | 56.80 | -5.60 | Provisional — historic ranks partly secondary |
| 87 | Colombia | Ghana | 43.00 | 20.20 | 22.80 | Provisional — historic ranks partly secondary |
| 88 | Australia | Egypt | 22.80 | 31.20 | -8.40 | Provisional — historic ranks partly secondary |
| 89 | Paraguay | France | 41.40 | 42.20 | -0.80 | Provisional — historic ranks partly secondary |
| 90 | Canada | Morocco | 51.60 | 34.00 | 17.60 | Provisional — historic ranks partly secondary |

## D. Programmatic validation results

| Check | Outcome |
|---|---|
| Original target IDs 61–90, dates, Team A/B | 30 IDs matched to read-only master snapshot |
| Exact five per side, unique recency positions | 60 × 5 = 300 rows, passed |
| Duplicate historical fixture per team | None within each five-match selection |
| Strict chronology / exclusion of current and future | Passed |
| Prior World Cup fixtures cross-referenced to master | **160/160** records passed |
| Latest previous fixture matched to reviewed X7 | **60/60** passed |
| Opponent rank matches previous research for same edition | Passed for all applicable references, including Scotland = 42 |
| Ranking edition sequence / same-day decision | Passed; 7 policy tests passed |
| Missing opponent ranking/date/fixture URL | 0 in the selected research |
| Explicit flagged senior-A records in new selected 300 | 0; earlier batch concerns preserved separately |
| Missing X8 averages or differences | 0 of 30 |
| Reproduction in fresh directory | **Byte-for-byte identical CSV**, SHA-256 `59514e58dcc34ace4a2908a964b761c0185c53dfc20cbfc4327552fdde819131` |

**Independent reproduction steps:** Save `X8_Matches61_90_Historical_Research.csv` and `X8_Matches61_90_Reproduce.py` to one folder; run `python X8_Matches61_90_Reproduce.py --test` and `python X8_Matches61_90_Reproduce.py`. No third-party Python packages needed. The script includes a snapshot of the previously reviewed master chronology, latest-X7 predecessors, and cross-batch rankings so that these consistency checks can run without editing or requiring the original Excel file.

## E. Unusual values, limitations and manual review

The largest absolute X8 in this batch is match **63** (Egypt vs IR Iran), **-35.20**. This is a legitimate result of the supplied five-opponent rank values; it is not itself proof of stronger or weaker match performance. It may merit later regression sensitivity analysis.

**Source-quality limitations:** Historical pre-tournament fixture lists are reused rather than exhaustively re-researched. The automated procedure does not independently verify the authenticity of every linked football webpage, the entirety of every country's historical match list, or the correctness of every ranking value within FIFA's original database. Most ranking *positions* are supported by dated **secondary** historical reproductions of FIFA rankings. Even though all 30 values calculate and reproduce, they should be reviewed as provisional for academic submission until required sources have been independently assessed. No source-date contradictions or mismatched historical rankings were detected *within the supplied and previously reviewed project data*.

**Arab Cup decision:** FIFA's 2025 Arab Cup appears in its official men's fixture archive. We have not obtained a definitive documented international-A classification for every team's specific appearance; any earlier affected records remain flagged in their original batches. None of those flagged December Arab Cup fixtures were among the five selected previous fixtures for targets 61–90, so this batch has no resulting blank averages on that account.

**No claimed source guarantee:** Passing arithmetic, chronology, or cross-batch consistency checks does not prove that the underlying historical football source is accurate. The primary reproducibility guarantee is of the calculations *given the recorded input*.

## F. Academic integrity declaration

ChatGPT assisted with retrieving/reusing historical football research, selecting and classifying source URLs, transcribing previously reviewed FIFA rankings, generating the Python code and validation tests, and preparing the reports. Python independently checked the recorded 300 rows for internal consistency and computed all 30 X8 differences. An independent clean-directory rerun produced exactly the same results CSV. This is an AI-assisted research/analysis process; external records and ranking provenance remain separately reviewable and are not certified solely by Python.

**Scope:** Only match IDs 61–90; no later X8 calculations. Original master workbook and prior-version X8 files were not modified.
