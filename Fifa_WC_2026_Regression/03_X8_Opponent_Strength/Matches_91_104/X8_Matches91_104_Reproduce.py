#!/usr/bin/env python3
"""Reproduce X8 for FIFA World Cup 2026 match IDs 91–104.

ACADEMIC INTEGRITY: Generative AI assisted with historical source selection,
research reuse, ranking transcription, this code's generation, and testing.
The input is an AI-assisted curated research CSV, not a direct FIFA database
export. Programmatic checks establish internal consistency, chronology, policy
and arithmetic but DO NOT authenticate websites or independently prove the
truth of every historical ranking/fixture.

Run from a directory containing this script and its Historical_Research.csv:
    python X8_Matches91_104_Reproduce.py --test
    python X8_Matches91_104_Reproduce.py

Only Python standard library; neither the master Excel file nor any prior
batch is needed or modified. An embedded frozen read-only reference snapshot
from the original master and previously reviewed results supports independent
cross-checks against the newly exported input.
"""
from __future__ import annotations
import csv,json,sys
from pathlib import Path
from datetime import date
from decimal import Decimal,ROUND_HALF_UP
from collections import defaultdict

ROOT=Path(__file__).resolve().parent
INPUT=ROOT/'X8_Matches91_104_Historical_Research.csv'
OUTPUT=ROOT/'X8_Matches91_104_Calculated_Results.csv'
FIFA_JUNE_11_RELEASE='https://inside.fifa.com/fifa-rankings/world-ranking/men/news/argentina-reclaim-top-spot-mens-world-ranking-fifa-coca-cola'
HISTORICAL_EDITIONS=[date.fromisoformat(s) for s in ('2025-09-18','2025-10-17','2025-11-19','2025-12-22','2026-01-19','2026-04-01','2026-06-11')]
IDS=set(range(91,105))
OUTPUT_FIELDS=['match_id','match_date','team_a','team_b','team_a_rank_sum','team_a_average_rank','team_b_rank_sum','team_b_average_rank','x8_opponent_strength_difference','calculation_status','manual_review_flags','team_a_records','team_b_records','ranking_source_quality']
REFERENCE_JSON = r'''{"master":{"1":{"match_date":"2026-06-11","team_a":"Mexico","team_b":"South Africa"},"2":{"match_date":"2026-06-11","team_a":"Korea Republic","team_b":"Czechia"},"3":{"match_date":"2026-06-12","team_a":"Canada","team_b":"Bosnia and Herzegovina"},"4":{"match_date":"2026-06-12","team_a":"USA","team_b":"Paraguay"},"5":{"match_date":"2026-06-13","team_a":"Haiti","team_b":"Scotland"},"6":{"match_date":"2026-06-13","team_a":"Australia","team_b":"Türkiye"},"7":{"match_date":"2026-06-13","team_a":"Brazil","team_b":"Morocco"},"8":{"match_date":"2026-06-13","team_a":"Qatar","team_b":"Switzerland"},"9":{"match_date":"2026-06-14","team_a":"Côte d'Ivoire","team_b":"Ecuador"},"10":{"match_date":"2026-06-14","team_a":"Germany","team_b":"Curaçao"},"11":{"match_date":"2026-06-14","team_a":"Netherlands","team_b":"Japan"},"12":{"match_date":"2026-06-14","team_a":"Sweden","team_b":"Tunisia"},"13":{"match_date":"2026-06-15","team_a":"Saudi Arabia","team_b":"Uruguay"},"14":{"match_date":"2026-06-15","team_a":"Spain","team_b":"Cabo Verde"},"15":{"match_date":"2026-06-15","team_a":"IR Iran","team_b":"New Zealand"},"16":{"match_date":"2026-06-15","team_a":"Belgium","team_b":"Egypt"},"17":{"match_date":"2026-06-16","team_a":"France","team_b":"Senegal"},"18":{"match_date":"2026-06-16","team_a":"Iraq","team_b":"Norway"},"19":{"match_date":"2026-06-16","team_a":"Argentina","team_b":"Algeria"},"20":{"match_date":"2026-06-16","team_a":"Austria","team_b":"Jordan"},"21":{"match_date":"2026-06-17","team_a":"Ghana","team_b":"Panama"},"22":{"match_date":"2026-06-17","team_a":"England","team_b":"Croatia"},"23":{"match_date":"2026-06-17","team_a":"Portugal","team_b":"Congo DR"},"24":{"match_date":"2026-06-17","team_a":"Uzbekistan","team_b":"Colombia"},"25":{"match_date":"2026-06-18","team_a":"Czechia","team_b":"South Africa"},"26":{"match_date":"2026-06-18","team_a":"Switzerland","team_b":"Bosnia and Herzegovina"},"27":{"match_date":"2026-06-18","team_a":"Canada","team_b":"Qatar"},"28":{"match_date":"2026-06-18","team_a":"Mexico","team_b":"Korea Republic"},"29":{"match_date":"2026-06-19","team_a":"Brazil","team_b":"Haiti"},"30":{"match_date":"2026-06-19","team_a":"Scotland","team_b":"Morocco"},"31":{"match_date":"2026-06-19","team_a":"Türkiye","team_b":"Paraguay"},"32":{"match_date":"2026-06-19","team_a":"USA","team_b":"Australia"},"33":{"match_date":"2026-06-20","team_a":"Germany","team_b":"Côte d'Ivoire"},"34":{"match_date":"2026-06-20","team_a":"Ecuador","team_b":"Curaçao"},"35":{"match_date":"2026-06-20","team_a":"Netherlands","team_b":"Sweden"},"36":{"match_date":"2026-06-20","team_a":"Tunisia","team_b":"Japan"},"37":{"match_date":"2026-06-21","team_a":"Uruguay","team_b":"Cabo Verde"},"38":{"match_date":"2026-06-21","team_a":"Spain","team_b":"Saudi Arabia"},"39":{"match_date":"2026-06-21","team_a":"Belgium","team_b":"IR Iran"},"40":{"match_date":"2026-06-21","team_a":"New Zealand","team_b":"Egypt"},"41":{"match_date":"2026-06-22","team_a":"Norway","team_b":"Senegal"},"42":{"match_date":"2026-06-22","team_a":"France","team_b":"Iraq"},"43":{"match_date":"2026-06-22","team_a":"Argentina","team_b":"Austria"},"44":{"match_date":"2026-06-22","team_a":"Jordan","team_b":"Algeria"},"45":{"match_date":"2026-06-23","team_a":"England","team_b":"Ghana"},"46":{"match_date":"2026-06-23","team_a":"Panama","team_b":"Croatia"},"47":{"match_date":"2026-06-23","team_a":"Portugal","team_b":"Uzbekistan"},"48":{"match_date":"2026-06-23","team_a":"Colombia","team_b":"Congo DR"},"49":{"match_date":"2026-06-24","team_a":"Scotland","team_b":"Brazil"},"50":{"match_date":"2026-06-24","team_a":"Morocco","team_b":"Haiti"},"51":{"match_date":"2026-06-24","team_a":"Switzerland","team_b":"Canada"},"52":{"match_date":"2026-06-24","team_a":"Bosnia and Herzegovina","team_b":"Qatar"},"53":{"match_date":"2026-06-24","team_a":"Czechia","team_b":"Mexico"},"54":{"match_date":"2026-06-24","team_a":"South Africa","team_b":"Korea Republic"},"55":{"match_date":"2026-06-25","team_a":"Curaçao","team_b":"Côte d'Ivoire"},"56":{"match_date":"2026-06-25","team_a":"Ecuador","team_b":"Germany"},"57":{"match_date":"2026-06-25","team_a":"Japan","team_b":"Sweden"},"58":{"match_date":"2026-06-25","team_a":"Tunisia","team_b":"Netherlands"},"59":{"match_date":"2026-06-25","team_a":"Türkiye","team_b":"USA"},"60":{"match_date":"2026-06-25","team_a":"Paraguay","team_b":"Australia"},"61":{"match_date":"2026-06-26","team_a":"Norway","team_b":"France"},"62":{"match_date":"2026-06-26","team_a":"Senegal","team_b":"Iraq"},"63":{"match_date":"2026-06-26","team_a":"Egypt","team_b":"IR Iran"},"64":{"match_date":"2026-06-26","team_a":"New Zealand","team_b":"Belgium"},"65":{"match_date":"2026-06-26","team_a":"Cabo Verde","team_b":"Saudi Arabia"},"66":{"match_date":"2026-06-26","team_a":"Uruguay","team_b":"Spain"},"67":{"match_date":"2026-06-27","team_a":"Panama","team_b":"England"},"68":{"match_date":"2026-06-27","team_a":"Croatia","team_b":"Ghana"},"69":{"match_date":"2026-06-27","team_a":"Algeria","team_b":"Austria"},"70":{"match_date":"2026-06-27","team_a":"Jordan","team_b":"Argentina"},"71":{"match_date":"2026-06-27","team_a":"Colombia","team_b":"Portugal"},"72":{"match_date":"2026-06-27","team_a":"Congo DR","team_b":"Uzbekistan"},"73":{"match_date":"2026-06-28","team_a":"South Africa","team_b":"Canada"},"74":{"match_date":"2026-06-29","team_a":"Germany","team_b":"Paraguay"},"75":{"match_date":"2026-06-29","team_a":"Netherlands","team_b":"Morocco"},"76":{"match_date":"2026-06-29","team_a":"Brazil","team_b":"Japan"},"77":{"match_date":"2026-06-30","team_a":"France","team_b":"Sweden"},"78":{"match_date":"2026-06-30","team_a":"Côte d'Ivoire","team_b":"Norway"},"79":{"match_date":"2026-06-30","team_a":"Mexico","team_b":"Ecuador"},"80":{"match_date":"2026-07-01","team_a":"England","team_b":"Congo DR"},"81":{"match_date":"2026-07-01","team_a":"USA","team_b":"Bosnia and Herzegovina"},"82":{"match_date":"2026-07-01","team_a":"Belgium","team_b":"Senegal"},"83":{"match_date":"2026-07-02","team_a":"Portugal","team_b":"Croatia"},"84":{"match_date":"2026-07-02","team_a":"Spain","team_b":"Austria"},"85":{"match_date":"2026-07-02","team_a":"Switzerland","team_b":"Algeria"},"86":{"match_date":"2026-07-03","team_a":"Argentina","team_b":"Cabo Verde"},"87":{"match_date":"2026-07-03","team_a":"Colombia","team_b":"Ghana"},"88":{"match_date":"2026-07-03","team_a":"Australia","team_b":"Egypt"},"89":{"match_date":"2026-07-04","team_a":"Paraguay","team_b":"France"},"90":{"match_date":"2026-07-04","team_a":"Canada","team_b":"Morocco"},"91":{"match_date":"2026-07-05","team_a":"Brazil","team_b":"Norway"},"92":{"match_date":"2026-07-05","team_a":"Mexico","team_b":"England"},"93":{"match_date":"2026-07-06","team_a":"Portugal","team_b":"Spain"},"94":{"match_date":"2026-07-06","team_a":"USA","team_b":"Belgium"},"95":{"match_date":"2026-07-07","team_a":"Argentina","team_b":"Egypt"},"96":{"match_date":"2026-07-07","team_a":"Switzerland","team_b":"Colombia"},"97":{"match_date":"2026-07-09","team_a":"France","team_b":"Morocco"},"98":{"match_date":"2026-07-10","team_a":"Spain","team_b":"Belgium"},"99":{"match_date":"2026-07-11","team_a":"Norway","team_b":"England"},"100":{"match_date":"2026-07-11","team_a":"Argentina","team_b":"Switzerland"},"101":{"match_date":"2026-07-14","team_a":"France","team_b":"Spain"},"102":{"match_date":"2026-07-15","team_a":"England","team_b":"Argentina"},"103":{"match_date":"2026-07-18","team_a":"France","team_b":"England"},"104":{"match_date":"2026-07-19","team_a":"Spain","team_b":"Argentina"}},"rank_reference":{"Serbia|2026-04-01":39,"Australia|2026-04-01":27,"Ghana|2026-04-01":74,"Belgium|2026-01-19":9,"Portugal|2026-01-19":6,"Jamaica|2026-04-01":71,"Nicaragua|2026-04-01":131,"Panama|2026-01-19":33,"Cameroon|2025-12-22":57,"El Salvador|2026-04-01":100,"Trinidad and Tobago|2026-04-01":102,"Austria|2026-01-19":24,"Côte d'Ivoire|2026-01-19":37,"Ghana|2025-10-17":73,"Guatemala|2026-04-01":96,"Kosovo|2026-04-01":78,"Denmark|2026-01-19":21,"Republic of Ireland|2026-01-19":59,"Gibraltar|2025-10-17":200,"Republic of Ireland|2026-04-01":59,"Uzbekistan|2026-04-01":50,"Tunisia|2026-01-19":47,"Iceland|2026-01-19":74,"Guatemala|2025-12-22":94,"Panama|2026-04-01":33,"North Macedonia|2026-04-01":67,"Italy|2026-01-19":13,"Wales|2026-01-19":35,"Austria|2025-10-17":24,"Germany|2026-04-01":10,"Senegal|2026-04-01":14,"Uruguay|2025-10-17":15,"Morocco|2026-01-19":8,"Greece|2026-01-19":46,"Mexico|2025-10-17":14,"USA|2025-10-17":16,"Peru|2026-04-01":53,"New Zealand|2026-04-01":85,"Nicaragua|2025-10-17":133,"Bolivia|2026-04-01":76,"Curaçao|2026-04-01":82,"Japan|2026-01-19":19,"Denmark|2025-10-17":20,"Switzerland|2026-04-01":19,"Mexico|2026-04-01":15,"Curaçao|2026-01-19":81,"Cameroon|2026-01-19":45,"Colombia|2025-10-17":13,"Venezuela|2026-04-01":49,"Kosovo|2026-01-19":79,"Romania|2026-01-19":49,"Spain|2025-10-17":1,"Egypt|2026-04-01":29,"Croatia|2026-01-19":11,"France|2026-01-19":3,"Tunisia|2025-10-17":43,"Norway|2026-04-01":31,"Madagascar|2026-04-01":104,"Burundi|2026-04-01":142,"Paraguay|2026-01-19":40,"Ecuador|2026-01-19":23,"Tunisia|2025-11-19":40,"Syria|2025-11-19":87,"Palestine|2025-11-19":96,"Jordan|2026-04-01":63,"Norway|2026-01-19":32,"Germany|2026-01-19":10,"Kosovo|2025-10-17":84,"France|2026-04-01":1,"Scotland|2026-01-19":38,"Korea Republic|2026-01-19":22,"Egypt|2025-12-22":35,"Burkina Faso|2025-12-22":62,"Saudi Arabia|2026-04-01":61,"Netherlands|2026-01-19":7,"New Zealand|2025-10-17":85,"USA|2026-04-01":16,"Finland|2026-04-01":73,"Ghana|2026-01-19":72,"Switzerland|2026-01-19":18,"Slovakia|2025-10-17":46,"Aruba|2026-04-01":189,"Scotland|2026-04-01":43,"Australia|2026-01-19":27,"China|2026-01-19":93,"Jamaica|2025-10-17":68,"Algeria|2026-04-01":28,"Lithuania|2025-10-17":146,"Iceland|2026-04-01":75,"England|2026-01-19":4,"Bolivia|2025-10-17":76,"Greece|2026-04-01":47,"Poland|2026-01-19":34,"Ukraine|2026-01-19":30,"Slovenia|2025-10-17":51,"Belgium|2026-04-01":9,"Austria|2026-04-01":24,"Canada|2026-01-19":29,"Haiti|2026-01-19":83,"Mali|2025-12-22":53,"Puerto Rico|2026-04-01":156,"Ecuador|2026-04-01":23,"Serbia|2026-01-19":39,"Egypt|2026-01-19":31,"Algeria|2026-01-19":28,"Uzbekistan|2025-09-18":54,"Iraq|2026-04-01":57,"Türkiye|2025-10-17":26,"Bermuda|2026-04-01":166,"Finland|2026-01-19":75,"Chile|2026-01-19":55,"Egypt|2025-10-17":32,"Mali|2026-04-01":52,"Gambia|2026-04-01":116,"Costa Rica|2026-01-19":51,"Nigeria|2026-01-19":26,"Uzbekistan|2025-10-17":55,"England|2026-04-01":4,"Haiti|2026-04-01":83,"Ecuador|2025-10-17":23,"Tunisia|2026-04-01":44,"Croatia|2026-04-01":11,"Mexico|2026-01-19":16,"USA|2026-01-19":15,"Liechtenstein|2025-10-17":206,"Brazil|2026-04-01":6,"Russia|2026-04-01":36,"Spain|2026-01-19":1,"Saudi Arabia|2026-01-19":61,"Nigeria|2025-12-22":38,"Northern Ireland|2026-04-01":70,"Côte d'Ivoire|2026-04-01":34,"Colombia|2026-01-19":14,"Brazil|2026-01-19":5,"Azerbaijan|2025-10-17":123,"Gambia|2026-01-19":116,"Peru|2026-01-19":53,"Morocco|2025-12-22":11,"Spain|2026-04-01":2,"Andorra|2026-04-01":173,"Bolivia|2026-01-19":76,"Jordan|2025-11-19":66,"Morocco|2026-04-01":8,"Sweden|2026-04-01":38,"Italy|2025-10-17":9,"Honduras|2026-04-01":66,"Zambia|2026-01-19":91,"Mauritania|2026-01-19":115,"Angola|2025-10-17":89,"Netherlands|2026-04-01":7,"Uruguay|2026-01-19":17,"Guatemala|2026-01-19":94,"Bosnia and Herzegovina|2025-10-17":75,"Cyprus|2025-10-17":125,"Colombia|2026-04-01":13,"Morocco|2025-11-19":11,"Wales|2026-04-01":37,"Korea Republic|2025-10-17":22,"Bosnia and Herzegovina|2026-04-01":65,"Dominican Republic|2026-04-01":143,"South Africa|2026-01-19":60,"Costa Rica|2026-04-01":51,"Albania|2025-10-17":61,"Slovenia|2026-04-01":58,"Montenegro|2025-10-17":81,"Nigeria|2026-04-01":26,"Chile|2026-04-01":54,"Armenia|2025-10-17":104,"Denmark|2026-04-01":20,"Jamaica|2026-01-19":70,"Bermuda|2026-01-19":169,"Algeria|2025-12-22":34,"Canada|2026-04-01":30,"Venezuela|2026-01-19":50,"Gabon|2026-01-19":86,"IR Iran|2025-10-17":21,"Australia|2025-10-17":25,"Korea Republic|2026-06-11":25,"Mexico|2026-06-11":14,"Qatar|2026-06-11":56,"Canada|2026-06-11":30,"Bosnia and Herzegovina|2026-06-11":64,"Switzerland|2026-06-11":19,"South Africa|2026-06-11":60,"Czechia|2026-06-11":40,"Morocco|2026-06-11":7,"Scotland|2026-06-11":42,"Haiti|2026-06-11":83,"Brazil|2026-06-11":6,"Australia|2026-06-11":27,"USA|2026-06-11":17,"Paraguay|2026-06-11":41,"Türkiye|2026-06-11":22,"Curaçao|2026-06-11":82,"Ecuador|2026-06-11":23,"Côte d'Ivoire|2026-06-11":33,"Germany|2026-06-11":10,"Japan|2026-06-11":18,"Tunisia|2026-06-11":45,"Sweden|2026-06-11":38,"Netherlands|2026-06-11":8,"Saudi Arabia|2026-06-11":61,"Spain|2026-06-11":2,"Cabo Verde|2026-06-11":67,"Uruguay|2026-06-11":16,"Egypt|2026-06-11":29,"New Zealand|2026-06-11":85,"IR Iran|2026-06-11":20,"Belgium|2026-06-11":9,"Iraq|2026-06-11":57,"France|2026-06-11":3,"Senegal|2026-06-11":15,"Norway|2026-06-11":31,"Algeria|2026-06-11":28,"Jordan|2026-06-11":63,"Austria|2026-06-11":24,"Argentina|2026-06-11":1,"Croatia|2026-06-11":11,"Panama|2026-06-11":34,"Ghana|2026-06-11":73,"England|2026-06-11":4,"Congo DR|2026-06-11":46,"Colombia|2026-06-11":13,"Uzbekistan|2026-06-11":50,"Portugal|2026-06-11":5},"x7_reference":{"91:A":{"previous_date":"2026-06-29","previous_opponent":"Japan","previous_wc_match_id":"76"},"91:B":{"previous_date":"2026-06-30","previous_opponent":"Côte d'Ivoire","previous_wc_match_id":"78"},"92:A":{"previous_date":"2026-06-30","previous_opponent":"Ecuador","previous_wc_match_id":"79"},"92:B":{"previous_date":"2026-07-01","previous_opponent":"Congo DR","previous_wc_match_id":"80"},"93:A":{"previous_date":"2026-07-02","previous_opponent":"Croatia","previous_wc_match_id":"83"},"93:B":{"previous_date":"2026-07-02","previous_opponent":"Austria","previous_wc_match_id":"84"},"94:A":{"previous_date":"2026-07-01","previous_opponent":"Bosnia and Herzegovina","previous_wc_match_id":"81"},"94:B":{"previous_date":"2026-07-01","previous_opponent":"Senegal","previous_wc_match_id":"82"},"95:A":{"previous_date":"2026-07-03","previous_opponent":"Cabo Verde","previous_wc_match_id":"86"},"95:B":{"previous_date":"2026-07-03","previous_opponent":"Australia","previous_wc_match_id":"88"},"96:A":{"previous_date":"2026-07-02","previous_opponent":"Algeria","previous_wc_match_id":"85"},"96:B":{"previous_date":"2026-07-03","previous_opponent":"Ghana","previous_wc_match_id":"87"},"97:A":{"previous_date":"2026-07-04","previous_opponent":"Paraguay","previous_wc_match_id":"89"},"97:B":{"previous_date":"2026-07-04","previous_opponent":"Canada","previous_wc_match_id":"90"},"98:A":{"previous_date":"2026-07-06","previous_opponent":"Portugal","previous_wc_match_id":"93"},"98:B":{"previous_date":"2026-07-06","previous_opponent":"USA","previous_wc_match_id":"94"},"99:A":{"previous_date":"2026-07-05","previous_opponent":"Brazil","previous_wc_match_id":"91"},"99:B":{"previous_date":"2026-07-05","previous_opponent":"Mexico","previous_wc_match_id":"92"},"100:A":{"previous_date":"2026-07-07","previous_opponent":"Egypt","previous_wc_match_id":"95"},"100:B":{"previous_date":"2026-07-07","previous_opponent":"Colombia","previous_wc_match_id":"96"},"101:A":{"previous_date":"2026-07-09","previous_opponent":"Morocco","previous_wc_match_id":"97"},"101:B":{"previous_date":"2026-07-10","previous_opponent":"Belgium","previous_wc_match_id":"98"},"102:A":{"previous_date":"2026-07-11","previous_opponent":"Norway","previous_wc_match_id":"99"},"102:B":{"previous_date":"2026-07-11","previous_opponent":"Switzerland","previous_wc_match_id":"100"},"103:A":{"previous_date":"2026-07-14","previous_opponent":"Spain","previous_wc_match_id":"101"},"103:B":{"previous_date":"2026-07-15","previous_opponent":"Argentina","previous_wc_match_id":"102"},"104:A":{"previous_date":"2026-07-14","previous_opponent":"France","previous_wc_match_id":"101"},"104:B":{"previous_date":"2026-07-15","previous_opponent":"England","previous_wc_match_id":"102"}},"pre_tournament_most_recent":{"Mexico":{"date":"2026-06-04","opponent":"Serbia"},"South Africa":{"date":"2026-06-06","opponent":"Jamaica"},"Korea Republic":{"date":"2026-06-03","opponent":"El Salvador"},"Czechia":{"date":"2026-06-04","opponent":"Guatemala"},"Canada":{"date":"2026-06-05","opponent":"Republic of Ireland"},"Bosnia and Herzegovina":{"date":"2026-06-06","opponent":"Panama"},"USA":{"date":"2026-06-06","opponent":"Germany"},"Paraguay":{"date":"2026-06-05","opponent":"Nicaragua"},"Haiti":{"date":"2026-06-05","opponent":"Peru"},"Scotland":{"date":"2026-06-06","opponent":"Bolivia"},"Australia":{"date":"2026-06-06","opponent":"Switzerland"},"Türkiye":{"date":"2026-06-06","opponent":"Venezuela"},"Brazil":{"date":"2026-06-06","opponent":"Egypt"},"Morocco":{"date":"2026-06-07","opponent":"Norway"},"Qatar":{"date":"2026-06-06","opponent":"El Salvador"},"Switzerland":{"date":"2026-06-06","opponent":"Australia"},"Côte d'Ivoire":{"date":"2026-06-04","opponent":"France"},"Ecuador":{"date":"2026-06-07","opponent":"Guatemala"},"Germany":{"date":"2026-06-06","opponent":"USA"},"Curaçao":{"date":"2026-06-06","opponent":"Aruba"},"Netherlands":{"date":"2026-06-08","opponent":"Uzbekistan"},"Japan":{"date":"2026-05-31","opponent":"Iceland"},"Sweden":{"date":"2026-06-04","opponent":"Greece"},"Tunisia":{"date":"2026-06-06","opponent":"Belgium"},"Saudi Arabia":{"date":"2026-06-09","opponent":"Senegal"},"Uruguay":{"date":"2026-03-31","opponent":"Algeria"},"Spain":{"date":"2026-06-08","opponent":"Peru"},"Cabo Verde":{"date":"2026-06-06","opponent":"Bermuda"},"IR Iran":{"date":"2026-06-04","opponent":"Mali"},"New Zealand":{"date":"2026-06-06","opponent":"England"},"Belgium":{"date":"2026-06-06","opponent":"Tunisia"},"Egypt":{"date":"2026-06-06","opponent":"Brazil"},"France":{"date":"2026-06-08","opponent":"Northern Ireland"},"Senegal":{"date":"2026-06-09","opponent":"Saudi Arabia"},"Iraq":{"date":"2026-06-09","opponent":"Venezuela"},"Norway":{"date":"2026-06-07","opponent":"Morocco"},"Argentina":{"date":"2026-06-09","opponent":"Iceland"},"Algeria":{"date":"2026-06-10","opponent":"Bolivia"},"Austria":{"date":"2026-06-01","opponent":"Tunisia"},"Jordan":{"date":"2026-06-07","opponent":"Colombia"},"Ghana":{"date":"2026-06-02","opponent":"Wales"},"Panama":{"date":"2026-06-06","opponent":"Bosnia and Herzegovina"},"England":{"date":"2026-06-10","opponent":"Costa Rica"},"Croatia":{"date":"2026-06-07","opponent":"Slovenia"},"Portugal":{"date":"2026-06-10","opponent":"Nigeria"},"Congo DR":{"date":"2026-06-09","opponent":"Chile"},"Uzbekistan":{"date":"2026-06-08","opponent":"Netherlands"},"Colombia":{"date":"2026-06-07","opponent":"Jordan"}}}'''
SNAPSHOT=json.loads(REFERENCE_JSON)
MASTER=SNAPSHOT['master']
RANK_REF=SNAPSHOT['rank_reference']
X7_REF=SNAPSHOT['x7_reference']
PRE_REF=SNAPSHOT['pre_tournament_most_recent']

def publication_decision(fixture:date, edition:date, fifa_before_opening_evidence:bool=False):
    if edition>fixture:return False,'REJECT_FUTURE_EDITION'
    if edition==fixture:
        if edition==date(2026,6,11) and fifa_before_opening_evidence:
            return True,'OFFICIAL_FIFA_PRE_OPENING_RELEASE'
        return False,'REJECT_SAME_DAY_WITHOUT_PRE_KICKOFF_PROOF'
    return True,'PRIOR_PUBLISHED_EDITION'

def policy_tests():
    checks=[
       publication_decision(date(2026,6,11),date(2026,6,11),True)[0],
       not publication_decision(date(2026,6,11),date(2026,6,11),False)[0],
       not publication_decision(date(2026,6,10),date(2026,6,11),True)[0],
       publication_decision(date(2026,6,12),date(2026,6,11))[0],
       publication_decision(date(2026,6,6),date(2026,4,1))[0],
       not publication_decision(date(2026,4,1),date(2026,4,1),False)[0],
       not publication_decision(date(2026,7,14),date(2026,7,20))[0],
       max(e for e in HISTORICAL_EDITIONS if e<date(2026,6,6))==date(2026,4,1),
       max(e for e in HISTORICAL_EDITIONS if e<date(2026,7,19))==date(2026,6,11),
    ]
    assert all(checks),checks
    return len(checks)

def ranked_allowed_and_latest(record):
    historical=date.fromisoformat(record['previous_match_date'])
    ranking=date.fromisoformat(record['ranking_publication_date'])
    is_wc=bool(record['previous_wc_match_id'].strip())
    # FIFA explicitly confirmed the June 11 edition preceded its opener.
    # Explicit source citation is mandatory for same-day eligibility.
    official_before=(is_wc and ranking==date(2026,6,11)
      and record['ranking_official_edition_announcement_url']==FIFA_JUNE_11_RELEASE
      and record['same_day_ranking_decision']=='FIFA_RELEASE_BEFORE_OPENING_MATCH_CONFIRMED_FOR_2026_06_11')
    allowed,decision=publication_decision(historical,ranking,official_before)
    if not allowed:raise ValueError(f'Ineligible ranking edition for {record["match_id"]} {record["team"]}: {decision}')
    eligible=[d for d in HISTORICAL_EDITIONS if d<historical or (d==historical and official_before)]
    if not eligible or ranking!=max(eligible):
        raise ValueError(f'Not the latest eligible FIFA publication: {record["match_id"]} {record["team"]} {historical} {ranking}')
    return decision

def validate_and_group(records):
    if len(records)!=140:raise ValueError(f'Expected exactly 140 history rows, got {len(records)}')
    groups=defaultdict(lambda:{'A':[],'B':[]})
    seen=set(); wc_count=0;x7_count=0;scotland_count=0
    for r in records:
        mid=int(r['match_id']);side=r['team_side'];recency=int(r['previous_match_recency'])
        key=(mid,side,recency)
        if mid not in IDS or side not in ('A','B') or recency not in range(1,6) or key in seen:
            raise ValueError(f'Invalid or duplicated match/side/recency {key}')
        seen.add(key)
        m=MASTER[str(mid)]
        if (r['match_date'],r['team_a'],r['team_b'])!=(m['match_date'],m['team_a'],m['team_b']):
            raise ValueError(f'Master order/date mismatch {key}')
        team=m['team_a' if side=='A' else 'team_b']
        if r['team']!=team:raise ValueError(f'Wrong team side {key}')
        if date.fromisoformat(r['previous_match_date'])>=date.fromisoformat(m['match_date']):
            raise ValueError(f'Current/future match incorrectly included {key}')
        if not r['previous_opponent'] or not r['fixture_source_url'] or not r['ranking_source_url']:
            raise ValueError(f'Missing historical opponent or source URL {key}')
        ranked_allowed_and_latest(r)
        opp_rank=r['opponent_fifa_rank'].strip()
        if not opp_rank: r['_rank']=None
        else:
            rank=int(opp_rank)
            if not 1<=rank<=211:raise ValueError(f'Out-of-range FIFA ranking {key}')
            refkey=r['previous_opponent']+'|'+r['ranking_publication_date']
            if refkey not in RANK_REF or rank!=RANK_REF[refkey]:
                raise ValueError(f'Historical rank disagrees with reviewed earlier batches {key} {refkey}: {rank}')
            if refkey=='Scotland|2026-06-11':
                if rank!=42:raise ValueError('Scotland June 11 FIFA rank must be 42')
                scotland_count+=1
            r['_rank']=rank
        previous_wc=r['previous_wc_match_id'].strip()
        if previous_wc:
            earlier_id=int(previous_wc)
            if earlier_id>=mid or str(earlier_id) not in MASTER:raise ValueError(f'Future or unknown WC fixture {key}')
            earlier=MASTER[str(earlier_id)]
            if r['team'] not in (earlier['team_a'],earlier['team_b']):raise ValueError(f'Team not in referenced previous WC fixture {key}')
            prior_opp=earlier['team_b'] if earlier['team_a']==team else earlier['team_a']
            if (r['previous_match_date'],r['previous_opponent'])!=(earlier['match_date'],prior_opp):
                raise ValueError(f'Incorrect WC opponent or date {key}')
            if r['ranking_publication_date']!='2026-06-11':raise ValueError(f'WC fixture must use June edition {key}')
            wc_count+=1
        else:
            if mid>96:raise ValueError('Unexpected pre-tournament match in quarter/semi/finals: '+str(key))
            if r['previous_match_date']>='2026-06-11':raise ValueError(f'Non-World-Cup pre-tournament fixture has impossible date {key}')
        groups[mid][side].append(r)
    if set(groups)!=IDS:raise ValueError('Missing match IDs in batch')
    for mid,teams in sorted(groups.items()):
        m=MASTER[str(mid)];cutoff=m['match_date']
        for side in ('A','B'):
            rr=sorted(teams[side],key=lambda r:int(r['previous_match_recency']))
            if len(rr)!=5 or [int(r['previous_match_recency']) for r in rr]!=[1,2,3,4,5]:
                raise ValueError(f'Not exactly five ordered fixtures: {mid}:{side}')
            identity=[(r['previous_match_date'],r['previous_opponent']) for r in rr]
            if len(set(identity))!=5:raise ValueError(f'Duplicate historical fixture: {mid}:{side}')
            if any(rr[i]['previous_match_date']<=rr[i+1]['previous_match_date'] for i in range(4)):
                raise ValueError(f'Historical dates not strictly most-recent-first: {mid}:{side}')
            team=rr[0]['team']
            earlier=[(m2['match_date'],j) for j,m2 in ((int(k),v) for k,v in MASTER.items()) if j<mid and m2['match_date']<cutoff and team in (m2['team_a'],m2['team_b'])]
            earlier.sort(reverse=True)
            chosen_wc=[int(r['previous_wc_match_id']) for r in rr if r['previous_wc_match_id'].strip()]
            expected_wc=[j for _,j in earlier[:5]]
            if chosen_wc!=expected_wc:raise ValueError(f'Skipped or incorrectly selected prior World Cup match {mid}:{side}')
            if len(expected_wc)<5:
                prev=PRE_REF.get(team)
                if prev is None or (rr[4]['previous_match_date'],rr[4]['previous_opponent'])!=(prev['date'],prev['opponent']):
                    raise ValueError(f'Pre-tournament predecessor mismatches reviewed research {mid}:{side}')
            if rr[0]['previous_wc_match_id']=='':raise ValueError(f'Latest fixture must be World Cup for {mid}:{side}')
            p=X7_REF[f'{mid}:{side}']
            if (rr[0]['previous_match_date'],rr[0]['previous_opponent'],rr[0]['previous_wc_match_id'])!=(p['previous_date'],p['previous_opponent'],p['previous_wc_match_id']):
                raise ValueError(f'X7 cross-check failed for {mid}:{side}')
            x7_count+=1
    return groups,wc_count,x7_count,scotland_count

def formatted(n):
    if n is None:return ''
    return str(n.quantize(Decimal('0.01'),rounding=ROUND_HALF_UP))

def calculate(records):
    groups,wc_count,x7_count,scotland_count=validate_and_group(records)
    results=[]
    for mid in sorted(IDS):
        a=groups[mid]['A'];b=groups[mid]['B'];allr=a+b
        sa=sum((Decimal(r['_rank']) for r in a),Decimal(0)) if all(r['_rank'] is not None for r in a) else None
        sb=sum((Decimal(r['_rank']) for r in b),Decimal(0)) if all(r['_rank'] is not None for r in b) else None
        av=sa/Decimal(5) if sa is not None else None
        bv=sb/Decimal(5) if sb is not None else None
        value=av-bv if av is not None and bv is not None else None
        flags=sorted({f.strip() for r in allr for f in r['manual_review_flags'].split(';') if f.strip()})
        if value is None:status='INCOMPLETE_MISSING_RANKING_DO_NOT_USE';flags.append('MISSING_REQUIRED_RANKING')
        elif flags:status='PROVISIONAL_MANUAL_REVIEW_REQUIRED'
        else:status='CALCULATED_SECONDARY_RANKING_EVIDENCE_NOT_DIRECTLY_FIFA_CERTIFIED'
        m=MASTER[str(mid)]
        results.append({'match_id':str(mid),'match_date':m['match_date'],'team_a':m['team_a'],'team_b':m['team_b'],
         'team_a_rank_sum':str(sa) if sa is not None else '',
         'team_a_average_rank':formatted(av),'team_b_rank_sum':str(sb) if sb is not None else '',
         'team_b_average_rank':formatted(bv),'x8_opponent_strength_difference':formatted(value),
         'calculation_status':status,'manual_review_flags':';'.join(flags),
         'team_a_records':str(len(a)),'team_b_records':str(len(b)),
         'ranking_source_quality':'Published historical FIFA editions; individual positions from prior-reviewed dated secondary rankings. Fixture data supported by master and official FIFA general chronology, with some match-specific reports. Twelve pre-tournament history records reused with their original evidence limitations.'})
    return results,wc_count,x7_count,scotland_count

def main():
    if '--test' in sys.argv:
        print('PASSED',policy_tests(),'ranking edition and same-day publication tests')
        return
    with INPUT.open(newline='',encoding='utf-8-sig') as f:records=list(csv.DictReader(f))
    results,wc_count,x7_count,scotland_count=calculate(records)
    with OUTPUT.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=OUTPUT_FIELDS,lineterminator='\n')
        writer.writeheader();writer.writerows(results)
    print(f'VALIDATED: 140 observations; {wc_count} prior World Cup fixtures; {x7_count} latest-X7 checks; Scotland rank 42 references: {scotland_count}')
    for r in results:print(f"{r['match_id']}: {r['team_a']} vs {r['team_b']} | A={r['team_a_average_rank']} B={r['team_b_average_rank']} X8={r['x8_opponent_strength_difference']} ({r['calculation_status']})")

if __name__=='__main__':main()
