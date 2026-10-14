import json, sys, collections, statistics as st
rows = json.loads(open(sys.argv[1]).read().replace('},\n]', '}\n]'))
n = len(rows)
stage = collections.Counter(r['refused'].split(' ',1)[1].split(':')[0] if r['refused']!='None' else 'ok' for r in rows)
print(f"chains={n} refusal_stages={dict(stage)}")
done = [r for r in rows if r['refused']=='None']
uniq = [r for r in done if r['unique']>=60]
print(f"done={len(done)} unique>=60 (no key repeat)={len(uniq)} cyclic={sum(1 for r in done if r['cycle'])}")
# position magnitude in quanta ~ 2^(60-shift): relative drift = dstate/2^(60-shift)
for s in (0,4,8):
    sub=[r for r in done if f"_s{s}_" in r['cfg']]
    rel=[r['dstate_quanta']/float(1<<(60-s)) for r in sub]
    dw=[r['dw_max']/2**32 for r in sub]
    dk=[r['dk_max'] for r in sub]
    q=lambda x:(min(x), st.median(x), max(x))
    a,b,c=q(rel); d,e,f=q(dw); g,h,i=q(dk)
    print(f"shift+{s}: n={len(sub)} rel_drift min/med/max = {a:.2e}/{b:.2e}/{c:.2e}  dw/cross turns = {d:.2e}/{e:.2e}/{f:.2e}  dk_max ulp = {g}/{h}/{i}")
    directed=[r for r in sub if r['signed']>=0.9 and r['dk_max']>4]
    print(f"  directed k-walks (signed>=0.9, dkmax>4): {len(directed)}")
p1=[r for r in done if r['p1']]
print(f"P1 reconstruct exact left inverse: {len(p1)}/{len(done)}")
p2=[r['p2_dk'] for r in done if r['p2_dk']>0]
print(f"P2 kick control: n={len(p2)} min={min(p2)} max={max(p2)} Q48 ulps")
