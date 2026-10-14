#!/usr/bin/env python3
"""X8 historical opponent strength, World Cup match IDs 31-60.

Academic integrity: Generative AI was used in historical research, source selection,
transcription/cross-checking of rankings, Python code generation and validation design.
Most rankings originate from dated SECONDARY reproductions of FIFA ranking editions,
not direct downloads of individual FIFA ranking records. The script checks arithmetic,
chronology and data structure; it does NOT authenticate websites, prove the complete
international match history, or resolve FIFA Arab Cup senior-A eligibility.

INPUT:  X8_Matches31_60_Historical_Research.csv (300 rows)
OUTPUT: X8_Matches31_60_Calculated_Results.csv (30 rows)
USAGE:  python X8_Matches31_60_Reproduce.py
        python X8_Matches31_60_Reproduce.py --test
"""
import csv, sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

INPUT = Path(__file__).with_name('X8_Matches31_60_Historical_Research.csv')
OUTPUT = Path(__file__).with_name('X8_Matches31_60_Calculated_Results.csv')
CONTROL_MATCHES = {1: ('2026-06-11', 'Mexico', 'South Africa'), 2: ('2026-06-11', 'Korea Republic', 'Czechia'), 3: ('2026-06-12', 'Canada', 'Bosnia and Herzegovina'), 4: ('2026-06-12', 'USA', 'Paraguay'), 5: ('2026-06-13', 'Haiti', 'Scotland'), 6: ('2026-06-13', 'Australia', 'Türkiye'), 7: ('2026-06-13', 'Brazil', 'Morocco'), 8: ('2026-06-13', 'Qatar', 'Switzerland'), 9: ('2026-06-14', "Côte d'Ivoire", 'Ecuador'), 10: ('2026-06-14', 'Germany', 'Curaçao'), 11: ('2026-06-14', 'Netherlands', 'Japan'), 12: ('2026-06-14', 'Sweden', 'Tunisia'), 13: ('2026-06-15', 'Saudi Arabia', 'Uruguay'), 14: ('2026-06-15', 'Spain', 'Cabo Verde'), 15: ('2026-06-15', 'IR Iran', 'New Zealand'), 16: ('2026-06-15', 'Belgium', 'Egypt'), 17: ('2026-06-16', 'France', 'Senegal'), 18: ('2026-06-16', 'Iraq', 'Norway'), 19: ('2026-06-16', 'Argentina', 'Algeria'), 20: ('2026-06-16', 'Austria', 'Jordan'), 21: ('2026-06-17', 'Ghana', 'Panama'), 22: ('2026-06-17', 'England', 'Croatia'), 23: ('2026-06-17', 'Portugal', 'Congo DR'), 24: ('2026-06-17', 'Uzbekistan', 'Colombia'), 25: ('2026-06-18', 'Czechia', 'South Africa'), 26: ('2026-06-18', 'Switzerland', 'Bosnia and Herzegovina'), 27: ('2026-06-18', 'Canada', 'Qatar'), 28: ('2026-06-18', 'Mexico', 'Korea Republic'), 29: ('2026-06-19', 'Brazil', 'Haiti'), 30: ('2026-06-19', 'Scotland', 'Morocco'), 31: ('2026-06-19', 'Türkiye', 'Paraguay'), 32: ('2026-06-19', 'USA', 'Australia'), 33: ('2026-06-20', 'Germany', "Côte d'Ivoire"), 34: ('2026-06-20', 'Ecuador', 'Curaçao'), 35: ('2026-06-20', 'Netherlands', 'Sweden'), 36: ('2026-06-20', 'Tunisia', 'Japan'), 37: ('2026-06-21', 'Uruguay', 'Cabo Verde'), 38: ('2026-06-21', 'Spain', 'Saudi Arabia'), 39: ('2026-06-21', 'Belgium', 'IR Iran'), 40: ('2026-06-21', 'New Zealand', 'Egypt'), 41: ('2026-06-22', 'Norway', 'Senegal'), 42: ('2026-06-22', 'France', 'Iraq'), 43: ('2026-06-22', 'Argentina', 'Austria'), 44: ('2026-06-22', 'Jordan', 'Algeria'), 45: ('2026-06-23', 'England', 'Ghana'), 46: ('2026-06-23', 'Panama', 'Croatia'), 47: ('2026-06-23', 'Portugal', 'Uzbekistan'), 48: ('2026-06-23', 'Colombia', 'Congo DR'), 49: ('2026-06-24', 'Scotland', 'Brazil'), 50: ('2026-06-24', 'Morocco', 'Haiti'), 51: ('2026-06-24', 'Switzerland', 'Canada'), 52: ('2026-06-24', 'Bosnia and Herzegovina', 'Qatar'), 53: ('2026-06-24', 'Czechia', 'Mexico'), 54: ('2026-06-24', 'South Africa', 'Korea Republic'), 55: ('2026-06-25', 'Curaçao', "Côte d'Ivoire"), 56: ('2026-06-25', 'Ecuador', 'Germany'), 57: ('2026-06-25', 'Japan', 'Sweden'), 58: ('2026-06-25', 'Tunisia', 'Netherlands'), 59: ('2026-06-25', 'Türkiye', 'USA'), 60: ('2026-06-25', 'Paraguay', 'Australia')}
PUBLISHED_RANKING_EDITIONS = ('2025-09-18','2025-10-17','2025-11-19','2025-12-22',
                              '2026-01-19','2026-04-01','2026-06-11')
FIFA_JUNE_RELEASE_NOTE = 'FIFA 11 June announcement explicitly says publication preceded World Cup kickoff'
RESULT_FIELDS = ['match_id','match_date','team_a','team_b','team_a_rank_sum',
                 'team_a_average_rank','team_b_rank_sum','team_b_average_rank',
                 'x8_opponent_strength_difference','calculation_status','manual_review_flags',
                 'team_a_records','team_b_records','ranking_source_quality']


def fmt(val):
    return str(val.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))


def published_before_fixture(pub, fixture, decision):
    '''A publication on the fixture day is legal ONLY when pre-kickoff is established.'''
    if pub < fixture:
        return True
    if pub > fixture:
        return False
    return (pub == date(2026,6,11)
            and decision == 'FIFA_CONFIRMED_RELEASE_BEFORE_OPENING_KICKOFF')


def selected_edition(pub, fixture, decision):
    '''Returns the newest eligible published edition from the agreed edition list.'''
    editions=[date.fromisoformat(i) for i in PUBLISHED_RANKING_EDITIONS]
    available=[i for i in editions if published_before_fixture(i, fixture,
             decision if i == pub else '')]
    return max(available) if available else None


def run_policy_tests():
    assert published_before_fixture(date(2026,6,11),date(2026,6,11),
           'FIFA_CONFIRMED_RELEASE_BEFORE_OPENING_KICKOFF')
    assert not published_before_fixture(date(2026,6,11),date(2026,6,11),'')
    assert not published_before_fixture(date(2026,6,11),date(2026,6,11),'UNCONFIRMED')
    assert not published_before_fixture(date(2026,6,11),date(2026,6,10),'')
    assert published_before_fixture(date(2026,4,1),date(2026,6,10),'')
    assert selected_edition(date(2026,6,11), date(2026,6,11), '') == date(2026,4,1)
    assert selected_edition(date(2026,6,11), date(2026,6,11),
                            'FIFA_CONFIRMED_RELEASE_BEFORE_OPENING_KICKOFF') == date(2026,6,11)
    assert selected_edition(date(2026,4,1), date(2026,6,10),'') == date(2026,4,1)
    assert selected_edition(date(2025,10,17), date(2025,11,18),'') == date(2025,10,17)
    return 9


def calculate(input_path=INPUT, output_path=OUTPUT):
    with open(input_path,encoding='utf-8-sig',newline='') as f:
        rows=list(csv.DictReader(f))
    if len(rows)!=300:raise ValueError(f'Expected 300 historical rows, found {len(rows)}')
    groups=defaultdict(list); seen=set(); warnings=[]
    for r in rows:
        mid=int(r['match_id']); side=r['team_side']; recency=int(r['previous_match_recency'])
        if mid not in range(31,61) or side not in ('A','B') or recency not in range(1,6):
            raise ValueError(f'Bad match/side/recency: {mid} {side} {recency}')
        key=(mid,side,recency)
        if key in seen:raise ValueError(f'Duplicate recency record: {key}')
        seen.add(key)
        cur,ta,tb=CONTROL_MATCHES[mid]
        if (r['match_date'],r['team_a'],r['team_b'])!=(cur,ta,tb):
            raise ValueError(f'Master fixture inconsistency: {key}')
        if r['team']!=(ta if side=='A' else tb):
            raise ValueError(f'Team name or A/B inversion: {key}')
        target=date.fromisoformat(cur);previous=date.fromisoformat(r['previous_match_date'])
        edition=date.fromisoformat(r['ranking_publication_date'])
        if previous>=target:raise ValueError(f'Future/current historical match {key}')
        if not published_before_fixture(edition,previous,r['same_day_ranking_decision']):
            raise ValueError(f'Ranking not proven available before kickoff: {key}')
        if selected_edition(edition,previous,r['same_day_ranking_decision'])!=edition:
            raise ValueError(f'Not latest eligible ranking edition: {key}')
        if not r['previous_opponent'] or not r['fixture_source_url'] or not r['ranking_source_url']:
            raise ValueError(f'Missing essential evidence field: {key}')
        rank_raw=r['opponent_fifa_rank']
        if rank_raw:
            rank=int(rank_raw)
            if not (1<=rank<=211):raise ValueError(f'Impossible FIFA rank: {key}')
        else:rank=None
        wc=r['previous_wc_match_id']
        if wc:
            prev_mid=int(wc)
            if prev_mid>=mid or prev_mid not in CONTROL_MATCHES:raise ValueError(f'Invalid World Cup predecessor {key}')
            pdate,pa,pb=CONTROL_MATCHES[prev_mid]
            if pdate!=r['previous_match_date'] or r['team'] not in (pa,pb):
                raise ValueError(f'Historical WC predecessor mismatch {key}')
            other=pb if r['team']==pa else pa
            if other!=r['previous_opponent']:raise ValueError(f'Wrong historical WC opponent {key}')
            if edition!=date(2026,6,11):raise ValueError(f'World Cup history not using June 11 edition {key}')
        groups[(mid,side)].append((r,rank,previous))
    if len(groups)!=60:raise ValueError('Expected 60 match/team groupings')
    out=[]
    for mid in range(31,61):
        cur,ta,tb=CONTROL_MATCHES[mid];sub=[]; allflags=[]
        for side,team in [('A',ta),('B',tb)]:
            rs=sorted(groups[(mid,side)],key=lambda z:int(z[0]['previous_match_recency']))
            if len(rs)!=5 or [int(z[0]['previous_match_recency']) for z in rs]!=list(range(1,6)):
                raise ValueError(f'Not exactly five earlier matches {mid} {side}')
            fixture_keys=[(x[0]['previous_match_date'],x[0]['previous_opponent']) for x in rs]
            if len(set(fixture_keys))!=5:raise ValueError(f'Duplicate fixture {mid} {side}')
            dates=[z[2] for z in rs]
            if dates!=sorted(dates,reverse=True):raise ValueError(f'Wrong prior-match order {mid} {side}')
            # Embedded original master records independently identify the latest preceding WC fixture.
            possible=[(a,(b if team==c else c),z)
                       for z,(a,b,c) in CONTROL_MATCHES.items()
                       if z<mid and a<cur and team in (b,c)]
            if possible:
                prev=max(possible,key=lambda t:(t[0],t[2]))
                if dates[0]!=date.fromisoformat(prev[0]) or rs[0][0]['previous_opponent']!=prev[1]:
                    raise ValueError(f'Wrong latest previous World Cup fixture {mid} {side}')
            allflags.extend((r['manual_review_flags'] for r,_,_ in rs if r['manual_review_flags']))
            nums=[rank for _,rank,_ in rs]
            if None in nums:sub.append(None)
            else:
                total=sum(nums)
                # Decimal division avoids binary float rounding; no intermediate rounding.
                sub.append((total,Decimal(total)/Decimal(5)))
        flags=';'.join(sorted(filter(None,set(';'.join(allflags).split(';')))))
        if None in sub:
            a_sum=a_avg=b_sum=b_avg=x8=''
            status='UNRESOLVED_ESSENTIAL_RANKING_DATA'
        else:
            a_sum,a_avg=sub[0]; b_sum,b_avg=sub[1]
            x8=fmt(a_avg-b_avg);a_avg=fmt(a_avg);b_avg=fmt(b_avg)
            status='CALCULATED_REQUIRES_MANUAL_REVIEW' if flags else 'CALCULATED_SECONDARY_HISTORICAL_EVIDENCE'
        out.append(dict(match_id=mid,match_date=cur,team_a=ta,team_b=tb,
            team_a_rank_sum=a_sum,team_a_average_rank=a_avg,
            team_b_rank_sum=b_sum,team_b_average_rank=b_avg,
            x8_opponent_strength_difference=x8,calculation_status=status,
            manual_review_flags=flags,team_a_records=5,team_b_records=5,
            ranking_source_quality='June 11 positions cross-checked using two dated secondary lists; earlier published editions reused from reviewed datasets; FIFA release confirms edition publication. Individual historical FIFA position verification not complete.'))
    with open(output_path,'w',encoding='utf-8-sig',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=RESULT_FIELDS);writer.writeheader();writer.writerows(out)
    print(f'Validated {len(rows)} observations, {len(groups)} team histories, {len(out)} outputs. Warnings: {sum(bool(z["manual_review_flags"]) for z in out)}.')
    return out

if __name__=='__main__':
    n=run_policy_tests()
    if '--test' in sys.argv:
        print(f'PASS {n} ranking policy tests')
    else:calculate()
