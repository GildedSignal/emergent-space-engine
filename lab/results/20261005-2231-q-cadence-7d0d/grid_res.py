"""Tuning grid 2: cadence vs distance to a mean-motion resonance (B17 family).
Sun + perturber (mu), ship near p:q, two starting phases stacked in one job.
Gate (B17 flavour): e-pump ratio in [0.8,1.25] (or |de|<0.03), libration-amplitude
ratio >= 0.8, regime (librate/circulate) match."""
import numpy as np, json
from multiprocessing import Pool
import cad
from cad import TWOPI, elements, Doll, run, fit_rate

D = 1.0; N2 = 1.0


def birth(pq, mu, s, e0=0.02, phs=(0.0, 1.7)):
    W = 2.5 * mu ** (2.0 / 3.0)
    p, q = pq
    n_ship = (p / q) * N2 * (1.0 + s * W)
    a0 = (1.0 / n_ship ** 2) ** (1 / 3)
    xs, ys, vxs, vys = [], [], [], []
    for lam0 in phs:
        E = cad.kepler_E(np.array([lam0]), np.array([e0]))[0]
        ta = 2 * np.arctan2(np.sqrt(1 + e0) * np.sin(E / 2), np.sqrt(1 - e0) * np.cos(E / 2))
        r = a0 * (1 - e0 * np.cos(E))
        w0 = 0.3
        x = r * np.cos(w0 + ta); y = r * np.sin(w0 + ta)
        v = np.sqrt(2 / r - 1 / a0)
        xs.append(x); ys.append(y); vxs.append(-v * np.sin(w0 + ta)); vys.append(v * np.cos(w0 + ta))
    return (np.array(xs), np.array(ys), np.array(vxs), np.array(vys)), n_ship


def res_point(args):
    pq, mu, s, N, T_orb = args
    doll = Doll(1.0 - mu, [dict(gm=mu, D=D, n=N2, ph=0.0)])
    (x, y, vx, vy), n_ship = birth(pq, mu, s)
    T = T_orb * TWOPI / n_ship
    out, fin = run(doll, dict(x=x, y=y, vx=vx, vy=vy), T, N,
                   sample=np.arange(2, T, 2 * TWOPI / n_ship))
    if out["e"].shape[0] < 10:
        return dict(pq=pq, mu=mu, s=s, N=N, fail=True)
    rows = []
    for b in range(x.size):
        lam_abs = np.unwrap(np.arctan2(out["ya"][:, b], out["xa"][:, b]))
        th = (pq[0] + pq[1]) * lam_abs - pq[0] * out["t"][:, b] - pq[1] * np.unwrap(out["w"][:, b])
        th = np.unwrap(th)
        wind = th[-1] - th[0]
        lib = abs(wind) < 1.5 * np.pi
        amp = 0.5 * (th.max() - th.min()) if lib else np.inf
        rows.append(dict(emax=out["e"][:, b].max(), wind=wind, lib=lib, amp=amp,
                         kicks=fin["kicks"][b]))
    return dict(pq=pq, mu=mu, s=s, N=N, fail=False, rows=rows)


def main():
    jobs, refjobs = [], []
    for pq in [(2, 1), (3, 2)]:
        for mu in (3e-5, 3e-4, 3e-3):
            for s in (-2.0, -1.0, -2 / 3, -1 / 3, 0.0, 1 / 3, 2 / 3, 1.0, 2.0):
                for N in (1, 2, 4, 8, 16, 32, 64):
                    jobs.append((pq, mu, s, N, 128))
                refjobs.append((pq, mu, s, 512, 128))
    print(f"{len(jobs)}+{len(refjobs)} jobs", flush=True)
    with Pool(4) as pool:
        res = pool.map(res_point, jobs)
        refs = pool.map(res_point, refjobs)
    np.save("res_grid.npy", (res, refs), allow_pickle=True)
    print("pq mu s | ph: ref(lib,amp,emax) K*")
    for rf in refs:
        pq, mu, s = rf["pq"], rf["mu"], rf["s"]
        line = f"{pq} {mu:.0e} {s:+.2f} |"
        for ph0, b in zip((0.0, 1.7), (0, 1)):
            rb = rf["rows"][b]
            ks = None
            for N in (1, 2, 4, 8, 16, 32, 64):
                r = [x for x in res if x["pq"] == pq and x["mu"] == mu and x["s"] == s and x["N"] == N]
                if not r or r[0].get("fail"):
                    continue
                rr = r[0]["rows"][b]
                pump = rr["emax"] / rb["emax"]
                okp = 0.8 <= pump <= 1.25 or (abs(rr["emax"] - rb["emax"]) < 0.03)
                okr = rr["lib"] == rb["lib"]
                oka = (not rb["lib"]) or (rr["lib"] and rr["amp"] / rb["amp"] >= 0.8)
                if okp and okr and oka:
                    ks = N
                    break
            line += f"  ph{b}: lib={rb['lib']} amp={rb['amp']:.2f} emax={rb['emax']:.4f} K*={ks}"
        print(line)


if __name__ == "__main__":
    main()
