"""Reproduce X7 Rest Days Difference for FIFA World Cup match IDs 91–104.

ACADEMIC INTEGRITY / GENERATIVE AI ASSISTANCE
--------------------------------------------
The historical fixture selections, official/media source research, source URLs,
and this Python program were prepared WITH GENERATIVE AI ASSISTANCE.
The historical input CSV was constructed by reading the user's unmodified
104-match master workbook, tracing each team's full earlier World Cup fixture
history, and associating published source pages located through web research.

IMPORTANT DISTINCTION:
  * Python REPRODUCES arithmetic and checks the exported chronology, team
    ordering and previous-master-match identifiers.
  * Python DOES NOT fetch, authenticate or independently verify live webpages,
    prove there were no unlisted fixtures, or guarantee the pages still exist.
  * The primary source_url is a match-specific report, feature or official video
    where possible. A few rows instead use a dated matchday article section.
    The source_type field identifies the distinction, including media reports
    and FIFA's non-English report.
  * The chronology_url is a GENERAL FIFA knockout-results listing. It is
    NOT counted as a second independent match-specific publication.
  * If two observations link to the same webpage it is ONE publication,
    not two independent sources.
  * Local match calendar dates are used, not article publication dates.

METHODOLOGY
-----------
RestDays = (current World Cup LOCAL calendar date - previous fixture LOCAL
            calendar date).days
X7 = Team A RestDays - Team B RestDays.
The difference of calendar dates is used; for instance July 19 - July 14 = 5.
AET and penalty shootouts have no special effect on this date calculation.

INPUTS:   X7_Matches91_104_Master_Extract.csv
          X7_Matches91_104_Previous_Matches.csv
OUTPUT:   X7_Matches91_104_Calculated_Results.csv
RUN:      python X7_Matches91_104_Reproduce.py

Only Python's standard library is used; the original Excel file is NOT opened
or modified by this script. No X8 work is performed.
"""
from __future__ import annotations
import csv
import json
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

BASE=Path(__file__).resolve().parent
PFX='X7_Matches91_104'
MASTER=BASE/f'{PFX}_Master_Extract.csv'
PREVIOUS=BASE/f'{PFX}_Previous_Matches.csv'
OUTPUT=BASE/f'{PFX}_Calculated_Results.csv'
FIELDS=[
 'match_id','match_date','team_a','team_b',
 'team_a_previous_date','team_a_previous_opponent','team_a_previous_match_id','team_a_rest_days',
 'team_b_previous_date','team_b_previous_opponent','team_b_previous_match_id','team_b_rest_days',
 'x7_rest_days_difference','team_a_source_url','team_b_source_url',
 'team_a_chronology_url','team_b_chronology_url','validation_notes'
]


def read_csv(path:Path)->list[dict[str,str]]:
    with path.open('r',encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))


def check_url(url:str, label:str)->None:
    """Check URL syntax only; DOES NOT prove a page is reachable or accurate."""
    u=urlparse(url)
    if u.scheme!='https' or not u.netloc or not u.path:
        raise ValueError(f'Missing or invalid-shaped URL for {label}: {url!r}')


def check_predecessor(r:dict[str,str], current:date)->int:
    """Check selected fixture really is latest in supplied earlier WC chronology."""
    label=f"match {r['match_id']} team {r['team']}"
    pd=date.fromisoformat(r['previous_match_date'])
    if pd>=current:raise ValueError(f'Previous date not strictly earlier: {label}')
    earlier=json.loads(r['earlier_world_cup_fixtures_json'])
    if not isinstance(earlier,list) or not earlier:
        raise ValueError(f'No earlier World Cup fixtures supplied: {label}')
    old_ids=set()
    for x in earlier:
        oldid=int(x['match_id'])
        if oldid in old_ids:raise ValueError(f'Duplicate prior World Cup ID: {label}')
        old_ids.add(oldid)
        if oldid>=int(r['match_id']) or date.fromisoformat(x['match_date'])>=current:
            raise ValueError(f'Future or current match in earlier history: {label}')
        if not x['opponent']:
            raise ValueError(f'Opponent missing in earlier history: {label}')
    latest=max(earlier,key=lambda x:(x['match_date'],int(x['match_id'])))
    if (int(latest['match_id'])!=int(r['previous_master_match_id']) or
        latest['match_date']!=r['previous_match_date'] or
        latest['opponent']!=r['previous_opponent']):
        raise ValueError(f'Selected predecessor is NOT latest in earlier master history: {label}')
    check_url(r['source_url'],f'{label} source_url')
    check_url(r['chronology_url'],f'{label} chronology_url')
    if r['chronology_source_type']!='GENERAL_FIFA_TOURNAMENT_RESULTS':
        raise ValueError(f'Incorrect general-source classification: {label}')
    if not r['source_type'].strip():
        raise ValueError(f'Primary-source classification missing: {label}')
    return (current-pd).days


def reproduce()->list[dict[str,object]]:
    matches=read_csv(MASTER)
    records=read_csv(PREVIOUS)
    ids=[int(row['match_id']) for row in matches]
    if ids!=list(range(91,105)):
        raise ValueError('Extract must contain original IDs 91–104 in exact order, once each.')
    if len(records)!=28:raise ValueError('Expected 28 historical team observations.')
    lookup={}
    for rec in records:
        key=(rec['match_id'],rec['side'])
        if rec['side'] not in ('A','B') or key in lookup:
            raise ValueError(f'Duplicate/unrecognised observation: {key}')
        lookup[key]=rec
    expected={(str(i),side) for i in range(91,105) for side in ('A','B')}
    if set(lookup)!=expected:raise ValueError('Missing or unexpected match-side records')

    out=[]
    for match in matches:
        mid=match['match_id'];current=date.fromisoformat(match['match_date'])
        a,b=lookup[mid,'A'],lookup[mid,'B']
        if (a['team']!=match['team_a'] or b['team']!=match['team_b']):
            raise ValueError(f'Team A/Team B order does not match extract for {mid}')
        a_rest=check_predecessor(a,current)
        b_rest=check_predecessor(b,current)
        if not a['previous_opponent'] or not b['previous_opponent']:
            raise ValueError(f'Previous fixture opponent missing for match {mid}')
        notes=[]
        for side,rec in [('A',a),('B',b)]:
            notes.append(rec['notes'])
            if rec['source_type']=='MATCHDAY_ARTICLE_WITH_FIXTURE_SECTION':
                notes.append(f'Team {side}: FIFA daily recap section, NOT a dedicated match report')
            if rec['source_type']=='MATCH_SPECIFIC_INDEPENDENT_REPORT':
                notes.append(f'Team {side}: independent media report, cross-check with official FIFA schedule')
            if rec['source_type']=='MATCH_SPECIFIC_VERIFIED_FIFA_YOUTUBE':
                notes.append(f'Team {side}: verified FIFA YouTube fixture clip, not a written match report')
            if rec['source_type']=='MATCH_SPECIFIC_FIFA_REPORT_UNUSUAL_URL':
                notes.append(f'Team {side}: unusual FIFA article URL structure (check if link changes)')
        if a['source_url']==b['source_url']:
            notes.append('Both teams use SAME primary URL: count as only ONE source')
        out.append({
            'match_id':mid,'match_date':match['match_date'],
            'team_a':a['team'],'team_b':b['team'],
            'team_a_previous_date':a['previous_match_date'],
            'team_a_previous_opponent':a['previous_opponent'],
            'team_a_previous_match_id':a['previous_master_match_id'],
            'team_a_rest_days':a_rest,
            'team_b_previous_date':b['previous_match_date'],
            'team_b_previous_opponent':b['previous_opponent'],
            'team_b_previous_match_id':b['previous_master_match_id'],
            'team_b_rest_days':b_rest,
            'x7_rest_days_difference':a_rest-b_rest,
            'team_a_source_url':a['source_url'],'team_b_source_url':b['source_url'],
            'team_a_chronology_url':a['chronology_url'],
            'team_b_chronology_url':b['chronology_url'],
            'validation_notes':' | '.join(notes),
        })

    # Cross-check common earlier fixtures in the exported histories.
    by_old_id={}
    for rec in records:
        by_old_id.setdefault(rec['previous_master_match_id'],[]).append(rec)
    if len(by_old_id)!=26:raise ValueError('Expected 26 distinct predecessor World Cup fixtures')
    for old_id, sides in by_old_id.items():
        if len(sides)>2:raise ValueError(f'Too many observations refer to prior ID {old_id}')
        if len(sides)==2:
            x,y=sides
            if (x['previous_match_date']!=y['previous_match_date'] or
                x['team']!=y['previous_opponent'] or
                y['team']!=x['previous_opponent'] or
                x['source_url']!=y['source_url']):
                raise ValueError(f'Contradictory historical fixture references for old ID {old_id}')

    with OUTPUT.open('w',encoding='utf-8-sig',newline='') as fh:
        writer=csv.DictWriter(fh,fieldnames=FIELDS,lineterminator='\r\n')
        writer.writeheader()
        writer.writerows(out)
    print('Match | Current date | Previous A ID/rest | Previous B ID/rest | X7')
    for r in out:
        print(f"{r['match_id']:>5} | {r['match_date']} | "
              f"{r['team_a_previous_match_id']:>3} / {r['team_a_rest_days']:>2} | "
              f"{r['team_b_previous_match_id']:>3} / {r['team_b_rest_days']:>2} | "
              f"{r['x7_rest_days_difference']:+d}")
    print(f"PASS: {len(out)} matches; {len(records)} observations; {len(by_old_id)} distinct older fixtures.")
    print('Source URLs are recorded research evidence; no live URL authentication is performed by this script.')
    return out

if __name__=='__main__':
    reproduce()
