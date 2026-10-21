#!/usr/bin/env python3
"""Exit by the user's frozen job criteria, retaining the underlying tool verdicts."""
import json,pathlib,re,sys
phase=sys.argv[1]
r=pathlib.Path(__file__).resolve().parent
d=r/phase
read=lambda name:(d/(name+'.txt')).read_text() if (d/(name+'.txt')).exists() else ''
checks={}
s=read('space')
for gate in ['G1','G2','G3','G4','G5','G6','B19']:
    checks[gate]=bool(re.search(r'^'+gate+r' PASS\b',s,re.M))
s=read('plane');b13=re.search(r'^B13 (?:PASS|FAIL).*? (\d+)/64 judged',s,re.M)
checks['B13_job_floor']=bool(b13 and int(b13[1])>=60)
checks['B17']=bool(re.search(r'^B17 PASS\b',s,re.M))
if (d/'test-results.json').exists():
    rows=json.loads((d/'test-results.json').read_text())
    built=(r/f'build-tests-{phase}.txt').read_text()
    expected=set(re.findall(r'Executable .+? \((target/release/deps/[^)]+)\)',built))
    checks['release_tests']=bool(expected and set(x['binary'] for x in rows)==expected and all(x['exit']==0 and x['counts'] and all(int(c[1])==0 for c in x['counts']) for x in rows))
else:
    counts=re.findall(r'test result: .*?(\d+) passed; (\d+) failed; (\d+) ignored;',read('tests'))
    checks['release_tests']=bool(counts and sum(int(x[0]) for x in counts)>0 and all(int(x[1])==0 for x in counts) and 'Doc-tests emergent_universe' in read('tests'))
s=read('replay')
asked=re.search(r'^replay-all:\s*(\d+) flight\(s\)',s,re.M)
checks['replay']=bool(asked and int(asked[1])>=3 and re.search(r'0 unchecked, 0 skipped \(time\), 0 regression',s))
s=read('digests')
checks['flight_digests']=('schedule disagreements: 0' in s and (phase=='shared' or bool(re.search(r'IDENTICAL:\s*8 flights',s))))
for flight in ['coast','burn']:
    s=read('n1000000_'+flight);lines=[x for x in s.splitlines() if x.startswith('ladder:')]
    v=dict(re.findall(r'(\w+)=([^ ]+)',lines[-1])) if lines else {}
    checks['N1_'+flight]=bool(v and v.get('n')=='1000000' and v.get('frames')=='1200' and v.get('truncated')=='false' and v.get('over')=='0' and float(v.get('max_ms','inf'))<=12 and float(v.get('lag_s','inf'))==0 and v.get('refusals')=='0' and 'frames behind: 0,' in s)
if phase=='final':
    c=json.loads((r/'final-cargo-summary.json').read_text())
    checks['exact_cargo_command']=c['observed_exec_exit']==0 and c['passed_failed_ignored']==[155,0,3]
result={'phase':phase,'meets_job_checks':all(checks.values()),'checks':checks}
(d/'evaluation.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
raise SystemExit(0 if result['meets_job_checks'] else 1)
