import json, re
rows={}
for ln in open("decisive.jsonl"):
    m=re.match(r'"seed":"(\w+)",(.*)',ln.strip())
    if not m: continue
    d=json.loads(m.group(2))
    rows[(m.group(1),d["method"],d["steps"])]=d
seeds=["H1","H2","H3","H4","H5","B1"]
judged_out={"H3":"ejects <2048 orbits at 64/orbit; reference maxdJ 9.2e-3 (stability boundary)",
            "H4":"ejects before 4096 orbits even at the 1024/orbit reference",
            "B1":"reference pumps e 0.02->0.129 (6.4x e0): resonant/chaotic per the frozen rule"}
refs={s:rows.get((s,"kdk",1024)) for s in seeds}
ctrl={s:rows.get((s,"kdk",64)) for s in seeds}
def gates(s,meth,st):
    r=refs[s]; c=ctrl[s]; d=rows[(s,meth,st)]
    if not r or not c: return None,None,None,None
    dom = abs(d["domdt"]-r["domdt"])<=0.10*abs(r["domdt"])
    em  = d["emax"]<=max(1.2*r["emax"],1.2*d["e0"]+0.02)
    jd  = d["maxdJ"]<=10*c["maxdJ"]
    return dom,em,jd,(dom and em and jd)
print(f"{'seed':4} {'cfg':>10} {'dom%':>8} {'emax/ref':>9} {'dJ/ctrl':>8}  verdict")
alive=[s for s in seeds if s not in judged_out]
for s in alive:
    for meth,st in [("kdk",k) for k in (64,32,16,8,4,2)]+[("y4",k) for k in (8,4,2)]:
        if (s,meth,st) not in rows: continue
        r,c,d=refs[s],ctrl[s],rows[(s,meth,st)]
        dom,em,jd,p=gates(s,meth,st)
        dp=100*(d["domdt"]-r["domdt"])/abs(r["domdt"])
        print(f"{s:4} {meth}-{st:<7} {dp:8.1f} {d['emax']/max(r['emax'],1e-9):9.3f} {d['maxdJ']/c['maxdJ']:8.1f}  {'PASS' if p else 'fail'}"
              +"" if p else f"   <- dom={dom} em={em} dJ={jd}")
# minimum uniform kdk cadence across alive seeds
for k in (64,32,16,8,4,2):
    ps=[gates(s,"kdk",k)[3] for s in alive if (s,"kdk",k) in rows]
    if all(ps): print(f"minimum uniform kdk cadence passing all non-resonant seeds: {k}/orbit (gain {64/k:.0f}x)"); break
else: print("no uniform cadence below 64 passes everywhere: 64 stays")
