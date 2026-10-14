# X8 Matches 6–30 — Independent Validation of Corrected Version 2

**Date:** 12 October 2026  
**Scope:** Review of `updated.zip` against the original batch and the consolidated X7 evidence. The original master workbook was not modified.

## Executive conclusion

The corrected v2 files **pass structural, numerical, and reproducibility checks**. All 25 X8 outputs reproduce exactly from the supplied 250 historical observations. Only two output values change relative to v1: match 25 changes from −0.80 to **−0.60** and match 28 from −19.00 to **−18.80**. These corrections follow from the 11 June FIFA ranking edition, released before the World Cup opener. **This is not an audit certifying all individual external ranking records or international-A fixture classifications.**

## Files supplied

- `X8_Matches6_30_Historical_Research_v2.csv` (250 rows)
- `X8_Matches6_30_Calculated_Results_v2.csv` (25 rows)
- `X8_Matches6_30_Correction_Change_Log_v2.csv` (42 documented log entries)
- `X8_Matches6_30_Reproduce_v2.py`
- `X8_Matches6_30_Validation_Report_v2.md`

## Reproducibility tests actually executed

- `python X8_Matches6_30_Reproduce_v2.py --test` -> nine tests passed.
- `python X8_Matches6_30_Reproduce_v2.py` in an isolated directory containing only v2 research CSV and script -> calculations completed for 25 matches and 250 observations.
- `cmp` of the regenerated and uploaded v2 result CSV -> **byte-for-byte identical**.
- Exact SHA-256 results CSV: `0200b05612b77658a740c7efa00642357c548fdde2f5e12abc0a150e268fccce`.

### Structural/cross-batch tests

| Check | Result |
|---|---|
| 25 unique IDs (6–30) and 250 input rows | Pass |
| Same per-record keys as original v1 data | Pass |
| 50 latest historical fixtures vs previous X7 research | 50/50 agree |
| Changes to previous opponent names or fixture dates | 0 |
| Changes to selected ranking publication edition | 4 records |
| Changes to numerical opponent rank | 2 records |
| Changes to X8 calculated result | 2 matches |
| Same-day June 11 records | 4 |
| FIFA edition published on earlier date | 246 |
| Manual-review flagged match IDs | 8, 14, 18, 20, 27 |

## Exact corrected outputs

| Match ID | Fixture | v1 X8 | v2 X8 | Mechanism |
|---|---|---:|---:|---|
| 25 | Czechia–South Africa | −0.80 | **−0.60** | Mexico opponent rank 15→14; Team B mean 56.60→56.40 |
| 28 | Mexico–Korea Republic | −19.00 | **−18.80** | Czechia opponent rank 41→40; Team B mean 60.80→60.60 |

The other 23 X8 values are unchanged. Korea Republic (25) and South Africa (60) retain their rank number but have their edition date and ranking evidence updated to 11 June 2026.

## External evidence spot-check

- FIFA official ranking announcement: https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola — dated 11 June 2026 16:45, explicitly says the edition was published hours before the World Cup began. The displayed time lacks an explicit timezone.
- FIFA first-match schedule: https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/articles/preview-matchday-one — first kickoff Mexico–South Africa 13:00 Mexico City, second Korea Republic–Czechia 20:00 Guadalajara on 11 June.
- MLS list as of 11 June: https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup — Mexico 14, Korea Republic 25, Czechia 40, South Africa 60.

**Precision limitation:** The script stores a release instant of 14:45 UTC by assuming the displayed 16:45 uses Zurich summer time (CEST). That exact UTC conversion is **not independently proven by the FIFA webpage**. The more defensible primary claim is FIFA's explicit text that its ranking had been published before kickoff. The input and report should preserve this distinction.

## Five unresolved flags

- **8 and 27 (Qatar):** FIFA Arab Cup fixture histories corroborated, but formal senior-A international classification not conclusively shown.
- **14 (Cabo Verde):** Bermuda friendly corroborated by secondary records, without direct official row-level match confirmation.
- **18 (Iraq):** Iraq–Jordan Arab Cup fixture corroborated, but senior-A status of the specific selection remains not conclusively shown.
- **20 (Jordan):** Jordan–Morocco Arab Cup fixture corroborated, but formal senior-A classification remains not conclusively shown.

Eight individual historical rows carry manual flags, distributed across the five match IDs. FIFA Data Centre team-history links may load dynamically and were not independently audited at row level in this review. Retain these flags. Most other historical rankings are supported by dated secondary editions rather than FIFA's official historical table directly.

## Code review and limitations

The script enforces five unique history rows for each side, chronological ordering, allowed ranking editions, explicit same-day timing rules, and no silent substitution of a missing rank with zero. It calculates Decimal means and exports two-decimal X8 values. Its nine policy tests cover representative acceptance and rejection paths, not all real-world data quality or chronology completeness. URL presence in the CSV does not establish URL accuracy or source independence.

## Academic integrity evidence

Record the following accurately: AI contributed to historical research, source selection, ranking transcription, v2 corrective research, script generation and test design. The data transformations and arithmetic were independently rerun and cross-checked against the saved input records. The four same-day ranking inputs remain subject to the documented assumption about the displayed article timestamp; the official pre-kickoff statement provides separate support. The five manual flags must not be represented as closed.

## Decision and next task

**Accept as versioned reproducible working data, conditional on retaining the documented source and eligibility limitations.** Keep both v1 and v2 unchanged. Use v2, not v1, when later consolidating X8. Proceed with match IDs 31–60 using the same methodology and an explicit 11 June ranking cutoff for historical fixtures from kickoff onward.

### SHA-256 evidence

- `X8_Matches6_30_Historical_Research_v2.csv`: `0bc9fb740a399ecc25083d7d3af4820aaff940cfbd0cd82b0f732e8a62f4408e`
- `X8_Matches6_30_Calculated_Results_v2.csv`: `0200b05612b77658a740c7efa00642357c548fdde2f5e12abc0a150e268fccce`
- `X8_Matches6_30_Reproduce_v2.py`: `cc283f5726214626662ef3759b4dfa222b0131e3aedb7af90bba1538cff5bfd6`
- `X8_Matches6_30_Correction_Change_Log_v2.csv`: `ba65525b446ce170a6d3ccfdd3c0d96a6e0bac0a89f73d53aeaa23d8d51fd44a`
