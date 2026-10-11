"""FINAL corrected sweep (the numbers in dossier.md). Reproduces in ~60 s:
    cd lab/results/20261011-0736-dynamics-ec74/work && python3 sweep_final.py
Deterministic (fixed seeds). Includes both controls."""
import numpy as np, json, time, sys
sys.path.insert(0, '.')
from swarm import run_swarm, Swarm, TWO_PI, kepler_states

def step_brute(sw, t, dt):
    a, e, varpi, M0 = sw.a, sw.e, sw.varpi, sw.M0
    x1, y1, vx1, vy1 = kepler_states(a, e, varpi, M0, t - dt)
    x2, y2, vx2, vy2 = kepler_states(a, e, varpi, M0, t)
    b_H = 3.0 * (sw.mu_g / 3.0) ** (1/3)
    hits = 0
    for i in range(sw.N):
        px0 = x1 - x1[i]; py0 = y1 - y1[i]; ux0 = vx1 - vx1[i]; uy0 = vy1 - vy1[i]
        px = x2 - x2[i]; py = y2 - y2[i]; ux = vx2 - vx2[i]; uy = vy2 - vy2[i]
        cross = (px0*ux0 + py0*uy0 < 0) & (px*ux + py*uy >= 0)
        cross[i] = False
        u = np.hypot(ux, uy)
        b = np.abs(px*uy - py*ux) / np.maximum(u, 1e-14)
        hits += int((cross & (b < b_H) & (u > 0.2*sw.u_floor_sigma)
                     & (np.arange(sw.N) > i)).sum())
    return hits

t0 = time.time()
# control (a): neighbour pruning vs brute force
A = Swarm(N=150, w=0.04, sigma_e=0.04, m=3e-4*0.04**3/2, seed=3)
B = Swarm(N=150, w=0.04, sigma_e=0.04, m=3e-4*0.04**3/2, seed=3)
dt = TWO_PI/128; ha = hb = 0; t = 0.0
for step in range(30*128):
    t += dt
    ha += A.step_all(t, dt, K=6)
    hb += step_brute(B, t, dt)
print(f"control (a) K=6 vs brute: {ha} vs {hb} -> {100*ha/max(hb,1):.1f}%")

# control (b): sampling convergence (impulse counts, S=128 vs 256)
for psi in [3e-4, 3e-6]:
    for S in [128, 256]:
        sw, res = run_swarm(psi, N=150, w=0.04, sigma_e=0.04, T_orbits=30,
                            S=S, K=6, seed=3)
        print(f"control (b) psi={psi:.0e} S={S}: impulses={len(res['log'])}")

# the sweep
out = {}
for psi in [3e-6, 3e-5, 3e-4]:
    sw, res = run_swarm(psi, N=300, w=0.04, sigma_e=0.04, T_orbits=100,
                        S=128, K=6, seed=0)
    chi = np.array([l[3] for l in res["log"]]); da = np.array([l[4] for l in res["log"]])
    strong = chi >= 0.3
    lam_s = strong.sum()/300/100
    oi = np.array([int(l[0]/TWO_PI) for l in res["log"]])
    cnt = np.bincount(oi[strong], minlength=101)[:101]
    fanes = {}
    for win in [1, 4, 16]:
        k = 101//win
        c = cnt[:k*win].reshape(k, win).sum(axis=1)
        fanes[win] = round(float(c.var()/c.mean()), 2) if c.mean() > 0 else None
    out[f"{psi:.0e}"] = dict(
        n_impulses=len(res["log"]), lam_strong=lam_s,
        lam_early=strong[oi < 25].sum()/300/25, lam_late=strong[oi >= 50].sum()/300/50,
        captures=sw.n_capture, capture_rate=sw.n_capture/300/100,
        sig_e0=res["sig_e"][0], sig_e_final=res["sig_e"][-1],
        sig_a0=res["sig_a"][0], sig_a_final=res["sig_a"][-1],
        chi_median=float(np.median(chi[strong])) if strong.sum() else None,
        frac_chi_gt1=float((chi[strong] > 1).mean()) if strong.sum() else None,
        drift_per_orbit=float(np.abs(da[strong]).mean()*lam_s) if strong.sum() else 0.0,
        n_strong=int(strong.sum()), fanos=fanes)
    print(json.dumps({f"{psi:.0e}": out[f"{psi:.0e}"]}))
json.dump(out, open("summary_final.json", "w"), indent=1)
print("wall", round(time.time()-t0, 1), "s")
