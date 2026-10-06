"""Decisive mixed scenes (held out): moons, belt, resonant pair, B12 ships.
Compares the fitted rule against fixed cadences 8/16/64/128 (and today's plane
default 128) at equal behaviour, reporting total kicks."""
import numpy as np, json, sys
from multiprocessing import Pool
import cad
from cad import TWOPI, elements, Doll, run, fit_rate
import rule as R

MU_P = 1e-3; GM_P = MU_P; GM_S = 1 - MU_P
RH = (MU_P / 3) ** (1 / 3)
N2 = 1.0


# ---------------- scene A: moons (B14) ----------------
def moon_job(args):
    f, e0, N_mode, retro, Torb, seed = args
    rng = np.random.default_rng(seed)
    doll = Doll(GM_P, [dict(gm=GM_S, D=1.0, n=N2, ph=0.0)])
    a0 = f * RH
    n = np.sqrt(GM_P / a0 ** 3)
    nph = 6
    ph = rng.uniform(0, TWOPI, nph)
    r = a0 * (1 - e0)
    sgn = -1.0 if retro else 1.0
    x = r * np.cos(ph); y = r * np.sin(ph)
    v = np.sqrt(GM_P * (2 / r - 1 / a0))
    vx = -v * np.sin(ph) * sgn; vy = v * np.cos(ph) * sgn
    T = Torb * TWOPI

    def Nfn(a, e, w, xx, yy, t):
        # rebinding rule: n from the current orbit, synodic vs the sun (n2)
        nn = np.sqrt(GM_P / np.abs(a) ** 3)
        return R.cadence(nn, N2, e)

    if N_mode == "rule":
        out, fin = run(doll, dict(x=x, y=y, vx=vx, vy=vy), T, Nfn,
                       sample=np.arange(2, T, TWOPI / n))
    else:
        out, fin = run(doll, dict(x=x, y=y, vx=vx, vy=vy), T, N_mode,
                       sample=np.arange(2, T, TWOPI / n))
    wd = fit_rate(out["t"], out["w"])
    return dict(f=f, e0=e0, mode=str(N_mode), retro=retro, wdot=wd,
                emax=out["e"].max(axis=0), a_end=out["a"][-1],
                kicks=fin["kicks"], n0=n)


# ---------------- scene B: belt (B14/B17 flavours) ----------------
MU_J = 9.54e-4

def belt_job(args):
    N_mode, seed, amax, amin, Torb = args
    rng = np.random.default_rng(seed)
    doll = Doll(1 - MU_J, [dict(gm=MU_J, D=1.0, n=N2, ph=0.0)])
    nb = 96
    a = rng.uniform(amin, amax, nb)
    e = rng.uniform(0.02, 0.2, nb)
    w = rng.uniform(0, TWOPI, nb)
    M = rng.uniform(0, TWOPI, nb)
    E = cad.kepler_E(M, e)
    r = a * (1 - e * np.cos(E))
    ta = 2 * np.arctan2(np.sqrt(1 + e) * np.sin(E / 2), np.sqrt(1 - e) * np.cos(E / 2))
    x = r * np.cos(w + ta); y = r * np.sin(w + ta)
    v = np.sqrt(2 / r - 1 / a)
    T = Torb * TWOPI
    W21 = 2.5 * MU_J ** (2 / 3)

    def Nfn(a_, e_, w_, xx, yy, t):
        nn = np.sqrt(1.0 / np.abs(a_) ** 3)
        N = R.cadence(nn, N2, e_)
        # resonance routing: |q n - p| < 2 W  -> not the kick layer's body
        W = 2.5 * MU_J ** (2 / 3)
        for (p, q) in ((2, 1), (3, 1), (5, 2), (7, 3)):
            N = np.where(np.abs(q * nn - p) < 2 * W * p, 1024.0, N)
        return N

    if N_mode == "rule":
        out, fin = run(doll, dict(x=x, y=y, vx=-v * np.sin(w + ta), vy=v * np.cos(w + ta)), T, Nfn,
                       sample=np.arange(2, T, TWOPI))
    else:
        out, fin = run(doll, dict(x=x, y=y, vx=-v * np.sin(w + ta), vy=v * np.cos(w + ta)), T, N_mode,
                       sample=np.arange(2, T, TWOPI))
    return dict(mode=str(N_mode), wdot=fit_rate(out["t"], out["w"]),
                emax=out["e"].max(axis=0), a_end=out["a"][-1],
                kicks=fin["kicks"], a0=a, e0=e)


# ---------------- scene C: resonant pairs held-out ----------------
def res_job(args):
    pq, mu, s, N_mode, T_orb = args
    from grid_res import birth
    doll = Doll(1.0 - mu, [dict(gm=mu, D=1.0, n=N2, ph=0.0)])
    (x, y, vx, vy), n_ship = birth(pq, mu, s)
    T = T_orb * TWOPI / n_ship

    def Nfn(a_, e_, w_, xx, yy, t):
        nn = np.sqrt(1.0 / np.abs(a_) ** 3)
        N = R.cadence(nn, N2, e_)
        # resonance routing: |q n - p| < 2 W  -> not the kick layer's body
        W = 2.5 * MU_J ** (2 / 3)
        for (p, q) in ((2, 1), (3, 1), (5, 2), (7, 3)):
            N = np.where(np.abs(q * nn - p) < 2 * W * p, 1024.0, N)
        return N

    if N_mode == "rule":
        out, fin = run(doll, dict(x=x, y=y, vx=vx, vy=vy), T, Nfn,
                       sample=np.arange(2, T, 2 * TWOPI / n_ship))
    else:
        out, fin = run(doll, dict(x=x, y=y, vx=vx, vy=vy), T, N_mode,
                       sample=np.arange(2, T, 2 * TWOPI / n_ship))
    rows = []
    for b in range(x.size):
        lam = np.unwrap(np.arctan2(out["ya"][:, b], out["xa"][:, b]))
        th = (pq[0] + pq[1]) * lam - pq[0] * out["t"][:, b] - pq[1] * np.unwrap(out["w"][:, b])
        th = np.unwrap(th)
        lib = abs(th[-1] - th[0]) < 1.5 * np.pi
        amp = 0.5 * (th.max() - th.min()) if lib else np.inf
        rows.append(dict(emax=out["e"][:, b].max(), lib=lib, amp=amp, kicks=fin["kicks"][b]))
    return dict(pq=pq, mu=mu, s=s, mode=str(N_mode), rows=rows)


def main():
    R.load("RULE.json")
    jobsA, jobsB, jobsC = [], [], []
    fs = [0.225, 0.275, 0.45]
    es = [0.15, 0.35]
    seed = 5000
    for f in fs:
        for e0 in es:
            for mode in ["rule", 8, 16, 64, 128, 256]:
                seed += 1
                jobsA.append((f, e0, mode, False, 50, seed))
            jobsA.append((f, e0, "rule", True, 50, seed + 1000))  # retro at rule
    jobsA.append((0.3, 0.2, "rule", True, 50, 777))
    for mode in ["rule", 8, 16, 64, 128, 512]:
        jobsB.append((mode, 2026, 0.64, 0.38, 300))
    for (pq, mu, s) in [((3, 2), 3e-4, 1.5), ((3, 2), 3e-4, -1.5), ((2, 1), 1e-3, 1 / 3)]:
        for mode in ["rule", 8, 16, 64, 128, 1024]:
            jobsC.append((pq, mu, s, mode, 256))
    print(f"A:{len(jobsA)} B:{len(jobsB)} C:{len(jobsC)}", flush=True)
    with Pool(6) as pool:
        resA = pool.map(moon_job, jobsA)
        resB = pool.map(belt_job, jobsB)
        resC = pool.map(res_job, jobsC)
    np.save("mixed.npy", (resA, resB, resC), allow_pickle=True)
    # ---- verdicts ----
    print("\n=== A: moons (B14: apsidal 10%, emax ratio [0.8,1.25], regime) ===")
    for f in fs:
        for e0 in es:
            ref = [r for r in resA if r["f"] == f and r["e0"] == e0 and r["mode"] == "256"][0]
            for mode in ["rule", "8", "16", "64", "128"]:
                rr = [r for r in resA if r["f"] == f and r["e0"] == e0 and r["mode"] == mode]
                if not rr:
                    continue
                r = rr[0]
                ok = np.abs(r["wdot"] / ref["wdot"] - 1) < 0.10
                ok &= (r["emax"] / ref["emax"] > 0.8) & (r["emax"] / ref["emax"] < 1.25)
                esc_r = ref["a_end"] < 0
                esc = r["a_end"] < 0
                reg = (esc == esc_r)
                print(f"f={f} e0={e0} N={mode}: pass {ok.mean()*100:.0f}% regime {reg.mean()*100:.0f}% "
                      f"kicks/body {r['kicks'].mean():.0f}")
    print("\n=== B: belt ===")
    refB = [r for r in resB if r["mode"] == "512"][0]
    W21 = 2.5 * MU_J ** (2 / 3)
    for mode in ["rule", "8", "16", "64", "128"]:
        r = [x for x in resB if x["mode"] == mode][0]
        n_body = 1.0 / r["a0"] ** 1.5
        inband = np.zeros(len(n_body), bool)
        for (p, q) in ((2, 1), (3, 1), (5, 2), (7, 3)):
            inband |= np.abs(q * n_body - p) < 2 * W21 * p
        ok = np.abs(r["wdot"] / refB["wdot"] - 1) < 0.10
        ok &= (r["emax"] / refB["emax"] > 0.8) & (r["emax"] / refB["emax"] < 1.25)
        print(f"N={mode}: pass out-of-band {ok[~inband].mean()*100:.0f}%  "
              f"total kicks {r['kicks'].sum():.4g} (mean {r['kicks'].mean():.0f})")
    print("\n=== C: resonant pairs (B17) ===")
    for (pq, mu, s) in [((3, 2), 3e-4, 1.5), ((3, 2), 3e-4, -1.5), ((2, 1), 1e-3, 1 / 3)]:
        ref = [r for r in resC if r["pq"] == pq and r["mu"] == mu and r["s"] == s and r["mode"] == "1024"][0]
        for mode in ["rule", "8", "16", "64", "128"]:
            r = [x for x in resC if x["pq"] == pq and x["mu"] == mu and x["s"] == s and x["mode"] == mode][0]
            oks = []
            for b, rb in enumerate(ref["rows"]):
                rr = r["rows"][b]
                pump = rr["emax"] / rb["emax"]
                okp = 0.8 <= pump <= 1.25 or abs(rr["emax"] - rb["emax"]) < 0.03
                okr = rr["lib"] == rb["lib"]
                oka = (not rb["lib"]) or (rr["lib"] and rr["amp"] / rb["amp"] >= 0.8)
                oks.append(okp and okr and oka)
            print(f"pq={pq} mu={mu:.0e} s={s:+.2f} N={mode}: pass {sum(oks)}/2 kicks {sum(x['kicks'] for x in r['rows']):.0f}")


if __name__ == "__main__":
    main()
