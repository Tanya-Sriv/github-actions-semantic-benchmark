#!/usr/bin/env python3
from pathlib import Path
import csv,json,sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen_prototype'))
from artifact_flow.analyzer import analyze_workflow
manifest=list(csv.DictReader((ROOT/'holdout-manifest.csv').open(encoding='utf-8')))
rows=[]; findings=[]
for case in manifest:
    path=ROOT/case['workflow_file']
    report=analyze_workflow(path)
    observed=sorted({f['rule_id'] for f in report['findings']})
    expected=sorted(x for x in case['expected_rules'].split(';') if x)
    match=observed==expected
    rows.append({**case,'observed_rules':';'.join(observed),'finding_count':len(report['findings']),'oracle_match':match})
    for f in report['findings']:
        findings.append({'case_id':case['case_id'],'label':case['label'],**f})

def positive(r): return bool(r['expected_rules'])
def observed(r): return bool(r['observed_rules'])
tp=sum(positive(r) and observed(r) for r in rows)
fn=sum(positive(r) and not observed(r) for r in rows)
fp=sum((not positive(r)) and observed(r) for r in rows)
tn=sum((not positive(r)) and (not observed(r)) for r in rows)
rule_exact=sum(r['oracle_match'] for r in rows)
summary={
 'prototype_version':'0.1-frozen',
 'holdout_cases':len(rows),
 'positive_cases':sum(positive(r) for r in rows),
 'negative_cases':sum(not positive(r) for r in rows),
 'case_level_confusion_matrix':{'tp':tp,'fp':fp,'tn':tn,'fn':fn},
 'case_level_precision':tp/(tp+fp) if tp+fp else None,
 'case_level_recall':tp/(tp+fn) if tp+fn else None,
 'case_level_specificity':tn/(tn+fp) if tn+fp else None,
 'exact_rule_oracle_matches':rule_exact,
 'exact_rule_oracle_match_rate':rule_exact/len(rows),
 'all_oracles_matched':all(r['oracle_match'] for r in rows),
 'false_positive_cases':[r['case_id'] for r in rows if not positive(r) and observed(r)],
 'false_negative_cases':[r['case_id'] for r in rows if positive(r) and not observed(r)],
 'claim_boundary':'Rules were frozen before the holdout cases were evaluated. Results apply to this designed holdout set and do not establish population-level accuracy.'
}
with (ROOT/'results'/'holdout-evaluation-matrix.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(ROOT/'results'/'holdout-findings.json').write_text(json.dumps(findings,indent=2)+'\n')
(ROOT/'results'/'holdout-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
