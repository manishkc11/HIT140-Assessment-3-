# X8 – Historical opponent and ranking data: Stage A audit

**Scope:** Match IDs 1–5; based on the user-provided research CSV and research narrative.  
**Status:** Structural/data-order checks passed; opponent ranking values remain provisional pending complete historical-edition verification. No X8 averages/differences were calculated.

## Structural checks

- 50 rows, 17 columns; five matches, two teams per match, five historical fixtures per team.
- Match IDs 1–5, 10 distinct investigated team histories; no duplicate `(match_id, team_side, previous_match_recency)` keys.
- All 50 historical match dates precede their corresponding target World Cup match dates.
- All 50 recorded ranking publication dates precede the associated historical fixture dates.
- No blank fields in the 17 CSV columns.
- Ranking editions represented: 1 Apr 2026 (20 observations), 19 Jan 2026 (20), 17 Oct 2025 (8), 22 Dec 2025 (2).
- CSV correctly identifies 49 ranking entries as provisional and one South Africa–Jamaica fixture as requiring extra review.

## External source spot checks

- Mexican historical fixtures and local dates correspond to the 2026 results archive: https://www.national-football-teams.com/country/121/2026/Mexico.html
- Canada's June 1 Uzbekistan and June 5 Ireland matches are corroborated by Canada Soccer: https://canadasoccer.com/camp/1924/mens-international-series-in-canada/
- South Africa vs Jamaica on 6 June 2026 is recorded in the team history, but the archive marks details partially incomplete: https://www.national-football-teams.com/country/172/2026/South_Africa.html
- The April 1, 2026 historical ranking agrees with sampled values in the CSV (Serbia 39, Australia 27, Ghana 74, Jamaica 71, Germany 10): https://wildstat.com/p/7001/ddate/2026-04-01
- FIFA official ranking news confirms release timing: https://inside.fifa.com/fifa-rankings/world-ranking/men/news/france-1st-fifa-coca-cola-world-ranking-april-2026 and https://inside.fifa.com/fifa-rankings/world-ranking/men/news/coca-cola-january-2026-afcon-morocco-top-10-senegal-climb

**Scope limitation:** These spot checks do not establish that all 50 opponent fixtures or all 50 ranking positions have been individually verified against official FIFA historical ranking tables.

## Archive URL date-parameter ambiguity – 10 observations

The CSV's archive links use query parameters that do not literally equal the recorded `ranking_publication_date`:

- **8 observations with publication date 17 Oct 2025:** archive URL uses `period=23+October+2025`.
- **2 observations with publication date 22 Dec 2025:** archive URL uses `period=21+December+2025`.

Both mismatched URL types were inspected: the **23 October parameter page displays the 17 October 2025 ranking edition**, and the **21 December parameter page displays the 22 December 2025 ranking edition**. Therefore this is a URL-date ambiguity, **not evidence that the wrong ranking edition was used**. Still replace the links with clearer, stable, edition-specific archive links where possible, and record the displayed edition date explicitly.

Affected observations:
- Match 1: South Africa's opponent Cameroon (22 Dec edition)
- Match 2: Korea Republic's opponent Ghana; Czechia's opponent Gibraltar (17 Oct)
- Match 3: Canada's opponent Guatemala (22 Dec); Bosnia and Herzegovina's opponent Austria (17 Oct)
- Match 4: USA's opponent Uruguay; Paraguay's opponents Mexico and USA (17 Oct)
- Match 5: Haiti's opponent Nicaragua; Scotland's opponent Denmark (17 Oct)

## Recommended next actions

1. Verify the **actual displayed historical edition and rank** for each opponent/ranking-date combination, preferably against FIFA's own historical ranking tables, otherwise with transparent independent historical corroboration.
2. Resolve the 10 ambiguous URL parameters and preserve exact evidence URLs, noting when a third-party source rather than an official archive is used.
3. Verify the South Africa–Jamaica fixture's status as a completed senior A international; do not silently omit it because its archive marks details incomplete.
4. Keep the original Stage A CSV unchanged. Export a separately versioned corrected CSV and a change log with each correction, old value, new value and supporting URL.
5. Once the research rows are checked, independently reproduce five X8 calculations from exported input data; do not use a current ranking or ranking published after the relevant historical match.

## Academic integrity record

The original Stage A CSV and report were AI-assisted. This audit used Python's standard-library CSV and datetime utilities for structural/date checks and spot-checked externally published match histories and rankings. All 50 individual historical ranks were **not** independently validated. Keep this note and the agent's subsequent corrections in the AI-declaration evidence folder.
