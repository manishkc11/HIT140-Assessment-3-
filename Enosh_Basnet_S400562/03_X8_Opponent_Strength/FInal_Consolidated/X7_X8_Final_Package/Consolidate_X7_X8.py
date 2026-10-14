"""FIFA 2026: reproducible merge and internal validation of X7 and X8.

Academic-integrity disclosure: Source selection, historical ranking research, initial
Python scripts, this consolidation script, and audit design were AI-assisted.
This program validates dates, chronology, cross-batch consistency and calculations;
it DOES NOT independently authenticate external FIFA/third-party source pages.

Run: python Consolidate_X7_X8.py
Requires Python standard library only; input CSVs must be in ./inputs/.
Outputs are written into ./outputs/. Source inputs are never modified.
"""
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IN = ROOT / 'inputs'
OUT = ROOT / 'outputs'
BATCHES = [
    ('1-5', 'x8_1_5_results.csv', 'x8_1_5_history.csv', 1, 5),
    ('6-30 v3', 'x8_6_30_v3_results.csv', 'x8_6_30_v3_history.csv', 6, 30),
    ('31-60', 'x8_31_60_results.csv', 'x8_31_60_history.csv', 31, 60),
    ('61-90', 'x8_61_90_results.csv', 'x8_61_90_history.csv', 61, 90),
    ('91-104', 'x8_91_104_results.csv', 'x8_91_104_history.csv', 91, 104),
]
HIST_FIELDS = [
    'match_id','match_date','team_side','team','previous_match_recency',
    'previous_match_date','previous_opponent','opponent_fifa_rank',
    'ranking_publication_date','previous_wc_match_id','fixture_source_url',
    'ranking_source_url','ranking_evidence_class','ranking_verification_status',
    'manual_review_flags','source_batch'
]
MERGE_FIELDS = ['match_id','rest_days_diff','last5_opponent_strength_diff']
INFO_FIELDS = ['match_id','match_date','stage','team_a','team_b',
               'rest_days_diff','last5_opponent_strength_diff',
               'team_a_rest_days','team_b_rest_days',
               'team_a_avg_opponent_rank','team_b_avg_opponent_rank',
               'x8_batch','review_status','review_notes']


def load(name):
    with (IN/name).open('r',encoding='utf-8-sig',newline='') as fh:
        return list(csv.DictReader(fh))


def write_csv(name, rows, cols):
    OUT.mkdir(exist_ok=True)
    with (OUT/name).open('w',encoding='utf-8',newline='') as fh:
        wr=csv.DictWriter(fh,fieldnames=cols,extrasaction='ignore',lineterminator='\n')
        wr.writeheader();wr.writerows(rows)


def iso(s):
    return date.fromisoformat(s)


def number(s):
    return Decimal(str(s))


def assert_ok(condition,message):
    if not condition: raise ValueError(message)


def main():
    x7_rows=load('x7_evidence.csv')
    x7_short=load('x7_merge.csv')
    assert_ok(len(x7_rows)==len(x7_short)==104,'X7 row count not 104')
    x7={int(r['match_id']):r for r in x7_rows}
    assert_ok(set(x7)==set(range(1,105)),'Missing/duplicate X7 IDs')
    assert_ok(len({int(r['match_id']) for r in x7_short})==104,'Duplicate X7 merge IDs')
    for short in x7_short:
        mid=int(short['match_id']);r=x7[mid]
        assert_ok(short['rest_days_diff']==r['rest_days_diff'],f'X7 extract mismatch {mid}')
        ma=iso(r['match_date']);a=(ma-iso(r['team_a_previous_match'])).days
        b=(ma-iso(r['team_b_previous_match'])).days
        assert_ok(a==int(r['team_a_rest_days']) and b==int(r['team_b_rest_days']),f'X7 rest date mismatch {mid}')
        assert_ok(a-b==int(r['rest_days_diff']),f'X7 difference mismatch {mid}')

    results={}
    histories=[]
    issue_labels=defaultdict(set)
    rank_reference=defaultdict(set)
    same_fixture=defaultdict(set)
    wc_ref_checked=0
    latest_x7_checked=0
    x8_recomputed=0
    batch_summary=[]
    same_day=0

    for label, results_fname, hist_fname, start, end in BATCHES:
        res=load(results_fname); hist=load(hist_fname)
        assert_ok(len(res)==end-start+1 and len(hist)==(end-start+1)*10,f'Batch size wrong: {label}')
        batch_ids=set(range(start,end+1))
        assert_ok({int(r['match_id']) for r in res}==batch_ids,f'Match IDs wrong: {label}')
        assert_ok(len({int(r['match_id']) for r in res})==len(res),f'Duplicate result IDs: {label}')
        for r in res:
            mid=int(r['match_id']); assert_ok(mid not in results,f'Overlapping X8 ID {mid}')
            a_sum=int(r['team_a_rank_sum']);b_sum=int(r['team_b_rank_sum'])
            if mid<=5:
                d=r['world_cup_match_date'];aavg=r['team_a_average_opponent_rank'];bavg=r['team_b_average_opponent_rank'];x8=r['x8_last5_opponent_strength_diff']
            else:
                d=r['match_date'];aavg=r['team_a_average_rank'];bavg=r['team_b_average_rank'];x8=r['x8_opponent_strength_difference']
            assert_ok(d==x7[mid]['match_date'],f'Date differs from X7 for ID {mid}')
            assert_ok((r['team_a'],r['team_b'])==(x7[mid]['team_a'],x7[mid]['team_b']),f'Team order mismatch ID {mid}')
            assert_ok(number(aavg)==Decimal(a_sum)/5 and number(bavg)==Decimal(b_sum)/5,f'Rank sum mismatch ID {mid}')
            assert_ok(number(x8)==number(aavg)-number(bavg),f'X8 arithmetic wrong ID {mid}')
            if r.get('manual_review_flags'): issue_labels[mid].add(r['manual_review_flags'])
            results[mid]={
                'batch':label,'date':d,'a':r['team_a'],'b':r['team_b'],
                'a_sum':a_sum,'b_sum':b_sum,'a_avg':number(aavg),
                'b_avg':number(bavg),'x8':number(x8)
            }
            x8_recomputed+=1

        grouped=defaultdict(list)
        for raw in hist:
            mid=int(raw['match_id']);side=raw['team_side'].upper()
            assert_ok(mid in batch_ids and side in ('A','B'),f'Incorrect history side/match ID {label} {mid}')
            fixture_date=raw.get('match_date') or raw.get('world_cup_match_date')
            assert_ok(fixture_date==x7[mid]['match_date'],f'History match date mismatch {label}/{mid}')
            team=raw['team'];current_team=x7[mid]['team_a' if side=='A' else 'team_b']
            assert_ok(team==current_team,f'Team mismatch in history {label}/{mid}/{side}')
            prior=raw['previous_match_date'];pub=raw['ranking_publication_date'];opponent=raw['previous_opponent']
            assert_ok(iso(prior)<iso(fixture_date),f'Future fixture found in history ID {mid}')
            assert_ok(iso(pub)<=iso(prior),f'Future ranking edition for ID {mid} opponent {opponent}')
            if pub==prior: same_day+=1
            rnk=int(raw['opponent_fifa_rank'])
            assert_ok(1<=rnk<=250,f'Invalid FIFA rank {mid}')
            recency=int(raw['previous_match_recency'])
            assert_ok(1<=recency<=5,f'Invalid recency {mid}')
            wc_id=raw.get('previous_wc_match_id','').strip()
            if wc_id:
                prev=int(wc_id)
                assert_ok(prev<mid,f'Non-earlier World Cup predecessor {mid}/{prev}')
                x7_prev=x7[prev]
                assert_ok(x7_prev['match_date']==prior and
                          ((x7_prev['team_a']==team and x7_prev['team_b']==opponent) or
                           (x7_prev['team_b']==team and x7_prev['team_a']==opponent)),
                          f'World Cup history discrepancy match {mid}, predecessor {prev}')
                wc_ref_checked+=1
            rank_reference[(opponent.casefold(),pub)].add(rnk)
            same_fixture[(team.casefold(),prior)].add(opponent.casefold())
            if mid<=5:
                rank_url=raw.get('primary_ranking_evidence_url') or raw.get('ranking_archive_url','')
                r_evidence=raw.get('ranking_evidence_level','')
                ver_status=raw.get('verification_status','')
            else:
                rank_url=raw.get('ranking_source_url','')
                r_evidence=raw.get('ranking_evidence_class','')
                ver_status=raw.get('ranking_verification_status','')
            flag=raw.get('manual_review_flags','')
            if flag: issue_labels[mid].add(flag)
            out={
                'match_id':mid,'match_date':fixture_date,'team_side':side,
                'team':team,'previous_match_recency':recency,'previous_match_date':prior,
                'previous_opponent':opponent,'opponent_fifa_rank':rnk,
                'ranking_publication_date':pub,'previous_wc_match_id':wc_id,
                'fixture_source_url':raw.get('fixture_source_url',''),
                'ranking_source_url':rank_url,'ranking_evidence_class':r_evidence,
                'ranking_verification_status':ver_status,'manual_review_flags':flag,
                'source_batch':label,
            }
            histories.append(out);grouped[(mid,side)].append(out)

        for mid in range(start,end+1):
            for side in ('A','B'):
                group=grouped[(mid,side)]
                assert_ok(len(group)==5,f'Missing five opponents for {mid}/{side}')
                assert_ok({g['previous_match_recency'] for g in group}=={1,2,3,4,5},f'Recency incomplete {mid}/{side}')
                group.sort(key=lambda x:x['previous_match_recency'])
                assert_ok(len({(g['previous_match_date'],g['previous_opponent']) for g in group})==5,f'Duplicate fixture {mid}/{side}')
                assert_ok([g['previous_match_date'] for g in group]==sorted([g['previous_match_date'] for g in group],reverse=True),f'History dates not descending: {mid}/{side}')
                expected_date=x7[mid][f'team_{side.lower()}_previous_match']
                expected_opp=x7[mid][f'team_{side.lower()}_previous_opponent']
                assert_ok((group[0]['previous_match_date'],group[0]['previous_opponent'])==(expected_date,expected_opp),f'X7 latest match discrepancy: {mid}/{side}')
                latest_x7_checked+=1
                assert_ok(sum(g['opponent_fifa_rank'] for g in group)==results[mid][f'{side.lower()}_sum'],f'Historic ranking sum mismatches result {mid}/{side}')
        batch_summary.append((label,len(res),len(hist)))

    assert_ok(set(results)==set(range(1,105)),'Missing results after consolidation')
    assert_ok(len(histories)==1040,'History count not 1040')
    conflicting_ranks={k:v for k,v in rank_reference.items() if len(v)>1}
    assert_ok(not conflicting_ranks,f'Cross-batch FIFA ranking conflicts: {conflicting_ranks}')
    fixture_conflicts={k:v for k,v in same_fixture.items() if len(v)>1}
    assert_ok(not fixture_conflicts,f'Historical fixture contradictions: {fixture_conflicts}')
    assert_ok(results[29]['x8']==Decimal('-43.60'),'Required Match 29 v3 correction missing')
    assert_ok(results[25]['x8']==Decimal('-.60') and results[28]['x8']==Decimal('-18.80'),
              'Prior June ranking corrections missing (Match IDs 25 or 28)')
    assert_ok(results[50]['x8']==Decimal('13.00'),'Match 50 drifted')

    merge=[];info=[];x8only=[];quality=[]
    for mid in range(1,105):
        x7r=x7[mid];x8=results[mid]
        rest=int(x7r['rest_days_diff']);strength=x8['x8']
        x8only.append({'match_id':mid,'last5_opponent_strength_diff':f'{strength:.2f}'})
        merge.append({'match_id':mid,'rest_days_diff':rest,'last5_opponent_strength_diff':f'{strength:.2f}'})
        flags='; '.join(sorted(issue_labels[mid]))
        issues=[]
        if mid==5: issues.append('Nicaragua Oct 2025 rank 133 remains provisional (alternative 132 changes X8 by -0.20)')
        if flags:issues.append('Original research flag: '+flags)
        if mid==50:issues.append('Legacy Scotland rank 41/42 flag refers to obsolete v2; v3 rank 42 used consistently')
        if mid==29:issues.append('Scotland rank 42 correction applied in Version 3; X8=-43.60')
        status='SOURCE_REVIEW' if (flags and mid!=50) or mid==5 else ('RESOLVED_LEGACY_FLAG' if mid==50 else 'WORKING_REPRODUCED')
        msg=' | '.join(issues)
        info.append({
            'match_id':mid,'match_date':x7r['match_date'],'stage':x7r['stage'],
            'team_a':x7r['team_a'],'team_b':x7r['team_b'],
            'rest_days_diff':rest,'last5_opponent_strength_diff':f'{strength:.2f}',
            'team_a_rest_days':int(x7r['team_a_rest_days']),
            'team_b_rest_days':int(x7r['team_b_rest_days']),
            'team_a_avg_opponent_rank':f"{x8['a_avg']:.2f}",
            'team_b_avg_opponent_rank':f"{x8['b_avg']:.2f}",
            'x8_batch':x8['batch'],'review_status':status,'review_notes':msg
        })
        if issues: quality.append({'match_id':mid,'team_a':x7r['team_a'],'team_b':x7r['team_b'],'review_status':status,'issue':msg,'x8_current':f'{strength:.2f}'})
    histories.sort(key=lambda r:(r['match_id'],r['team_side'],r['previous_match_recency']))
    write_csv('X8_104_Merge_Ready.csv',x8only,['match_id','last5_opponent_strength_diff'])
    write_csv('X7_X8_104_Merge_Ready.csv',merge,MERGE_FIELDS)
    write_csv('X7_X8_104_With_Match_Info.csv',info,INFO_FIELDS)
    write_csv('X8_104_Historical_Evidence.csv',histories,HIST_FIELDS)
    write_csv('X7_X8_Source_Review_Log.csv',quality,['match_id','team_a','team_b','review_status','issue','x8_current'])
    stats=Counter(i['review_status'] for i in info)
    x7zeros=sum(int(i['rest_days_diff'])==0 for i in info)
    x8zeros=sum(number(i['last5_opponent_strength_diff'])==0 for i in info)
    rank_count=len(rank_reference)
    assert_ok(latest_x7_checked==208,'X7 cross-match count mismatch')
    report=f'''# X7 + X8 Consolidation — Final Internal Validation

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
| Latest historical match agrees with X7 | {latest_x7_checked}/208 pass |
| Historical World Cup predecessor IDs/dates/opponents | {wc_ref_checked} references pass |
| Historical ranking publication not after match date | 1040/1040 pass |
| Same-day edition records requiring separate publication timing evidence | {same_day} |
| Same opponent + edition numerical conflicts across batches | {len(conflicting_ranks)} |
| Same team's historical date assigned inconsistent opponents | {len(fixture_conflicts)} |
| Unique opponent-edition ranking keys | {rank_count} |
| Reused pre-tournament matches / ranking archive completeness independently verified on the open web | **Not established** |

## Summary distributions

- X7 zero differences: **{x7zeros}/104**.
- X8 zero differences: **{x8zeros}/104**.
- X8 range: **{min(r['x8'] for r in results.values()):.2f} to {max(r['x8'] for r in results.values()):.2f}**.
- X8 source review statuses: {dict(stats)}.

## Source-review queue

The following matches retain flagged or historically provisional source details. See `X7_X8_Source_Review_Log.csv` for full notes.

'''
    for q in quality:
        report+=f"- Match {q['match_id']}: **{q['review_status']}** — {q['issue']}\n"
    report+='''
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
'''
    (OUT/'X7_X8_Consolidation_Validation_Report.md').write_text(report,encoding='utf-8')
    print('VALIDATION PASS: 104 match rows; 1040 historical records; 208 X7 predecessor checks; '
          f'{wc_ref_checked} earlier World Cup references; {len(quality)} review-log records; {len(conflicting_ranks)} ranking conflicts.')
    for label,m,h in batch_summary: print(f'  {label}: {m} matches, {h} historical observations')
    print('X7 zeros:',x7zeros,'X8 zeros:',x8zeros,'X8 range',min(r['x8'] for r in results.values()),max(r['x8'] for r in results.values()))


if __name__=='__main__':main()
