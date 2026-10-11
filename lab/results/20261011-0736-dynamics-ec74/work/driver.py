"""Driver: the decisive Psi sweep + twins. Saves results.npz + summary.json."""
import numpy as np, json, time, sys
sys.path.insert(0, '.')
from swarm import run_swarm, run_pair, Swarm, kepler_states, TWO_PI

N, W, SE, T, S, K = 300, 0.04, 0.04, 200, 128, 6
PSIS = [3e-6, 3e-5, 3e-4, 3e-3]
t00 = time.time()

def strong(log, chi_min=0.3):
    t_arr = np.array([l[0] for l in log]); chi = np.array([l[3] for l in log])
    da = np.array([l[4] for l in log]); de = np.array([l[5] for l in log])
    s = chi >= chi_min
    oi = (t_arr[s] / TWO_PI).astype(int)
    cnt = np.bincount(oi, minlength=T + 1)[:T + 1]
    return cnt, chi[s], da[s], de[s]

summary = {}
store = {}
for psi in PSIS:
    t0 = time.time()
    sw, res = run_swarm(psi, N=N, w=W, sigma_e=SE, T_orbits=T, S=S, K=K, seed=0)
    cnt, chi_s, da_s, de_s = strong(res["log"])
    lam = cnt.sum() / N / T
    lam_early = cnt[:50].sum() / N / 50.0
    lam_late = cnt[100:200].sum() / N / 100.0
    fanos = {}
    for win in [1, 4, 16, 64]:
        k = len(cnt) // win
        c = cnt[:k * win].reshape(k, win).sum(axis=1)
        mu = c.mean()
        fanos[win] = float(c.var() / mu) if mu > 0 else None
    mu_g = psi * SE**3
    r_H = (mu_g / 3.0)**(1/3)
    n2d = N / (2 * np.pi * max(W, SE))
    fill = n2d * np.pi * (3 * r_H)**2
    summary[psi] = dict(
        wall_s=round(time.time() - t0, 1), n_impulses=len(res["log"]),
        lam_strong=lam, lam_early=lam_early, lam_late=lam_late,
        sig_e0=res["sig_e"][0], sig_e_final=res["sig_e"][-1],
        sig_a0=res["sig_a"][0], sig_a_final=res["sig_a"][-1],
        chi_med=float(np.median(chi_s)) if len(chi_s) else None,
        chi_p90=float(np.percentile(chi_s, 90)) if len(chi_s) else None,
        frac_chi_gt1=float((chi_s > 1).mean()) if len(chi_s) else None,
        da_med=float(np.median(da_s)) if len(da_s) else None,
        da_p90=float(np.percentile(da_s, 90)) if len(da_s) else None,
        fanos=fanos, filling=float(fill),
        drift_per_orbit=float((np.abs(da_s).mean() * lam) if len(da_s) else 0.0),
    )
    store[f"psi{psi:.0e}_cnt"] = cnt
    store[f"psi{psi:.0e}_sige"] = np.array(res["sig_e"])
    store[f"psi{psi:.0e}_siga"] = np.array(res["sig_a"])
    print(json.dumps({f"{psi:.0e}": summary[psi]}))

for psi in PSIS:
    t0 = time.time()
    A, B, D = run_pair(psi, N=N, w=W, sigma_e=SE, T_orbits=T, S=S, K=K, seed=0)
    D = D.copy(); D[np.isnan(D)] = 0.0
    t_orb = np.arange(T + 1)
    band = (D > 3e-8) & (D < 0.3) & (t_orb > 0)
    if band.sum() > 10:
        p = np.polyfit(t_orb[band], np.log(D[band]), 1)
        slope, T_L = p[0], (1.0 / p[0] if p[0] > 0 else np.inf)
        r = np.corrcoef(t_orb[band], np.log(D[band]))[0, 1]
    else:
        slope, T_L, r = 0.0, np.inf, 0.0
    lam = summary[psi]["lam_strong"]
    summary[psi].update(TL_orbits=float(T_L), growth_rate_per_orbit=float(slope),
                        fit_r=float(r), TLx_lam=float(T_L * lam) if lam > 0 else None,
                        D_final=float(D[-1]), twin_wall_s=round(time.time() - t0, 1))
    store[f"psi{psi:.0e}_D"] = D
    print(f"twin psi={psi:.0e}: T_L={T_L:.1f} orbits  slope={slope:.4f}/orbit r={r:.3f} "
          f"lam={lam:.2e}  T_L*lam={(T_L*lam if lam>0 else float('nan')):.2f}")

np.savez_compressed("results.npz", **store)
json.dump(summary, open("summary.json", "w"), indent=1, default=str)
print("TOTAL", round(time.time() - t00, 1), "s")
