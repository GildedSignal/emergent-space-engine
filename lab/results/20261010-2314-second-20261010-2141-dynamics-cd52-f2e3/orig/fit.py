#!/usr/bin/env python3
"""Fit growth laws from matrix2_raw.log + curves/; write results.json and print a summary."""
import json, math, os, re, statistics as st

R = {}
pat = re.compile(r"^(\S+) RESULT (\d+) ([\d.e-]+) ([\d.e-]+) ([\d.e-]+) ([\d.e-]+) (\d+) ([\d.e-]+) ([\d.e-]+) ([\d.e-]+) ([\d.e-]+) (\d+) (\d+)")
lines = [l for l in open("matrix2_raw.log") if l.startswith(("pos","neg","cad","n","m5n"))]
runs = []
for l in lines:
    m = pat.match(l.strip())
    if not m: continue
    g = m.groups()
    runs.append(dict(label=g[0], N=int(g[1]), mu=float(g[2]), spon=float(g[4]),
                     T=float(g[8]), lam_raw=float(g[7]), L=float(g[8-1]) if False else float(m.group(9)),
                     dH=float(g[10]), nren=int(g[11]), fb=int(g[12]), seed=int(g[7-0]) if False else int(g[6])))

def fit_curve(path):
    try: pts = [tuple(map(float, l.split())) for l in open(path) if l.strip()]
    except OSError: return None
    if len(pts) < 4: return None
    T = max(t for t,_ in pts)
    tail = [(t,L) for t,L in pts if t > 0.4*T]
    if len(tail) < 3: tail = pts
    ts = [p[0] for p in tail]; Ls = [p[1] for p in tail]
    def r2(x, y):
        n=len(x); mx=sum(x)/n; my=sum(y)/n
        sxy=sum((a-mx)*(b-my) for a,b in zip(x,y)); sxx=sum((a-mx)**2 for a in x); syy=sum((b-my)**2 for b in y)
        if sxx==0 or syy==0: return 0.0, 0.0
        b=sxy/sxx; a=my-b*mx
        ss=sum((y-(a+b*x))**2 for x,y in zip(x,y))
        return b, 1-ss/syy if syy>0 else 0.0
    b1, q1 = r2(ts, Ls)                 # L vs t   (exponential)
    lts = [math.log(max(t,1e-9)) for t in ts]
    b2, q2 = r2(lts, Ls)                # L vs ln t (algebraic)
    law = "exp" if q1 >= q2 - 0.02 and b1 > 0 else ("alg" if b2 > 0 else "flat")
    return dict(law=law, lam_exp=b1 if b1>0 else 0.0, gamma=b2 if b2>0 else 0.0,
                q_exp=q1, q_alg=q2, npts=len(pts), T=T)

groups = {}
for r in runs:
    c = fit_curve(f"curves/{r['label']}_s{r['seed']}.dat") or {}
    r.update(c); groups.setdefault(r["label"], []).append(r)

def med(rs, k): 
    v=[x[k] for x in rs if x.get(k) is not None]
    return st.median(v) if v else None

out = {"labels": {}}
print(f"{'label':10} {'N':>5} {'mu':>8} {'spon':>5} {'law':>5} {'lam_exp':>10} {'gamma':>7} {'lam_raw':>9} {'dH':>9} {'fb':>10} seeds")
for lab in sorted(groups):
    rs = groups[lab]
    laws = [x.get("law","?") for x in rs]
    row = dict(N=rs[0]["N"], mu=rs[0]["mu"], spon=rs[0]["spon"], law=st.mode(laws) if laws else None,
               lam_exp=med(rs,"lam_exp"), gamma=med(rs,"gamma"), lam_raw=med(rs,"lam_raw"),
               dH=med(rs,"dH"), fb=med(rs,"fb"), n=len(rs))
    out["labels"][lab] = row
    print(f"{lab:10} {row['N']:5} {row['mu']:8.0e} {row['spon']:5.0f} {str(row['law']):>5} "
          f"{(row['lam_exp'] or 0):10.4g} {(row['gamma'] or 0):7.3g} {row['lam_raw']:9.4g} "
          f"{row['dH']:9.2e} {int(row['fb'] or 0):10} {len(rs)}")

# E1: cadence ratio to truth (cad256), N=200 mu=1e-4
base = out["labels"].get("cad256", {}).get("lam_exp")
nbase = out["labels"].get("neg", {}).get("lam_exp") or 0.0
if base:
    print("\nE1 cadence (N=200, mu=1e-4): spon  lam_exp  ratio-to-truth256")
    cad = []
    for sp in [4,8,16,32,64,256]:
        v = out["labels"].get(f"cad{sp}", {}).get("lam_exp")
        if v is not None:
            cad.append((sp, v, v/base)); print(f"  {sp:5} {v:9.4g} {v/base:10.2f}")
    out["E1_cadence"] = cad
# E2: exponent of lam_excess vs N (mu=1e-4)
import math
pts = []
for nn in [50,100,200,400,800]:
    v = out["labels"].get(f"n{nn}", {}).get("lam_exp")
    if v is not None and v > nbase:
        pts.append((math.log(nn), math.log(v-nbase)))
if len(pts) >= 3:
    n=len(pts); mx=sum(p[0] for p in pts)/n; my=sum(p[1] for p in pts)/n
    b=sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts)
    syy=sum((p[1]-my)**2 for p in pts); ss=sum((p[1]-(my+b*(p[0]-mx)))**2 for p in pts)
    print(f"\nE2 N-scaling (mu=1e-4): alpha = {b:.3f}  (R2={1-ss/syy if syy else 0:.3f}), baseline neg lam_exp={nbase:.4g}")
    out["E2_alpha"] = b
json.dump(out, open("results.json","w"), indent=1)
print("\nwrote results.json")
