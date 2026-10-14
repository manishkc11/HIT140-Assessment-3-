#!/usr/bin/env python3
"""Reproduce X8 for World Cup 2026 master match IDs 6–30 from a research CSV.

ACADEMIC INTEGRITY / PROVENANCE
--------------------------------
The historical fixture research, manual selection of published ranking editions,
selection of source URLs, interpretation of data and initial preparation of this
script were assisted by a generative AI model (ChatGPT). The historical CSV is
an auditable research input, not an official FIFA database export. Many ranks
were transcribed from historical third-party archives. This script performs
arithmetic and structural/temporal validation only; it CANNOT authenticate
external web pages or guarantee the list of five is exhaustive.

REPRODUCTION
------------
Place this script beside X8_Matches6_30_Historical_Research.csv and run
    python X8_Matches6_30_Reproduce.py
No non-standard Python dependencies or downloads required.
The original master Excel file is never read or modified by this script.
"""
from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

BASE = Path(__file__).resolve().parent
INPUT = BASE / 'X8_Matches6_30_Historical_Research.csv'
OUTPUT = BASE / 'X8_Matches6_30_Calculated_Results.csv'
EXPECTED_IDS = set(range(6, 31))

OUTPUT_COLUMNS = [
    'match_id','match_date','team_a','team_b',
    'team_a_rank_sum','team_a_average_rank',
    'team_b_rank_sum','team_b_average_rank',
    'x8_opponent_strength_difference',
    'calculation_status','manual_review_flags',
    'team_a_records','team_b_records','ranking_source_quality'
]


def parse_date(s: str, desc: str) -> date:
    try:
        return date.fromisoformat(s)
    except (TypeError, ValueError) as exc:
        raise ValueError(f'Invalid/missing date in {desc}: {s!r}') from exc


def read_input() -> dict[int, dict[str, list[dict[str, str]]]]:
    with INPUT.open('r', newline='', encoding='utf-8-sig') as f:
        data = list(csv.DictReader(f))
    if len(data) != 250:
        raise ValueError(f'Expected 250 team-match observations; found {len(data)}')
    grouped = defaultdict(lambda: {'A': [], 'B': []})
    fixtures = {}
    seen = set()
    for n, r in enumerate(data, start=2):
        try:
            mid = int(r['match_id'])
            recency = int(r['previous_match_recency'])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'Invalid match_id/recency at CSV line {n}') from exc
        side = r['team_side']
        if mid not in EXPECTED_IDS or side not in ('A', 'B') or recency not in range(1, 6):
            raise ValueError(f'Unexpected match/side/recency at line {n}: {mid}/{side}/{recency}')
        key = (mid, side, recency)
        if key in seen:
            raise ValueError(f'Duplicate observation {key}')
        seen.add(key)
        current = parse_date(r['match_date'], f'{key} target match')
        previous = parse_date(r['previous_match_date'], f'{key} historical fixture')
        published = parse_date(r['ranking_publication_date'], f'{key} ranking publication')
        if not previous < current:
            raise ValueError(f'Historical fixture not before target match for {key}')
        if not published < previous:
            # The user's conservative rule: same-day ranking must have verified
            # pre-kickoff release time. The input contains no such time, so reject it.
            raise ValueError(f'Ranking publication not strictly before historical fixture for {key}')
        if not r['previous_opponent'].strip():
            raise ValueError(f'Missing historical opponent for {key}')
        if not r['fixture_source_url'].strip() or not r['ranking_source_url'].strip():
            raise ValueError(f'Missing source URL for {key}')
        if r['opponent_fifa_rank'].strip():
            try:
                rank = int(r['opponent_fifa_rank'])
            except ValueError as exc:
                raise ValueError(f'Non-integer ranking at {key}') from exc
            if not 1 <= rank <= 211:
                raise ValueError(f'Ranking out of range at {key}: {rank}')
        r['_recency'] = recency
        r['_previous_date'] = previous
        r['_rank'] = r['opponent_fifa_rank'].strip()
        if r['team'] != r['team_'+side.lower()]:
            raise ValueError(f'Team A/B mismatch for {key}')
        target_key = (r['match_date'], r['team_a'], r['team_b'])
        if mid in fixtures and fixtures[mid] != target_key:
            raise ValueError(f'Inconsistent target-match identity for ID {mid}')
        fixtures[mid] = target_key
        grouped[mid][side].append(r)
    if set(grouped) != EXPECTED_IDS:
        raise ValueError(f'Missing / additional match IDs: {sorted(set(grouped) ^ EXPECTED_IDS)}')
    for mid, sides in grouped.items():
        for side in ('A', 'B'):
            group = sorted(sides[side], key=lambda r: r['_recency'])
            if len(group) != 5 or [r['_recency'] for r in group] != [1, 2, 3, 4, 5]:
                raise ValueError(f'Missing or duplicate recency 1–5 for {mid}/{side}')
            if len({(r['previous_match_date'], r['previous_opponent']) for r in group}) != 5:
                raise ValueError(f'Duplicate historical fixture date+opponent for {mid}/{side}')
            if not all(group[i]['_previous_date'] > group[i+1]['_previous_date'] for i in range(4)):
                raise ValueError(f'Non-descending chronological order for {mid}/{side}')
    return dict(grouped)


def average_and_sum(records: list[dict[str, str]]):
    if any(not r['_rank'] for r in records):
        return None, None
    total = sum((Decimal(r['_rank']) for r in records), Decimal('0'))
    return total, total / Decimal(5)


def fmt_decimal(v: Decimal | None, digits: str = '0.00') -> str:
    if v is None:
        return ''
    return str(v.quantize(Decimal(digits), rounding=ROUND_HALF_UP))


def export():
    data = read_input()
    result = []
    for mid in range(6, 31):
        a = sorted(data[mid]['A'], key=lambda r: r['_recency'])
        b = sorted(data[mid]['B'], key=lambda r: r['_recency'])
        a_sum, a_avg = average_and_sum(a)
        b_sum, b_avg = average_and_sum(b)
        all_rows = a+b
        issues = sorted({flag.strip() for r in all_rows
                         for flag in r['manual_review_flags'].split(';') if flag.strip()})
        if any(r['ranking_verification_status'] == 'UNVERIFIED' for r in all_rows):
            issues.append('UNVERIFIED_HISTORICAL_RANKING')
        if a_avg is None or b_avg is None or 'RANKING_CONFLICT_WITH_V2' in issues:
            status = 'INCOMPLETE_DO_NOT_USE'
            diff = None
        else:
            diff = a_avg-b_avg   # NO intermediate rounding
            status = 'PROVISIONAL_REQUIRES_MANUAL_REVIEW' if issues else 'CALCULATED_SECONDARY_RANKING_EVIDENCE'
        r = dict(match_id=str(mid), match_date=a[0]['match_date'],
                 team_a=a[0]['team_a'], team_b=a[0]['team_b'],
                 team_a_rank_sum=str(a_sum) if a_sum is not None else '',
                 team_a_average_rank=fmt_decimal(a_avg),
                 team_b_rank_sum=str(b_sum) if b_sum is not None else '',
                 team_b_average_rank=fmt_decimal(b_avg),
                 x8_opponent_strength_difference=fmt_decimal(diff),
                 calculation_status=status, manual_review_flags=';'.join(sorted(set(issues))),
                 team_a_records='5', team_b_records='5',
                 ranking_source_quality='Historical published editions, mostly secondary archives; not universal direct FIFA row-level verification')
        result.append(r)
    with OUTPUT.open('w', encoding='utf-8', newline='') as f:
        writer=csv.DictWriter(f, fieldnames=OUTPUT_COLUMNS, lineterminator='\n')
        writer.writeheader()
        writer.writerows(result)
    print(f'Wrote {OUTPUT.name}: {len(result)} records')
    for r in result:
        print(f"{r['match_id']:>2} {r['team_a']:<23} v {r['team_b']:<23} "
              f"{r['team_a_average_rank']:>6} {r['team_b_average_rank']:>6} "
              f"X8={r['x8_opponent_strength_difference']:>7} {r['calculation_status']}")
    return result

if __name__ == '__main__':
    export()
