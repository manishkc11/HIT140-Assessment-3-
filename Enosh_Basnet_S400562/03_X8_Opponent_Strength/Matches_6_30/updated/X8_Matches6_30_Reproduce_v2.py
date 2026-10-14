#!/usr/bin/env python3
"""Reproduce X8 match IDs 6-30 from the VERSION-2 historical research CSV.

AI / ACADEMIC INTEGRITY
The selection and transcription of historical football fixtures, published FIFA
ranking editions, secondary archive positions, source URLs, and the preparation
of this validation/code were assisted by ChatGPT. This is NOT a FIFA database
export. The Python checks confirm structure, recorded chronology, edition
eligibility, and arithmetic; they cannot independently authenticate webpages,
confirm a roster's international-A eligibility, or prove the fixtures exhaustive.

RUN
  python X8_Matches6_30_Reproduce_v2.py
  python X8_Matches6_30_Reproduce_v2.py --test
Requires only the Python standard library. The original master workbook and
all v1 files are neither opened for writing nor modified.

SAME-DAY POLICY
- Rank editions earlier than the fixture's local date are eligible.
- An edition on the fixture's local date is eligible only with (a) a documented
  official pre-kickoff statement, (b) timestamp evidence with UTC offsets, and
  (c) publication instant strictly before actual kickoff UTC.
- If absent / after kickoff, fallback to a separately recorded *prior-edition*
  rank, with an explicit warning; otherwise leave that team's X8 unavailable.
- The FIFA article shows 11 June 2026 16:45, without a stated timezone.
  The stored 14:45 UTC timestamp interprets it as Zurich CEST (UTC+02:00).
  This timezone assumption is NOT independently established by the page;
  FIFA's explicit 'published ... before ... World Cup gets under way' text
  independently supports the substantive before-kickoff ordering.
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'X8_Matches6_30_Historical_Research_v2.csv'
OUTPUT = BASE / 'X8_Matches6_30_Calculated_Results_v2.csv'
IDS = set(range(6, 31))
EDITION_DATES = tuple(map(date.fromisoformat, (
    '2025-09-18', '2025-10-17', '2025-11-19', '2025-12-22',
    '2026-01-19', '2026-04-01', '2026-06-11',
)))
FIELDS = [
    'match_id','match_date','team_a','team_b',
    'team_a_rank_sum','team_a_average_rank',
    'team_b_rank_sum','team_b_average_rank',
    'x8_opponent_strength_difference',
    'calculation_status','manual_review_flags',
    'team_a_records','team_b_records','ranking_source_quality'
]


def utc_timestamp(text):
    if not text.strip():
        return None
    d = datetime.fromisoformat(text.strip().replace('Z', '+00:00'))
    if d.tzinfo is None or d.utcoffset() is None:
        raise ValueError('UTC timestamp requires explicit timezone: '+text)
    return d.astimezone(timezone.utc)


def eligible_edition(fixture_local_date, selected_edition_date, release_utc='',
                     kickoff_utc='', official_before_kickoff_evidence=False):
    """Return (eligible, cause). Used for both regular and same-day editions."""
    if selected_edition_date < fixture_local_date:
        return True, 'EDITION_PUBLISHED_ON_PREVIOUS_DATE'
    if selected_edition_date > fixture_local_date:
        return False, 'FUTURE_PUBLICATION_DATE'
    if not official_before_kickoff_evidence:
        return False, 'NO_OFFICIAL_SAME_DAY_PREKICKOFF_EVIDENCE'
    release, kickoff = utc_timestamp(release_utc), utc_timestamp(kickoff_utc)
    if release is None or kickoff is None:
        return False, 'SAME_DAY_TIMING_UNVERIFIED'
    if release >= kickoff:
        return False, 'RELEASE_NOT_BEFORE_KICKOFF'
    return True, 'VERIFIED_PRE_KICKOFF_SAME_DAY_PUBLICATION'


def edition_policy_tests():
    match_date = date(2026, 6, 11)
    edition_date = date(2026, 6, 11)
    release = '2026-06-11T14:45:00+00:00'
    kickoff = '2026-06-11T19:00:00+00:00'
    assert eligible_edition(match_date, edition_date, release, kickoff, True)[0]
    assert eligible_edition(match_date, edition_date, release,
                            '2026-06-11T14:00:00+00:00', True)[0] is False
    assert eligible_edition(match_date, edition_date, release, kickoff, False)[0] is False
    assert eligible_edition(match_date, edition_date, '', kickoff, True)[0] is False
    assert eligible_edition(match_date, date(2026, 4, 1))[0]
    assert eligible_edition(match_date, date(2026, 7, 20))[0] is False
    # Guadalajara match kicks off at 02:00 UTC on the NEXT date, but local date is June 11.
    assert eligible_edition(match_date, edition_date, release,
                            '2026-06-12T02:00:00+00:00', True)[0]
    # Actual rank fallback behavior: missing release evidence returns April's rank.
    sample = {'match_id':'25','team_side':'B','previous_match_recency':'1',
       'previous_match_date':'2026-06-11','match_date':'2026-06-18',
       'ranking_publication_date':'2026-06-11','previous_opponent':'Mexico',
       'ranking_source_url':'https://www.mlssoccer.com/news/fifa-world-rankings-every-team-at-the-world-cup',
       'fixture_source_url':'https://www.fifa.com/en/',
       'same_day_publication_decision':'', 'ranking_release_evidence_url':'',
       'ranking_release_utc':'', 'historical_kickoff_utc':kickoff,
       'opponent_fifa_rank':'14','preceding_edition_rank':'15',
       'preceding_edition_date':'2026-04-01',
       'preceding_edition_source_url':'https://wildstat.com/p/7001/ddate/2026-04-01'}
    fallback_rank, fallback_reason = evaluate_row(sample)
    assert fallback_rank == 15 and fallback_reason.startswith('FALLBACK_')
    sample['preceding_edition_rank'] = ''
    missing_rank, missing_reason = evaluate_row(sample)
    assert missing_rank is None and missing_reason.startswith('REJECTED_')
    return 9


def numeric_rank(value, context):
    if not value.strip():
        return None
    try:
        val = int(value)
    except ValueError as exc:
        raise ValueError(f'Non-integer FIFA ranking {context}: {value}') from exc
    if not 1 <= val <= 211:
        raise ValueError(f'Out-of-range FIFA ranking {context}: {val}')
    return val


def evaluate_row(r):
    context = (r['match_id'], r['team_side'], r['previous_match_recency'])
    fixture = date.fromisoformat(r['previous_match_date'])
    target = date.fromisoformat(r['match_date'])
    edition = date.fromisoformat(r['ranking_publication_date'])
    if not fixture < target:
        raise ValueError(f'Historical match is not prior to target {context}')
    if edition not in EDITION_DATES:
        raise ValueError(f'Unrecognised historical FIFA ranking edition {context}: {edition}')
    if not r['previous_opponent'].strip() or not r['ranking_source_url'].strip() or not r['fixture_source_url'].strip():
        raise ValueError(f'Missing required fixture/ranking source or opponent {context}')
    prior = max((d for d in EDITION_DATES if d < fixture), default=None)
    same_day_evidence = (
        r.get('same_day_publication_decision','').startswith('ACCEPT_FIFA_SAYS_BEFORE_TOURNAMENT')
        and 'inside.fifa.com' in r.get('ranking_release_evidence_url','')
        and bool(r.get('fixture_kickoff_source_url',''))
    )
    approved, reason = eligible_edition(
        fixture, edition, r.get('ranking_release_utc',''),
        r.get('historical_kickoff_utc',''), same_day_evidence)
    if approved:
        expected = edition if edition == fixture else prior
        if edition != expected:
            raise ValueError(f'Nonlatest edition {context}: selected {edition}, expected {expected}')
        rank = numeric_rank(r['opponent_fifa_rank'], context)
        return rank, reason
    # Same-day or future editions can only be replaced with a *recorded* older rank.
    # Future-dated editions never silently pass validation.
    if edition > fixture:
        raise ValueError(f'Future-dated ranking edition {context}: {edition}')
    fb_edition = r.get('preceding_edition_date','').strip()
    fb_rank = r.get('preceding_edition_rank','').strip()
    if not fb_edition or not fb_rank:
        return None, 'REJECTED_SAME_DAY_NO_FALLBACK:'+reason
    fb_date = date.fromisoformat(fb_edition)
    if fb_date != prior or not r.get('preceding_edition_source_url',''):
        raise ValueError(f'Invalid/missing preceding edition evidence {context}')
    return numeric_rank(fb_rank, context), 'FALLBACK_TO_PRECEDING_EDITION:'+reason


def read_and_validate():
    with INPUT.open('r', newline='', encoding='utf-8-sig') as f:
        data = list(csv.DictReader(f))
    if len(data) != 250:
        raise ValueError(f'Expected 250 observations, got {len(data)}')
    grouped = defaultdict(lambda: {'A': [], 'B': []})
    seen = set()
    target_fixtures = {}
    warnings = Counter()
    for r in data:
        mid = int(r['match_id']); side=r['team_side']; pos=int(r['previous_match_recency'])
        key = (mid, side, pos)
        if mid not in IDS or side not in ('A','B') or pos not in range(1,6) or key in seen:
            raise ValueError(f'Unexpected or duplicate observation: {key}')
        seen.add(key)
        if r['team'] != r['team_'+side.lower()]:
            raise ValueError(f'Team order mismatch at {key}')
        fixture_identity=(r['match_date'],r['team_a'],r['team_b'])
        if mid in target_fixtures and target_fixtures[mid] != fixture_identity:
            raise ValueError(f'Inconsistent match details for {mid}')
        target_fixtures[mid]=fixture_identity
        r['_rank'],r['_ranking_rule'] = evaluate_row(r)
        warnings[r['_ranking_rule']]+=1
        grouped[mid][side].append(r)
    if set(grouped)!=IDS:
        raise ValueError(f'Expected match IDs 6-30, got {sorted(grouped)}')
    for mid, pair in grouped.items():
        for side in ('A','B'):
            rows=sorted(pair[side],key=lambda x:int(x['previous_match_recency']))
            if len(rows)!=5 or [int(x['previous_match_recency']) for x in rows]!=list(range(1,6)):
                raise ValueError(f'Expected five uniquely numbered history rows: {mid}/{side}')
            keys=[(x['previous_match_date'], x['previous_opponent']) for x in rows]
            if len(set(keys))!=5:
                raise ValueError(f'Duplicate historical fixtures: {mid}/{side}')
            if not all(rows[i]['previous_match_date']>rows[i+1]['previous_match_date'] for i in range(4)):
                raise ValueError(f'History is not most-recent-first: {mid}/{side}')
    return grouped,warnings


def fmt(v):
    return '' if v is None else str(v.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))


def run():
    tests=edition_policy_tests()
    groups,warnings=read_and_validate()
    result=[]
    for mid in range(6,31):
        ar=groups[mid]['A'];br=groups[mid]['B'];both=ar+br
        a_total=sum((Decimal(x['_rank']) for x in ar),Decimal(0)) if all(x['_rank'] is not None for x in ar) else None
        b_total=sum((Decimal(x['_rank']) for x in br),Decimal(0)) if all(x['_rank'] is not None for x in br) else None
        a_avg=a_total/Decimal(5) if a_total is not None else None
        b_avg=b_total/Decimal(5) if b_total is not None else None
        diff=a_avg-b_avg if a_avg is not None and b_avg is not None else None
        flags={f.strip() for x in both for f in x['manual_review_flags'].split(';') if f.strip()}
        if any(x['_ranking_rule'].startswith('FALLBACK_') for x in both): flags.add('SAME_DAY_FALLBACK_APPLIED')
        if any(x['_rank'] is None for x in both):flags.add('UNRESOLVED_RANKING')
        if diff is None:status='INCOMPLETE_DO_NOT_USE'
        elif flags:status='PROVISIONAL_REQUIRES_MANUAL_REVIEW'
        else:status='CALCULATED_SECONDARY_RANKING_EVIDENCE'
        result.append({
            'match_id':str(mid),'match_date':ar[0]['match_date'],
            'team_a':ar[0]['team_a'],'team_b':ar[0]['team_b'],
            'team_a_rank_sum':str(a_total) if a_total is not None else '',
            'team_a_average_rank':fmt(a_avg),
            'team_b_rank_sum':str(b_total) if b_total is not None else '',
            'team_b_average_rank':fmt(b_avg),
            'x8_opponent_strength_difference':fmt(diff),
            'calculation_status':status,'manual_review_flags':';'.join(sorted(flags)),
            'team_a_records':str(len(ar)),'team_b_records':str(len(br)),
            'ranking_source_quality':'Published historic editions; June 11 same-day supported by FIFA pre-kickoff statement (UTC display zone inferred); most position sources are secondary; Arab Cup senior A flags retained',
        })
    with OUTPUT.open('w', newline='', encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n')
        writer.writeheader();writer.writerows(result)
    print(f'Passed {tests} same-day and general-edition policy tests')
    print(f'Validated {len(groups)} matches, {sum(len(p[s]) for p in groups.values() for s in ("A","B"))} historical observations')
    print('Decision counts:',dict(warnings))
    for r in result:
        print(f"#{r['match_id']:>2} {r['team_a']:<22} v {r['team_b']:<22} A={r['team_a_average_rank']:>6} B={r['team_b_average_rank']:>6} X8={r['x8_opponent_strength_difference']:>7}")
    assert next(r for r in result if r['match_id']=='25')['x8_opponent_strength_difference']=='-0.60'
    assert next(r for r in result if r['match_id']=='28')['x8_opponent_strength_difference']=='-18.80'
    return result

if __name__=='__main__':
    if '--test' in sys.argv:
        print(f'PASSED {edition_policy_tests()} ranking-policy tests')
    else:
        run()
