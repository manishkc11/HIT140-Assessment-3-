# X7 Rest Days Difference — Review Notes (Matches 11–30)

**Review date:** 12 October 2026  
**Scope:** 20 pasted match results (IDs 11–30).  
**Status:** All 20 reported X7 values independently recomputed from the dates shown in the agent's report. The agent's four downloadable source/code files have **not** been supplied for this batch, so the Python reproduction, file integrity, match-ID joins, and exhaustive historical-source coverage remain **unverified**.

## Calculation method

For each team: `rest_days = (current_match_date - previous_match_date).days` (calendar-date difference).  
`X7 = rest_days_team_a - rest_days_team_b`.

## Independent arithmetic check

| Match ID | A rest | B rest | Recomputed X7 | Arithmetic status |
|---:|---:|---:|---:|---|
| 11 | 6 | 14 | -8 | Pass |
| 12 | 10 | 8 | +2 | Pass |
| 13 | 6 | 76 | -70 | Pass |
| 14 | 7 | 9 | -2 | Pass |
| 15 | 11 | 9 | +2 | Pass |
| 16 | 9 | 9 | 0 | Pass |
| 17 | 8 | 7 | +1 | Pass |
| 18 | 7 | 9 | -2 | Pass |
| 19 | 7 | 6 | +1 | Pass |
| 20 | 15 | 9 | +6 | Pass |
| 21 | 15 | 11 | +4 | Pass |
| 22 | 7 | 10 | -3 | Pass |
| 23 | 7 | 8 | -1 | Pass |
| 24 | 9 | 10 | -1 | Pass |
| 25 | 7 | 7 | 0 | Pass |
| 26 | 5 | 6 | -1 | Pass |
| 27 | 6 | 5 | +1 | Pass |
| 28 | 7 | 7 | 0 | Pass |
| 29 | 6 | 6 | 0 | Pass |
| 30 | 6 | 6 | 0 | Pass |

## Independent external spot checks

- **Match 13 (Uruguay):** Uruguay's federation lists 31 March 2026 versus Algeria as the immediately preceding senior international before Saudi Arabia on 15 June 2026. Thus 76 calendar days is substantiated. Official history: https://www.auf.org.uy/historico-partidos/1/----1/ . Saudi Arabia's 9 June Senegal match is recorded in match logs: https://fbref.com/en/players/62592fc1/matchlogs/nat_tm/Musab-Al-Juwayr-Match-Logs . **Do not silently remove the -70 outlier.** Review influence during regression diagnostics.
- **Match 15 (Iran):** 4 June 2026 Iran 2–0 Mali is documented at https://www.worldfootball.net/match-report/co571/fifa-friendlies/ma12107128/iran_mali/ and in match schedules at https://fbref.com/en/squads/6a08f71e/2026/matchlogs/c218/schedule/IR-Iran-Men-Scores-and-Fixtures-Friendlies-M . This fixture was later than Iran's 29 May Gambia match.
- **Match 11 (Japan):** Japan's FA confirms the 31 May 2026 Iceland friendly: https://www.jfa.jp/eng/samuraiblue/20260531/ . FIFA confirms Netherlands vs Japan was on 14 June local venue date: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/netherlands-japan-preview-live-stream-team-news-tickets . Hence Japan's stated 14-day gap is supported.
- **Second group matches:** The FIFA World Cup schedule supports the reported chronology from 18 June onward: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums . This is an initial chronology check, not a full validation of every source record.

## Pending checks before approving this batch for the master dataset

1. Download and inspect the **calculated results CSV**, **historical previous matches CSV**, **master extract CSV**, and **Python reproduction script**.
2. Run the script locally and compare its output to the supplied results; check the expected input filenames and retained team ordering.
3. Review all 40 team-level source links for completeness, not just the existence of a historical fixture.
4. Check that all match IDs join uniquely to the master and that no current-match or later information is used.
5. Retain original AI conversation history and all corrections for the university AI declaration.

**Academic integrity:** Historical fixture research and Python code creation were AI-assisted. Independent review herein covers the arithmetic in the pasted summary plus selected external sources. Do not claim a complete independent validation of the entire batch until the files and remaining historical fixtures have been checked.
