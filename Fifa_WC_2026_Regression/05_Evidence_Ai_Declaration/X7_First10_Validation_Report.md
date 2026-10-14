# X7 Rest Days Difference — Validation Report (First 10 Matches)
**Review date:** 12 October 2026
**Scope:** Match IDs 1–10 of the FIFA World Cup 2026 Objective 2.1 master extract.

## Inputs examined
- `X7_First10_Master_Extract.csv` (10 matches; no changes made)
- `X7_First10_Previous_Matches.csv` (20 team-side historical match records and URLs)
- `X7_First10_Reproduce.py` (Python standard library, no dependencies)
- `X7_First10_Calculated_Results.csv` (10 X7 outputs)

## Verification procedure
1. Executed `python X7_First10_Reproduce.py` successfully from the extracted folder.
2. Compared SHA-256 of results CSV before and after execution; hashes matched exactly.
3. Independently recomputed date arithmetic for every row with Python.
4. Verified unique match IDs (1–10), unique A/B source keys, nonempty historical opponents, Team A/Team B joins, and that prior fixture dates precede the prediction fixture.
5. Reviewed public historical national-team match schedules and relevant FIFA/football federation sources for the recorded previous fixtures.

## Results
| ID | Team A | Team B | Team A previous | Team B previous | A interval | B interval | X7 |
|---:|---|---|---|---|---:|---:|---:|
| 1 | Mexico | South Africa | 2026-06-04 (Serbia) | 2026-06-06 (Jamaica) | 7 | 5 | +2 |
| 2 | Korea Republic | Czechia | 2026-06-03 (El Salvador) | 2026-06-04 (Guatemala) | 8 | 7 | +1 |
| 3 | Canada | Bosnia and Herzegovina | 2026-06-05 (Republic of Ireland) | 2026-06-06 (Panama) | 7 | 6 | +1 |
| 4 | USA | Paraguay | 2026-06-06 (Germany) | 2026-06-05 (Nicaragua) | 6 | 7 | -1 |
| 5 | Haiti | Scotland | 2026-06-05 (Peru) | 2026-06-06 (Bolivia) | 8 | 7 | +1 |
| 6 | Australia | Türkiye | 2026-06-06 (Switzerland) | 2026-06-06 (Venezuela) | 7 | 7 | +0 |
| 7 | Brazil | Morocco | 2026-06-06 (Egypt) | 2026-06-07 (Norway) | 7 | 6 | +1 |
| 8 | Qatar | Switzerland | 2026-06-06 (El Salvador) | 2026-06-06 (Australia) | 7 | 7 | +0 |
| 9 | Côte d'Ivoire | Ecuador | 2026-06-04 (France) | 2026-06-07 (Guatemala) | 10 | 7 | +3 |
| 10 | Germany | Curaçao | 2026-06-06 (USA) | 2026-06-06 (Aruba) | 8 | 8 | +0 |

**Arithmetic result:** all 10 X7 values verified. **Historical fixture check:** all 20 previous-fixture date/opponent pairs are corroborated by accessible published match chronologies. These checks are not a guarantee that the underlying historical databases contain every senior international played.

## Historical chronology links used for checking
For each match, Team A and Team B are listed separately; full primary sources and notes remain in `X7_First10_Previous_Matches.csv`.

- Match 1: Mexico — https://www.national-football-teams.com/country/121/2026/Mexico.html; South Africa — https://www.national-football-teams.com/country/172/2026/South_Africa.html
- Match 2: Korea Republic — https://www.national-football-teams.com/country/173/2026/South_Korea.html; Czechia — https://www.national-football-teams.com/country/50/2026/Czechia.html
- Match 3: Canada — https://www.national-football-teams.com/country/36/2026/Canada.html; Bosnia and Herzegovina — https://www.national-football-teams.com/country/26/2026/Bosnia_Herzegovina.html
- Match 4: USA — https://www.national-football-teams.com/country/200/2026/Usa.html; Paraguay — https://www.national-football-teams.com/country/144/2026/Paraguay.html
- Match 5: Haiti — https://www.national-football-teams.com/country/81/2026/Haiti.html; Scotland — https://www.national-football-teams.com/country/162/2026/Scotland.html
- Match 6: Australia — https://www.national-football-teams.com/country/12/2026/Australia.html; Türkiye — https://www.national-football-teams.com/country/192/2026/Turkey.html
- Match 7: Brazil — https://www.national-football-teams.com/country/28/2026/Brazil.html; Morocco — https://www.national-football-teams.com/country/125/2026/Morocco.html
- Match 8: Qatar — https://www.national-football-teams.com/country/150/2026/Qatar.html; Switzerland — https://www.national-football-teams.com/country/180/2026/Switzerland.html
- Match 9: Côte d'Ivoire — https://www.national-football-teams.com/country/209/2026/Ivory_Coast.html; Ecuador — https://www.national-football-teams.com/country/56/2026/Ecuador.html
- Match 10: Germany — https://www.national-football-teams.com/country/71/2026/Germany.html; Curaçao — https://www.national-football-teams.com/country/280/2026/Curacao.html

## Limitations and documentation corrections
- **South Africa:** Jamaica v South Africa on 2026-06-06 appears in the public team chronology as a partially documented fixture. There is a reported score discrepancy between sources; X7 needs only the date and latest-match status, which are corroborated. Retain the qualification rather than asserting fully verified match details.
- **Date convention:** The calculation uses calendar-date difference `(world_cup_date - previous_match_date).days`. It does not count strictly full off-days. For a 7-day gap, there are typically six intervening calendar dates. Because both sides are calculated identically, changing to intervening off-days would not change X7.
- **AI disclosure:** The source match data was collected with AI assistance. The Python script docstring currently says `manually researched historical match details ... (not AI estimates)`, which could misrepresent the provenance. Suggested correction: `AI-assisted research of historical match details and source URLs, subsequently reviewed by the student; not estimated by the calculation script.`
- **Script scope:** The program reproduces calculations from entered source data but does not fetch websites, verify their contents or independently establish that each chosen fixture is the most recent.
- **Master workbook:** Only the provided 10-row extract was available for this review. The extraction was not compared cell-for-cell with the original 104-match Excel workbook. The full master workbook should remain untouched until the student approves merging results by `match_id`.
- **Extra records:** Later World Cup matches must include earlier World Cup matches as prior fixtures where appropriate; do not assume every previous game is a pre-tournament friendly.

## Suggested report evidence statement
`An AI assistant helped identify historical fixtures and generate a Python script for X7. We retained input-level source URLs, executed the script, recomputed each of the first ten values independently and cross-checked fixture dates against historical match chronologies. A partially documented South Africa friendly was flagged as a limitation. The final method used a consistent calendar-date difference and preserved the original match IDs.`

**Status:** Suitable to proceed with expanding X7 under the same verification protocol, without claiming all 104 values are complete or entering the first 10 into the master dataset until reviewed.
