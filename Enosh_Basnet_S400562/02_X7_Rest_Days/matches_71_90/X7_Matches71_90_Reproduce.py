"""Reproduce FIFA World Cup 2026 X7 for match IDs 71–90 from exported CSVs.

ACADEMIC INTEGRITY AND AI ASSISTANCE
This Python code and its preceding selection of historical fixtures, opponents and
source URLs were prepared with generative AI assistance. Those selections were
checked against the original master workbook and published FIFA/association
historical records. Only the present X7 calculations are produced here.

The script verifies chronological/relational consistency using previous World
Cup fixture histories exported from the original master workbook. It DOES NOT
fetch or authenticate source URLs, independently confirm all external fixture
claims, or exclude every theoretically possible unlisted senior international.
The website audit is human/AI-assisted research separate from arithmetic.

The source_url field may identify a single match report/video/feature, or an
explicitly labelled MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION. A FIFA-published match-specific official YouTube highlight is identified separately. chronology_url is
always a GENERAL FIFA tournament-wide fixture results page and is NOT a second
independent source. Identical URLs are ONE source, even when cited for both
teams that previously met each other.

Convention:
rest days = (current local calendar date - previous completed fixture date).days
X7 = Team A rest days - Team B rest days.
No goal scored/penalty shootout/extra time information affects date difference.

Input: X7_Matches71_90_Master_Extract.csv and
       X7_Matches71_90_Previous_Matches.csv
Output: X7_Matches71_90_Calculated_Results.csv
No Excel workbook is read or modified. No X8 is calculated.
Run: python X7_Matches71_90_Reproduce.py
Only the Python standard library is needed.
"""
from __future__ import annotations
from datetime import date
from pathlib import Path
import csv,json

BASE=Path(__file__).resolve().parent
P='X7_Matches71_90'
MASTER=BASE/f'{P}_Master_Extract.csv'
PREVIOUS=BASE/f'{P}_Previous_Matches.csv'
RESULTS=BASE/f'{P}_Calculated_Results.csv'
OUTPUT_COLUMNS=['match_id','match_date','team_a','team_b',
 'team_a_previous_date','team_a_previous_opponent','team_a_rest_days',
 'team_b_previous_date','team_b_previous_opponent','team_b_rest_days',
 'x7_rest_days_difference','team_a_source_url','team_b_source_url',
 'team_a_chronology_url','team_b_chronology_url','validation_notes']

def load(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def check_prev(record,current):
    label=f"match {record['match_id']} team {record['team']}"
    past=record['previous_match_date'].strip()
    if not past: return None
    prev=date.fromisoformat(past)
    if prev >= current:raise ValueError(f'Previous match not before target: {label}')
    records=json.loads(record['earlier_world_cup_fixtures_json'])
    if not records:raise ValueError(f'No eligible earlier World Cup matches: {label}')
    for rr in records:
        assert all(v in rr for v in ('match_id','match_date','opponent')),label
        if int(rr['match_id'])>=int(record['match_id']):raise ValueError(f'Future master match ID: {label}')
        if date.fromisoformat(rr['match_date'])>=current:raise ValueError(f'Future history date: {label}')
    latest=max(records,key=lambda r:(r['match_date'],int(r['match_id'])))
    if ((str(latest['match_id'])!=record['previous_master_match_id']) or
        latest['match_date']!=past or latest['opponent']!=record['previous_opponent']):
        raise ValueError(f'Previous fixture is not latest in exported master history: {label}')
    if not record['source_url'].startswith('https://'):
        raise ValueError(f'Missing/invalid-shaped source URL: {label}')
    if not record['chronology_url'].startswith('https://'):
        raise ValueError(f'Missing general chronology URL: {label}')
    if record['chronology_source_type']!='GENERAL_FIFA_TOURNAMENT_RESULTS':
        raise ValueError(f'Unlabelled chronology source: {label}')
    allowed={'MATCH_SPECIFIC','MATCH_SPECIFIC_FEATURE','MATCH_SPECIFIC_VIDEO',
       'MATCH_SPECIFIC_ASSOCIATION','MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION',
       'MATCH_SPECIFIC_FIFA_YOUTUBE'}
    if record['source_type'] not in allowed:raise ValueError(f'Unclassified evidence: {label}')
    return (current-prev).days

def run():
    matches=load(MASTER); prev=load(PREVIOUS)
    if [int(m['match_id']) for m in matches]!=list(range(71,91)):
        raise ValueError('Match extract must contain IDs 71-90 in order, exactly once')
    if len(prev)!=40:raise ValueError('Expected 40 earlier-team observations')
    bykey={}
    for r in prev:
        k=(r['match_id'],r['side'])
        if r['side'] not in ('A','B') or k in bykey:
            raise ValueError(f'Duplicate/incorrect side observation: {k}')
        bykey[k]=r
    if set(bykey)!={(str(i),s) for i in range(71,91) for s in ('A','B')}:
        raise ValueError('Missing/unexpected match-side history')
    out=[]
    for m in matches:
        mid=m['match_id'];cur=date.fromisoformat(m['match_date'])
        a,b=bykey[mid,'A'],bykey[mid,'B']
        if a['team']!=m['team_a'] or b['team']!=m['team_b']:
            raise ValueError(f'Incorrect team ordering for match ID {mid}')
        ra=check_prev(a,cur);rb=check_prev(b,cur)
        issues=[]
        if ra is None or not a['previous_opponent']:issues.append('MISSING or UNVERIFIED Team A prior match')
        if rb is None or not b['previous_opponent']:issues.append('MISSING or UNVERIFIED Team B prior match')
        for name,r in [('A',a),('B',b)]:
            if r['source_type']=='MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION':
                issues.append(f'Team {name}: general matchday article, not dedicated report')
            if r['source_type']=='MATCH_SPECIFIC_FIFA_YOUTUBE':
                issues.append(f'Team {name}: official FIFA YouTube match-specific highlights')
        if a['source_url']==b['source_url']:
            issues.append('Both sides share one source URL; NOT independent sources')
        value=(ra-rb) if (ra is not None and rb is not None and a['previous_opponent'] and b['previous_opponent']) else ''
        notes=' | '.join([a['notes'],b['notes'],*issues])
        out.append({'match_id':mid,'match_date':m['match_date'],'team_a':m['team_a'],'team_b':m['team_b'],
            'team_a_previous_date':a['previous_match_date'],'team_a_previous_opponent':a['previous_opponent'],
            'team_a_rest_days':ra if ra is not None else '',
            'team_b_previous_date':b['previous_match_date'],'team_b_previous_opponent':b['previous_opponent'],
            'team_b_rest_days':rb if rb is not None else '',
            'x7_rest_days_difference':value,'team_a_source_url':a['source_url'],
            'team_b_source_url':b['source_url'],'team_a_chronology_url':a['chronology_url'],
            'team_b_chronology_url':b['chronology_url'],'validation_notes':notes})
    # For any reused preceding World Cup fixture, confirm its two sides and date agree.
    prior={}
    for r in prev:prior.setdefault(r['previous_master_match_id'],[]).append(r)
    for old_id,entries in prior.items():
        if len(entries)>2:raise ValueError(f'Too many previous sides for fixture {old_id}')
        if len(entries)==2:
            a,b=entries
            if (a['previous_match_date']!=b['previous_match_date'] or
                a['team']!=b['previous_opponent'] or b['team']!=a['previous_opponent'] or
                a['source_url']!=b['source_url']):
                raise ValueError(f'Conflicting previous fixture evidence for {old_id}')
    if len(prior)!=30:raise ValueError(f'Unexpected prior fixture count {len(prior)}, expected 30')
    with RESULTS.open('w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=OUTPUT_COLUMNS,lineterminator='\r\n')
        writer.writeheader();writer.writerows(out)
    print('ID | Date | Team A | Team B | A rest | B rest | X7')
    for r in out:
        print(f"{r['match_id']} | {r['match_date']} | {r['team_a']} | {r['team_b']} | {r['team_a_rest_days']} | {r['team_b_rest_days']} | {r['x7_rest_days_difference']}")
    print(f'OK: {len(out)} matches; {len(prev)} observations; {len(prior)} distinct prior fixtures; results saved.')

if __name__=='__main__':run()
