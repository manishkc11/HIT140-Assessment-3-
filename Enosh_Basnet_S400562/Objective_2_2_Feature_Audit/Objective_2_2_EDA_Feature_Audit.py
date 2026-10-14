#!/usr/bin/env python3
"""Read-only Objective 2.2 feature and EDA audit. AI-assisted authoring.

Usage:
  python Objective_2_2_EDA_Feature_Audit.py --model-zip 'Regression_2_2_Final (2(1).zip' \
      --master-xlsx 'FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting(2).xlsx' \
      --evaluation-zip 'Part3_Evaluation(1).zip' --output-dir audit_out

No regression estimator is fitted; provided model predictions and metrics are only inspected.
An XLSX parser based on the Python standard library reads cached worksheet values.
Its purpose is auditing the source master; it never edits the workbook.
"""
import argparse, csv, hashlib, io, json, math, re, textwrap, zipfile
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict
import xml.etree.ElementTree as ET
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

FEATURES = ['team_fifa_rank','team_elo_rating_before','team_last5_avg_goals_scored',
            'team_last5_win_rate','is_knockout','is_host_nation',
            'wc_matches_played_before','wc_goals_conceded_before']
CODES = [f'X{i}' for i in range(1,9)]
GOAL = 'goals_scored'
TITLES = ['FIFA rank','Elo rating','Last-5 goals/match','Last-5 win rate',
          'Knockout stage','Host nation','Prior WC matches','Prior WC goals conceded']
NS = {'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
      'p':'http://schemas.openxmlformats.org/package/2006/relationships'}

def filehash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_csv_archive(path, suffix):
    with zipfile.ZipFile(path) as arc:
        matches = [x for x in arc.namelist() if x.endswith(suffix) and '.ipynb_checkpoints' not in x and '__MACOSX' not in x]
        if len(matches)!=1: raise ValueError(f'Expected exactly one {suffix}, found {matches}')
        return pd.read_csv(io.BytesIO(arc.read(matches[0])))

def load_json_archive(path, suffix):
    with zipfile.ZipFile(path) as arc:
        matches=[x for x in arc.namelist() if x.endswith(suffix) and '.ipynb_checkpoints' not in x and '__MACOSX' not in x]
        if len(matches)!=1: raise ValueError(f'Expected one {suffix}: {matches}')
        return json.loads(arc.read(matches[0]).decode('utf8'))

def colnum(ref):
    letters=re.match(r'[A-Z]+',ref).group(0); n=0
    for c in letters: n=26*n+ord(c)-64
    return n-1

def read_xlsx_sheet(file_or_bytes, name):
    """Read cached XLSX values with stdlib; numerically typed dates stay Excel serials."""
    stream=io.BytesIO(file_or_bytes) if isinstance(file_or_bytes,bytes) else str(file_or_bytes)
    with zipfile.ZipFile(stream) as z:
        wb=ET.fromstring(z.read('xl/workbook.xml'))
        rels=ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))
        paths={r.attrib['Id']:r.attrib['Target'] for r in rels}
        sheet=next(s for s in wb.findall('m:sheets/m:sheet',NS) if s.attrib['name']==name)
        rel_id=sheet.attrib[f"{{{NS['r']}}}id"]
        target=paths[rel_id].lstrip('/')
        if not target.startswith('xl/'): target='xl/'+target
        # tolerate '..' relative target
        import posixpath
        target=posixpath.normpath(target)
        string_table=[]
        if 'xl/sharedStrings.xml' in z.namelist():
            root=ET.fromstring(z.read('xl/sharedStrings.xml'))
            for si in root.findall('m:si',NS):
                string_table.append(''.join(n.text or '' for n in si.findall('.//m:t',NS)))
        xml=ET.fromstring(z.read(target)); items=[]
        for row in xml.findall('.//m:sheetData/m:row',NS):
            d={}
            for c in row.findall('m:c',NS):
                ci=colnum(c.attrib['r']); kind=c.attrib.get('t','n'); v=c.find('m:v',NS)
                if kind=='inlineStr':
                    val=''.join(n.text or '' for n in c.findall('.//m:t',NS))
                elif v is None or v.text is None: val=None
                elif kind=='s': val=string_table[int(v.text)]
                elif kind in ('str','e'): val=v.text
                elif kind=='b': val=bool(int(v.text))
                else:
                    try: val=float(v.text); val=int(val) if val.is_integer() else val
                    except ValueError:val=v.text
                d[ci]=val
            items.append(d)
        if not items: return pd.DataFrame()
        w=max(max(row.keys(),default=-1) for row in items)+1
        data=[[row.get(i) for i in range(w)] for row in items]
        cols=[str(x) if x is not None else f'_unnamed_{i}' for i,x in enumerate(data[0])]
        return pd.DataFrame(data[1:],columns=cols)

def as_date(series):
    # original spreadsheet has Excel date serials
    return pd.to_datetime(series.map(lambda x: (datetime(1899,12,30)+timedelta(days=float(x))) if isinstance(x,(float,int,np.integer)) else x))

def make_vif(X):
    """VIF using auxiliary regressions WITH intercept (no final outcome model)."""
    arr=X.to_numpy(dtype=float); ans=[]
    for j in range(arr.shape[1]):
        y=arr[:,j]; others=np.delete(arr,j,axis=1)
        design=np.column_stack((np.ones(len(arr)),others))
        coef, *_=np.linalg.lstsq(design,y,rcond=None)
        denom=float(((y-y.mean())**2).sum())
        r2=1-float(((y-design@coef)**2).sum())/denom if denom>0 else float('nan')
        value=float(1/(1-r2)) if np.isfinite(r2) and r2<1-1e-12 else float('inf')
        ans.append(value)
    return np.array(ans)

def audit(args):
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True); figures=out/'figures';figures.mkdir(exist_ok=True)
    df=load_csv_archive(args.model_zip,'data/Regression_2_2_208_Team_Rows.csv')
    preds=load_csv_archive(args.model_zip,'outputs/Predictions.csv')
    metrics=load_csv_archive(args.model_zip,'outputs/Metrics.csv')
    settings=load_json_archive(args.model_zip,'outputs/Model_Settings.json')
    src_wb_bytes=None
    with zipfile.ZipFile(args.model_zip) as z:
        files=[f for f in z.namelist() if f.endswith('/data/Source_104_Matches.xlsx') and '.ipynb_checkpoints' not in f]
        if len(files)!=1:raise ValueError('Missing source workbook')
        src_wb_bytes=z.read(files[0])
    source=read_xlsx_sheet(src_wb_bytes,'Master_104_Matches')
    external=read_xlsx_sheet(args.master_xlsx,'Master_104_Matches')
    ratings=read_xlsx_sheet(src_wb_bytes,'X1_X2_Inputs')
    form=read_xlsx_sheet(src_wb_bytes,'X3_X5_Detail')
    evidence=read_xlsx_sheet(src_wb_bytes,'Last5_Evidence')
    source['match_date']=as_date(source['match_date'])
    external['match_date']=as_date(external['match_date'])
    df['match_date']=pd.to_datetime(df['match_date']);preds['match_date']=pd.to_datetime(preds['match_date'])
    errors=[];warnings=[]
    def assertcheck(ok,label):
        if not bool(ok): errors.append(label)
    def note_warning(label):warnings.append(label)
    assertcheck(len(source)==len(external)==104,'Source match count not 104')
    compare_cols=['match_id','match_date','stage','team_a','team_b','team_a_goals','team_b_goals','goal_difference']+['fifa_rank_diff','elo_rating_diff','last5_avg_goals_scored_diff','last5_win_rate_diff']
    unequal=[]
    for c in compare_cols:
        if not source[c].fillna('_NULL_').astype(str).equals(external[c].fillna('_NULL_').astype(str)):
            unequal.append(c)
    assertcheck(not unequal,f'External master differs in {unequal}')
    assertcheck(len(df)==208 and set(df.match_id)==set(range(1,105)),'Row count or match IDs incorrect')
    assertcheck((df.groupby('match_id').size()==2).all(),'Not exactly 2 team rows each match')
    assertcheck(not df.duplicated(['match_id','team']).any(),'Duplicate team-match rows')
    assertcheck(not df.duplicated(['match_id','side']).any(),'Duplicate match-side rows')
    assertcheck(set(df.side.dropna())=={'A','B'},'Invalid side values')
    assertcheck(set(FEATURES)==set(settings['features']) and len(settings['features'])==8,'Feature list mismatch')
    assertcheck(df[FEATURES+[GOAL]].apply(pd.to_numeric,errors='coerce').notna().all().all(),'Missing/non-numeric values')
    assertcheck(((df[GOAL]>=0)&(df[GOAL]%1==0)).all(),'Invalid target')
    match_lookup=source.set_index('match_id')
    target_mismatch=[]; team_mismatch=[]; date_mismatch=[]; stage_mismatch=[]
    for r in df.itertuples(index=False):
        s=match_lookup.loc[r.match_id]
        team=s.team_a if r.side=='A' else s.team_b
        opp=s.team_b if r.side=='A' else s.team_a
        goals=s.team_a_goals if r.side=='A' else s.team_b_goals
        if r.team!=team or r.opponent!=opp:team_mismatch.append(r.match_id)
        if int(r.goals_scored)!=int(goals):target_mismatch.append(r.match_id)
        if r.match_date!=s.match_date:date_mismatch.append(r.match_id)
        if r.stage!=s.stage:stage_mismatch.append(r.match_id)
    assertcheck(not (target_mismatch or team_mismatch or date_mismatch or stage_mismatch),
                f'Master mismatch: target={target_mismatch}, team={team_mismatch}, date={date_mismatch}, stage={stage_mismatch}')
    for c in ['team_fifa_rank','team_elo_rating_before','team_last5_avg_goals_scored','team_last5_win_rate']:
        assertcheck(df[c].notna().all(),f'Missing {c}')
    # Verify source support matches X1,X2,X3,X5 team records and internal differences
    support_r=ratings.set_index('match_id');support_f=form.set_index('match_id'); support_errors=[]
    for r in df.itertuples(index=False):
        a=support_r.loc[r.match_id];f=support_f.loc[r.match_id]
        values=(a.fifa_rank_a,a.elo_a_before,f.team_a_last5_avg_goals,f.team_a_last5_win_rate) if r.side=='A' else (a.fifa_rank_b,a.elo_b_before,f.team_b_last5_avg_goals,f.team_b_last5_win_rate)
        truevals=(r.team_fifa_rank,r.team_elo_rating_before,r.team_last5_avg_goals_scored,r.team_last5_win_rate)
        if not np.allclose(values,truevals,atol=1e-8):support_errors.append((r.match_id,r.side))
    assertcheck(not support_errors,f'Historical supporting sheets mismatch {support_errors[:10]}')
    # Check pre-match WC cumulative values from source match chronology; updates occur after each date
    history=defaultdict(lambda: [0,0]); cumulative_errors=[]
    joined=df.set_index(['match_id','side'])
    for date,g in source.sort_values(['match_date','match_id']).groupby('match_date',sort=True):
        for m in g.itertuples(index=False):
            for side,team in [('A',m.team_a),('B',m.team_b)]:
                r=joined.loc[(m.match_id,side)];n,con=history[team]
                if r.wc_matches_played_before!=n or r.wc_goals_conceded_before!=con:
                    cumulative_errors.append((int(m.match_id),side,int(n),int(con)))
        for m in g.itertuples(index=False):
            history[m.team_a][0]+=1;history[m.team_a][1]+=int(m.team_b_goals)
            history[m.team_b][0]+=1;history[m.team_b][1]+=int(m.team_a_goals)
    assertcheck(not cumulative_errors,f'Cumulative WC histories mismatched {cumulative_errors[:10]}')
    # Check teams, host, knockout flag
    assertcheck((df['is_host_nation']==df.team.isin(['Mexico','Canada','USA']).astype(int)).all(),'Host flag inconsistent')
    assertcheck((df['is_knockout']==df.stage.ne('Group Stage').astype(int)).all(),'Knockout flag inconsistent')
    assertcheck(df.team_last5_win_rate.between(0,1).all(),'Invalid win rates')
    # Evidence audit: source documents are NOT independently authenticated
    evidence_report={'evidence_rows':len(evidence),'historical_dates_checked':0,'historical_date_violations':0,
                     'evidence_five_history_groups':0,'evidence_missing_history_groups':0,
                     'evidence_avg_goals_inconsistent':0,'evidence_win_rate_inconsistent':0}
    expected_groups={(int(m),side) for m in range(1,105) for side in ('A','B')}
    if {'match_id','side','historical_date','target_date','goals_for','win_indicator','lag'}.issubset(evidence.columns):
        ev=evidence[evidence['match_id'].notna()].copy()
        groups=ev.groupby(['match_id','side']);evidence_report['evidence_five_history_groups']=int((groups.size()==5).sum());evidence_report['evidence_missing_history_groups']=208-evidence_report['evidence_five_history_groups']
        before=(pd.to_numeric(ev.historical_date,errors='coerce')<pd.to_numeric(ev.target_date,errors='coerce'))
        evidence_report['historical_dates_checked']=len(ev);evidence_report['historical_date_violations']=int((~before).sum())
        for (m,side),part in groups:
            if len(part)!=5:continue
            r=joined.loc[(int(m),side)]
            if not np.isclose(part.goals_for.astype(float).sum()/5,r.team_last5_avg_goals_scored,atol=1e-7):evidence_report['evidence_avg_goals_inconsistent']+=1
            if not np.isclose(part.win_indicator.astype(float).sum()/5,r.team_last5_win_rate,atol=1e-7):evidence_report['evidence_win_rate_inconsistent']+=1
    # Partition directly from saved original predictions; no training
    assertcheck(len(preds)==208 and set(preds.data_split)=={'train','test'},'Prediction/split file invalid')
    assertcheck(not preds.duplicated(['match_id','side']).any(),'Duplicate prediction side')
    pair=df.merge(preds[['match_id','side','data_split','predicted_goals']+FEATURES+[GOAL]],on=['match_id','side'],suffixes=('','_pred'),validate='one_to_one')
    for c in FEATURES+[GOAL]:
        assertcheck(np.allclose(pair[c],pair[c+'_pred'],atol=1e-10),f'Saved predictions have mismatched {c}')
    split_count=preds.groupby('data_split').agg(team_rows=('match_id','size'),matches=('match_id','nunique'))
    assertcheck(int(split_count.loc['train','team_rows'])==164 and int(split_count.loc['test','team_rows'])==44 and
                int(split_count.loc['train','matches'])==82 and int(split_count.loc['test','matches'])==22,
                'Split 164/44, 82/22 mismatch')
    assertcheck(not set(preds.loc[preds.data_split=='train','match_id']) & set(preds.loc[preds.data_split=='test','match_id']), 'Match leaked train/test')
    train=preds[preds.data_split=='train'].copy();test=preds[preds.data_split=='test'].copy()
    assertcheck(train.match_date.max()<test.match_date.min(),'Split not strictly chronological')
    # Verify saved metrics exactly from model's saved predictions, do not retrain
    mt=dict(zip(metrics.metric,metrics.value))
    # Compare separately supplied Part 3 evaluation artifacts without running their model-training code.
    eval_data=load_csv_archive(args.evaluation_zip,'inputs/task22_data.csv')
    eval_preds=load_csv_archive(args.evaluation_zip,'inputs/task22_predictions.csv')
    eval_metrics=load_csv_archive(args.evaluation_zip,'results/model_metrics.csv')
    eval_summary=load_json_archive(args.evaluation_zip,'results/evaluation_summary.json')
    eval_data['match_date']=pd.to_datetime(eval_data['match_date'])
    eval_preds['match_date']=pd.to_datetime(eval_preds['match_date'])
    assertcheck(df.equals(eval_data), 'Part 3 evaluation input differs from the provided 208 team rows')
    assertcheck(preds.equals(eval_preds), 'Part 3 evaluation predictions differ from saved model predictions')
    comparison=eval_metrics.loc[(eval_metrics['task'].astype(str)=='2.2')&(eval_metrics['split']=='test')].copy()
    comparison.to_csv(out/'Provided_Model_Comparison.csv',index=False)
    ols=comparison.loc[comparison['model']=='Supplied OLS']
    assertcheck(len(ols)==1 and np.isclose(float(ols.iloc[0]['R2']),float(mt['test_R2'])), 'Part 3 supplied OLS test R2 differs')
    eval_detail=eval_summary['2.2']
    assertcheck(eval_detail['train_rows']==164 and eval_detail['test_rows']==44,'Part 3 evaluation split differs')
    ridge=comparison.loc[comparison['model']=='Ridge'].iloc[0]
    lasso=comparison.loc[comparison['model']=='Lasso'].iloc[0]
    saved_metric_diffs={}
    for split,frame in [('train',train),('test',test)]:
        y=frame.goals_scored.to_numpy(float);pr=frame.predicted_goals.to_numpy(float)
        test_metrics={f'{split}_MAE':np.mean(np.abs(y-pr)),f'{split}_RMSE':np.sqrt(np.mean((y-pr)**2)),
                      f'{split}_R2':1-np.sum((y-pr)**2)/np.sum((y-y.mean())**2)}
        for name,value in test_metrics.items():
            saved_metric_diffs[name]=abs(float(value)-float(mt[name]));assertcheck(np.isclose(value,mt[name],atol=1e-12),f'Provided metric differs {name}')
    # descriptives and target frequency
    use=FEATURES+[GOAL];summary=df[use].describe(percentiles=[.25,.5,.75]).T
    summary['missing']=df[use].isna().sum();summary['variable_code']=[*CODES,'Y']
    summary=summary.rename(columns={'count':'n','25%':'q1','50%':'median','75%':'q3','std':'std_dev'})
    summary[['variable_code','n','mean','std_dev','min','q1','median','q3','max','missing']].to_csv(out/'Objective_2_2_EDA_Summary.csv',index_label='column_name',float_format='%.8g')
    target_counts=df.goals_scored.value_counts().sort_index()
    (out/'Goals_Scored_Frequency.csv').write_text('goals_scored,count,percent\n'+''.join(f'{int(k)},{int(v)},{100*v/len(df):.3f}\n' for k,v in target_counts.items()))
    # Correlations all (descriptive only), train (development appropriate)
    corr_all=df[use].corr();corr_train=train[use].corr()
    corr_all.to_csv(out/'Full_Descriptive_Correlations.csv',float_format='%.8g')
    corr_train.to_csv(out/'Training_Predictor_Correlations.csv',float_format='%.8g')
    # VIF: auxiliary linear regressions WITH intercept, training only. Confirm inverse correlation method
    vif=make_vif(train[FEATURES]); inv=np.linalg.inv(train[FEATURES].corr().to_numpy(dtype=float));assertcheck(np.allclose(vif,np.diag(inv),rtol=1e-8,atol=1e-7),'VIF inverse correlation crosscheck failed')
    vif_table=pd.DataFrame({'code':CODES,'feature':FEATURES,'training_vif':vif,'screen':np.select([vif>10,vif>5],['Above 10: high','Above 5: investigate'],default='Below 5')});vif_table.to_csv(out/'Training_VIF_Results.csv',index=False,float_format='%.7g')
    # IQR flags for continuous predictors, exclude binary by definition
    continuous=[FEATURES[i] for i in [0,1,2,3,6,7]];outlier_rows=[]
    for col in continuous:
        q1,q3=train[col].quantile([.25,.75]);iqr=q3-q1;lo=q1-1.5*iqr;hi=q3+1.5*iqr
        # training-only thresholds, training observations only
        for r in train.loc[(train[col]<lo)|(train[col]>hi)].itertuples(index=False):
            outlier_rows.append({'match_id':r.match_id,'team':r.team,'feature':col,'observed_value':getattr(r,col),
                                 'training_lower_fence':lo,'training_upper_fence':hi,'notes':'IQR screening flag, not confirmed error'})
    pd.DataFrame(outlier_rows,columns=['match_id','team','feature','observed_value','training_lower_fence','training_upper_fence','notes']).to_csv(out/'Training_IQR_Flags.csv',index=False)
    # Train-test comparison
    shifts=[]
    for col in FEATURES:
        a=train[col];b=test[col];outside=int(((b<a.min())|(b>a.max())).sum())
        shifts.append({'code':CODES[FEATURES.index(col)],'feature':col,'train_mean':a.mean(),'test_mean':b.mean(),
          'train_min':a.min(),'train_max':a.max(),'test_min':b.min(),'test_max':b.max(),
          'test_rows_outside_train_range':outside})
    pd.DataFrame(shifts).to_csv(out/'Train_Test_Feature_Shift.csv',index=False,float_format='%.7g')
    # relative stage / host
    stage_ct=pd.crosstab(preds['data_split'],preds['stage'])
    host_ct=pd.crosstab(preds['data_split'],preds['is_host_nation'])
    # variable rationale; 4 expected shared, fifth concept caveat
    rationale=[
      ('Official FIFA ranking position (lower is stronger)','Official historical ranking before kickoff; supplied X1_X2_Inputs','Baseline relative strength','Yes if historical release precedes kickoff','Yes — FIFA ranking','Correlates with Elo; shared 2.1 X1','Historical source editions not fully reauthenticated'),
      ('Pre-match international Elo points (higher stronger)','X1_X2_Inputs Elo team snapshot','Continuous estimated team strength','Yes if pre-match snapshot is correct','Yes — Elo rating','Closely related to FIFA rank; 2.1 X2','Elo provider/timestamp not independently verified'),
      ('Mean goals scored in five preceding senior internationals, goals/match','X3_X5_Detail / Last5_Evidence; excludes target match','Recent offensive form','Yes if all five previous fixtures completed','Yes — prior-five goals scored','Related to win rate; 2.1 X3','Historical data comes from linked third-party records'),
      ('Fraction of wins among previous five matches, 0–1','X3_X5_Detail / Last5_Evidence','Recent result form','Yes if calculated before kickoff','Yes — prior-five win rate','Related to goals scored; 2.1 X5','Tied discrete 0.2 increments'),
      ('Binary indicator, 1 scheduled knockout / 0 group','Scheduled stage in master worksheet','Match environment and incentives','Yes — stage is fixed pre-match','No','Highly related to prior WC games','Little knockout representation in training'),
      ('Binary 1 Mexico/Canada/USA, else 0','Predetermined host set','Home-tournament setting','Yes — host status predetermined','No','Limited host sample','Host is not identical to playing in home country/venue'),
      ('Number of earlier completed WC matches, count','Chronological master results, strictly earlier dates','Tournament experience/exposure','Yes — earlier fixtures only','No','Closely related to stage and goals-conceded total','Training max 3; test max 7'),
      ('Cumulative goals conceded in earlier completed WC fixtures, goals','Chronological master scores, strictly earlier dates','Defensive tournament record','Yes — excludes current match','Concept overlap — prior goals conceded','Conceptually resembles 2.1 last-5 goals conceded (X4)','Different window/aggregation, but shared defensive-concession concept; rubric clarification needed'),
    ]
    pd.DataFrame([{'code':CODES[i],'column_name':FEATURES[i],'definition_units':v[0], 'construction':v[1],
       'predictive_rationale':v[2],'pre_match_availability':v[3],'shared_with_2_1':v[4],
       'redundancy':v[5],'limitations':v[6]} for i,v in enumerate(rationale)]).to_csv(out/'Objective_2_2_Feature_Justification.csv',index=False)
    # Graphs: professional, non-deceptive scales, >=300 DPI
    plt.rcParams.update({'font.size':9,'axes.titlesize':11,'axes.labelsize':9,'savefig.dpi':320,'axes.spines.top':False,'axes.spines.right':False})
    navy='#24435B';cyan='#2D8294';amber='#B57C34';grey='#697988'
    fig,ax=plt.subplots(figsize=(7.25,3.85)); colors=[navy if x<=2 else cyan for x in target_counts.index]
    rect=ax.bar(target_counts.index,target_counts.values,color=colors,width=.73)
    ax.bar_label(rect,padding=3,fontsize=8);ax.set(xlabel='Goals scored by one team in one match',ylabel='Team-match observations',title='Figure A. Distribution of goals scored (208 team-match rows)')
    ax.set_xticks(target_counts.index);ax.set_ylim(0,max(target_counts.values)*1.16)
    ax.text(.99,.98,f'Mean = {df.goals_scored.mean():.2f} goals',transform=ax.transAxes,ha='right',va='top',fontsize=8,color=grey)
    fig.tight_layout();fig.savefig(figures/'figA_goals_scored_distribution.png',dpi=320);plt.close(fig)
    fig,ax=plt.subplots(figsize=(9.0,6.9)); arr=corr_train.to_numpy()
    im=ax.imshow(arr,vmin=-1,vmax=1,cmap='RdBu_r',aspect='equal')
    labels=[*CODES,'Goals scored'];ax.set_xticks(range(9),labels,rotation=48,ha='right');ax.set_yticks(range(9),labels)
    for i in range(9):
        for j in range(9):
            value=arr[i,j];ax.text(j,i,f'{value:+.2f}',ha='center',va='center',fontsize=8,color='white' if abs(value)>.62 else '#1B2733')
    ax.set_title('Figure B. Pearson correlations — training data only (n = 164)',pad=15)
    fig.colorbar(im,ax=ax,fraction=.046,pad=.03,label='Pearson correlation')
    fig.tight_layout();fig.savefig(figures/'figB_train_correlation_heatmap.png',dpi=320);plt.close(fig)
    fig,ax=plt.subplots(2,2,figsize=(10,7.3));axs=ax.ravel()
    for axx,col,title in zip(axs[:2],['team_elo_rating_before','team_last5_avg_goals_scored'],['Pre-match Elo','Previous-five average goals']):
        axx.scatter(df[col],df.goals_scored,alpha=.33,s=22,color=navy,linewidths=0)
        axx.set(xlabel=title,ylabel='Actual goals scored',title=title)
    for axx,col,title,labs in [(axs[2],'is_knockout','Scheduled stage',['Group','Knockout']),
                                (axs[3],'is_host_nation','Host nationality',['Non-host','Host'])]:
        vals=[df.loc[df[col]==k,'goals_scored'] for k in [0,1]]
        axx.boxplot(vals,positions=[0,1],widths=.48,patch_artist=True,boxprops={'facecolor':'#DCE6ED'},medianprops={'color':amber})
        axx.set_xticks([0,1],labs);axx.set(xlabel=title,ylabel='Actual goals scored',title=title)
        for k,series in enumerate(vals):axx.text(k,max(df.goals_scored)+.2,f'n={len(series)}',ha='center',fontsize=8,color=grey)
    for a in axs:a.set_ylim(bottom=-.3,top=max(df.goals_scored)+.75)
    fig.suptitle('Figure C. Selected features and observed goals (descriptive; all 208)',fontsize=13)
    fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(figures/'figC_features_vs_goals_scored.png',dpi=320);plt.close(fig)
    fig,axs=plt.subplots(1,3,figsize=(11.0,3.85))
    cut=pd.crosstab(preds.data_split,preds.is_knockout).reindex(['train','test'],fill_value=0)
    xpos=np.arange(2);axs[0].bar(xpos,cut.get(0,pd.Series([0,0])).values,color=navy,label='Group');axs[0].bar(xpos,cut.get(1,pd.Series([0,0])).values,bottom=cut.get(0,pd.Series([0,0])).values,color=amber,label='Knockout')
    axs[0].set_xticks(xpos,['Train','Test']);axs[0].set(title='Scheduled match stage',ylabel='Team observations');axs[0].legend(fontsize=8)
    a=train.wc_matches_played_before.value_counts().sort_index();b=test.wc_matches_played_before.value_counts().sort_index();bins=sorted(set(a.index)|set(b.index));xs=np.arange(len(bins))
    axs[1].bar(xs-.2,[a.get(i,0) for i in bins],width=.4,color=navy,label='Train');axs[1].bar(xs+.2,[b.get(i,0) for i in bins],width=.4,color=amber,label='Test')
    axs[1].set_xticks(xs,bins);axs[1].set(title='Prior completed WC matches',xlabel='Count',ylabel='Team observations');axs[1].legend(fontsize=8)
    axs[2].boxplot([train.team_elo_rating_before,test.team_elo_rating_before],positions=[0,1],tick_labels=['Train','Test'],patch_artist=True,boxprops={'facecolor':'#DCE6ED'},medianprops={'color':amber})
    axs[2].set(title='Pre-match Elo by partition',ylabel='Elo rating')
    fig.suptitle('Figure D. Chronological train/test distribution shift',fontsize=13)
    fig.tight_layout(rect=[0,0,1,.94]);fig.savefig(figures/'figD_train_test_shift.png',dpi=320);plt.close(fig)
    # detailed report, avoid claiming factual verification from internal computations
    r=lambda col: [round(float(corr_train.loc[col,GOAL]),3),round(float(corr_all.loc[col,GOAL]),3)]
    highest=sorted(zip(FEATURES,vif),key=lambda it:it[1],reverse=True)
    dev_status='REVISION REQUIRED' if not errors else 'REVISION REQUIRED — data integrity also failed'
    report=f'''# Objective 2.2 — Targeted EDA, Feature Selection and Methodological Audit

**Decision: {dev_status}.** Source files inspected read-only. All quantitative calculations below are derived from the supplied 208-row dataset, source master, model outputs and Part 3 evaluation files. No model was retrained.

## 1. Confirmed dataset and construction

- Team-match observations: **{len(df)}**, representing **{df.match_id.nunique()} unique football matches**, two linked team rows per match; not 208 independent fixtures.
- Exactly **8 explanatory variables** and one non-negative whole-number goal target. All model input columns contain numeric, nonmissing values. Duplicate match-side records: **{int(df.duplicated(['match_id','side']).sum())}**.
- Team names, opponents, sides, dates and actual goals are consistent with the supplied master workbook: **{len(target_mismatch)+len(team_mismatch)+len(date_mismatch)+len(stage_mismatch)}** mismatches. Uploaded master matches model's source master on all compared modelling fields: **{'yes' if not unequal else 'no'}**.
- X1–X4 team-level data match supporting X1_X2_Inputs and X3_X5_Detail sheets: **{len(support_errors)} mismatches**. For cumulative features X7–X8, the source scores reconstruct each prior-day historical count/total exactly: **{len(cumulative_errors)} mismatches**.
- Previous-five detailed evidence has **{evidence_report['evidence_rows']} records**. Of 208 team histories, **{evidence_report['evidence_five_history_groups']}** have exactly five source observations; historical date-order failures: **{evidence_report['historical_date_violations']}**; reconstructed goals-average mismatches: **{evidence_report['evidence_avg_goals_inconsistent']}**; win-rate mismatches: **{evidence_report['evidence_win_rate_inconsistent']}**.
- Stage flag matches recorded group/knockout stage, and host flag equals Mexico/Canada/USA: **passed**. The host feature identifies team nationality, not confirmed venue-based home advantage.
- **Source verification boundary:** spreadsheet reconciliation and chronology are computationally verified. Federation/FIFA ranking releases, Elo-provider history and third-party international-results records are documented inputs, **not externally authenticated in this audit**.

## 2. Feature-reuse requirement — CRITICAL

The four explicitly reused concepts are FIFA ranking, Elo rating, previous-five average goals scored, and previous-five win rate (X1–X4). The new *knockout*, *host*, and *World Cup matches played* features are distinct. However, **X8 cumulative World Cup goals conceded uses the same substantive goals-conceded defensive statistic as Objective 2.1's X4 (previous-five average goals conceded difference)**. Different windows (World Cup cumulative vs last five), and differences versus team-level measurement, do not automatically make the concepts distinct. On a strict maximum-four-shared-*concepts* reading, this creates a **potential fifth overlap** and prevents unqualified certification of the requirement. **Required action:** confirm acceptance with lecturer/rubric; if counted as shared, the model owner must propose a different genuinely distinct pre-kickoff eighth feature and rerun only the necessary future modelling/review stages with training-only selection. No feature was changed here.

## 3. Descriptive EDA (208 team-match observations)

- Goals scored distribution: {', '.join(f'{k}: {v} ({v/len(df)*100:.1f}%)' for k,v in target_counts.items())}.
- Mean goals: **{df.goals_scored.mean():.3f}**, sample SD: **{df.goals_scored.std(ddof=1):.3f}**, range: **{df.goals_scored.min()}–{df.goals_scored.max()}**. For grouped stage breakdown, the observed mean is **{df[df.is_knockout==0].goals_scored.mean():.3f}** for group-stage team rows (n={int((df.is_knockout==0).sum())}) and **{df[df.is_knockout==1].goals_scored.mean():.3f}** for knockout team rows (n={int((df.is_knockout==1).sum())}). This is descriptive, not a causal stage effect.
- Host observations: **{int(df.is_host_nation.sum())}/{len(df)} ({df.is_host_nation.mean()*100:.1f}%)**. The host indicator and stage indicator are binary; zero-heavy early cumulative histories and 0.2-step last-five win rates have limited/discrete variation.
- All predictor means, SDs and quantiles are in `Objective_2_2_EDA_Summary.csv`; frequency counts in `Goals_Scored_Frequency.csv`.
- Training-only IQR flags for numerical candidate features (binary flags excluded): **{len(outlier_rows)} feature-row flags**. IQR flags indicate candidates for checking, not bad data or automatic removals. They are recorded in `Training_IQR_Flags.csv`. Full-sample EDA is descriptive only.
- All-data Pearson correlations with goals scored: {', '.join(f'{CODES[i]} = {corr_all.loc[c,GOAL]:+.3f}' for i,c in enumerate(FEATURES))}. These are marginal associations, not significance tests, causation or guaranteed incremental effects.

## 4. Train/test distribution and generalisation — MODERATE

The existing date boundary is **{test.match_date.min().date().isoformat()}**, with 164 training rows (82 matches) and 44 test rows (22 matches). Both sides of every match remain in the same partition. Training has **{int((train.is_knockout==0).sum())} group and {int((train.is_knockout==1).sum())} knockout** team rows; testing has **{int((test.is_knockout==0).sum())} group and {int((test.is_knockout==1).sum())} knockout** rows. The knockout indicator does vary in training, but only {100*train.is_knockout.mean():.1f}% of training rows are knockout compared with 100% in testing.

Host nation rows: **{int(train.is_host_nation.sum())} train** and **{int(test.is_host_nation.sum())} test**; this small sample limits a stable separate host effect. World Cup matches played before the fixture range **{int(train.wc_matches_played_before.min())}–{int(train.wc_matches_played_before.max())} in training** versus **{int(test.wc_matches_played_before.min())}–{int(test.wc_matches_played_before.max())} in testing**, leaving **{int(((test.wc_matches_played_before<train.wc_matches_played_before.min())|(test.wc_matches_played_before>train.wc_matches_played_before.max())).sum())} test rows outside the training range**. Elo additionally has **{int(((test.team_elo_rating_before<train.team_elo_rating_before.min())|(test.team_elo_rating_before>train.team_elo_rating_before.max())).sum())} test rows beyond the observed training range**. This is direct evidence of covariate shift/extrapolation risk, not proof any single variable caused poor performance. See `Train_Test_Feature_Shift.csv`.

## 5. Correlation, redundancy and VIF (training only)

Predictor correlations from 164 train rows: rank vs Elo **{corr_train.loc['team_fifa_rank','team_elo_rating_before']:+.3f}**, goals-scored form vs win rate **{corr_train.loc['team_last5_avg_goals_scored','team_last5_win_rate']:+.3f}**, prior WC matches vs cumulative WC conceded **{corr_train.loc['wc_matches_played_before','wc_goals_conceded_before']:+.3f}**; knockout vs prior WC matches **{corr_train.loc['is_knockout','wc_matches_played_before']:+.3f}**. VIF from auxiliary least-squares regressions **with an intercept**: {', '.join(f'{CODES[FEATURES.index(c)]} {v:.2f}' for c,v in highest)}. VIF was independently cross-checked against the diagonal of the inverse training predictor-correlation matrix. Interpret thresholds above 5 as a prompt for investigation, not an instruction to delete any predictor. Neither pairwise correlation nor VIF establishes independent predictive contribution.

## 6. Saved model results — MODERATE limitation

From saved `Predictions.csv` and `Metrics.csv` (no new fitting): **test MAE {mt['test_MAE']:.3f} goals**, **RMSE {mt['test_RMSE']:.3f} goals**, and **R² {mt['test_R2']:.3f}**. Training R² is **{mt['train_R2']:.3f}**. The saved mean-predictor baseline has test MAE **{mt['test_mean_baseline_MAE']:.3f}** and RMSE **{mt['test_mean_baseline_RMSE']:.3f}**. Recomputed saved-prediction metric discrepancies are below **{max(saved_metric_diffs.values()):.2e}**.

Part 3 evaluation reports the supplied OLS test MAE/RMSE/R² as **{mt['test_MAE']:.3f}/{mt['test_RMSE']:.3f}/{mt['test_R2']:.3f}**. Its saved Ridge result is **MAE {ridge['MAE']:.3f}, RMSE {ridge['RMSE']:.3f}, R² {ridge['R2']:.3f}** and Lasso **MAE {lasso['MAE']:.3f}, RMSE {lasso['RMSE']:.3f}, R² {lasso['R2']:.3f}**; Part 3 reports a training-CV-selected **{eval_detail['cv_selected_model']} alpha {eval_detail['cv_selected_alpha']}**. These are **existing evaluation outputs**, not newly fitted or selected models in this audit. Avoid using final test performance to select explanatory variables.

## 7. Recommendations by severity

- **CRITICAL — Shared-feature rule:** Obtain written clarification of whether cumulative prior WC goals conceded counts as the same goals-conceded concept as Objective 2.1. A strict reading implies five shared concepts. Affected: Objective 2.2 predictor definition, `Regression_2_2.py`, dataset and saved fitted model **if** replacement is needed; no changes made here.
- **MODERATE — Distribution shift:** Training covers only 10 knockout matches (20 team rows), while test covers 22 knockout matches. 32 test rows exceed the training experience range. Report this and interpret performance as later-stage generalisation, not uniform performance across the tournament. Affected: final 4-page Word report/methodology language, not current data.
- **MODERATE — Provenance:** X1–X4 rolling historical source data are computationally reconciled but official date-specific publications and every source match were not independently authenticated here. Affected: dataset methodology/evidence statement and source documentation; investigate records if independent audit finds conflict.
- **MINOR — Observational dependence and count outcome:** Each fixture contributes two related team rows; goals are discrete and non-negative while ordinary linear regression is unbounded. Avoid treating 208 rows as independent matches or interpreting coefficients causally. Affected: final report limitations and later statistical inference.

## 8. Recommended illustration and academic disclosure

Prefer **Figure D (Training vs Testing Feature Distributions)** in the four-page report: it conveys the large knockout/experience shift underlying limited generalisation. Figure A is a good alternative when the section emphasises the outcome distribution. Figure B is training-only by design; Figure C is descriptive and uses all 208 observations. All at 320 DPI.

**AI assistance:** A generative AI system assisted in inspecting the provided source files, drafting auditing code and source classifications, carrying out calculations, generating graphics and preparing the written interpretation. Source-book numerical reconciliation and script tests are independently reproducible; **external publication authenticity and every historical entry were not independently verified by those tests**. No original workbook, source ZIP, model output or past project file was altered. No model was retrained, tuned or replaced.
'''
    (out/'Objective_2_2_Methodological_Audit.md').write_text(report,encoding='utf-8')
    # structured outputs for independent review
    detailed={'decision':dev_status,'errors':errors,'warnings':warnings,'rows':len(df),'matches':df.match_id.nunique(),
        'evidence':evidence_report,'source_master_equal':not unequal,'training_matches':int(split_count.loc['train','matches']),
        'test_matches':int(split_count.loc['test','matches']), 'vif':dict(zip(FEATURES,vif.tolist())),
        'main_metrics':{k:mt[k] for k in ('test_MAE','test_RMSE','test_R2')},'training_iqr_flags':len(outlier_rows),
        'original_master_sha256':filehash(args.master_xlsx)}
    (out/'audit_checks.json').write_text(json.dumps(detailed,indent=2,default=str),encoding='utf8')
    if errors:raise AssertionError('AUDIT INTEGRITY ERRORS: '+str(errors))
    print('OK 208 team rows / 104 matches, 8 predictors; prior WC histories match source; saved metrics verified.')
    print('Train/test',len(train),len(test),'Training VIF',dict(zip(CODES,np.round(vif,3))))
    print('Evidence',evidence_report,'IQR flags',len(outlier_rows),'Decision',dev_status)
    return detailed

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--model-zip',default='Regression_2_2_Final (2(1).zip')
    p.add_argument('--master-xlsx',default='FIFA_WC2026_All_8_Variables_Master_Consistent_Formatting(2).xlsx')
    p.add_argument('--evaluation-zip',default='Part3_Evaluation(1).zip')
    p.add_argument('--output-dir',default='audit_out')
    args=p.parse_args()
    audit(args)
