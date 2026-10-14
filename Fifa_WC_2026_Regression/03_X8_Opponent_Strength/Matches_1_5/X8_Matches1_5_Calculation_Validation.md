# X8 Stage B — Calculation and Validation Report (Match IDs 1–5)

**Project:** FIFA World Cup 2026, multiple linear regression, Objective 2.1  
**Variable:** X8 — Last-5 Opponent Strength Difference  
**Date of calculation:** 12 October 2026  
**Scope:** Master match IDs **1, 2, 3, 4 and 5 only**  
**Source input:** `X8_Matches1_5_Historical_Opponents_Rankings_v2_verified.csv`  
**Exported, byte-identical copy of source input:** `X8_Matches1_5_Input_Extract.csv`  
**Calculated results:** `X8_Matches1_5_Calculated_Results.csv`  
**Reproduction code:** `X8_Matches1_5_Reproduce.py`

## Definition and calculation convention

For each World Cup fixture, choose each side's five most recent completed senior international fixtures **before that World Cup fixture**. For each previous fixture, use the FIFA ranking **of that fixture's opponent** from the most recent historical FIFA ranking publication before that historical fixture. The input file records those research selections; this Stage B exercise does **not** perform new online ranking research.

\[
\text{X8} = \frac{r_{A1}+r_{A2}+r_{A3}+r_{A4}+r_{A5}}{5}
- \frac{r_{B1}+r_{B2}+r_{B3}+r_{B4}+r_{B5}}{5}
\]

Here a lower FIFA **rank number** corresponds to a higher-ranked opponent; X8 is an *average of ordinal positions*, **not** FIFA rating points. The calculation uses Python `int` and `decimal.Decimal`, with no intermediate rounding. The output displays both averages and X8 to two decimal places.

## Input validation performed by the script

1. The CSV has **exactly 50** observations, representing **5 master match IDs × 2 teams × 5 historical matches**.
2. Every match ID is from **1–5**, with exactly five observations for side A and exactly five for side B.
3. Within each `match_id`/`team_side`, the five `previous_match_recency` values are **1, 2, 3, 4, 5**, without duplicates.
4. There are no duplicate combinations of match ID, team side, previous fixture date and previous opponent. An opponent **may validly occur more than once** if played on different dates (e.g., South Africa played Panama twice).
5. Both sides have consistent World Cup dates and reciprocal opponent labels, preserving the recorded Team A/Team B ordering.
6. Every row passes **ranking publication date < historical fixture date < World Cup match date**.
7. Each `verified_historical_edition` date matches the row's `ranking_publication_date`.
8. Recency 1–5 is in descending chronological order; opponent ranking positions are positive integers.
9. Each row includes an HTTPS primary ranking evidence URL (the presence and syntax of a URL do **not** independently authenticate a webpage).

All checks passed for the supplied v2 input. The validation **cannot** by itself establish that the selected fixtures are truly the five most recent worldwide, or that the archived ranking positions are identical to FIFA's official row-level historical database. Those matters depend on the earlier, AI-assisted source audit.

## Results (baseline ranks as supplied by v2)

| Match ID | World Cup match date | Team A | Team B | A rank sum | B rank sum | Team A mean | Team B mean | **X8 = A − B** |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | 2026-06-11 | Mexico | South Africa | 155 | 325 | 31.00 | 65.00 | **-34.00** |
| 2 | 2026-06-11 | Korea Republic | Czechia | 336 | 454 | 67.20 | 90.80 | **-23.60** |
| 3 | 2026-06-12 | Canada | Bosnia and Herzegovina | 324 | 172 | 64.80 | 34.40 | **+30.40** |
| 4 | 2026-06-12 | USA | Paraguay | 54 | 215 | 10.80 | 43.00 | **-32.20** |
| 5 | 2026-06-13 | Haiti | Scotland | 392 | 234 | 78.40 | 46.80 | **+31.60** |

In the CSV files, positive X8 values have no leading plus sign; in this report the plus signs are shown for readability.

### Match 1 — Independently understandable manual example

**Team A: Mexico** — previous opponents and historically applicable ranking positions, most recent first:

| Previous fixture date | Opponent | Rank | Ranking publication date |
|---|---|---:|---|
| 2026-06-04 | Serbia | 39 | 2026-04-01 |
| 2026-05-30 | Australia | 27 | 2026-04-01 |
| 2026-05-22 | Ghana | 74 | 2026-04-01 |
| 2026-03-31 | Belgium | 9 | 2026-01-19 |
| 2026-03-28 | Portugal | 6 | 2026-01-19 |

Sum = 39 + 27 + 74 + 9 + 6 = **155**; average = 155 / 5 = **31**.

**Team B: South Africa**:

| Previous fixture date | Opponent | Rank | Ranking publication date |
|---|---|---:|---|
| 2026-06-06 | Jamaica | 71 | 2026-04-01 |
| 2026-05-29 | Nicaragua | 131 | 2026-04-01 |
| 2026-03-31 | Panama | 33 | 2026-01-19 |
| 2026-03-27 | Panama | 33 | 2026-01-19 |
| 2026-01-04 | Cameroon | 57 | 2025-12-22 |

Sum = 71 + 131 + 33 + 33 + 57 = **325**; average = 325 / 5 = **65**.

**X8 for Match 1 = 31 − 65 = -34.00.** The two Panama records are separate fixtures on separate dates and are not duplicates.

## Source-quality limitation: October 2025 Nicaragua position

The v2 baseline lists **Nicaragua as rank 133** in the **17 October 2025** historical edition, applicable to Haiti's **18 November 2025** qualifier. The primary evidence URL stored in the input is:

- Historical edition reference (third-party): https://worldcdb.com/fifarannking.htm
- Official FIFA edition announcement (confirms edition context, **not** necessarily Nicaragua's individual rank): https://inside.fifa.com/fifa-rankings/world-ranking/men/news/coca-cola-mens-world-ranking-october-2025-argentina-germany

An independent audit reported a conflicting contemporary claim of **132** for Nicaragua. **A source URL directly supporting that alternative is not present in the v2 input record**, so this exercise cannot resolve the discrepancy. **Do not describe the 133 position as directly verified against FIFA's official row-level ranking archive.** The input baseline remains **133** unchanged.

### Sensitivity for Match ID 5 only

- **Haiti baseline opponents' ranks:** Peru 53, New Zealand 85, Iceland 74, Tunisia 47, Nicaragua **133**.
- Haiti baseline sum = **392**, average = 392 / 5 = **78.40**.
- Scotland opponents' ranks: Bolivia 76, Curaçao 82, Côte d'Ivoire 37, Japan 19, Denmark 20.
- Scotland sum = **234**, average = 234 / 5 = **46.80**.
- **Baseline X8 = 78.40 − 46.80 = +31.60.**
- If October Nicaragua was actually **132**, Haiti's alternative sum would be **391** and its alternative average **78.20**.
- **Alternative X8 = 78.20 − 46.80 = +31.40.**
- **Change in X8 = -0.20** (the alternative is 0.20 smaller than the provisional baseline).

This alternative is a *sensitivity illustration*, **not** a correction to the submitted v2 rank or a finding that the 132 figure is correct. Nicaragua's separate **April 2026** ranking of 131 appearing elsewhere in the file is a different ranking edition and **is not affected** by this scenario.

## Ranking edition coverage in the 50 input records

| Ranking publication date | Input observations |
|---|---:|
| 2025-10-17 | 8 |
| 2025-12-22 | 2 |
| 2026-01-19 | 20 |
| 2026-04-01 | 20 |
| **Total** | **50** |

Some rank evidence in the original v2 file comes from dated **third-party ranking archives**, even when FIFA's public news announcements verify the ranking release date. This calculation does not elevate that secondary evidence to official FIFA row-level verification. Full per-row source URLs, verification notes, opponent names, dates and rankings are preserved **unchanged** in `X8_Matches1_5_Input_Extract.csv`.

## Reproducibility test

Place `X8_Matches1_5_Reproduce.py` and `X8_Matches1_5_Input_Extract.csv` in the same directory. Run:

```bash
python X8_Matches1_5_Reproduce.py
```

The script creates `X8_Matches1_5_Calculated_Results.csv` in the same directory. It uses only Python's standard library, including `csv`, `datetime` and `decimal`, and requires no external packages or internet access.

**Test performed:** Executed the script in a *separate temporary directory* using copies of only the reproduction script and exported input extract. The resulting CSV was **byte-for-byte identical** to the supplied calculated-results CSV. Its SHA-256 hash was:

`74dbd0d9c01938b7f25acd9938d69746f9b893fbfe6d361be19a6f07f21d3337`

The exported input CSV itself was byte-for-byte identical to the v2 verified source; neither the original research CSV nor the v2 source was edited.

## Academic integrity disclosure

**AI assistance:** Earlier stages used generative AI to identify prior football fixtures, research historical ranking editions, compare conflicting archived sources, and prepare the verified v2 research dataset. In this stage, AI generated Python code, assisted with data validation, performed the arithmetic through code, and drafted the validation documentation. The records and rankings originated from the reviewed v2 CSV rather than fresh automated retrieval of FIFA data. The script reproduces calculations and checks internal consistency but **does not authenticate URLs or replace independent validation of historical football sources**.

**Scope restriction:** Calculations were performed only for match IDs **1–5**. No changes were made to the master Excel workbook or either existing research CSV. No calculations for IDs 6–104 were performed.
