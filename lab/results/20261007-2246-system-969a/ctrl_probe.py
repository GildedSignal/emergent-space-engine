"""Do the negative controls fire at a plane-like reach (R = 5e-3, ~2^10 x body radii)?
S8 spread belt, n=3000. Counts truth pairs by annulus gap: the window's job is pairs
with gap < R (only those can be within R); ctrlA drops the R-widening (must keep only
gap<=0 pairs -> misses the (0,R) shell), ctrlB drops the quantum widening."""
import importlib.util, json
import numpy as np
spec = importlib.util.spec_from_file_location("sp", "store_probe.py")
# reuse functions without re-running the module body: copy the pieces
TAU = 2*np.pi
def run(R, n, seed):
    rng = np.random.default_rng(seed)
    a = rng.uniform(0.7, 1.3, n); e = rng.rayleigh(0.05, n)
    pom = rng.uniform(0, TAU, n); M0 = rng.uniform(0, TAU, n)
    # truth via dense sampling
    S = 256; t = np.linspace(0, TAU, S, endpoint=False)
    n_ = a**-1.5
    M = M0[None,:] + n_[None,:]*t[:,None]
    E = M.copy()
    for _ in range(6): E = E - (E - e*np.sin(E) - M)/(1 - e*np.cos(E))
    r = a*(1 - e*np.cos(E)); nu = 2*np.arctan2(np.sqrt(1+e)*np.sin(E/2), np.sqrt(1-e)*np.cos(E/2))
    phi = nu + pom[None,:]
    pos = np.stack([r*np.cos(phi), r*np.sin(phi)], -1)
    truth = []
    for i in range(n-1):
        d = pos[:, i+1:, :] - pos[:, i, :][:, None, :]
        d2 = np.einsum("tsd,tsd->ts", d, d).min(axis=0)
        truth.extend((i, i+1+j) for j in np.nonzero(d2 < R*R)[0])
    # annuli (true, unquantized)
    rmin = a*(1-e); rmax = a*(1+e)
    def window_pairs(with_R, with_q):
        p = a*(1-e*e); g = (1-e)/(1+e)
        m, ex = np.frexp(p); mq = np.round(m*4096)
        p_q = mq*2.0**(ex-12); g_q = np.clip(np.round(g*4096),1,4096)/4096
        k_q = (1+g_q)/2; rperi = p_q*k_q; rapo = p_q*k_q/g_q
        lo, hi = rperi.copy(), rapo.copy()
        if with_q:
            qp = 2.0**-12; gg = rperi/rapo
            pad = rapo*(qp+qp/gg) + rperi*qp
            lo, hi = lo-pad, hi+pad
        if with_R: lo, hi = lo-R, hi+R
        u_lo, u_hi = 1/hi, 1/lo
        order = np.argsort(u_lo); lo_s, hi_s = u_lo[order], u_hi[order]
        pairs = set()
        for rk in range(n-1):
            stop = np.searchsorted(lo_s, hi_s[rk], side="right")
            for o in range(rk+1, stop):
                if hi_s[o] >= lo_s[rk]:
                    i, j = int(order[rk]), int(order[o]); pairs.add((i,j) if i<j else (j,i))
        return pairs
    gaps = {}
    for i, j in truth:
        gaps[(i,j)] = max(rmin[i]-rmax[j], rmin[j]-rmax[i], 0.0)  # >0: disjoint annuli
    shell = sum(1 for v in gaps.values() if v > 0)
    full = window_pairs(True, True); A = window_pairs(False, True); B = window_pairs(True, False)
    return {
        "R": R, "n": n, "truth_pairs": len(truth),
        "truth_pairs_with_disjoint_annuli": shell,
        "window_misses": sum(1 for p in truth if p not in full),
        "ctrlA_noR_misses": sum(1 for p in truth if p not in A),
        "ctrlB_noQuantum_misses": sum(1 for p in truth if p not in B),
    }
res = [run(5e-3, 3000, 4242), run(5e-3, 3000, 777)]
print(json.dumps(res, indent=1))
json.dump(res, open("ctrl_probe.json","w"), indent=1)
