#!/usr/bin/env python3
"""Analysis for run 20261009-2212-dynamics-79ef: encounter-stream statistics."""
import json, math, sys, os
import numpy as np

ORBIT = 2*math.pi
WORK = "/home/glmlab/actions-runner/_work/emergent-space-engine/lab-3/lab/results/20261009-2212-dynamics-79ef/work/"

def load_ev(tag):
    d = np.loadtxt(WORK+f"{tag}_ev.tsv", skiprows=2)
    return d  # cols: t i j dRH a1b e1b a1a e1a a2b e2b a2a e2a

def load_out(tag):
    d = np.loadtxt(WORK+f"{tag}_out.tsv", skiprows=1)
    return d  # t e_rms _ bound dE

def rate_curve(ev, N, tmax, bin_orb=5.0):
    edges = np.arange(0, tmax/ORBIT+bin_orb, bin_orb)
    h,_ = np.histogram(ev[:,0]/ORBIT, bins=edges)
    return edges[:-1]+bin_orb/2, h/(N*bin_orb)  # events per body per orbit

def lambda_stat(ev, N, lo=50, hi=150):
    m = (ev[:,0]/ORBIT>=lo)&(ev[:,0]/ORBIT<hi)
    return m.sum()/(N*(hi-lo))

def branching(ev, N, lam_s, taus_orb=(0.5,1.0,2.0), boot=2000, rng=None):
    rng = rng or np.random.default_rng(7)
    per = {}
    # per-body streams
    streams = {}
    for k in (1,2):
        for b,t in zip(ev[:,k].astype(int), ev[:,0]):
            streams.setdefault(b, []).append(t)

    for tau in taus_orb:
        w = tau*ORBIT
        cnts = []
        for b,ts in streams.items():
            idx = np.searchsorted(ts, ts+w, side='right') - np.arange(len(ts))-1
            cnts.extend(idx.tolist())
        cnts = np.array(cnts, float)
        b_hat = cnts.mean()/(lam_s*tau) - 1.0
        bs = []
        for _ in range(boot):
            s = rng.choice(cnts, size=len(cnts), replace=True)
            bs.append(s.mean()/(lam_s*tau)-1.0)
        per[tau] = (b_hat, np.percentile(bs,2.5), np.percentile(bs,97.5))
    return per

def shuffle_control(ev, N, lam_s, taus_orb=(0.5,1.0,2.0), nrep=20):
    rng = np.random.default_rng(11)
    streams = {}
    for k in (1,2):
        for b,t in zip(ev[:,k].astype(int), ev[:,0]):
            streams.setdefault(b, []).append(t)
    out = {}
    for tau in taus_orb:
        vals=[]
        for rep in range(nrep):
            flat=[]
            for b in streams:
                ts = np.sort(np.array(streams[b]))
                if len(ts)<3: flat.append((b,ts)); continue
                gaps = np.diff(ts)
                rng.shuffle(gaps)
                ts2 = np.concatenate([[ts[0]], ts[0]+np.cumsum(gaps)])
                flat.append((b,ts2))
            w = tau*ORBIT; tot=[]
            for b,ts in flat:
                idx = np.searchsorted(ts, ts+w, side='right') - np.arange(len(ts))-1
                tot.extend(idx.tolist())
            vals.append(np.mean(tot)/(lam_s*tau)-1.0)
        out[tau] = (float(np.mean(vals)), float(np.std(vals)))
    return out

def clusters(ev, gap_orb=0.5):
    streams = {}
    for k in (1,2):
        for b,t in zip(ev[:,k].astype(int), ev[:,0]):
            streams.setdefault(b, []).append(t)
    sizes=[]
    for b in streams:
        ts=np.sort(np.array(streams[b]))
        if len(ts)==0: continue
        c=1
        for a,z in zip(ts[:-1],ts[1:]):
            if z-a> gap_orb*ORBIT: sizes.append(c); c=1
            else: c+=1
        sizes.append(c)
    sizes=np.array(sizes)
    mx=sizes.max()
    # geometric tail ratio: P(s) ~ (1-r) r^(s-1); r from P(s>=2)/P(s>=1)= mean(s>1 fraction)
    r = float((sizes>1).mean())
    return sizes, mx, r

def windows(ev, N, worb=10.0, lo=50, hi=150):
    nb = int((hi-lo)/worb)
    counts = np.zeros(N)
    allc=[]
    for _ in range(1): pass
    # counts per body per window, aggregated distribution
    per = np.zeros((N, nb))
    m=(ev[:,0]/ORBIT>=lo)&(ev[:,0]/ORBIT<hi)
    w_idx = ((ev[m,0]/ORBIT-lo)/worb).astype(int)
    np.clip(w_idx,0,nb-1,out=w_idx)
    for k in (1,2):
        bs = ev[m,k].astype(int)
        np.add.at(per, (bs, w_idx), 1)
    allc = per.ravel()
    med=np.median(allc[allc>0]) if (allc>0).any() else 0
    lam_w = allc.mean()
    p99=np.percentile(allc,99); p999=np.percentile(allc,99.9); mxm=allc.max()
    # Poisson synthetic same mean
    rng=np.random.default_rng(3)
    syn=rng.poisson(lam_w, size=len(allc))
    return dict(mean_window=float(lam_w), median_nonzero=float(med),
                p99=float(p99), p999=float(p999), max=float(mxm),
                poisson_p99=float(np.percentile(syn,99)), poisson_max=float(syn.max()),
                frac_zero=float((allc==0).mean()))

def e_fit(outd, lo=50, hi=150):
    t=outd[:,0]/ORBIT; e=outd[:,1]
    m=(t>=lo)&(t<=hi)
    if m.sum()<5 or e[m].min()<=0: return None
    sl=np.polyfit(np.log(t[m]), np.log(e[m]), 1)
    return float(sl[0]), float(e[m][0]), float(e[m][-1])

def main():
    res={}
    N=600
    for tag in ["r1","r2","r3","hot","w10","m8","w30"]:
        if not os.path.exists(WORK+f"{tag}_ev.tsv"): continue
        tmax=ev[:,0].max()
        lc_t,lc=rate_curve(ev,N,tmax)
        lam=lambda_stat(ev,N,50,150 if tag!="w30" else 180)
        ef=e_fit(outd)
        dE=outd[:,4].max()
        res[tag]=dict(n_events=int(len(ev)), lam_stat=float(lam),
                      e_growth=(ef if ef is None else dict(exp=ef[0], e_at_lo=ef[1], e_at_hi=ef[2])),
                      dE_max=float(dE),
                      rate_t0_50=float(lc[:10].mean()), rate_50_end=float(lc[10:].mean()),
                      e_rms_final=float(outd[-1,1]))
    # branching on baseline seeds
    for tag in ["r1","r2","r3","m8","w30"]:
        if tag not in res: continue
        lam=res[tag]["lam_stat"]
        res[tag]["branching"]={str(k):[float(x) for x in v] for k,v in branching(ev,N,lam).items()}
    ev=load_ev("r1")
    res["r1"]["shuffle"]={str(k):[float(x) for x in v] for k,v in shuffle_control(ev,N,res["r1"]["lam_stat"]).items()}
    for tag in ["r1","r2","r3"]:
        if tag not in res: continue
        sizes,mx,r=clusters(ev)
        res[tag]["clusters"]=dict(max=int(mx), tail_ratio=r,
                                  n_clusters=int(len(sizes)),
                                  hist={int(s):int((sizes==s).sum()) for s in range(1,min(6,mx)+1)},
                                  sizes_ge7=int((sizes>=7).sum()))
        res[tag]["windows"]=windows(ev,N)
    json.dump(res, open(WORK+"analysis.json","w"), indent=1)
    for tag in res:
        print(tag, json.dumps(res[tag], default=str)[:600])
main()
