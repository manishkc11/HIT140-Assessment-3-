#!/usr/bin/env python3
"""Reproduce X8 for FIFA World Cup match IDs 61-90.

ACADEMIC INTEGRITY / PROVENANCE
ChatGPT assisted historical-match research reuse, source selection, transcription
of previously reviewed FIFA-ranking positions, code generation and validation.
Previous fixtures and rankings come from project research, NOT a FIFA database
export. This program validates internally recorded facts, chronology, edition
policy and arithmetic; it cannot independently authenticate external websites,
prove completeness of historical schedules or certify senior-A selection status.

Standalone use:
    python X8_Matches61_90_Reproduce.py --test
    python X8_Matches61_90_Reproduce.py

Requires only the adjacent Historical_Research.csv and Python standard library.
The embedded snapshot of previous master-match details, X7 predecessors and
previously reviewed (opponent, ranking edition) pairs is for consistency checks.
Original Excel workbook and earlier batches are never written to.
"""
from __future__ import annotations
import csv
import json
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/'X8_Matches61_90_Historical_Research.csv'
OUTPUT=ROOT/'X8_Matches61_90_Calculated_Results.csv'
FIFA_BEFORE_KICKOFF='https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola'
EDITION_DATES=[date.fromisoformat(x) for x in ('2025-09-18','2025-10-17','2025-11-19','2025-12-22','2026-01-19','2026-04-01','2026-06-11')]
IDS=set(range(61,91))
FIELDS=['match_id','match_date','team_a','team_b','team_a_rank_sum','team_a_average_rank','team_b_rank_sum','team_b_average_rank','x8_opponent_strength_difference','calculation_status','manual_review_flags','team_a_records','team_b_records','ranking_source_quality']
# IMPORTANT: The embedded reference block is GENERATED from already-reviewed
# project datasets and is independent of the new research CSV. It does not
# substitute for an external FIFA source check.
EMBEDDED_REFERENCE_JSON = r'''{"master":{"1":{"match_date":"2026-06-11","team_a":"Mexico","team_b":"South Africa"},"2":{"match_date":"2026-06-11","team_a":"Korea Republic","team_b":"Czechia"},"3":{"match_date":"2026-06-12","team_a":"Canada","team_b":"Bosnia and Herzegovina"},"4":{"match_date":"2026-06-12","team_a":"USA","team_b":"Paraguay"},"5":{"match_date":"2026-06-13","team_a":"Haiti","team_b":"Scotland"},"6":{"match_date":"2026-06-13","team_a":"Australia","team_b":"Türkiye"},"7":{"match_date":"2026-06-13","team_a":"Brazil","team_b":"Morocco"},"8":{"match_date":"2026-06-13","team_a":"Qatar","team_b":"Switzerland"},"9":{"match_date":"2026-06-14","team_a":"Côte d'Ivoire","team_b":"Ecuador"},"10":{"match_date":"2026-06-14","team_a":"Germany","team_b":"Curaçao"},"11":{"match_date":"2026-06-14","team_a":"Netherlands","team_b":"Japan"},"12":{"match_date":"2026-06-14","team_a":"Sweden","team_b":"Tunisia"},"13":{"match_date":"2026-06-15","team_a":"Saudi Arabia","team_b":"Uruguay"},"14":{"match_date":"2026-06-15","team_a":"Spain","team_b":"Cabo Verde"},"15":{"match_date":"2026-06-15","team_a":"IR Iran","team_b":"New Zealand"},"16":{"match_date":"2026-06-15","team_a":"Belgium","team_b":"Egypt"},"17":{"match_date":"2026-06-16","team_a":"France","team_b":"Senegal"},"18":{"match_date":"2026-06-16","team_a":"Iraq","team_b":"Norway"},"19":{"match_date":"2026-06-16","team_a":"Argentina","team_b":"Algeria"},"20":{"match_date":"2026-06-16","team_a":"Austria","team_b":"Jordan"},"21":{"match_date":"2026-06-17","team_a":"Ghana","team_b":"Panama"},"22":{"match_date":"2026-06-17","team_a":"England","team_b":"Croatia"},"23":{"match_date":"2026-06-17","team_a":"Portugal","team_b":"Congo DR"},"24":{"match_date":"2026-06-17","team_a":"Uzbekistan","team_b":"Colombia"},"25":{"match_date":"2026-06-18","team_a":"Czechia","team_b":"South Africa"},"26":{"match_date":"2026-06-18","team_a":"Switzerland","team_b":"Bosnia and Herzegovina"},"27":{"match_date":"2026-06-18","team_a":"Canada","team_b":"Qatar"},"28":{"match_date":"2026-06-18","team_a":"Mexico","team_b":"Korea Republic"},"29":{"match_date":"2026-06-19","team_a":"Brazil","team_b":"Haiti"},"30":{"match_date":"2026-06-19","team_a":"Scotland","team_b":"Morocco"},"31":{"match_date":"2026-06-19","team_a":"Türkiye","team_b":"Paraguay"},"32":{"match_date":"2026-06-19","team_a":"USA","team_b":"Australia"},"33":{"match_date":"2026-06-20","team_a":"Germany","team_b":"Côte d'Ivoire"},"34":{"match_date":"2026-06-20","team_a":"Ecuador","team_b":"Curaçao"},"35":{"match_date":"2026-06-20","team_a":"Netherlands","team_b":"Sweden"},"36":{"match_date":"2026-06-20","team_a":"Tunisia","team_b":"Japan"},"37":{"match_date":"2026-06-21","team_a":"Uruguay","team_b":"Cabo Verde"},"38":{"match_date":"2026-06-21","team_a":"Spain","team_b":"Saudi Arabia"},"39":{"match_date":"2026-06-21","team_a":"Belgium","team_b":"IR Iran"},"40":{"match_date":"2026-06-21","team_a":"New Zealand","team_b":"Egypt"},"41":{"match_date":"2026-06-22","team_a":"Norway","team_b":"Senegal"},"42":{"match_date":"2026-06-22","team_a":"France","team_b":"Iraq"},"43":{"match_date":"2026-06-22","team_a":"Argentina","team_b":"Austria"},"44":{"match_date":"2026-06-22","team_a":"Jordan","team_b":"Algeria"},"45":{"match_date":"2026-06-23","team_a":"England","team_b":"Ghana"},"46":{"match_date":"2026-06-23","team_a":"Panama","team_b":"Croatia"},"47":{"match_date":"2026-06-23","team_a":"Portugal","team_b":"Uzbekistan"},"48":{"match_date":"2026-06-23","team_a":"Colombia","team_b":"Congo DR"},"49":{"match_date":"2026-06-24","team_a":"Scotland","team_b":"Brazil"},"50":{"match_date":"2026-06-24","team_a":"Morocco","team_b":"Haiti"},"51":{"match_date":"2026-06-24","team_a":"Switzerland","team_b":"Canada"},"52":{"match_date":"2026-06-24","team_a":"Bosnia and Herzegovina","team_b":"Qatar"},"53":{"match_date":"2026-06-24","team_a":"Czechia","team_b":"Mexico"},"54":{"match_date":"2026-06-24","team_a":"South Africa","team_b":"Korea Republic"},"55":{"match_date":"2026-06-25","team_a":"Curaçao","team_b":"Côte d'Ivoire"},"56":{"match_date":"2026-06-25","team_a":"Ecuador","team_b":"Germany"},"57":{"match_date":"2026-06-25","team_a":"Japan","team_b":"Sweden"},"58":{"match_date":"2026-06-25","team_a":"Tunisia","team_b":"Netherlands"},"59":{"match_date":"2026-06-25","team_a":"Türkiye","team_b":"USA"},"60":{"match_date":"2026-06-25","team_a":"Paraguay","team_b":"Australia"},"61":{"match_date":"2026-06-26","team_a":"Norway","team_b":"France"},"62":{"match_date":"2026-06-26","team_a":"Senegal","team_b":"Iraq"},"63":{"match_date":"2026-06-26","team_a":"Egypt","team_b":"IR Iran"},"64":{"match_date":"2026-06-26","team_a":"New Zealand","team_b":"Belgium"},"65":{"match_date":"2026-06-26","team_a":"Cabo Verde","team_b":"Saudi Arabia"},"66":{"match_date":"2026-06-26","team_a":"Uruguay","team_b":"Spain"},"67":{"match_date":"2026-06-27","team_a":"Panama","team_b":"England"},"68":{"match_date":"2026-06-27","team_a":"Croatia","team_b":"Ghana"},"69":{"match_date":"2026-06-27","team_a":"Algeria","team_b":"Austria"},"70":{"match_date":"2026-06-27","team_a":"Jordan","team_b":"Argentina"},"71":{"match_date":"2026-06-27","team_a":"Colombia","team_b":"Portugal"},"72":{"match_date":"2026-06-27","team_a":"Congo DR","team_b":"Uzbekistan"},"73":{"match_date":"2026-06-28","team_a":"South Africa","team_b":"Canada"},"74":{"match_date":"2026-06-29","team_a":"Germany","team_b":"Paraguay"},"75":{"match_date":"2026-06-29","team_a":"Netherlands","team_b":"Morocco"},"76":{"match_date":"2026-06-29","team_a":"Brazil","team_b":"Japan"},"77":{"match_date":"2026-06-30","team_a":"France","team_b":"Sweden"},"78":{"match_date":"2026-06-30","team_a":"Côte d'Ivoire","team_b":"Norway"},"79":{"match_date":"2026-06-30","team_a":"Mexico","team_b":"Ecuador"},"80":{"match_date":"2026-07-01","team_a":"England","team_b":"Congo DR"},"81":{"match_date":"2026-07-01","team_a":"USA","team_b":"Bosnia and Herzegovina"},"82":{"match_date":"2026-07-01","team_a":"Belgium","team_b":"Senegal"},"83":{"match_date":"2026-07-02","team_a":"Portugal","team_b":"Croatia"},"84":{"match_date":"2026-07-02","team_a":"Spain","team_b":"Austria"},"85":{"match_date":"2026-07-02","team_a":"Switzerland","team_b":"Algeria"},"86":{"match_date":"2026-07-03","team_a":"Argentina","team_b":"Cabo Verde"},"87":{"match_date":"2026-07-03","team_a":"Colombia","team_b":"Ghana"},"88":{"match_date":"2026-07-03","team_a":"Australia","team_b":"Egypt"},"89":{"match_date":"2026-07-04","team_a":"Paraguay","team_b":"France"},"90":{"match_date":"2026-07-04","team_a":"Canada","team_b":"Morocco"}},"rank_reference":{"Serbia|2026-04-01":39,"Australia|2026-04-01":27,"Ghana|2026-04-01":74,"Belgium|2026-01-19":9,"Portugal|2026-01-19":6,"Jamaica|2026-04-01":71,"Nicaragua|2026-04-01":131,"Panama|2026-01-19":33,"Cameroon|2025-12-22":57,"El Salvador|2026-04-01":100,"Trinidad and Tobago|2026-04-01":102,"Austria|2026-01-19":24,"Côte d'Ivoire|2026-01-19":37,"Ghana|2025-10-17":73,"Guatemala|2026-04-01":96,"Kosovo|2026-04-01":78,"Denmark|2026-01-19":21,"Republic of Ireland|2026-01-19":59,"Gibraltar|2025-10-17":200,"Republic of Ireland|2026-04-01":59,"Uzbekistan|2026-04-01":50,"Tunisia|2026-01-19":47,"Iceland|2026-01-19":74,"Guatemala|2025-12-22":94,"Panama|2026-04-01":33,"North Macedonia|2026-04-01":67,"Italy|2026-01-19":13,"Wales|2026-01-19":35,"Austria|2025-10-17":24,"Germany|2026-04-01":10,"Senegal|2026-04-01":14,"Uruguay|2025-10-17":15,"Morocco|2026-01-19":8,"Greece|2026-01-19":46,"Mexico|2025-10-17":14,"USA|2025-10-17":16,"Peru|2026-04-01":53,"New Zealand|2026-04-01":85,"Nicaragua|2025-10-17":133,"Bolivia|2026-04-01":76,"Curaçao|2026-04-01":82,"Japan|2026-01-19":19,"Denmark|2025-10-17":20,"Switzerland|2026-04-01":19,"Mexico|2026-04-01":15,"Curaçao|2026-01-19":81,"Cameroon|2026-01-19":45,"Colombia|2025-10-17":13,"Venezuela|2026-04-01":49,"Kosovo|2026-01-19":79,"Romania|2026-01-19":49,"Spain|2025-10-17":1,"Egypt|2026-04-01":29,"Croatia|2026-01-19":11,"France|2026-01-19":3,"Tunisia|2025-10-17":43,"Norway|2026-04-01":31,"Madagascar|2026-04-01":104,"Burundi|2026-04-01":142,"Paraguay|2026-01-19":40,"Ecuador|2026-01-19":23,"Tunisia|2025-11-19":40,"Syria|2025-11-19":87,"Palestine|2025-11-19":96,"Jordan|2026-04-01":63,"Norway|2026-01-19":32,"Germany|2026-01-19":10,"Kosovo|2025-10-17":84,"France|2026-04-01":1,"Scotland|2026-01-19":38,"Korea Republic|2026-01-19":22,"Egypt|2025-12-22":35,"Burkina Faso|2025-12-22":62,"Saudi Arabia|2026-04-01":61,"Netherlands|2026-01-19":7,"New Zealand|2025-10-17":85,"USA|2026-04-01":16,"Finland|2026-04-01":73,"Ghana|2026-01-19":72,"Switzerland|2026-01-19":18,"Slovakia|2025-10-17":46,"Aruba|2026-04-01":189,"Scotland|2026-04-01":43,"Australia|2026-01-19":27,"China|2026-01-19":93,"Jamaica|2025-10-17":68,"Algeria|2026-04-01":28,"Lithuania|2025-10-17":146,"Iceland|2026-04-01":75,"England|2026-01-19":4,"Bolivia|2025-10-17":76,"Greece|2026-04-01":47,"Poland|2026-01-19":34,"Ukraine|2026-01-19":30,"Slovenia|2025-10-17":51,"Belgium|2026-04-01":9,"Austria|2026-04-01":24,"Canada|2026-01-19":29,"Haiti|2026-01-19":83,"Mali|2025-12-22":53,"Puerto Rico|2026-04-01":156,"Ecuador|2026-04-01":23,"Serbia|2026-01-19":39,"Egypt|2026-01-19":31,"Algeria|2026-01-19":28,"Uzbekistan|2025-09-18":54,"Iraq|2026-04-01":57,"Türkiye|2025-10-17":26,"Bermuda|2026-04-01":166,"Finland|2026-01-19":75,"Chile|2026-01-19":55,"Egypt|2025-10-17":32,"Mali|2026-04-01":52,"Gambia|2026-04-01":116,"Costa Rica|2026-01-19":51,"Nigeria|2026-01-19":26,"Uzbekistan|2025-10-17":55,"England|2026-04-01":4,"Haiti|2026-04-01":83,"Ecuador|2025-10-17":23,"Tunisia|2026-04-01":44,"Croatia|2026-04-01":11,"Mexico|2026-01-19":16,"USA|2026-01-19":15,"Liechtenstein|2025-10-17":206,"Brazil|2026-04-01":6,"Russia|2026-04-01":36,"Spain|2026-01-19":1,"Saudi Arabia|2026-01-19":61,"Nigeria|2025-12-22":38,"Northern Ireland|2026-04-01":70,"Côte d'Ivoire|2026-04-01":34,"Colombia|2026-01-19":14,"Brazil|2026-01-19":5,"Azerbaijan|2025-10-17":123,"Gambia|2026-01-19":116,"Peru|2026-01-19":53,"Morocco|2025-12-22":11,"Spain|2026-04-01":2,"Andorra|2026-04-01":173,"Bolivia|2026-01-19":76,"Jordan|2025-11-19":66,"Morocco|2026-04-01":8,"Sweden|2026-04-01":38,"Italy|2025-10-17":9,"Honduras|2026-04-01":66,"Zambia|2026-01-19":91,"Mauritania|2026-01-19":115,"Angola|2025-10-17":89,"Netherlands|2026-04-01":7,"Uruguay|2026-01-19":17,"Guatemala|2026-01-19":94,"Bosnia and Herzegovina|2025-10-17":75,"Cyprus|2025-10-17":125,"Colombia|2026-04-01":13,"Morocco|2025-11-19":11,"Wales|2026-04-01":37,"Korea Republic|2025-10-17":22,"Bosnia and Herzegovina|2026-04-01":65,"Dominican Republic|2026-04-01":143,"South Africa|2026-01-19":60,"Costa Rica|2026-04-01":51,"Albania|2025-10-17":61,"Slovenia|2026-04-01":58,"Montenegro|2025-10-17":81,"Nigeria|2026-04-01":26,"Chile|2026-04-01":54,"Armenia|2025-10-17":104,"Denmark|2026-04-01":20,"Jamaica|2026-01-19":70,"Bermuda|2026-01-19":169,"Algeria|2025-12-22":34,"Canada|2026-04-01":30,"Venezuela|2026-01-19":50,"Gabon|2026-01-19":86,"IR Iran|2025-10-17":21,"Australia|2025-10-17":25,"Korea Republic|2026-06-11":25,"Mexico|2026-06-11":14,"Qatar|2026-06-11":56,"Canada|2026-06-11":30,"Bosnia and Herzegovina|2026-06-11":64,"Switzerland|2026-06-11":19,"South Africa|2026-06-11":60,"Czechia|2026-06-11":40,"Morocco|2026-06-11":7,"Scotland|2026-06-11":42,"Haiti|2026-06-11":83,"Brazil|2026-06-11":6,"Australia|2026-06-11":27,"USA|2026-06-11":17,"Paraguay|2026-06-11":41,"Türkiye|2026-06-11":22,"Curaçao|2026-06-11":82,"Ecuador|2026-06-11":23,"Côte d'Ivoire|2026-06-11":33,"Germany|2026-06-11":10,"Japan|2026-06-11":18,"Tunisia|2026-06-11":45,"Sweden|2026-06-11":38,"Netherlands|2026-06-11":8,"Saudi Arabia|2026-06-11":61,"Spain|2026-06-11":2,"Cabo Verde|2026-06-11":67,"Uruguay|2026-06-11":16,"Egypt|2026-06-11":29,"New Zealand|2026-06-11":85,"IR Iran|2026-06-11":20,"Belgium|2026-06-11":9,"Iraq|2026-06-11":57,"France|2026-06-11":3,"Senegal|2026-06-11":15,"Norway|2026-06-11":31,"Algeria|2026-06-11":28,"Jordan|2026-06-11":63,"Austria|2026-06-11":24,"Argentina|2026-06-11":1,"Croatia|2026-06-11":11,"Panama|2026-06-11":34,"Ghana|2026-06-11":73,"England|2026-06-11":4,"Congo DR|2026-06-11":46,"Colombia|2026-06-11":13,"Uzbekistan|2026-06-11":50,"Portugal|2026-06-11":5},"x7":{"61:A":["2026-06-22","Senegal",41],"61:B":["2026-06-22","Iraq",42],"62:A":["2026-06-22","Norway",41],"62:B":["2026-06-22","France",42],"63:A":["2026-06-21","New Zealand",40],"63:B":["2026-06-21","Belgium",39],"64:A":["2026-06-21","Egypt",40],"64:B":["2026-06-21","IR Iran",39],"65:A":["2026-06-21","Uruguay",37],"65:B":["2026-06-21","Spain",38],"66:A":["2026-06-21","Cabo Verde",37],"66:B":["2026-06-21","Saudi Arabia",38],"67:A":["2026-06-23","Croatia",46],"67:B":["2026-06-23","Ghana",45],"68:A":["2026-06-23","Panama",46],"68:B":["2026-06-23","England",45],"69:A":["2026-06-22","Jordan",44],"69:B":["2026-06-22","Argentina",43],"70:A":["2026-06-22","Algeria",44],"70:B":["2026-06-22","Austria",43],"71:A":["2026-06-23","Congo DR",48],"71:B":["2026-06-23","Uzbekistan",47],"72:A":["2026-06-23","Colombia",48],"72:B":["2026-06-23","Portugal",47],"73:A":["2026-06-24","Korea Republic",54],"73:B":["2026-06-24","Switzerland",51],"74:A":["2026-06-25","Ecuador",56],"74:B":["2026-06-25","Australia",60],"75:A":["2026-06-25","Tunisia",58],"75:B":["2026-06-24","Haiti",50],"76:A":["2026-06-24","Scotland",49],"76:B":["2026-06-25","Sweden",57],"77:A":["2026-06-26","Norway",61],"77:B":["2026-06-25","Japan",57],"78:A":["2026-06-25","Curaçao",55],"78:B":["2026-06-26","France",61],"79:A":["2026-06-24","Czechia",53],"79:B":["2026-06-25","Germany",56],"80:A":["2026-06-27","Panama",67],"80:B":["2026-06-27","Uzbekistan",72],"81:A":["2026-06-25","Türkiye",59],"81:B":["2026-06-24","Qatar",52],"82:A":["2026-06-26","New Zealand",64],"82:B":["2026-06-26","Iraq",62],"83:A":["2026-06-27","Colombia",71],"83:B":["2026-06-27","Ghana",68],"84:A":["2026-06-26","Uruguay",66],"84:B":["2026-06-27","Algeria",69],"85:A":["2026-06-24","Canada",51],"85:B":["2026-06-27","Austria",69],"86:A":["2026-06-27","Jordan",70],"86:B":["2026-06-26","Saudi Arabia",65],"87:A":["2026-06-27","Portugal",71],"87:B":["2026-06-27","Croatia",68],"88:A":["2026-06-25","Paraguay",60],"88:B":["2026-06-26","IR Iran",63],"89:A":["2026-06-29","Germany",74],"89:B":["2026-06-30","Sweden",77],"90:A":["2026-06-28","South Africa",73],"90:B":["2026-06-29","Netherlands",75]}}'''
REFERENCES=json.loads(EMBEDDED_REFERENCE_JSON)
MASTER=REFERENCES['master']
RANK_REFERENCE=REFERENCES['rank_reference']
X7_REFERENCE=REFERENCES['x7']

def rank_edition_allowed(fixture_date, edition_date, official_before_opening=False):
    """Select only published ranking editions available before kickoff.

    FIFA states its 11-Jun edition was published *hours before* the opening
    World Cup match. The exact timestamp's displayed timezone isn't explicit,
    so acceptance of the World Cup opening-day ranking is grounded in FIFA's
    textual before-opening assertion rather than invented UTC precision.
    Other same-day ranking entries are REJECTED without separate proof.
    """
    if edition_date>fixture_date:return False,'REJECT_FUTURE_EDITION'
    if edition_date==fixture_date:
        if fixture_date==date(2026,6,11) and official_before_opening:
            return True,'FIFA_OFFICIAL_PRE_OPENING_SAME_DAY_CONFIRMED'
        return False,'REJECT_UNVERIFIED_SAME_DAY_RELEASE'
    return True,'EARLIER_PUBLISHED_EDITION'

def policy_tests():
    assert rank_edition_allowed(date(2026,6,11),date(2026,6,11),True)[0]
    assert not rank_edition_allowed(date(2026,6,11),date(2026,6,11),False)[0]
    assert rank_edition_allowed(date(2026,6,12),date(2026,6,11))[0]
    assert not rank_edition_allowed(date(2026,6,1),date(2026,6,11))[0]
    assert not rank_edition_allowed(date(2026,6,15),date(2026,7,20))[0]
    assert rank_edition_allowed(date(2026,5,30),date(2026,4,1))[0]
    assert not rank_edition_allowed(date(2026,4,1),date(2026,4,1),False)[0]
    return 7

def check_latest_date_edition(r):
    fixture=date.fromisoformat(r['previous_match_date'])
    publication=date.fromisoformat(r['ranking_publication_date'])
    if publication not in EDITION_DATES:
        raise ValueError('Unexpected historical FIFA ranking publication: '+r['ranking_publication_date'])
    same_day=(r['same_day_ranking_decision']=='FIFA_OFFICIAL_RELEASE_BEFORE_OPENING_KICKOFF')
    allowed,reason=rank_edition_allowed(fixture,publication,same_day)
    if not allowed:raise ValueError(f'Not eligible ranking at match {r["match_id"]} {r["team"]}: {reason}')
    eligible=[d for d in EDITION_DATES if d<fixture or (d==fixture and fixture==date(2026,6,11) and same_day)]
    if not eligible or publication!=max(eligible):
        raise ValueError(f'Non-latest edition for {r["team"]} vs {r["previous_opponent"]} {fixture}: {publication}')
    if same_day and r.get('ranking_official_edition_announcement_url','')!=FIFA_BEFORE_KICKOFF:
        raise ValueError('Unsupported same-day FIFA release source: '+r['match_id'])
    return reason

def validate_and_group(rows):
    if len(rows)!=300:raise ValueError(f'Expected 300 observations; received {len(rows)}')
    groups=defaultdict(lambda:{'A':[],'B':[]})
    seen=set(); previous_identity={}; flags=set();wc_checks=0;x7_checks=0
    for r in rows:
        mid=int(r['match_id']); side=r['team_side'];recency=int(r['previous_match_recency'])
        if mid not in IDS or side not in ('A','B') or recency not in range(1,6):
            raise ValueError('Unexpected target/side/recency: '+str((mid,side,recency)))
        k=(mid,side,recency)
        if k in seen:raise ValueError('Repeated recency key: '+str(k))
        seen.add(k)
        m=MASTER[str(mid)]
        if (r['match_date'],r['team_a'],r['team_b'])!=(m['match_date'],m['team_a'],m['team_b']):
            raise ValueError('Original master ID/date/team order mismatch: '+str(mid))
        if r['team']!=m['team_a' if side=='A' else 'team_b']:
            raise ValueError('Mismatch with designated Team A or B: '+str(k))
        if date.fromisoformat(r['previous_match_date']) >= date.fromisoformat(r['match_date']):
            raise ValueError('Current or future historical match: '+str(k))
        if not r['previous_opponent'] or not r['fixture_source_url'] or not r['ranking_source_url']:
            raise ValueError('Missing opponent or supporting source: '+str(k))
        check_latest_date_edition(r)
        pair=(r['previous_opponent'],r['ranking_publication_date'])
        if r['opponent_fifa_rank'].strip():
            try:rank=int(r['opponent_fifa_rank'])
            except ValueError:raise ValueError('Non-integer ranking '+str(k))
            if not 1<=rank<=211:raise ValueError('Ranking outside 1-211: '+str(k))
            previous_rank=RANK_REFERENCE.get('|'.join(pair))
            if previous_rank is not None and rank!=previous_rank:
                raise ValueError(f'Cross-batch ranking conflict at {k}: {pair} {rank} vs {previous_rank}')
            if pair==('Scotland','2026-06-11') and rank!=42:
                raise ValueError('Scotland June 2026 must be rank 42')
            r['_rank']=rank
        else:
            r['_rank']=None
            flags.add('MISSING_HISTORICAL_RANKING')
        pmi=r.get('previous_wc_match_id','').strip()
        if pmi:
            j=int(pmi)
            if j>=mid or str(j) not in MASTER:raise ValueError('Bad prior WC match reference: '+str(k))
            old=MASTER[str(j)]
            if r['team'] not in (old['team_a'],old['team_b']):raise ValueError('Team absent from referenced match: '+str(k))
            opp=old['team_b'] if old['team_a']==r['team'] else old['team_a']
            if opp!=r['previous_opponent'] or old['match_date']!=r['previous_match_date']:
                raise ValueError('Prior WC date/opponent inconsistent with original master: '+str(k))
            wc_checks+=1
        groups[mid][side].append(r)
        for flag in r.get('manual_review_flags','').split(';'):
            if flag.strip():flags.add(flag.strip())
    if set(groups)!=IDS:raise ValueError('Missing / extra target match IDs')
    for mid,pair in groups.items():
        for side in ('A','B'):
            a=sorted(pair[side],key=lambda r:int(r['previous_match_recency']))
            if len(a)!=5 or [int(x['previous_match_recency']) for x in a]!=[1,2,3,4,5]:
                raise ValueError('Incomplete history '+str((mid,side)))
            keys=[(r['previous_match_date'],r['previous_opponent']) for r in a]
            if len(set(keys))!=5:raise ValueError('Duplicate historical fixtures '+str((mid,side)))
            dates=[r['previous_match_date'] for r in a]
            if not all(dates[i]>dates[i+1] for i in range(4)):
                raise ValueError('Wrong recency chronology: '+str((mid,side)))
            # A complete World Cup master is embedded: check none was skipped.
            complete=[]
            team=a[0]['team'];cutoff=MASTER[str(mid)]['match_date']
            for j in range(1,mid):
                mr=MASTER[str(j)]
                if mr['match_date']<cutoff and team in (mr['team_a'],mr['team_b']):
                    complete.append((mr['match_date'],j))
            complete.sort(reverse=True)
            chosen_wc=[int(r['previous_wc_match_id']) for r in a if r['previous_wc_match_id']]
            expected_wc=[j for _,j in complete[:5]]
            if chosen_wc!=expected_wc:
                raise ValueError('One or more eligible earlier World Cup fixtures omitted '+str((mid,side)))
            prev=a[0];xref=X7_REFERENCE[f'{mid}:{side}']
            if (prev['previous_match_date'],prev['previous_opponent'],int(prev.get('previous_wc_match_id') or 0))!=tuple(xref):
                raise ValueError('X7 latest predecessor disagreement '+str((mid,side)))
            x7_checks+=1
    return groups,flags,wc_checks,x7_checks

def money(n):return '' if n is None else f'{n.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP):.2f}'

def compute(rows):
    groups,flags,wc_checks,x7_checks=validate_and_group(rows)
    out=[]
    for mid in range(61,91):
        pair=groups[mid];a=pair['A'];b=pair['B'];both=a+b
        asum=sum((Decimal(r['_rank']) for r in a),Decimal(0)) if all(r['_rank'] is not None for r in a) else None
        bsum=sum((Decimal(r['_rank']) for r in b),Decimal(0)) if all(r['_rank'] is not None for r in b) else None
        av=asum/Decimal(5) if asum is not None else None
        bv=bsum/Decimal(5) if bsum is not None else None
        val=av-bv if av is not None and bv is not None else None
        review=sorted({flag.strip() for r in both for flag in r.get('manual_review_flags','').split(';') if flag.strip()})
        if val is None:review.append('INCOMPLETE_RANKING_RESEARCH');status='INCOMPLETE_DO_NOT_USE'
        elif review:status='PROVISIONAL_REQUIRES_MANUAL_REVIEW'
        else:status='CALCULATED_SECONDARY_RANKING_EVIDENCE_NOT_FULLY_FIFA_VERIFIED'
        out.append({'match_id':str(mid),'match_date':a[0]['match_date'],'team_a':a[0]['team_a'],'team_b':a[0]['team_b'],
          'team_a_rank_sum':str(asum) if asum is not None else '', 'team_a_average_rank':money(av),
          'team_b_rank_sum':str(bsum) if bsum is not None else '', 'team_b_average_rank':money(bv),
          'x8_opponent_strength_difference':money(val),'calculation_status':status,
          'manual_review_flags':';'.join(review),'team_a_records':str(len(a)),'team_b_records':str(len(b)),
          'ranking_source_quality':'June 11 ranks checked against previously reviewed published edition; pre-tournament ranks reused from v3 and 31-60 research, predominantly secondary historical ranking archives; football fixtures sourced to FIFA general chronology or earlier evidence.'})
    return out,wc_checks,x7_checks

def run():
    with INPUT.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    out,wc_checks,x7_checks=compute(rows)
    with OUTPUT.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator='\n');w.writeheader();w.writerows(out)
    print('Validated 300 rows, 30 targets, '+str(wc_checks)+' previous World Cup fixture references, '+str(x7_checks)+' latest-predecessor checks')
    for r in out:print(f"{r['match_id']} {r['team_a']} vs {r['team_b']}: A={r['team_a_average_rank']} B={r['team_b_average_rank']} X8={r['x8_opponent_strength_difference']} {r['calculation_status']}")
    return out

if __name__=='__main__':
    if '--test' in sys.argv:
        print('PASSED',policy_tests(),'ranking publication-policy tests')
    else:
        run()
