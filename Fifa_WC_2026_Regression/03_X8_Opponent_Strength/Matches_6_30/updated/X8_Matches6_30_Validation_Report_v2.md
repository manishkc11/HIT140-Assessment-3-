# X8 Matches 6–30 — v2 Correction, Evidence and Validation Report

## Scope and academic-integrity statement

This report documents corrections and source review for historical opponent ranking research for World Cup match IDs **6–30 only**. The original v1 files and master Excel workbook are **not edited**. The historical research and primary/secondary source comparison were conducted with generative AI assistance; ChatGPT also generated the correction process and Python code. Python validates documented facts and performs arithmetic but cannot certify external documents, eligibility as FIFA international-A games, or complete national-team schedules by itself.

**Result:** 250 historical team-match observations in 25 target fixtures; 25 computed differences; exactly two differences changed (match IDs 25 and 28). All values continue to require the team's independent source-quality review.

## 1. FIFA ranking release and two opening-day fixtures

FIFA's announcement is dated **11 June 2026, 16:45** on its official website and **explicitly states that the June ranking was published a few hours before the 2026 World Cup began**. The FIFA webpage does **not** explicitly show the timezone next to 16:45. Interpreting the time as Zurich local summer time (CEST, UTC+02:00) yields **14:45 UTC**; this conversion is an **inference, not a directly verified FIFA metadata timestamp**. The official textual statement is separate evidence that the release preceded the Mexico–South Africa opener. Even interpreting the displayed 16:45 as UTC, it precedes the opener at 19:00 UTC.

* FIFA release article: https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola?entryId=&requester=MediaHub
* FIFA match 1 preview: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/mexico-south-africa-preview-live-stream-team-news-tickets?searchOverlay=1
* FIFA match 2 preview: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/korea-republic-czechia-live-stream-team-news-tickets

| Event | Local date and time | Timezone | Comparable UTC time | Evidence and confidence |
|---|---|---|---|---|
| FIFA ranking article displays 16:45 | 11 Jun 2026 16:45 | CEST **assumed**, not stated on webpage | 11 Jun 14:45 UTC **inferred** | Official article explicitly says ranking released before the World Cup began |
| Mexico vs South Africa kickoff (earlier match ID 1) | 11 Jun 13:00 | Mexico City UTC−06:00 | **11 Jun 19:00 UTC** | Official FIFA fixture preview |
| Korea Republic vs Czechia kickoff (earlier match ID 2) | 11 Jun 20:00 | Guadalajara UTC−06:00 | **12 Jun 02:00 UTC** | Official FIFA fixture preview |

The same-day ranking is therefore included in the four affected records. If later evidence overturns the time interpretation, the script supports explicit fallback to the April edition using stored preceding-edition ranks, without silently relabelling June ranks as April ranks.

### June 11 opponent ranks

| Opponent | 11 June ranking | v1 April ranking | Official FIFA July retrospective corroboration |
|---|---:|---:|---|
| Korea Republic | **25** | 25 | 32nd in July, **down 7** places → June 25th |
| Mexico | **14** | 15 | 10th in July, **up 4** places → June 14th |
| South Africa | **60** | 60 | 54th in July, **up 6** places → June 60th |
| Czechia | **40** | 41 | 48th in July, **down 8** places → June 40th |

* Contemporaneous list of the June 11 edition: https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup
* FIFA's official **20 July 2026** ranking report giving July positions and movement since June: https://inside.fifa.com/fifa-rankings/world-ranking/men/news/spain-top-mens-world-rankings-after-second-world-cup

**Important:** The July article corroborates the *previous June positions retrospectively*. It is **not** being used as a ranking edition available before the June historical matches.

## 2. Numeric change summary

| Match ID | Team A | Team B | v1 Team A avg | v1 Team B avg | v1 X8 | v2 Team A avg | v2 Team B avg | v2 X8 |
|---|---|---|---:|---:|---:|---:|---:|---:|
| 25 | Czechia | South Africa | 55.80 | 56.60 | -0.80 | 55.80 | 56.40 | **-0.60** |
| 28 | Mexico | Korea Republic | 41.80 | 60.80 | -19.00 | 41.80 | 60.60 | **-18.80** |

For match 25, the preceding-opponent ranking for Mexico falls from 15 to 14, reducing South Africa's average by 1/5 = **0.20**. Thus X8 increases from −0.80 to **−0.60**. For match 28, Czechia's ranking falls from 41 to 40, reducing Korea Republic's average by **0.20**, and X8 increases from −19.00 to **−18.80**. Korea Republic's and South Africa's numeric ranks do not change, but their *historical ranking edition dates and sources* do.

Other 23 matches' X8 values remain unchanged. No intermediate means were rounded. Team A/B ordering remains as in v1.

## 3. Status of previously flagged matches

| Target ID | Evidence added | What is confirmed | Remains unresolved |
|---|---|---|---|
| 8 | FIFA Qatar team data centre | Qatar vs Tunisia (7 Dec 2025), Syria (4 Dec), Palestine (1 Dec) appear in official FIFA men's match history | Formal individual senior-A eligibility; retain original flag |
| 14 | beIN Sports and FBref | Cabo Verde vs Bermuda 6 Jun 2026 corroborated in two secondary fixtures sources | Direct official FIFA individual match record not established; retain flag |
| 18 | FIFA Jordan team data centre; Jordan FA match record | Iraq vs Jordan 12 Dec 2025 appears in official FIFA men's archive on Jordan's entry; Jordan FA calls it FIFA-recorded | The specific Iraq selection's international-A classification not certified; retain flag |
| 20 | FIFA Jordan team data centre | Jordan vs Morocco, final on 18 Dec 2025, appears in FIFA men's archive | Formal individual A status not explicitly certified; retain flag |
| 27 | FIFA Qatar team data centre | Qatar vs Tunisia 7 Dec and Syria 4 Dec appear | Formal A status not explicitly certified; retain flag |

* FIFA Qatar team history (language locale Indonesian): https://inside.fifa.com/id/data-centre/teams/qatar
* FIFA Jordan team history (language locale Portuguese): https://inside.fifa.com/pt/data-centre/teams/jordan
* Jordan Football Association record for Jordan–Iraq: https://jfa.jo/arsh_match.php?id1=1199&id_mon=1
* beIN Sports Cabo Verde–Bermuda: https://www.beinsports.com/en-au/football/friendlies/cabo-verde-vs-bermuda-2026-06-06
* FBref Cabo Verde friendly log: https://fbref.com/en/squads/31fa6fa6/2026/matchlogs/c218/schedule/Cabo-Verde-Men-Scores-and-Fixtures-Friendlies-M

FIFA's own Data Centre is substantially stronger evidence for the **existence, opponent and date** of the Arab Cup fixtures than the initial general tournament schedule. Nevertheless, FIFA notes on its website that inclusion/approval as an international-A result is a separate classification question. Hence these records remain clearly labelled provisional in the research file and their calculation-status flags are not cleared. Iraq's FIFA counterpart record is the *Jordan* Data Centre page, not a separately retrieved Iraq page; this is explicitly distinguished in the CSV.

## 4. Validation logic and test evidence

The v2 script enforces:

1. 250 observations = 25 IDs × 2 teams × 5 histories; IDs 6–30 only, with stable team ordering, five distinct preceding fixtures in newest-to-oldest order, and dates earlier than the World Cup fixture.
2. Ranking publication dates must be among the known historical editions and use the latest preceding edition; same-day editions require both verified official pre-kickoff evidence and UTC-stamped release/kickoff comparison.
3. For an uncertain same-day publication, it uses the separately provided prior edition **and the prior edition's own historical rank**, or reports missing data instead of guessing. A future edition is rejected.
4. Rank values must be integers 1–211. Missing required ranking values produce blank X8; the script never replaces missing rankings with zero.
5. Averages are computed using `Decimal` and divided by exactly five; only final formatted output uses two decimal places.
6. Research-source classifications are not magically promoted by passing arithmetic checks.

Nine internal policy tests cover valid pre-kickoff timing, missing verification, missing timestamp, post-kickoff publication, future editions, historical prior edition acceptance, the Guadalajara UTC next-day case, explicit April fallback, and a missing-fallback failure. **All nine passed.**

Actual v2 dataset policy outcomes: **246 earlier-date edition records, four documented same-day edition records**. Current complete calculations: **25/25**. The seven Arab Cup rows and one Cabo Verde record still carry their original manual verification flags, spanning five target IDs.

### Independent reproduction

Place both v2 files in the same folder and run:

```bash
python X8_Matches6_30_Reproduce_v2.py --test
python X8_Matches6_30_Reproduce_v2.py
```

The second command writes `X8_Matches6_30_Calculated_Results_v2.csv` from the exported v2 historical research CSV and uses **no external download**. It was independently executed in a new temporary folder and its CSV output compared **byte-for-byte** with the submitted results file. The comparison passed.

### Preservation and audit

Only new v2 filenames are written by the reproduction script; it does not modify `Master Dataset.xlsx`, `X8_Matches6_30_Historical_Research.csv`, `X8_Matches6_30_Calculated_Results.csv`, or previous X8 batches. The change log distinguishes rank-number corrections (2) from edition, URL, documentation, and evidence-classification updates. No historical opponent, historical fixture date, master ID, or Team A/B ordering was changed.

**Remaining manual review:** (a) document explicitly which national team selections are officially A-class internationals for FIFA Arab Cup rows; (b) if relying on 16:45 as an exact UTC time, obtain an official source identifying the webpage's timezone; (c) ensure the historic ranking positions outside the four corrected June observations agree with FIFA's archived official tables, not merely one secondary archive; (d) obtain an individual official match record for Cabo Verde–Bermuda if necessary.

## 5. Academic integrity declaration (report-ready)

"Generative AI (ChatGPT) helped locate and interpret official FIFA notices and team histories, identify the four opening-day ranking records affected by a same-day publication rule, corroborate published ranking positions, produce versioned CSVs and a change log, and write Python calculation and validation tests. The code was executed and the results independently reproduced from exported inputs. We preserved the previous source files and did not modify the master workbook. FIFA's ranking article provides direct before-kickoff textual evidence, while its displayed publication time lacks an explicit timezone; the UTC conversion is therefore marked as an inference. The five existing manual verification flags remain documented and must not be reported as definitively resolved until supporting evidence permits it."

## 6. Output checksums (SHA-256)

- `X8_Matches6_30_Historical_Research.csv`: `690eed27950771159d740ca83289d25d42abe3d951940a44ef527910d3039ddd`
- `X8_Matches6_30_Calculated_Results.csv`: `323590138924fa93eb6a54b65e7ebc9c30c233f0db16d9a24e7b86e47ab9204d`
- `X8_Matches6_30_Historical_Research_v2.csv`: `0bc9fb740a399ecc25083d7d3af4820aaff940cfbd0cd82b0f732e8a62f4408e`
- `X8_Matches6_30_Calculated_Results_v2.csv`: `0200b05612b77658a740c7efa00642357c548fdde2f5e12abc0a150e268fccce`
- `X8_Matches6_30_Reproduce_v2.py`: `cc283f5726214626662ef3759b4dfa222b0131e3aedb7af90bba1538cff5bfd6`
- `X8_Matches6_30_Correction_Change_Log_v2.csv`: `ba65525b446ce170a6d3ccfdd3c0d96a6e0bac0a89f73d53aeaa23d8d51fd44a`
