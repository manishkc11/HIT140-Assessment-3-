# X7 + X8 Consolidation — Final Internal Validation

## Scope and outputs

- Match IDs: **104 unique records, 1–104**; original Team A/Team B order preserved.
- X7: all 104 calendar-day differences recomputed from previous-match dates.
- X8: all **104** differences recomputed from source ranking sums, including all **1,040 historical observations**.
- Batch selection: **1–5 verified**, **6–30 Version 3**, **31–60 reviewed**, **61–90 reviewed**, **91–104 reviewed**.
- Match 29 corrected to **−43.60** (Scotland 11 June 2026 rank 42); Match 25 remains −0.60; Match 28 remains −18.80; Match 50 remains +13.00.
- The original 20-column master workbook was **not** modified; the combined CSV is join-ready by `match_id`.

## Programmatic checks completed

| Check | Finding |
|---|---|
| X7 calendar-day arithmetic | 104/104 pass |
| X8 rank sum / five-match averages / final differences | 104/104 pass |
| Complete histories (5 fixtures × 2 sides) | 208/208 pass |
| Latest historical match agrees with X7 | 208/208 pass |
| Historical World Cup predecessor IDs/dates/opponents | 384 references pass |
| Historical ranking publication not after match date | 1040/1040 pass |
| Same-day edition records requiring separate publication timing evidence | 11 |
| Same opponent + edition numerical conflicts across batches | 0 |
| Same team's historical date assigned inconsistent opponents | 0 |
| Unique opponent-edition ranking keys | 225 |
| Reused pre-tournament matches / ranking archive completeness independently verified on the open web | **Not established** |

## Summary distributions

- X7 zero differences: **62/104**.
- X8 zero differences: **0/104**.
- X8 range: **-45.20 to 57.20**.
- X8 source review statuses: {'WORKING_REPRODUCED': 95, 'SOURCE_REVIEW': 8, 'RESOLVED_LEGACY_FLAG': 1}.

## Source-review queue

The following matches retain flagged or historically provisional source details. See `X7_X8_Source_Review_Log.csv` for full notes.

- Match 5: **SOURCE_REVIEW** — Nicaragua Oct 2025 rank 133 remains provisional (alternative 132 changes X8 by -0.20)
- Match 8: **SOURCE_REVIEW** — Original research flag: FIFA_ARAB_CUP_SENIOR_STATUS_REVIEW
- Match 14: **SOURCE_REVIEW** — Original research flag: PARTIALLY_DOCUMENTED_FRIENDLY
- Match 18: **SOURCE_REVIEW** — Original research flag: FIFA_ARAB_CUP_SENIOR_STATUS_REVIEW
- Match 20: **SOURCE_REVIEW** — Original research flag: FIFA_ARAB_CUP_SENIOR_STATUS_REVIEW
- Match 27: **SOURCE_REVIEW** — Original research flag: FIFA_ARAB_CUP_SENIOR_STATUS_REVIEW
- Match 29: **WORKING_REPRODUCED** — Scotland rank 42 correction applied in Version 3; X8=-43.60
- Match 37: **SOURCE_REVIEW** — Original research flag: PARTIALLY_DOCUMENTED_FRIENDLY
- Match 50: **RESOLVED_LEGACY_FLAG** — Original research flag: SCOTLAND_JUNE_RANK_CONFLICT_WITH_PRIOR_V2_41_VS_42 | Legacy Scotland rank 41/42 flag refers to obsolete v2; v3 rank 42 used consistently
- Match 52: **SOURCE_REVIEW** — Original research flag: FIFA_ARAB_CUP_SENIOR_STATUS_REVIEW

Match 50's legacy Scotland ranking discrepancy is resolved in the consolidated data; its original research flag is retained for traceability. The seven other flagged matches (8, 14, 18, 20, 27, 37, 52) need their specified fixture/classification source reviews. Match 5 retains the provisional Nicaragua rank note.

## Important limitations

1. Historical-ranking positions depend partly on dated **third-party reproductions**, not uniformly on direct FIFA ranking row exports; internal consistency is not source authentication.
2. Earlier Arab Cup senior-A eligibility and several fixture-level evidentiary limitations are preserved, not silently marked verified.
3. X7 is an elapsed **calendar-date interval** (not strict full days between fixtures); keep this definition consistent in the report.
4. Recorded FIFA ranking numbers are inverse strength indicators: lower average rank means stronger-ranked prior opponents. X8 follows Team A minus Team B.
5. Before statistical modelling, examine the exceptional **X7 = −70** value for Match 13 as a leverage/sensitivity issue. Do not discard it merely for being extreme.
6. X7 and X8 are pre-match features; do not use target-match scores as predictors.

## Academic integrity statement

Generative AI assisted in historical fixture research, finding and transcribing rankings, preparing code, identifying and correcting discrepancies, and producing this consolidation and audit. Code reproduces the **calculation and internal date/ranking consistency checks** from exported inputs; it does not independently verify the authenticity or exhaustiveness of external football websites. Retain the original research, corrections, prompts, and the student's own independent spot-checks when preparing the AI declaration.

## Reproduce

`python Consolidate_X7_X8.py` from the package folder. All required source CSVs are included in `inputs/`; outputs go to `outputs/`. Python standard library only.
