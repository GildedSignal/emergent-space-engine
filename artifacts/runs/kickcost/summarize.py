import json, pathlib, re
root=pathlib.Path(__file__).parent
out={}
for phase in ['before','lazy','shared','final']:
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
    out[phase]={'logs':result,'marginal_bytes':memory}
(root/'measurements.json').write_text(json.dumps(out,indent=2)+'\n')
for phase,result in out.items():
    print(phase,result['marginal_bytes'])
    for k,v in result['logs'].items():
        if k in ['space','plane','replay','digests','tests'] or k.startswith('rebind'):
            print(k,v)
