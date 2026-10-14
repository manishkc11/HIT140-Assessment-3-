"""Audit and consolidate six AI-assisted FIFA World Cup 2026 X7 research batches.

This code was prepared with AI assistance. It checks internal consistency, not
whether every cited football website is independently accurate or complete.

Folder version: put this script in the 02_X7_Rest_Days folder OR its
Final_Consolidated subfolder. Keep the six batch folders in 02_X7_Rest_Days.
The script reads CSVs from these folders and does not require ZIP archives.
"""
from __future__ import annotations
import csv
from datetime import date
from pathlib import Path
from collections import Counter
from hashlib import sha256

ROOT = Path(__file__).resolve().parent
BATCH_FOLDERS = [
    ('First_10_Matches', 'first_10_matches'),
    ('Matches_11_30', 'matches_11_30', 'matches_11_30'),
    ('Matches_31_50', 'matches_31_50'),
    ('Matches_51_70', 'matches_51_70'),
    ('Matches_71_90', 'matches_71_90'),
    ('Matches_91_104', 'matches_91_104'),
]


def find_batch_folder(aliases: tuple[str, ...]) -> Path:
    """Find a batch folder next to this script or one level above it."""
    names = {name.casefold() for name in aliases}
    for base in (ROOT, ROOT.parent):
        for item in base.iterdir():
            if item.is_dir() and item.name.casefold() in names:
                return item
    raise FileNotFoundError(
        f"Could not find folder {aliases[0]!r} in {ROOT} or {ROOT.parent}. "
        "Move the script into 02_X7_Rest_Days/Final_Consolidated "
        "and keep the batch folders in 02_X7_Rest_Days."
    )


def read_table(folder: Path, marker: str) -> list[dict[str, str]]:
    """Read one matching CSV, allowing ZIP-extracted nested subfolders."""
    hits = [
        path for path in folder.rglob('*.csv')
        if marker.casefold() in path.name.casefold()
        and not path.name.startswith('._')
        and '__MACOSX' not in path.parts
    ]
    if len(hits) != 1:
        raise ValueError(
            f"Expected one CSV containing {marker!r} inside {folder}, "
            f"found {len(hits)}: {hits}"
        )
    with hits[0].open('r', encoding='utf-8-sig', newline='') as txt:
        return list(csv.DictReader(txt))


all_masters = []
all_results = []
all_previous = []
for aliases in BATCH_FOLDERS:
    folder = find_batch_folder(aliases)
    masters = read_table(folder, 'Master_Extract')
    results = read_table(folder, 'Calculated_Results')
    previous = read_table(folder, 'Previous_Matches')
    assert len(masters) == len(results), folder
    assert len(previous) == 2 * len(results), folder
    print(f'Loaded {len(results)} matches from {folder}')
    all_masters.extend(masters)
    all_results.extend(results)
    all_previous.extend(previous)

assert len(all_results)==104 and len(all_masters)==104 and len(all_previous)==208
assert [int(r['match_id']) for r in all_results]==list(range(1,105))
assert [int(r['match_id']) for r in all_masters]==list(range(1,105))
master={int(r['match_id']):r for r in all_masters}
previous={(int(r['match_id']),r['side']):r for r in all_previous}
assert len(previous)==208

full=[];issues=[]
for result in all_results:
    mid=int(result['match_id'])
    m=master[mid]
    for k in ['match_date','team_a','team_b']:
        assert result[k]==m[k],(mid,k,result[k],m[k])
    current=date.fromisoformat(m['match_date'])
    a,b=(previous[mid,side] for side in ('A','B'))
    for side,rec in [('a',a),('b',b)]:
        assert rec['team']==m[f'team_{side}']
        assert result[f'team_{side}_previous_date']==rec['previous_match_date']
        assert result[f'team_{side}_previous_opponent']==rec['previous_opponent']
        assert result[f'team_{side}_source_url']==rec['source_url']
        prev_date=date.fromisoformat(rec['previous_match_date'])
        assert prev_date<current
        rest=(current-prev_date).days
        assert int(result[f'team_{side}_rest_days'])==rest

        # For any team that appeared in an earlier World Cup match in master,
        # ensure the latest such match is used as the predecessor.
        past=[]
        for otherid,other in master.items():
            if otherid>=mid or date.fromisoformat(other['match_date'])>=current: continue
            if rec['team']==other['team_a']: past.append((otherid,other['match_date'],other['team_b']))
            elif rec['team']==other['team_b']: past.append((otherid,other['match_date'],other['team_a']))
        if past:
            oldid,olddate,oldopp=max(past,key=lambda x:(x[1],x[0]))
            if (rec['previous_match_date'],rec['previous_opponent']) != (olddate,oldopp):
                issues.append(f'Match {mid}, team {rec["team"]}: latest WC fixture {oldid} {olddate} vs {oldopp} differs from selection {rec["previous_match_date"]} vs {rec["previous_opponent"]}')
            # Stored predecessor ID, where provided, must match earlier master.
            stored=rec.get('previous_master_match_id','')
            if stored and int(stored)!=oldid:
                issues.append(f'Match {mid}, team {rec["team"]}: stored previous ID {stored} differs from computed {oldid}')
        elif rec.get('previous_master_match_id','').strip():
            issues.append(f'Match {mid}, team {rec["team"]}: historical ID provided even though no earlier WC fixture')

    x7=int(result['team_a_rest_days'])-int(result['team_b_rest_days'])
    assert x7==int(result['x7_rest_days_difference']),(mid,x7,result['x7_rest_days_difference'])
    full.append({
        'match_id':mid,
        'match_date':m['match_date'],
        'stage':m.get('stage',''),
        'team_a':m['team_a'],'team_b':m['team_b'],
        'team_a_previous_match':a['previous_match_date'],
        'team_a_previous_opponent':a['previous_opponent'],
        'team_a_rest_days':int(result['team_a_rest_days']),
        'team_b_previous_match':b['previous_match_date'],
        'team_b_previous_opponent':b['previous_opponent'],
        'team_b_rest_days':int(result['team_b_rest_days']),
        'rest_days_diff':x7,
        'team_a_source_url':a['source_url'],'team_b_source_url':b['source_url'],
    })

if issues:
    print('ISSUES:')
    for x in issues: print('  ',x)
    raise SystemExit(f'{len(issues)} chronological issues; cannot approve consolidation')

# Export master-merge file and detailed evidence file.
for name,columns in [
 ('X7_104_Merge_Ready.csv',['match_id','rest_days_diff']),
 ('X7_104_Full_Evidence.csv',list(full[0].keys())),
]:
    path=ROOT/name
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=columns,extrasaction='ignore')
        w.writeheader(); w.writerows(full)
    print('OUTPUT',name,len(full),'rows','SHA256',sha256(path.read_bytes()).hexdigest())

vals=[r['rest_days_diff'] for r in full]
print('TOTAL:',len(vals),'zero=',vals.count(0),'negative=',sum(v<0 for v in vals),'positive=',sum(v>0 for v in vals))
print('Distribution:',dict(sorted(Counter(vals).items())))
print('Min:',min(vals),'max:',max(vals),'mean:',round(sum(vals)/len(vals),3))
print('Latest prior WC fixture check: PASS for all eligible team observations.')
print('No blank/missing date inputs or duplicate match IDs.')
