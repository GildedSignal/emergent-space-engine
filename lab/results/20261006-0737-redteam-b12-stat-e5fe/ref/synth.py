# What B12's exponent says about laws whose error is bounded by construction: planted errors on accurate trajectories.
import glob, numpy as np
def gexp(err):
    W=16; n=len(err); first=max(n//10,1)
    edge=lambda j: n if j==W else int(round(first*(n/first)**(j/W)))
    pts=[]
    for j in range(W):
        a,b=edge(j),edge(j+1)
        if b<=a: continue
        top=np.max(np.abs(err[a:b]))
        if top>0: pts.append((np.log(np.sqrt(a*(b-1))),np.log(top)))
    p=np.array(pts); return np.polyfit(p[:,0],p[:,1],1)[0]
rng=np.random.default_rng(1)
rows={'A bounded: 1e-7*(e(t)-e0)':[], 'B bounded: 1e-7*(a(t)-a0)/(R_H/sep)':[], 'C bounded: 1e-7*(1/r2(t) clipped)':[], 'D random walk per encounter':[], 'E drift':[]}
for f in sorted(glob.glob('runs/dump/truth_*.txt')):
    d=np.loadtxt(f); t,e,r,ecc,a=d[:,0],d[:,1],d[:,2],d[:,4],d[:,5]
    rows['A bounded: 1e-7*(e(t)-e0)'].append(gexp(1e-7*(ecc-ecc[0])/0.01))
    rows['B bounded: 1e-7*(a(t)-a0)/(R_H/sep)'].append(gexp(1e-7*(a-a[0])/0.0693))
    rows['C bounded: 1e-7*(1/r2(t) clipped)'].append(gexp(1e-7*(np.minimum(1/r,5)-min(1/r[0],5))))
    enc=np.concatenate([[0],np.diff((r<1).astype(int))==1])
    rows['D random walk per encounter'].append(gexp(1e-7*np.cumsum(enc*rng.normal(size=len(r)))))
    rows['E drift'].append(gexp(1e-9*np.arange(len(r))))
for k,v in rows.items(): print(f"{k:40s} median exponent {np.median(v):.3f}  (16 ships: {' '.join(f'{x:.2f}' for x in v)})")
