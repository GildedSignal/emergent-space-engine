import json, pathlib, re
root=pathlib.Path(__file__).parent
out={}
for phase in ['before','lazy','panels','shared','final']:
    d=root/phase
    if not d.exists(): continue
    result={}
    for p in sorted(d.glob('*.txt')):
        s=p.read_text(); result[p.stem]={'exit':re.findall(r'runner: exit=(\d+)',s), 'results':[x for x in s.splitlines() if x.startswith(('rebind:', 'ladder:', 'replay-all:', 'IDENTICAL:', 'schedule disagreements:', 'test result:')) or re.match(r'\s*(?:PASS|FAIL|G[1-6]|B13|B17|B19)\b',x)]}
    memory={}
    for flight in ['coast','burn']:
        zero=d/f'n0_{flight}.txt'
        if not zero.exists():continue
        def values(p):
            s=p.read_text()
            m=re.search(r'memory: n=\d+ build_peak=(\d+) end_peak=(\d+) end_current=(\d+)',s)
            return list(map(int,m.groups())) if m else None
        z=values(zero)
        for n in [100000,1000000]:
            p=d/f'n{n}_{flight}.txt'
            v=values(p) if p.exists() else None
            if z and v:memory[f'{n}_{flight}']=dict(zip(['birth_B','peak_B','end_B'],[(x-y)/n for x,y in zip(v,z)]))
    fit={}
    for n in [0,100000,1000000]:
        p=d/f'prof{n}.txt'
        if p.exists():
            text=p.read_text()
            row=next((x for x in text.splitlines() if 'fit: bind_surface' in x),None)
            if row: fit[str(n)]={'mean_us':float(row.split()[-1])/1000}
            part=next((x for x in text.splitlines() if x.startswith('fit_breakdown_us:')),None)
            if part and str(n) in fit:fit[str(n)]['components_us']=dict((k,float(v)) for k,v in re.findall(r'(\w+)=([\d.]+)',part))
    tests=None
    if (d/'test-results.json').exists():
        rows=json.loads((d/'test-results.json').read_text())
        tests={'passed_failed_ignored':[sum(int(c[i]) for r in rows for c in r['counts']) for i in range(3)],'bad_exits':sum(r['exit']!=0 for r in rows)}
    if tests is None and (d/'tests.txt').exists():
        counts=re.findall(r'test result: .*?(\d+) passed; (\d+) failed; (\d+) ignored;', (d/'tests.txt').read_text())
        tests={'passed_failed_ignored':[sum(int(c[i]) for c in counts) for i in range(3)],'aggregate_exit':'not recorded after session interruption'}
    out[phase]={'logs':result,'marginal_bytes':memory,'actual_fit_us':fit,'tests':tests}
(root/'measurements.json').write_text(json.dumps(out,indent=2)+'\n')
for phase,result in out.items():
    print(phase,'marginal bytes:',result['marginal_bytes'])
    print(phase,'flown FIT us:',result['actual_fit_us'],'tests:',result['tests'])
