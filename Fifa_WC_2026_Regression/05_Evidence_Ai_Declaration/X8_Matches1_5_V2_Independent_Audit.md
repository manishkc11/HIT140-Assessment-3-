# X8 historical opponent FIFA rankings — Version 2 independent audit

**Reviewed:** 12 October 2026  
**Files:** `X8_Matches1_5_Historical_Opponents_Rankings(1).csv`, `X8_Matches1_5_Historical_Opponents_Rankings_v2_verified(1).csv`, `X8_Matches1_5_Ranking_Verification_Change_Log_v2(1).csv`.

## 1. Machine-checked findings

- Exactly **50 observations** in both the original and version 2 datasets, with identical `(match_id, team_side, previous_match_recency)` identifiers.
- Five World Cup match IDs (1–5), two team sides per match, five previous opponents per side; no missing slots or duplicate identifiers.
- All original match/team/opponent/fixture dates, recorded historical ranking publication dates, and **all 50 opponent FIFA ranking integers are unchanged**.
- Across columns shared by both CSVs, changes occur only in `verification_status` (50 rows), `research_notes` (50 rows) and `ranking_archive_url` (10 rows).
- The change log contains **17 records:** 10 URL corrections and 7 source-conflict reviews. The 10 URL changes match the amended data rows.
- Ranking edition counts: 17 Oct 2025 (8), 22 Dec 2025 (2), 19 Jan 2026 (20), 1 Apr 2026 (20).
- Every historical ranking publication date precedes the historical fixture date, which precedes its associated World Cup fixture. There are no missing mandatory dates or non-integer rank positions.
- Version 2 includes provenance, source quality/evidence level, original URL/rank, conflicts and AI-assistance disclosure columns.

These checks establish file consistency and chronological logic, **not that every historical team match or each one of the 50 ranking positions has been independently authenticated against FIFA.**

## 2. External evidence spot-checks

- The 1 April 2026 Wildstat historical table explicitly lists Serbia #39, Senegal #14, Uzbekistan #50, Ireland #59, Ghana #74 and Kosovo #78. FIFA publishes an announcement for this edition.
  https://wildstat.com/p/7001/ddate/2026-04-01  
  https://inside.fifa.com/fifa-rankings/world-ranking/men/news/france-1st-fifa-coca-cola-world-ranking-april-2026
- The 22 December 2025 Wildstat historical table lists Cameroon #57 and Guatemala #94.
  https://wildstat.com/p/7001/ddate/2025-12-22
- The `worldcdb.com` comparison table is labelled 19 January 2026 and has an *October 2025* historical column, which visibly supports several of the recorded October values (e.g. Gibraltar #200). Because this is a multi-edition, selectively abbreviated table, readers must inspect the appropriate historical column rather than mistaking the leading 2026 column for October.
  https://worldcdb.com/fifarannking.htm
- ESPN's April 2026 article supports Serbia #39, Senegal #14, and (in the 'Honorable Mentions' section) Ghana #74.
  https://www.espn.co.uk/football/story/_/id/46664763/fifa-mens-top-50-world-rankings

## 3. Outstanding source issue — Nicaragua, October 2025

**Match 5, Haiti's fifth historical opponent (18 Nov 2025): Nicaragua #133, ranking edition 17 October 2025.** Version 2 replaced its `ranking_archive_url` with `https://worldcdb.com/fifarannking.htm`. That table abbreviates its positions after roughly rank 120 and therefore **does not visibly establish Nicaragua #133 in the accessible excerpt**. The cited primary evidence should be made more direct.

Independent dated records supporting **#133** include:
- https://www.laprensani.com/2025/10/19/deportes/3549368-nicaragua-desciende-en-el-ranking-mundial-de-la-fifa
- https://sociotrak.com/country.php?lang=es&team=NCA (edition-by-edition history)
- https://football-ranking.com/rankByZone?period=23+October+2025&zone=Central+America (labels the selected displayed edition as 17 Oct 2025; URL parameter is misleading)

**Disagreement to disclose:** `https://nuevaya.com.ni/deportes-ya/nicaragua-baja-dos-puestos-en-ranking-fifa/` (17 Oct 2025) reports #132, whereas the sources above report #133. The evidence currently leans toward #133, but an official date-specific archived row or full published table would be the strongest resolution. The current value need not be changed without stronger evidence. Preserve the discrepancy in the source log.

## 4. Decision and next action

**Accept Version 2 as a structurally valid, version-controlled research dataset, conditionally ready for Stage B calculations.** Keep the original CSV unchanged. Before treating calculated X8 values as fully validated, update the Nicaragua evidence reference and conflict note (or explicitly mark it as unresolved), then calculate only match IDs 1–5 using a reproducible Python script.

The final report and AI declaration should say that AI helped research match histories and rankings, compare third-party archives, generate code, and document discrepancies. Reproducible Python arithmetic cannot authenticate the original historical sources.
