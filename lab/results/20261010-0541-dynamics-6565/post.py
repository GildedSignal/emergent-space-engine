import gzip
import numpy as np

def load(p, tb):
    raw = gzip.open(p + ".events.bin.gz","rb").read()
    a = np.frombuffer(raw, dtype=np.dtype([('t','<f4'),('i','<i4'),('j','<i4')]))
    t = a['t'].astype(float); m = t >= tb
    return t[m], a['i'][m], a['j'][m]
def burn(p):
    samp = np.loadtxt(p + ".samples.txt"); em = samp[:,1]; ts = samp[:,0]
    m = np.median(em[-len(em)//3:]); idx = np.where(np.abs(em/m - 1.0) < 0.15)[0]
    return ts[idx[0]]

def fano(t, W=1.0):
    nb = int((t[-1]-t[0])//W)
    if nb < 8: return None
    c,_ = np.histogram(t, bins=nb, range=(t[0], t[0]+nb*W))
    return c.var()/c.mean()

def branching(t, i, j, N, twin=30.0):
    n = len(t); bodies = {}
    for k in range(n):
        bodies.setdefault(i[k], []).append(t[k]); bodies.setdefault(j[k], []).append(t[k])
    for b in bodies: bodies[b] = np.sort(np.array(bodies[b]))
    tot = 0
    for k in range(n):
        for b in (i[k], j[k]):
            tb_ = bodies[b]
            tot += np.searchsorted(tb_, t[k]+twin) - np.searchsorted(tb_, t[k], side='right')
    base = 2 * (2*n/(t[-1]-t[0])/N) * twin
    return tot/n - base, tot/n, base

def drift_null_fano(t, Wl=2.0, reps=200, seed=11):
    rng = np.random.default_rng(seed)
    nb = int((t[-1]-t[0])//Wl)+1
    edges = t[0] + np.arange(nb+1)*Wl
    c,_ = np.histogram(t, bins=edges); lam = c/Wl
    out=[]
    for r in range(reps):
        ts=[]
        for k in range(len(lam)):
            n = rng.poisson(lam[k]*Wl)
            if n: ts.append(edges[k]+rng.uniform(0,Wl,n))
        ts=np.sort(np.concatenate(ts))
        f=fano(ts)
        if f: out.append(f)
    return np.quantile(out,[.05,.5,.95])

RUNS = [("t0005_s21",2000),("t002_s21",2000),("t002_s22",2000),("t01_s21",2000),
        ("t01_s22",2000),("t05n_s21",1000),("t20n_s21",1000),("t20n_s22",1000)]
TB  = {"t0005_s21":115.6,"t002_s21":129.1,"t01_s21":58.8}
rows=[]
for p,N in RUNS:
    tb = TB.get(p) or burn(p)
    t,i,j = load(p,tb)
    F = fano(t)
    lo,md,hi = drift_null_fano(t)
    b,obs,base = branching(t,i,j,N)
    cnt = np.bincount(np.concatenate([i,j]), minlength=N)
    med=np.median(cnt); p99=np.quantile(cnt,0.99)
    rows.append(f"{p:12s} n={len(t):7d} Fano={F:6.2f} driftNull[{lo:5.1f},{md:5.1f},{hi:5.1f}] "
                f"branch={b:+8.2f} (obs {obs:7.1f} base {base:7.1f}) "
                f"lam/body/orb={cnt.mean()/(t[-1]-t[0])*2*np.pi:7.2f} CV={cnt.std()/cnt.mean():4.2f} p99/med={p99/max(med,1):4.1f}")
with open("post_table.txt","w") as f:
    f.write("\n".join(rows)+"\n")
print("\n".join(rows))
