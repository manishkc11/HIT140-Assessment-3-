# X8 matches 31–60 — Independent audit

**Audit date:** 12 October 2026  
**Inputs:** User-uploaded `Archive(2).zip`, earlier X8 matches 1–5 verified input, X8 matches 6–30 corrected v2 research/results, and consolidated X7 evidence.  
**Status:** Calculations accepted as reproducible *working data*; a cross-batch inconsistency in earlier match 29 requires targeted correction; all source-quality limitations are retained.

## 1. Independent file and computation checks

| Test | Result |
|---|---|
| Five expected deliverables in ZIP | PASS |
| Current match IDs | 31–60 inclusive, exactly 30 |
| Research observations | 300 = 30 matches × 2 teams × 5 matches |
| Five distinct chronological previous fixtures per team | PASS (script validation) |
| Original Team A/B ordering and match dates | PASS against embedded master chronology |
| Previous World Cup fixture identities / dates | PASS for 84 references against embedded master chronology |
| Latest previous fixture against original consolidated X7 evidence | **60/60 independently matched** |
| Python publication policy unit tests | **9/9 pass** |
| Independently recomputed X8 from raw ranking sums | **30/30 pass** |
| Isolated reproduction of calculated CSV | PASS: byte-identical SHA-256 |
| Null/blank ranking values in selected baseline | 0 |
| Manual-review matches | 37, 50, 52 |

**SHA-256 of original and reproduced CSV:** `8a3e185ca2876e40ac2bd3e5c3b70c0b9210bbac6016db466445398f3ddaa270`.

The Python checks verify the provided dataset's arithmetic, dates, grouping, and internal references. They cannot independently certify that every external football record and third-party ranking archive is historically correct.

## 2. Material cross-batch discrepancy discovered

**Scotland's 11 June 2026 FIFA ranking was 42, not 41.** Both the dated WildStat table and MLS's 11 June World Cup ranking list show 42:

- https://wildstat.com/p/7001/ddate/2026-06-11
- https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup

A programmatic cross-batch check across the X8 1–5, corrected v2 X8 6–30, and X8 31–60 datasets found **one inconsistent opponent/edition pair**:

- **Earlier match 29 — Brazil vs Haiti:** Haiti's preceding match was vs Scotland on 13 June. The X8 6–30 v2 input lists Scotland at **41**. Changing this to **42** increases Haiti's prior-opponent average by `1/5 = 0.20`. Since Haiti is Team B, the corrected match 29 X8 becomes **−43.60** instead of **−43.40**.
- **Current match 50 — Morocco vs Haiti:** The newer research correctly lists Scotland as **42** in both sides' histories. Match 50 stays **+13.00**. The result is unaffected because both team averages incorporate the same +0.20 adjustment.

**Action:** Create a versioned X8 6–30 **v3** correction for the Scotland record and match 29 calculation, with change log and reproducibility test. Do **not** overwrite earlier v1 or v2 artifacts. Preserve the 31–60 input as-is; its Scotland rank and X8 values are correct according to the available dated ranking evidence. Recheck all previously reused Scotland entries at this edition when later batches are generated.

The corrected record is not one of the four June 11 corrections previously made to 6–30; this is an additional, separately documented issue.

## 3. Outstanding source reviews — and improved evidence

### Match 37 — Cabo Verde vs Bermuda on 6 June 2026

- The research flags Cabo Verde's 6 June Bermuda friendly as partially documented.
- **New official source:** FIFA's warm-up report explicitly lists **Cabo Verde 3–0 Bermuda** under **6 June**: https://www.fifa.com/en/articles/pre-tournament-warm-up-results-fixtures-scorers
- Dated April 1 2026 historical ranking archive shows **Bermuda 166th**: https://wildstat.com/p/7001/ddate/2026-04-01
- **Recommendation:** Update match-specific evidence to FIFA and consider clearing the *fixture-existence/date* concern after source confirmation. Retain the general note that rank 166 comes from a secondary historical ranking table rather than direct FIFA row-level export. Baseline X8 for match 37 remains **−42.80**.

### Match 50 — Scotland 11 June ranking

- Scotland's June rank **42** is independently corroborated by two dated secondary sources (above).
- Current batch uses rank 42 for both relevant observations; X8 stays **+13.00**.
- The historical inconsistency belongs to earlier **match 29** and needs the v3 patch described above.

### Match 52 — Qatar–Tunisia FIFA Arab Cup on 7 December 2025

- Official FIFA match archive records the fixture: https://www.plus.fifa.com/en/content/qatar-vs-tunisia/bc83f358-3f07-4101-a3be-32a99189402d
- Qatar Football Association classifies the report under **National Teams / First Team**: https://www.qfa.qa/en/news/qatar-exits-arab-cup-following-defeat-to-tunisia
- Qatar's FA also reports that the December ranking was influenced by the team’s Arab Cup performance: https://www.qfa.qa/en/news/maroons-drop-three-spots-in-december-fifa-ranking
- FIFA's December ranking announcement says Arab Cup results featured in the relevant international fixture period: https://ipt.fifa.com/fifa-rankings/world-ranking/men/news/coca-cola-december-2025-rank-spain-top-morocco-arab-cup-win
- **Recommendation:** There is substantial official evidence for treating this as eligible senior first-team opposition, subject to the group's recorded operational definition of 'senior international'. Do not claim an individually retrieved FIFA 'A-match approval' flag without that evidence. Current match 52 X8 **−17.20** remains provisional until the methodology decision is recorded.

## 4. Source limitations

- Most historical opponent ranking values are carried forward from dated **secondary FIFA ranking reproductions**. A published ranking edition date is not itself direct confirmation of every team's position.
- The tournament-wide FIFA fixture page is a **general chronology source**, not independent match-specific verification for every repeated row.
- `reused_match_specific_url_unverified` entries were not exhaustively opened/validated in this audit.
- Independent script validation of the latest World Cup predecessor (X7) and date-based ranking choices does not prove complete histories outside the World Cup.

## 5. Submission and academic-integrity actions

1. Retain the five AI-generated files for matches 31–60 in `03_X8_Opponent_Strength/Matches_31_60/`.
2. Retain **this independent audit** in `05_Evidence_and_AI_Declaration/`.
3. Ask the research agent to make the targeted **match 29 v3** amendment to the earlier X8 6–30 research/results (not to 31–60) and to update source classifications for 37 and 52 with appropriate evidence and caveats.
4. Reproduce the corrected batch locally and record the result. Then continue with X8 match IDs 61–90, preserving source quality flags.
5. Accurately disclose AI use for source research, record creation, Python code generation, and validation; do not claim wholly manual or wholly official-source verification.

**Conclusions:** All **30 X8 values in batch 31–60** are arithmetically reproducible with the supplied inputs. The **earlier match 29** must be revised from −43.40 to **−43.60** to reconcile Scotland's 11 June ranking. Stronger evidence improves the status of matches 37 and 52 but must be formally recorded before changing review classifications.
