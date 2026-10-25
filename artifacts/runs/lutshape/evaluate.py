#!/usr/bin/env python3
"""Evaluate the unchanged job gates; retain the broader B13 tool's FAIL."""
import json,pathlib,re,sys
root=pathlib.Path(__file__).resolve().parent
result={}
for phase in ['before','final']:
 read=lambda name:(root/phase/(name+'.txt')).read_text()
 checks={g:bool(re.search(r'^'+g+r' PASS\b',read('space'),re.M)) for g in ['G1','G2','G3','G4','G5','G6','B19']}
 b13=re.search(r'^B13 (PASS|FAIL).*? (\d+)/64 judged',read('B13'),re.M)
 checks['B13_job_floor']=bool(b13 and int(b13[2])>=60)
 checks['B17']=bool(re.search(r'^B17 PASS\b',read('B17'),re.M))
 checks['replay']=bool(re.search(r'0 unchecked, 0 skipped \(time\), 0 regression',read('replay')))
 if phase=='before':
  rows=json.loads((root/phase/'test-results.json').read_text())
  checks['release_tests']=bool(len(rows)==32 and all(r['exit']==0 for r in rows))
  counts=[sum(int(c[i]) for r in rows for c in r['counts']) for i in range(3)]
 else:
  cargo=json.loads((root/'final-cargo-summary.json').read_text())
  checks['release_tests']=cargo['observed_exec_exit']==0 and cargo['passed_failed_ignored']==[158,0,3] and cargo['max_test_wall_s']<60
  counts=cargo['passed_failed_ignored']
 for flight in ['coast','burn']:
  text=read('n1000000_'+flight)
  line=re.findall(r'^ladder:.*$',text,re.M)[-1]
  v=dict(re.findall(r'(\w+)=([^ ]+)',line))
  checks['N1_'+flight]=v['frames']=='1200' and v['truncated']=='false' and v['refusals']=='0' and v['over']=='0' and float(v['max_ms'])<=12 and float(v['lag_s'])==0 and 'frames behind: 0,' in text
 result[phase]={'qualifies':all(checks.values()),'checks':checks,'release_passed_failed_ignored':counts,'B13_tool':b13[1] if b13 else 'MISSING','B13_judged':int(b13[2]) if b13 else None,'B17_status':'PASS' if checks['B17'] else 'TIMEOUT' if 'exit=124' in read('B17') else 'FAIL'}
(root/'verdict.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(0 if result['final']['qualifies'] else 1)
