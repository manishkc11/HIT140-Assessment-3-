"""Reproduce X7 (rest-day difference) for FIFA World Cup 2026 match IDs 11–30.

ACADEMIC INTEGRITY / RESEARCH PROVENANCE
----------------------------------------
- The match extract was copied read-only from the team's original Master Dataset.xlsx.
- Previous-match details were researched WITH AI ASSISTANCE through published
  FIFA, AFC, national-association and fixture-history pages. The research is
  recorded in X7_Matches11_30_Previous_Matches.csv (two records per match).
- Web citations and notes are *evidence to audit*, not proof created by Python.
  This script does not access websites, automatically verify match-history
  completeness, or make assumptions about unrecorded international fixtures.
- Calendar-date convention matches the first X7 batch: rest days are the
  integer number of dates separating current match and previous match,
  including the difference of endpoints (e.g., 11 Jun minus 4 Jun = 7).
- X7 = Team A rest days - Team B rest days; keep the exact master Team A/B order.
- Friendly internationals count. The most recent prior World Cup fixture counts.
- Missing or uncertain dates are NOT imputed as zero; corresponding outputs
  stay empty, and the record is flagged in validation_notes.
- This script neither reads nor modifies the Excel master workbook.

Place these files together:
    X7_Matches11_30_Master_Extract.csv
    X7_Matches11_30_Previous_Matches.csv
    X7_Matches11_30_Reproduce.py

Run: python X7_Matches11_30_Reproduce.py
Dependencies: Python standard library only.
Output: X7_Matches11_30_Calculated_Results.csv
"""
from __future__ import annotations
import csv
from datetime import date
from pathlib import Path

BASE = Path(__file__).resolve().parent
MATCH_FILE = BASE / 'X7_Matches11_30_Master_Extract.csv'
PREVIOUS_FILE = BASE / 'X7_Matches11_30_Previous_Matches.csv'
OUTPUT_FILE = BASE / 'X7_Matches11_30_Calculated_Results.csv'

OUTPUT_COLUMNS = [
    'match_id','match_date','team_a','team_b',
    'team_a_previous_date','team_a_previous_opponent','team_a_rest_days',
    'team_b_previous_date','team_b_previous_opponent','team_b_rest_days',
    'x7_rest_days_difference','team_a_source_url','team_b_source_url',
    'team_a_chronology_url','team_b_chronology_url','validation_notes'
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open('r',encoding='utf-8-sig',newline='') as handle:
        return list(csv.DictReader(handle))


def parse_iso(value: str) -> date:
    return date.fromisoformat(value)


def date_or_blank(value: str, target_date: date, record: str) -> tuple[date | None, int | None]:
    """Treat missing dates as unavailable, and reject future/current fixtures."""
    if not value.strip():
        return None, None
    dt = parse_iso(value)
    if dt >= target_date:
        raise ValueError(f'Previous fixture is not before target match: {record}: {dt}')
    return dt, (target_date - dt).days


def main() -> None:
    matches = read_csv(MATCH_FILE)
    previous = read_csv(PREVIOUS_FILE)
    actual_ids = [int(m['match_id']) for m in matches]
    if actual_ids != list(range(11, 31)):
        raise ValueError(f'Expected exactly match_id 11..30 in order: {actual_ids}')
    if len(previous) != 40:
        raise ValueError(f'Expected 40 team histories (20 matches x 2), got {len(previous)}')

    histories: dict[tuple[str,str], dict[str,str]] = {}
    for r in previous:
        key = (r['match_id'], r['side'])
        if key in histories or r['side'] not in {'A','B'}:
            raise ValueError(f'Duplicate or invalid historical record: {key}')
        if not r['source_url'].startswith('https://'):
            raise ValueError(f'Missing supporting source URL: {key}')
        if not r['chronology_url'].startswith('https://'):
            raise ValueError(f'Missing chronological verification URL: {key}')
        histories[key] = r

    output: list[dict[str,object]] = []
    for m in matches:
        mid = m['match_id']
        kickoff_date = parse_iso(m['match_date'])
        ra = histories.get((mid,'A'))
        rb = histories.get((mid,'B'))
        if ra is None or rb is None:
            raise ValueError(f'Missing Team A or Team B research record: {mid}')
        if ra['team'] != m['team_a'] or rb['team'] != m['team_b']:
            raise ValueError(f'Team or A/B ordering mismatch at {mid}')

        da, rest_a = date_or_blank(ra['previous_match_date'],kickoff_date,mid+' A')
        db, rest_b = date_or_blank(rb['previous_match_date'],kickoff_date,mid+' B')
        x7 = rest_a-rest_b if rest_a is not None and rest_b is not None else ''
        issues = []
        if da is None: issues.append('UNVERIFIED: no usable Team A previous-match date')
        if db is None: issues.append('UNVERIFIED: no usable Team B previous-match date')
        if not ra['previous_opponent'].strip() or not rb['previous_opponent'].strip():
            issues.append('UNVERIFIED: missing previous opponent')
            x7 = ''
        notes=' | '.join(n for n in [ra.get('notes',''),rb.get('notes',''),*issues] if n)
        output.append({
            'match_id':mid, 'match_date':kickoff_date.isoformat(),
            'team_a':m['team_a'],'team_b':m['team_b'],
            'team_a_previous_date':da.isoformat() if da else '',
            'team_a_previous_opponent':ra['previous_opponent'],
            'team_a_rest_days':rest_a if rest_a is not None else '',
            'team_b_previous_date':db.isoformat() if db else '',
            'team_b_previous_opponent':rb['previous_opponent'],
            'team_b_rest_days':rest_b if rest_b is not None else '',
            'x7_rest_days_difference':x7,
            'team_a_source_url':ra['source_url'],
            'team_b_source_url':rb['source_url'],
            'team_a_chronology_url':ra['chronology_url'],
            'team_b_chronology_url':rb['chronology_url'],
            'validation_notes':notes,
        })

    with OUTPUT_FILE.open('w',encoding='utf-8-sig',newline='') as handle:
        writer=csv.DictWriter(handle,fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(output)

    print('ID  Date        Team A           Team B                  A rest  B rest   X7')
    for r in output:
        diff=r['x7_rest_days_difference']
        fmt=(f'{diff:+d}' if isinstance(diff,int) else 'UNVERIFIED')
        print(f"{int(r['match_id']):>2}  {r['match_date']}  {r['team_a']:<16} {r['team_b']:<22} "
              f"{str(r['team_a_rest_days']):>6}  {str(r['team_b_rest_days']):>6}  {fmt:>5}")
    print(f'Processed {len(output)} matches, wrote {OUTPUT_FILE.name}')

if __name__ == '__main__':
    main()
