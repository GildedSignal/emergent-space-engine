"""Mixed decisive scene 1: the belt (Sun + Jupiter, 96 test bodies, a in
[0.38, 0.64] sep, e in [0.02,0.2]), horizon 300 Jupiter orbits, reference N=512.
Per-body verdicts: apsidal 10%, e-max ratio [0.8,1.25], bound/eject match.
Total kicks for fixed N in {8,16,32,64,128} vs the rule."""
import numpy as np, json
from multiprocessing import Pool
import cad
from cad import TWOPI, elements, Doll, run, fit_rate

MU = 9.54e-4
GM_S = 1 - MU
D = 1.0; N2 = 1.0


def belt_births(nb, seed, amax=0.64, amin=0.38):
    rng = np.random.default_rng(seed)
    a = rng.uniform(amin, amax, nb)
    e = rng.uniform(0.02, 0.2, nb)
    w = rng.uniform(0, TWOPI, nb)
    M = rng.uniform(0, TWOPI, nb)
    E = cad.kepler_E(M, e)
    r = a * (1 - e * np.cos(E))
    ta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    x = r * np.cos(w + ta); y = r * np.sin(w + ta)
    v = np.sqrt(2 / r - 1 / a)
    return dict(x=x, y=y, vx=-v * np.sin(w + ta), vy=v * np.cos(w + ta)), a, e, w


def make_Nfn(rule, a0):
    def Nfn(a, e, w, x, y, t):
        return rule(a, e, a0)
    return Nfn


def run_case(args):
    N_mode, seed = args
    doll = Doll(GM_S, [dict(gm=MU, D=D, n=N2, ph=0.0)])
    s0, a0, e0, w0 = belt_births(96, seed)
    T = 300 * TWOPI
    if callable(N_mode):
        Nfn = make_Nfn(N_mode, a0)
        out, fin = run(doll, s0, T, Nfn, sample=None)
        # element series needed: rerun with sampling cheaply via final only
        out_s, fin_s = run(doll, s0, T, Nfn, sample=np.arange(2, T, TWOPI))
        return dict(mode="rule", kicks=fin_s["kicks"], a_end=out_s["a"][-1],
                    emax=out_s["e"].max(axis=0), wdot=fit_rate(out_s["t"], out_s["w"]),
                    a0=a0, e0=e0, t_series=out_s["t"].shape[0])
    out, fin = run(doll, s0, T, N_mode, sample=np.arange(2, T, TWOPI))
    return dict(mode=N_mode, kicks=fin["kicks"], a_end=out["a"][-1],
                emax=out["e"].max(axis=0), wdot=fit_rate(out["t"], out["w"]),
                a0=a0, e0=e0, t_series=out["t"].shape[0])


def main():
    seed = 2026
    modes = [8, 16, 32, 64, 128, 512]
    with Pool(6) as pool:
        res = pool.map(run_case, [(m, seed) for m in modes])
    ref = [r for r in res if r["mode"] == 512][0]
    for r in res:
        if r["mode"] == 512:
            continue
        ok = (np.abs(r["wdot"] / ref["wdot"] - 1) < 0.10) & np.isfinite(ref["wdot"])
        ok &= (r["emax"] / ref["emax"] > 0.8) & (r["emax"] / ref["emax"] < 1.25)
        inj = ok.mean()
        print(f"N={r['mode']}: pass {inj*100:.0f}%  total kicks {r['kicks'].sum():.3g} "
              f"(per body mean {r['kicks'].mean():.0f})")
        r["ok"] = ok
    np.save("belt_fixed.npy", res, allow_pickle=True)


if __name__ == "__main__":
    main()
