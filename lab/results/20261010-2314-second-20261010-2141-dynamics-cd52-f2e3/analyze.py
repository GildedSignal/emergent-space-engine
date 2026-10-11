#!/usr/bin/env python3
"""Decisive-matrix analysis: dt x N x mu scan of lambda_max at mu<=1e-5 with the
conjunction census as admission gate. Reads light_raw.log + heavy_raw.log, fits the
same tail-fit law as fit2.py on the r2_ curves, computes K = da/R_H, and prints the
prediction tests (P2-P8)."""
import math, re, statistics as st

pat = re.compile(r"^(\S+) RESULT (\d+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) (\d+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) (\d+) (\d+)")
cpat = re.compile(r"^(\S+) CONJ (\d+) ([\d.e+-]+) ([\d.e+-]+) (\d+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) ([\d.e+-]+) (\d+) (\d+) (\d+) (\d+)")

runs = {}
for fn in ["light_raw.log", "heavy_raw.log", "light2_raw.log", "heavy2_raw.log"]:
    try: lines = open(fn).read().splitlines()
    except OSError: continue
    for l in lines:
        m = pat.match(l)
        if m:
            g = m.groups()
            key = (g[0], int(g[6]))
            runs.setdefault(key, {})["res"] = dict(N=int(g[1]), mu=float(g[2]), spon=float(g[4]),
                T=float(g[9]), lam_raw=float(g[7]), dH=float(g[10]), nren=int(g[11]), fb=int(g[12]))
            continue
        m = cpat.match(l)
        if m:
            g = m.groups()
            key = (g[0], int(g[4]))
            runs.setdefault(key, {})["conj"] = dict(minr=float(g[5]), r_sqrt=float(g[6]),
                r_kill3=float(g[7]), rh=float(g[8]), n_sqrt=int(g[9]), n_kill3=int(g[10]),
                n_3rh=int(g[11]), n_10rh=int(g[12]))

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
    b1, q1 = r2(ts, Ls); lts=[math.log(max(t,1e-9)) for t in ts]
    b2, q2 = r2(lts, Ls)
    law = "exp" if q1 >= q2 - 0.02 and b1 > 0 else ("alg" if b2 > 0 else "flat")
    return dict(law=law, lam_exp=b1 if b1>0 else 0.0, q_exp=q1, q_alg=q2, npts=len(pts))

# attach curve fits: label pattern -> curve file name
def curve_for(label, seed):
    m = re.match(r"n(\d+)_s(\d+)", label)
    if m and m.group(1) == "800": return f"curves/r2_n800_s{m.group(2)}_{seed}.dat"
    if m: return f"curves/r2_n{m.group(1)}_s{m.group(2)}_{seed}.dat"
    m = re.match(r"h(\d+)", label)
    if m: return f"curves/r2_h{m.group(1)}_{seed}.dat"
    m = re.match(r"m([\d.e+-]+)_s(\d+)", label)
    if m: return f"curves/r2_m{m.group(1)}_s{m.group(2)}_{seed}.dat"
    return None

for (label, seed), d in runs.items():
    cf = curve_for(label, seed)
    d["fit"] = fit_curve(cf) if cf else None
    d["curve"] = cf

# group by cell
cells = {}
for (label, seed), d in sorted(runs.items()):
    cells.setdefault(label, []).append(d)

def K_of(N, mu):  # mean spacing in mutual Hill radii, a=1, width 0.1
    return (0.1/N) / pow(2.0*(mu/N)/3.0, 1.0/3.0)

print(f"{'cell':16} {'N':>4} {'mu':>8} {'spon':>5} {'T':>4} {'K':>6} | {'lam_exp med':>10} {'lam/2pi':>8} {'law':>4} | {'lam_raw':>8} {'dH':>8} {'fb':>7} | {'n_sqrt':>6} {'n_kill3':>7} {'minr':>9} seeds")
table = {}
for label in sorted(cells, key=lambda s: (len(s), s)):
    rs = cells[label]
    r0 = rs[0]["res"]; c0 = rs[0].get("conj", {})
    fits = [r["fit"] for r in rs if r["fit"]]
    lam = st.median([f["lam_exp"] for f in fits]) if fits else None
    law = st.mode([f["law"] for f in fits]) if fits else "?"
    N, mu, spon, T = r0["N"], r0["mu"], r0["spon"], r0["T"]
    K = K_of(N, mu)
    nrt = st.median([r["res"]["lam_raw"] for r in rs])
    dH  = st.median([r["res"]["dH"] for r in rs])
    fb  = st.median([r["res"]["fb"] for r in rs])
    nsq = sum(r.get("conj",{}).get("n_sqrt",0) for r in rs if "conj" in r)
    nk3 = st.median([r["conj"]["n_kill3"] for r in rs if "conj" in r]) if any("conj" in r for r in rs) else None
    minr= min(r["conj"]["minr"] for r in rs if "conj" in r) if any("conj" in r for r in rs) else None
    table[label] = dict(N=N, mu=mu, spon=spon, T=T, K=K, lam=lam, law=law, nrt=nrt, dH=dH, fb=fb, nsq=nsq, nk3=nk3, minr=minr, nseeds=len(rs))
    print(f"{label:16} {N:4} {mu:8.0e} {spon:5.0f} {T:4.0f} {K:6.3f} | "
          f"{(lam if lam is not None else float('nan')):10.4f} {(lam/(2*math.pi) if lam else float('nan')):8.3f} {law:>4} | "
          f"{nrt:8.4g} {dH:8.2e} {int(fb):7} | {nsq:6} {int(nk3 or 0):7} {(minr if minr else float('nan')):9.2e} {len(rs)}")

print("\n== per-seed (label seed lam_exp law fb dH n_sqrt minr) ==")
for (label, seed), d in sorted(runs.items()):
    f = d.get("fit"); c = d.get("conj", {}); r = d["res"]
    print(f"  {label:16} {seed} {(f['lam_exp'] if f else float('nan')):9.4f} {(f['law'] if f else '?'):>4} "
          f"{r['fb']:8} {r['dH']:9.2e} {c.get('n_sqrt','-'):>3} {c.get('minr',float('nan')):9.2e}")

print("\n== prediction tests ==")
def lam_of(label): return table.get(label, {}).get("lam")
# P2: dt-robustness at N=200, mu=1e-5, T=50
r64, r256, r1024 = lam_of("n200_s64"), lam_of("n200_s256"), lam_of("n200_s1024")
if r64 and r1024:
    print(f"P2  N=200 mu=1e-5: lam(s64)={r64:.3f} lam(s256)={r256:.3f} lam(s1024)={r1024:.3f}  "
          f"ratio 1024/64 = {r1024/r64:.2f}  -> {'HELD (dt-robust)' if 0.75 <= r1024/r64 <= 1.30 else 'FAILED'}")
# N=50 and N=800 dt-ratios
for nn in ["n50", "n800"]:
    a, b = lam_of(f"{nn}_s64"), lam_of(f"{nn}_s1024")
    if a and b: print(f"P2' {nn}: lam(s64)={a:.3f} lam(s1024)={b:.3f}  ratio = {b/a:.2f}")
# P3: level
ok3 = [ (l,v) for l,v in table.items() if v["lam"] and v["mu"]<=1e-5 and v["nsq"]==0 and v["T"]>=50 ]
if ok3:
    vals = [v["lam"]/(2*math.pi) for _,v in ok3]
    print(f"P3  gate-passing mu<=1e-5 cells: lam/2pi in [{min(vals):.3f},{max(vals):.3f}] "
          f"(pred [0.35,0.55]) -> {'HELD' if all(0.35<=x<=0.55 for x in vals) else 'FAILED'}  ({len(vals)} cells)")
# P4: mu-axis
l5, l6, l7 = lam_of("n200_s1024"), lam_of("m0.000001_s1024"), lam_of("m0.0000001_s1024")
if l5 and l6: print(f"P4  lam(1e-5)={l5:.3f} lam(1e-6)={l6:.3f} ratio={l6/l5:.2f} (>=0.6 held)"
                     + (f"  lam(1e-7)={l7:.3f} ratio={l7/l5:.2f}" if l7 else ""))
# P5: N-axis at spon 64 (same T? n800 is T=25; note)
a,b,c = lam_of("n50_s64"), lam_of("n200_s64"), lam_of("n800_s64")
if a and b and c: print(f"P5  N-axis s64: n50={a:.3f} n200={b:.3f} n800(T25)={c:.3f}")
# P6: gate vs fb
gate = [(l, v["nsq"], v["fb"]) for l,v in table.items() if v["mu"]<=1e-5]
bad = [(l,ns,fb) for l,ns,fb in gate if ns>0]
print(f"P6  mu<=1e-5 cells with gate failure (n_sqrt>0): {bad if bad else 'none'}")
# P7: fallback blindness
for l,v in table.items():
    pass
seen = {}
for (label, seed), d in runs.items(): seen.setdefault(label, []).append(d["res"]["fb"])
blind = [(l, fbs) for l, fbs in seen.items() if l.startswith("n") and "_s" in l and max(fbs)>0]
print(f"P7  cells with any fb>0 (by seed): {[(l, fbs) for l,fbs in blind] or 'none'}")
# P8: horizon
h64, h1024 = lam_of("h64"), lam_of("h1024")
if h64 and r64: print(f"P8  N=200 s64: lam(T25)={h64:.3f} lam(T50)={r64:.3f} ratio={h64/r64:.2f}"
                      + (f" | s1024: lam(T25)={h1024:.3f} lam(T50)={r1024:.3f} ratio={h1024/r1024:.2f}" if h1024 and r1024 else ""))
