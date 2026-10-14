# X7 – Rest Days Difference: Independent Validation of Matches 31–50

**Assessment:** Reproducible working data; no calculation corrections identified.  
**Date of review:** 12 October 2026  
**Original upload:** `matches_31_50.zip`  
**Scope:** 20 current matches (IDs 31–50), 40 team-level previous-match observations.

## 1. Files and contents

All four expected files were present:

- `X7_Matches31_50_Master_Extract.csv` — 20 matches with match IDs, dates, teams, stages, groups.
- `X7_Matches31_50_Previous_Matches.csv` — 40 previous-match observations, opponents, dates, source references and provenance notes.
- `X7_Matches31_50_Calculated_Results.csv` — 20 results and supporting details.
- `X7_Matches31_50_Reproduce.py` — Python standard-library reproduction script.

## 2. Validation performed

| Check | Result | Method |
|---|---|---|
| Match IDs are exactly 31–50 | PASS | Parsed master-extract CSV and checked IDs/record count. |
| 20 results and 40 history observations | PASS | Counted CSV rows. |
| 40 previous fixtures agree with previously uploaded master extracts (IDs 1–30) | PASS | Independently matched each team to its most recent earlier World Cup fixture by match date and opposing team. |
| Previous fixture predates each current fixture | PASS | Parsed ISO dates, validated date sequence. |
| All team A/B rest days and X7 values | PASS | Independently recomputed calendar-day differences from recorded fixture dates. |
| Run of supplied Python script | PASS | Executed the script in a separate temporary directory using the supplied inputs. |
| Byte-for-byte reproduction of calculated results CSV | PASS | Regenerated output bytes exactly match supplied calculated CSV. |
| Preservation of Team A/B names and order | PASS | Cross-checked results, history and master extract. |

**Output SHA-256:** `e30adb6debb69ea0fe893364157213f11f48876d7d6e7aff571325cdf647fb9a`

## 3. Results

**X7 formula:** `rest_days_difference = (current_date - team_a_previous_date).days - (current_date - team_b_previous_date).days`.

- Match 31 — Türkiye vs Paraguay: **X7 = −1** (6 − 7 days).
- Match 32 — USA vs Australia: **X7 = +1** (7 − 6 days).
- Matches 33–50: **X7 = 0** in every case.
- Distribution: 18 zeros, one −1, one +1.

This limited variability is consistent with both sides having similar interval lengths between World Cup group-stage matches. It does not mean the variable is universally uninformative; evaluate it across all 104 matches.

## 4. External reference review

The official FIFA tournament schedule/results independently supports the relevant previous World Cup group-stage fixtures and the current fixtures for this batch:

- FIFA tournament schedule/results: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/match-schedule-fixtures-results-teams-stadiums
- CAF official match-specific report confirming Spain vs Cabo Verde on 15 June 2026: https://www.cafonline.com/fifa-world-cup/news/cape-verde-stun-spain-to-claim-historic-point-on-world-cup-debut/
- England Football match account confirming England vs Croatia on 17 June 2026: https://www.englandfootball.com/articles/2026/Jun/17/harry-kane-croatia-world-cup-match-reaction-20261706

Source notes:

- The 40 observations describe **20 unique previous World Cup fixtures**; the same match-specific source is appropriately reused for both teams that played in that fixture. These are not 40 independent source documents.
- General FIFA `chronology_url` links are contextual references, not second independent confirmations.
- The FIFA link for England vs Croatia in the supplied file has an unusual duplicated-looking path, but it is indexed with the correct June 17 match report; a simpler official FIFA highlights link is available: https://www.fifa.com/fr/watch/69ls3TcVt6PIJPxhiREehA . Replacing the long URL is optional for clarity, not required to correct the X7 arithmetic.
- The source records include a YouTube link for Norway vs Iraq. The independently inspected FIFA schedule supports this fixture and date, but **the video link's ownership/content was not independently authenticated in this review**.
- Not every one of the 20 match-specific URLs was individually audited for availability. The source CSV is a documented evidence trail, not a certificate that each link remains accessible.

## 5. Reproducibility and academic integrity

The script uses Python's standard library to calculate X7, check record counts, verify ordering, and flag missing or invalid dates. It does **not** independently authenticate websites or prove source independence. Its documentation explicitly acknowledges AI-assisted historical fixture research. Retain the raw files, original AI conversation, and this separate review report.

## 6. Decision and next step

**Accept as reproducible working data for Batch 3 (31–50); no X7 values require correction.** Continue with IDs 51–70, using the same elapsed-calendar-date rule, cross-checking every team's previous match against the complete earlier tournament chronology, and preserving evidence and provenance. The original master workbook remains untouched by this review.
