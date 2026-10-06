"""Tuning grid: N*(f, e) for moons in the planet's doll (B14 family).
Also validates the replica against the classical quadrupole apsidal rate."""
import numpy as np, json, sys, os
from multiprocessing import Pool
import cad
from cad import TWOPI, elements, Doll, run, fit_rate

MU = 1e-3
GM_P = MU; GM_S = 1.0 - MU
D = 1.0; N2 = 1.0
RH = (MU / 3) ** (1 / 3)


def moon_point(args):
    f, e0, N, Torb, nph, seed, retro = args
    rng = np.random.default_rng(seed)
    doll = Doll(GM_P, [dict(gm=GM_S, D=D, n=N2, ph=0.0)])
    a0 = f * RH
    n = np.sqrt(GM_P / a0 ** 3)
    ph = rng.uniform(0, TWOPI, nph)
    w0 = rng.uniform(0, TWOPI, nph)
    M0 = rng.uniform(0, TWOPI, nph)
    E = cad.kepler_E(M0, np.full(nph, e0))
    r = a0 * (1 - e0 * np.cos(E))
    x = r * np.cos(w0 + np.arctan2(np.sqrt(1 - e0 ** 2) * np.sin(E), np.cos(E) - e0))
    y = r * np.sin(w0 + np.arctan2(np.sqrt(1 - e0 ** 2) * np.sin(E), np.cos(E) - e0))
    ta = np.arctan2(y, x)
    v = np.sqrt(GM_P * (2 / r - 1 / a0))
    sgn = -1.0 if retro else 1.0
    vx = -v * np.sin(ta) * sgn; vy = v * np.cos(ta) * sgn
    T = Torb * TWOPI
    out, fin = run(doll, dict(x=x, y=y, vx=vx, vy=vy), T, N,
                   sample=np.arange(2, T, TWOPI / n))
    wd = fit_rate(out["t"], out["w"])
    emax = out["e"].max(axis=0)
    a_end = out["a"][-1]
    # error type: compare first vs second half rate of e-envelope max
    mid = out["e"].shape[0] // 2
    dw = np.abs(out["w"] - out["w"][0])
    return dict(f=f, e0=e0, N=N, retro=retro,
                wdot=list(wd), emax=list(emax), a_end=list(a_end),
                e_series=out["e"], t_last=out["t"][-1], kicks=list(fin["kicks"]))


def collect(res):
    r = dict(f=res["f"], e0=res["e0"], N=res["N"], retro=res["retro"])
    r["wdot"] = np.array(res["wdot"]); r["emax"] = np.array(res["emax"])
    r["a_end"] = np.array(res["a_end"]); r["kicks"] = np.array(res["kicks"])
    r["T"] = res["t_last"]
    return r


def main():
    fs = [0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
    es = [0.05, 0.1, 0.2, 0.3]
    Ns = [2, 3, 4, 6, 8, 12, 16, 24, 32]
    Torb = 30
    nph = 6
    jobs = []
    seed = 1000
    for f in fs:
        for e0 in es:
            for N in Ns + [256]:
                seed += 1
                jobs.append((f, e0, N, Torb, nph, seed, False))
    print(f"{len(jobs)} jobs", flush=True)
    with Pool(4) as pool:
        res = pool.map(moon_point, jobs)
    np.save("moon_grid.npy", res, allow_pickle=True)

    # classical check at N=512
    for r in res:
        if r["N"] == 256 and r["e0"] == 0.05:
            wd = np.median(r["wdot"])
            a0 = r["f"] * RH
            n = np.sqrt(GM_P / a0 ** 3)
            tau = (GM_S / GM_P) * (a0 / D) ** 3
            print(f"classical f={r['f']}: meas {wd:+.5f} cl {0.75*n*tau:+.5f} ratio {wd/(0.75*n*tau):.3f}")


if __name__ == "__main__":
    main()
