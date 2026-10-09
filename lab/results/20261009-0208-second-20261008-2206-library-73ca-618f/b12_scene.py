#!/usr/bin/env python3
"""B12's own scene, planted laws, alpha-profile test (second-author run on 20261008-2206-library-73ca).

Scene (mirrors crates/universe/examples/jacobi.rs + records.rs edge convention):
  circular restricted three-body, mu = 2^-10 (Jupiter-like), rotating frame n=1,
  star at (-mu,0), planet at (1-mu,0). Doll edge = sep/16 (the engine's
  2^(2*dlog2 m/5) rule = 0.907 Hill). Ships: retrograde irregular satellites,
  pericentre 0.5-0.72 Hill, apocentre 1.0-1.25 Hill (straddles the edge), random
  orientation -- the strong-solar-tide regime; ~5 edge crossings per planet orbit.
  (A heliocentric co-orbital population at 1.2-2.6 Hill offsets was tried first:
  the Wisdom chaotic zone ejects every seed within 10^3 orbits, so the gate's
  replacement rule applies and the surviving population is the retrograde one.)
  Doll bookkeeping runs in every law, every step inside the doll: state carried
  planet-relative with doll-local sources (the indirect term, law.md), rotation
  about the barycenter expressed in local form r' <- ph*r' + (ph-1)*Z2.

Laws (planted, both sides):
  sym-fixed   : 2nd-order symplectic split K/2 Rot/2 D Rot/2 K/2, fixed dt   -> BOUNDED control
  sym-var     : same split, dt = dt_base*(0.5+0.5*min(1, d/(2 Hill))) re-chosen
                from the state each step (the plane's failure mode)           -> COMPOUNDING plant
  rk4-fixed   : classic RK4 on the rotating-frame ODE, fixed dt               -> COMPOUNDING plant
  sym-sched   : sym-fixed with dt/4 for t < 300 orbits, then dt_base
                (scheduled refinement: bounded law + transient)               -> adversarial BOUNDED

Error series: |C(t) - C0|/|C0| sampled once per planet orbit, C the Jacobi constant.
Run (decisive):
  python3 b12_scene.py --select          # ~5 min: selection pass, writes seeds.json
  python3 b12_scene.py --law sym-var & etc (parallel)
  python3 b12_scene.py --analyse
"""
import argparse, json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MU = 2.0 ** -10
Z1 = complex(-MU, 0.0)
Z2 = complex(1.0 - MU, 0.0)
HILL = (MU / 3.0) ** (1.0 / 3.0)
EDGE = (1.0 - MU) / 16.0    # engine convention: sep * 2^(2*dlog2(m)/5) = sep/16 = 0.907 Hill
ENH = 2.0 * HILL            # step-enhancement radius for sym-var
DEATH_R = 3.0               # escape
DEATH_D = 5e-3              # impact on the planet
TWOPI = 2.0 * math.pi
Z1L = Z1 - Z2               # star as seen from the doll origin


def gradPhi(r, local=False):
    if local:
        d1 = r - Z1L
        d2 = r
        a1 = (1.0 - MU) / (np.abs(d1) ** 3)
        a2 = MU / (np.abs(d2) ** 3)
        return a1 * (Z1L - r) + a2 * (-r)
    d1 = r - Z1
    d2 = r - Z2
    a1 = (1.0 - MU) / (np.abs(d1) ** 3)
    a2 = MU / (np.abs(d2) ** 3)
    return a1 * (Z1 - r) + a2 * (Z2 - r)


def phi(r):
    return (1.0 - MU) / np.abs(r - Z1) + MU / np.abs(r - Z2)


def jacobi(r, p):
    v = p - 1j * r
    return np.abs(r) ** 2 + 2.0 * phi(r) - np.abs(v) ** 2


def kick(r, p, hdt, loc):
    """Kick with doll-local arithmetic for seeds inside the doll (handoff path)."""
    if loc.any():
        g = gradPhi(r)
        rl = r - Z2
        gl = gradPhi(rl, local=True)
        p += hdt * np.where(loc, gl, g)
    else:
        p += hdt * gradPhi(r)


def sympl_step(r, p, dt, loc):
    """One 2nd-order symplectic step K/2 R/2 D R/2 K/2; dt scalar or per-seed array.
    Doll-local arithmetic (handoff rounding path) for seeds inside the doll."""
    scalar = np.isscalar(dt)
    ph = np.exp(-0.5j * dt)
    kick(r, p, 0.5 * dt, loc)
    li = np.flatnonzero(loc)
    lo = np.flatnonzero(~loc)
    for half in range(2):          # R/2 D R/2
        if len(li):
            if scalar:
                r[li] = ph * (r[li] - Z2) + (ph - 1.0) * Z2 + Z2
                p[li] *= ph
            else:
                r[li] = ph[li] * (r[li] - Z2) + (ph[li] - 1.0) * Z2 + Z2
                p[li] *= ph[li]
        if len(lo):
            if scalar:
                r[lo] *= ph
                p[lo] *= ph
            else:
                r[lo] *= ph[lo]
                p[lo] *= ph[lo]
        if half == 0:              # drift between the half-rotations
            if len(li):
                d = dt if scalar else dt[li]
                r[li] = (r[li] - Z2) + d * p[li] + Z2
            if len(lo):
                d = dt if scalar else dt[lo]
                r[lo] += d * p[lo]
    kick(r, p, 0.5 * dt, loc)


def f_rv(r, v, local=False):
    """Rotating-frame ODE (optionally in doll-local coordinates)."""
    acc = gradPhi(r, local=local)
    if local:
        return v, r + Z2 + acc - 2j * v
    return v, r + acc - 2j * v


def _rk4_group(r, v, dt, local):
    off = Z2 if local else 0.0
    rl = r - off
    k1r, k1v = f_rv(rl, v, local=local)
    k2r, k2v = f_rv(rl + 0.5 * dt * k1r, v + 0.5 * dt * k1v, local=local)
    k3r, k3v = f_rv(rl + 0.5 * dt * k2r, v + 0.5 * dt * k2v, local=local)
    k4r, k4v = f_rv(rl + dt * k3r, v + dt * k3v, local=local)
    return rl + (dt / 6.0) * (k1r + 2 * k2r + 2 * k3r + k4r) + off, v + (dt / 6.0) * (k1v + 2 * k2v + 2 * k3v + k4v)


def rk4_step(r, v, dt, loc):
    if loc.any():
        i = np.flatnonzero(loc)
        r[i], v[i] = _rk4_group(r[i], v[i], dt, True)
    if (~loc).any():
        i = np.flatnonzero(~loc)
        r[i], v[i] = _rk4_group(r[i], v[i], dt, False)


def make_candidates(n, rng):
    r0 = np.empty(n, complex)
    v0 = np.empty(n, complex)
    for i in range(n):
        q = HILL * rng.uniform(0.55, 0.75)
        Q = HILL * rng.uniform(0.95, 1.05)
        a = 0.5 * (q + Q)
        th = rng.uniform(0.0, TWOPI)
        u = np.exp(1j * th)
        pos = Z2 + q * u
        vp = math.sqrt(MU * (2.0 / q - 1.0 / a))
        vpc = -1j * vp * u            # retrograde
        r0[i] = pos
        v0[i] = 1j * Z2 + vpc - 1j * pos
    return r0, v0


def run_law(name, r, v, korbits, dt_base, steps_per_orbit):
    """Integrate one law; per-seed time for sym-var; errs (n, korbits), nan after death."""
    n = len(r)
    p = v + 1j * r
    c0 = jacobi(r, p)
    errs = np.full((n, korbits), np.nan)
    alive = np.ones(n, bool)
    inside = np.abs(r - Z2) < EDGE
    crossings = np.zeros(n, np.int64)
    death = np.full(n, -1, np.int64)
    t = np.zeros(n)
    kn = np.ones(n, np.int64)
    var = name == "sym-var"
    is_rk4 = name == "rk4-fixed"
    sched_switch = 300.0 * TWOPI if name == "sym-sched" else -1.0
    max_steps = int((2.0 if var else 1.0) * steps_per_orbit * korbits) + (4 * steps_per_orbit * 300 if name == "sym-sched" else 0) + 64
    done = 0
    while (kn <= korbits).any() and done < max_steps:
        done += 1
        if var:
            d = np.abs(r - Z2)
            dt = dt_base * (0.5 + 0.5 * np.minimum(1.0, d / ENH))
        elif sched_switch > 0:
            dt = dt_base / 4.0 if t.max() < sched_switch else dt_base
        else:
            dt = dt_base
        loc = np.abs(r - Z2) < EDGE
        if is_rk4:
            vv = p - 1j * r
            rk4_step(r, vv, dt, loc)
            p = vv + 1j * r
        else:
            sympl_step(r, p, dt, loc)   # per-seed dt, elementwise
        t += dt
        now_in = np.abs(r - Z2) < EDGE
        crossings += (alive & (now_in != inside)).astype(np.int64)
        inside = np.where(alive, now_in, inside)
        dead = alive & ((np.abs(r) > DEATH_R) | (np.abs(r - Z2) < DEATH_D))
        if dead.any():
            death[dead] = int(kn[dead].max())
            alive &= ~dead
            r[~alive] = np.nan
            p[~alive] = np.nan
        while True:
            m = alive & (kn <= korbits) & (t >= kn * TWOPI)
            if not m.any():
                break
            errs[m, kn[m] - 1] = np.abs(jacobi(r[m], p[m]) - c0[m]) / np.abs(c0[m])
            kn[m] += 1
    return errs, crossings, death


def decade_exponents(m, ks):
    out = {}
    for d in range(0, 5):
        lo, hi = 10 ** d, 10 ** (d + 1)
        ilo = min(range(len(ks)), key=lambda i: abs(ks[i] - lo))
        ihi = min(range(len(ks)), key=lambda i: abs(ks[i] - hi))
        if ks[ihi] < hi * 0.5 or ihi <= ilo or m[ihi] <= 0 or m[ilo] <= 0:
            continue
        out[d] = (math.log(m[ihi]) - math.log(m[ilo])) / (math.log(ks[ihi]) - math.log(ks[ilo]))
    return out


def window_slope(m, ks, k_lo, k_hi):
    ilo = min(range(len(ks)), key=lambda i: abs(ks[i] - k_lo))
    ihi = min(range(len(ks)), key=lambda i: abs(ks[i] - k_hi))
    return (math.log(m[ihi]) - math.log(m[ilo])) / (math.log(ks[ihi]) - math.log(ks[ilo]))


def analyse(errs, crossings, death, korbits, name, res):
    n = errs.shape[0]
    ks_all = np.arange(1, korbits + 1)
    rows = []
    for i in range(n):
        col = errs[i]
        good = np.isfinite(col)
        ks = ks_all[good]
        if len(ks) < korbits * 0.5 or not good.any():
            rows.append(dict(seed=int(i), verdict="lost-early", crossings=int(crossings[i]), death=int(death[i])))
            continue
        m = np.maximum.accumulate(col[good])
        de = decade_exponents(m.tolist(), ks.tolist())
        top = de.get(3)
        w_full = window_slope(m.tolist(), ks.tolist(), 1, korbits)
        w_1e3 = window_slope(m.tolist(), ks.tolist(), 1, 1000)
        rows.append(dict(seed=int(i), final=float(m[-1]), alpha=[de.get(d) for d in range(4)],
                         alpha_top=top, w_full=w_full, w_1e3=w_1e3,
                         crossings=int(crossings[i]), death=int(death[i]),
                         verdict=("lost" if death[i] > 0 else ("noise" if m[-1] < 1e-12 else ("COMPOUND" if (top is not None and top > 0.2) else "BOUNDED")))))
    ok = [r for r in rows if r["verdict"] in ("BOUNDED", "COMPOUND")]
    ok.sort(key=lambda r: r["final"])
    med = ok[len(ok) // 2] if ok else None
    res[name] = dict(rows=rows, median=med)
    print(f"\n== {name} ==")
    for r in rows:
        if "alpha" not in r:
            print(f"  seed {r['seed']:2d} LOST-EARLY")
            continue
        a = " ".join("nan" if x is None else f"{x:+.2f}" for x in r["alpha"])
        print(f"  seed {r['seed']:2d} crossings {r['crossings']:6d} final {r['final']:.2e} "
              f"alpha[{a}] w1e4 {r['w_full']:+.2f} w1e3 {r['w_1e3']:+.2f} -> {r['verdict']}")
    if med:
        a = " ".join("nan" if x is None else f"{x:+.2f}" for x in med["alpha"])
        print(f"  MEDIAN seed {med['seed']}: final {med['final']:.2e} alpha[{a}] -> {med['verdict']}")
    sys.stdout.flush()
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["select", "law", "analyse", "all"])
    ap.add_argument("--lawname")
    ap.add_argument("--candidates", type=int, default=40)
    ap.add_argument("--keep", type=int, default=16)
    ap.add_argument("--korbits", type=int, default=10000)
    ap.add_argument("--steps-per-orbit", type=int, default=256)
    args = ap.parse_args()
    dt_base = TWOPI / args.steps_per_orbit
    res = {}
    if args.mode in ("select", "all"):
        rng = np.random.default_rng(20261009)
        r0, v0 = make_candidates(args.candidates, rng)
        print(f"scene: mu={MU:.6e} hill={HILL:.5f} edge={EDGE:.5f} ({EDGE/HILL:.3f} Hill) dt={dt_base:.5f} "
              f"({args.steps_per_orbit}/orbit) horizon={args.korbits} orbits", flush=True)
        errs, cross, death = run_law("sym-fixed", r0.copy(), v0.copy(), args.korbits, dt_base, args.steps_per_orbit)
        surv = death < 0
        enough = surv & (cross >= 20)
        idx = np.where(enough)[0]
        order = idx[np.argsort(-cross[idx], kind="stable")][: args.keep]
        print(f"selection: {int(surv.sum())}/{args.candidates} survive, {int(enough.sum())} with >=20 crossings; kept {len(order)}: {order.tolist()}", flush=True)
        print("crossings of kept:", cross[order].tolist(), flush=True)
        json.dump(dict(r0_real=r0[order].real.tolist(), r0_imag=r0[order].imag.tolist(),
                       v0_real=v0[order].real.tolist(), v0_imag=v0[order].imag.tolist(),
                       crossings=cross[order].tolist(), death=death[order].tolist(),
                       survivors=int(surv.sum()), candidates=args.candidates, keep=len(order),
                       korbits=args.korbits, steps_per_orbit=args.steps_per_orbit,
                       mu=MU, hill=HILL, edge=EDGE, dt_base=dt_base),
                  open(os.path.join(HERE, "seeds.json"), "w"), indent=1)
        np.savez_compressed(os.path.join(HERE, "series_sym-fixed.npz"), errs=errs[order], crossings=cross[order], death=death[order])
        analyse(errs[order], cross[order], death[order], args.korbits, "sym-fixed", res)
        json.dump(res, open(os.path.join(HERE, "partial_sym-fixed.json"), "w"), indent=1)
    elif args.mode == "law":
        assert args.lawname
        sd = json.load(open(os.path.join(HERE, "seeds.json")))
        r0 = np.array(sd["r0_real"]) + 1j * np.array(sd["r0_imag"])
        v0 = np.array(sd["v0_real"]) + 1j * np.array(sd["v0_imag"])
        e, c, d = run_law(args.lawname, r0.copy(), v0.copy(), sd["korbits"], sd["dt_base"], sd["steps_per_orbit"])
        np.savez_compressed(os.path.join(HERE, f"series_{args.lawname}.npz"), errs=e, crossings=c, death=d)
        analyse(e, c, d, sd["korbits"], args.lawname, res)
        json.dump(res, open(os.path.join(HERE, f"partial_{args.lawname}.json"), "w"), indent=1)
    elif args.mode == "analyse":
        sd = json.load(open(os.path.join(HERE, "seeds.json")))
        for law in ("sym-fixed", "sym-var", "rk4-fixed", "sym-sched"):
            f = os.path.join(HERE, f"series_{law}.npz")
            if not os.path.exists(f):
                print(f"missing {f}")
                continue
            z = np.load(f)
            analyse(z["errs"], z["crossings"], z["death"], sd["korbits"], law, res)
        json.dump(res, open(os.path.join(HERE, "b12_alpha.json"), "w"), indent=1)
        print("\nwrote b12_alpha.json")


if __name__ == "__main__":
    main()
