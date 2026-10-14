# X7 Matches 11–30 — Independent Review

**Review date:** 12 October 2026
**Status:** Computation verified; selected historical evidence corroborated; full historical completeness not independently certified.

## Inputs inspected
ZIP: `matches_11_30(1).zip`

All four files present:

- `X7_Matches11_30_Previous_Matches.csv`
- `X7_Matches11_30_Calculated_Results.csv`
- `X7_Matches11_30_Master_Extract.csv`
- `X7_Matches11_30_Reproduce.py`

## Reproduction audit
- Master extract: 20 unique match IDs, 11–30, in order.
- Previous-match records: 40 unique (match ID, team side) pairs.
- Result rows: 20.
- Every previous date falls before its corresponding World Cup fixture.
- All 20 reported X7 values equal the calendar-date difference for Team A minus Team B.
- `python X7_Matches11_30_Reproduce.py` executed successfully using the Python standard library.
- Output CSV was byte-identical after reproduction (SHA-256 unchanged).
- Matches 25–30 were matched against earlier fixtures in the first batch’s master extract; all 12 prior-match team references agreed.

## Independent source corroboration (selected, not exhaustive)
- **Match 11:** Netherlands v Uzbekistan (8 June) corroborated by Dutch association OnsOranje: https://www.onsoranje.nl/toernooien/7996/wedstrijd/334677; Japan v Iceland (31 May) by Japan FA: https://www.jfa.jp/eng/samuraiblue/news/00036396/
- **Match 12:** Belgium v Tunisia (6 June) corroborated by Belgium FA: https://static.belgianfootball.be/project/publiek/rencinter/en/wed_15009.htm
- **Match 13:** Uruguay FA official chronological history puts Algeria (31 March) immediately before Saudi Arabia (15 June): https://www.auf.org.uy/historico-partidos/1/; hence the -70 interval can be retained, rather than discarded as an arithmetic error.
- **Match 15:** AFC confirms IR Iran defeated Mali prior to the World Cup: https://www.the-afc.com/en/more/international_friendlies.html/news/iraq-hold-spain-ir-iran-ease-past-mali
- **Match 20:** Austria v Tunisia (1 June) corroborated by independent match records: https://www.sofascore.com/football/match/tunisia-austria/tUbsEUb
- **Match 21:** Ghana FA identifies Wales as its latest friendly before Panama: https://ghanafa.org/black-stars-arrive-in-providence-for-final-phase-of-world-cup-preparations; Reuters dates the Wales–Ghana match to 2 June: https://www.reuters.com/sports/soccer/wales-equalise-late-draw-with-world-cup-bound-ghana-2026-06-02/
- **Match 23:** DR Congo v Chile (9 June) classified as a senior friendly by multiple match records: https://www.worldfootball.net/match-report/co571/fifa-friendlies/ma12027026/dr-congo_chile/ and https://fbref.com/en/squads/9be9f315/2026/matchlogs/schedule/Congo-DR-Men-Scores-and-Fixtures
- **Panama/Bosnia 6 June:** Bosnia FA match sheet: https://www.nfsbih.ba/en/a-national-team-results-for-year2026/panama-bosnia-and-herzegovina/

## Important methodological limitations
1. **Source URL checks in code are syntactic only.** The script checks `https://` presence; it does not download, verify content, or prove that the preceding match is truly the most recent.
2. **31/40 records reuse the exact same URL** as both `source_url` and `chronology_url`; they are not independent corroboration.
3. **General FIFA summary and tournament pages are reused across records**. For a high-confidence trail, record match-specific association/fixture links when available, or honestly label a general source as general.
4. **Match 13 = −70** is a meaningful extreme value. Preserve and later evaluate regression influence (e.g., sensitivity analysis), not arbitrary deletion.
5. **Local calendar dates** were used for historical matches. Keep the date basis consistent; a post-midnight change in a news article is not automatically a fixture-date change.
6. Do not describe all 40 source records as individually externally audited. Internal calculation validation and external source validation are separate activities.

## Suggested follow-up
- Archive the original agent ZIP unchanged.
- Keep the reproduced script/output and this validation note in the evidence folder.
- Before running the complete model, review more match-specific primary sources, especially any missing schedule confirmation, and document exceptions.
- Proceed with match IDs 31–50 using the same calculation convention and a clearer one-source-versus-two-source distinction.

## SHA-256 manifests

- `X7_Matches11_30_Previous_Matches.csv` — `0ad6dfceb1504d2d3b97724e78e9cdc32c4f92a1bc701339f3f307e75dfdd011`
- `X7_Matches11_30_Calculated_Results.csv` — `6acf3c26e8e18761c0e9aedd5d1c630e13c2355f66d1acd57b0cf7c530422df3`
- `X7_Matches11_30_Master_Extract.csv` — `e9ef22c2bdb2f44803213e9c8b689a9612c294272248ea02f2c5bba5147d5999`
- `X7_Matches11_30_Reproduce.py` — `5d924d162365c118d2a14ec8c85660dba978f79c785b41f83008c5bb72d58a65`
