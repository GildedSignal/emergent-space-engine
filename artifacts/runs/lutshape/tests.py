#!/usr/bin/env python3
"""The complete default suite, serial binaries, capped at 59 s; split a slow binary by test."""
import json,pathlib,re,subprocess,sys
phase=sys.argv[1]
root=pathlib.Path(__file__).resolve().parents[3]
log=(root/f'artifacts/runs/lutshape/build-tests-{phase}.txt').read_text()
binaries=re.findall(r'Executable (.+?) \((target/release/deps/[^)]+)\)',log)
results=[]
for label,binary in binaries:
    name='tests-'+pathlib.Path(binary).name
    status=subprocess.run(['python3','artifacts/runs/lutshape/run.py',phase,name,binary,'--test-threads=1']).returncode
    p=root/f'artifacts/runs/lutshape/{phase}/{name}.txt'
    s=p.read_text()
    if status==124:
        listed=subprocess.run([binary,'--list','--format=terse'],capture_output=True,text=True,check=True).stdout
        for test in [x[:-6] for x in listed.splitlines() if x.endswith(': test')]:
            exact=name+'-'+re.sub(r'[^\w.-]','_',test)
            ret=subprocess.run(['python3','artifacts/runs/lutshape/run.py',phase,exact,binary,'--exact',test,'--test-threads=1']).returncode
            text=(root/f'artifacts/runs/lutshape/{phase}/{exact}.txt').read_text()
            results.append(dict(binary=binary,test=test,exit=ret,counts=re.findall(r'test result: .*?(\d+) passed; (\d+) failed; (\d+) ignored;',text)))
    else:
        results.append(dict(binary=binary,label=label,exit=status,counts=re.findall(r'test result: .*?(\d+) passed; (\d+) failed; (\d+) ignored;',s)))
    (root/f'artifacts/runs/lutshape/{phase}/test-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('test_totals:',[sum(int(c[i]) for r in results for c in r['counts']) for i in range(3)],'bad_exits',sum(r['exit']!=0 for r in results),flush=True)
raise SystemExit(any(r['exit']!=0 for r in results))
