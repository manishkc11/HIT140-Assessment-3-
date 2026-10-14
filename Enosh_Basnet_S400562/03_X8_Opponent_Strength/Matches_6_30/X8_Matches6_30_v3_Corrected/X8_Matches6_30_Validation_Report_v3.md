# X8 Matches 6–30 — Version 3 targeted correction and validation

## Scope
This version was regenerated from the user-provided **v2** research file; the older files remain unchanged. It corrects exactly one historical input: **Match 29** (Brazil vs Haiti), Haiti's previous fixture against Scotland on **13 June 2026**, with the Scotland rank from the 11 June 2026 FIFA ranking edition updated **41 → 42**. The working ranking source is the dated secondary archive documented in the historical CSV: https://wildstat.com/p/7001/ddate/2026-06-11. This file does not claim direct row-level verification against the FIFA database.

## Calculated effect

| Item | Version 2 | Version 3 |
| --- | ---: | ---: |
| Scotland rank for Haiti's match | 41 | 42 |
| Brazil rank sum | 83 | 83 |
| Brazil average | 16.60 | 16.60 |
| Haiti rank sum | 300 | 301 |
| Haiti average | 60.00 | 60.20 |
| Match 29 X8 | −43.40 | **−43.60** |

**All 24 other X8 results are unchanged.** The only changes to the calculated-results file are the three Match 29 fields (`team_b_rank_sum`, `team_b_average_rank`, and `x8_opponent_strength_difference`). In the underlying research CSV, exactly one cell was modified (`opponent_fifa_rank`).

## Independent calculation and reproducibility checks

- Historical observations: **250**, 5 per team per match, match IDs **6–30**.
- Ranking policy tests: **9 passed**.
- Reproduction script: executed successfully, using the corrected research CSV as input.
- Original vs v3 research: exactly **one field changed in one record**.
- Original vs v3 results: exactly **one match changed**, with the three derived fields noted above.
- v3 source data SHA-256: `7041332831b06ada023cbf6206df6355d23dad93e6ac48a935fe5b7fa275a25e`.
- v3 result data SHA-256: `bb50ca0efd3cadf9b86c6b42e9c81c6ad8b58dc2c0ea7f2d260015986956cd42`.
- Earlier v2 source data SHA-256: `0bc9fb740a399ecc25083d7d3af4820aaff940cfbd0cd82b0f732e8a62f4408e`.
- Earlier v2 result data SHA-256: `0200b05612b77658a740c7efa00642357c548fdde2f5e12abc0a150e268fccce`.

To reproduce from the v3 research file in the same folder as the script:

```bash
python X8_Matches6_30_Reproduce_v3.py --test
python X8_Matches6_30_Reproduce_v3.py
```

This Python script will **write** `X8_Matches6_30_Calculated_Results_v3.csv` in that folder; keep the archive copy as an evidence snapshot if you want to compare hashes after rerunning.

## Academic integrity and limitations

The original historical fixture/ranking research and Python code were AI-assisted. This v3 correction, code adaptation, and difference tests were also AI-assisted. The Python checks establish that the output is consistent with the recorded inputs; they **do not independently authenticate** the football source websites or resolve prior manual review flags for the wider 6–30 dataset.

For consolidation into all 104 matches, **use v3 for match IDs 6–30**, especially Match 29 X8 = **−43.60**. Do not use v2's obsolete −43.40 value. The first-five, 31–60, 61–90, and 91–104 batches are separate inputs.
