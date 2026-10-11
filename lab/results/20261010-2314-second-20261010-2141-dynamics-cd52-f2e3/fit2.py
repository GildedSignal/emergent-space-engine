#!/usr/bin/env python3
"""Fixed record regeneration for run 20261010-2141 (silver, checker defect #1).

The shipped fit.py matched matrix2 log labels to curves/{label}_s{seed}.dat -- the
*buggy-matrix* curves -- while matrix2.sh writes r_-prefixed curves from the corrected
binary. Its law/lam_exp entries therefore fitted pre-fix curves while lam_raw/dH/fb came
from corrected runs: a mix, and cad128 had no buggy curve at all (law "?", lam_exp null).

This fit2.py fits ONLY corrected curves:
  - shipped  : curves/r_{label}_s{seed}.dat   (from matrix2_raw.log rows)
  - this run : curves/r2_cad{sp}_s{sd}.dat    (corrected cad64/cad256 rerun, block A,
                logged to matrix2b_raw.log) -- completes E1's truth base.
Fit methodology (tail fit on t>0.4T, law classification, slopes) is UNCHANGED from the
shipped fit.py: only the curve provenance is fixed.
Outputs results2.json and prints the table. Fits run on the shipped curves; the two new
cadence cells are fitted on this run's curves.
"""
import json, math, os, re, statistics as st

R = {}
pat = re.compile(r"^(\S+) RESULT (\d+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) (\d+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) (\d+) (\d+)")
runs = []
labels_b = set()
for l in open("matrix2_raw.log"):
    m = pat.match(l.strip())
    if not m: continue
    g = m.groups()
    runs.append(dict(src="shipped", label=g[0], N=int(g[1]), mu=float(g[2]), spon=float(g[4]),
                     T=float(g[8]), lam_raw=float(g[7]), L=float(g[9]), seed=int(g[6]),
                     dH=float(g[10]), nren=int(g[11]), fb=int(g[12])))
try:
    for l in open("matrix2b_raw.log"):
        m = pat.match(l.strip())
        if not m: continue
        g = m.groups()
        runs.append(dict(src="rerun", label=g[0], N=int(g[1]), mu=float(g[2]), spon=float(g[4]),
                         T=float(g[8]), lam_raw=float(g[7]), L=float(g[9]), seed=int(g[6]),
                         dH=float(g[10]), nren=int(g[11]), fb=int(g[12])))
        labels_b.add(g[0])
except OSError:
    pass

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
    cands = [f"curves/r2_{r['label']}_s{r['seed']}.dat"] if r["label"] in labels_b \
            else [f"curves/r_{r['label']}_s{r['seed']}.dat"]
    c = None
    for p in cands:
        c = fit_curve(p)
        if c: c["curve"] = p; break
    if not c: c = dict(curve=None)
    r.update(c); groups.setdefault(r["label"], []).append(r)

def med(rs, k):
    v=[x[k] for x in rs if x.get(k) is not None]
    return st.median(v) if v else None

out = {"labels": {}}
print(f"{'label':10} {'src':>7} {'N':>5} {'mu':>8} {'spon':>5} {'law':>5} {'lam_exp':>10} {'lam_raw':>9} {'dH':>9} {'fb':>10} seeds curve")
for lab in sorted(groups):
    rs = groups[lab]
    laws = [x.get("law","?") for x in rs]
    row = dict(N=rs[0]["N"], mu=rs[0]["mu"], spon=rs[0]["spon"], law=st.mode(laws) if laws else None,
               lam_exp=med(rs,"lam_exp"), lam_raw=med(rs,"lam_raw"),
               dH=med(rs,"dH"), fb=med(rs,"fb"), n=len(rs),
               src=rs[0]["src"], curve=rs[0].get("curve"))
    out["labels"][lab] = row
    print(f"{lab:10} {row['src']:>7} {row['N']:5} {row['mu']:8.0e} {row['spon']:5.0f} {str(row['law']):>5} "
          f"{(row['lam_exp'] or 0):10.4g} {row['lam_raw']:9.4g} "
          f"{row['dH']:9.2e} {int(row['fb'] or 0):10} {len(rs)} {os.path.basename(row['curve'] or '-')}")

# E1: cadence (N=200, mu=1e-4) against the corrected cad256 truth base
base = out["labels"].get("cad256", {}).get("lam_exp")
if base:
    print("\nE1 cadence (N=200, mu=1e-4, corrected curves): spon  lam_exp  ratio-to-truth256")
    cad = []
    for sp in [8,32,64,128,256]:
        v = out["labels"].get(f"cad{sp}", {}).get("lam_exp")
        if v is not None:
            cad.append((sp, v, v/base)); print(f"  {sp:5} {v:9.4g} {v/base:10.2f}")
    out["E1_cadence"] = cad
# E2: exponent of lam_excess vs N (mu=1e-4) on corrected curves
nbase = out["labels"].get("neg", {}).get("gamma") or 0.0
pts = []
for nn in [50,100,200,400]:
    v = out["labels"].get(f"n{nn}", {}).get("lam_exp")
    if v is not None and v > (out["labels"].get("neg",{}).get("lam_exp") or 0.0):
        pts.append((math.log(nn), math.log(v - (out["labels"].get("neg",{}).get("lam_exp") or 0.0))))
if len(pts) >= 3:
    n=len(pts); mx=sum(p[0] for p in pts)/n; my=sum(p[1] for p in pts)/n
    b=sum((p[0]-mx)*(p[1]-my) for p in pts)/sum((p[0]-mx)**2 for p in pts)
    syy=sum((p[1]-my)**2 for p in pts); ss=sum((p[1]-(my+b*(p[0]-mx)))**2 for p in pts)
    print(f"\nE2 N-scaling (mu=1e-4, corrected curves): alpha = {b:.3f}  (R2={1-ss/syy if syy else 0:.3f})")
    out["E2_alpha"] = b
json.dump(out, open("results2.json","w"), indent=1)
print("\nwrote results2.json")
