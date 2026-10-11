#!/usr/bin/env python3
"""Belt information-production instrument — run 20261011-1332-dynamics-8269.

Restricted Sun-Jupiter-Saturn (planets on prescribed Kepler orbits, no mutual J-S
interaction), planar test bodies advanced by a symplectic Kepler map
(exact Kepler drift under the Sun + planetary kicks with the indirect term, KDK).
Measures per body: Lyapunov exponent (shadow renormalization, d0 = 1e-9 AU,
renormalized each Jupiter orbit), filtered (81-orbit running mean of 10-per-orbit
bin means, a proper-element proxy) element deviation from birth, and quantum-hitting
rates. Config: dt = P_J/100 (~24 steps/orbit at a = 2 AU), T = 5000 Jupiter orbits.

Phases: C1, C2, R1, R1f (each saves raw_<tag>.npz), then `analyze`.
Floats explore; this measures rates and behaviours, not canonical outcomes.
"""
import numpy as np, json, time, sys, os

MU = 4.0 * np.pi ** 2          # AU^3 / yr^2
M_J, M_S = 9.5458e-4, 2.858e-4  # solar masses
A_J, E_J, A_S, E_S = 5.2, 0.048, 9.54, 0.054
MUJ, MUS = MU * M_J, MU * M_S
D0 = 1e-9                      # shadow offset (AU)
OUT = os.path.dirname(os.path.abspath(__file__))


def kepler_solve(M, e, iters=8):
    E = M + e * np.sin(M)
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1.0 - e * np.cos(E))
    return E


def elem_to_state(a, e, M, w, mu=MU):
    E = kepler_solve(M, e)
    X = a * (np.cos(E) - e)
    Y = a * np.sqrt(1 - e * e) * np.sin(E)
    n = np.sqrt(mu / a ** 3)
    Ed = n / (1 - e * np.cos(E))
    VX = -a * np.sin(E) * Ed
    VY = a * np.sqrt(1 - e * e) * np.cos(E) * Ed
    c, s = np.cos(w), np.sin(w)
    return X * c - Y * s, X * s + Y * c, VX * c - VY * s, VX * s + VY * c


def state_to_elem(x, y, vx, vy, mu=MU):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    a = 1.0 / (2.0 / r - v2 / mu)
    cf = v2 - mu / r
    ex = (cf * x - rv * vx) / mu
    ey = (cf * y - rv * vy) / mu
    return a, np.hypot(ex, ey)


def drift(x, y, vx, vy, dt, mu=MU):
    """Exact elliptic Kepler drift (f&g in eccentric anomaly). Unbound -> frozen."""
    r0 = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    with np.errstate(divide="ignore", invalid="ignore"):
        a = 1.0 / (2.0 / r0 - v2 / mu)
    cf = v2 - mu / r0
    ex = (cf * x - rv * vx) / mu
    ey = (cf * y - rv * vy) / mu
    e = np.hypot(ex, ey)
    ok = (a > 1e-3) & (e < 0.995) & np.isfinite(a) & np.isfinite(e)
    a_ = np.where(ok, a, 1.0)
    e_ = np.clip(np.where(ok, e, 0.0), 0.0, 0.99)
    sa = np.sqrt(mu * a_)
    cosE0 = np.clip((1.0 - r0 / a_) / np.maximum(e_, 1e-12), -1, 1)
    sinE0 = np.where(e_ > 1e-12, rv / np.maximum(e_ * sa, 1e-300), 0.0)
    E0 = np.arctan2(sinE0, cosE0)
    n = np.sqrt(mu / a_ ** 3)
    M1 = E0 - e_ * np.sin(E0) + n * dt
    E1 = kepler_solve(M1, e_)
    dE = E1 - E0
    cd, sd = np.cos(dE), np.sin(dE)
    r1 = a_ * (1.0 - e_ * np.cos(E1))
    f = 1.0 - (a_ / r0) * (1.0 - cd)
    g = dt - (dE - sd) / n
    fd = -(sa / (r0 * r1)) * sd
    gd = 1.0 - (a_ / r1) * (1.0 - cd)
    return (np.where(ok, f * x + g * vx, x),
            np.where(ok, f * y + g * vy, y),
            np.where(ok, fd * x + gd * vx, vx),
            np.where(ok, fd * y + gd * vy, vy), ok)


def planet_track(a, e, w, M0, nst, dt):
    t = dt * np.arange(nst)
    n = np.sqrt(MU / a ** 3)
    E = kepler_solve(M0 + n * t, np.full(nst, e))
    X = a * (np.cos(E) - e)
    Y = a * np.sqrt(1 - e * e) * np.sin(E)
    c, s = np.cos(w), np.sin(w)
    px, py = X * c - Y * s, X * s + Y * c
    return px, py, (px * px + py * py) ** 1.5


def run_belt(tag, N, a0, e0, T_orb=5000.0, dt_orb=1.0 / 100, seed=8269):
    rng = np.random.default_rng(seed + (abs(hash(tag)) % 10000))
    Mn = rng.uniform(-np.pi, np.pi, N)
    w = rng.uniform(-np.pi, np.pi, N)
    x, y, vx, vy = elem_to_state(a0, e0, Mn, w)
    # stacked: [0:N] main, [N:2N] shadow (offset in x by D0)
    X = np.concatenate([x, x + D0])
    Y = np.concatenate([y, y])
    VX = np.concatenate([vx, vx])
    VY = np.concatenate([vy, vy])
    alive = np.ones(2 * N, bool)

    nst = int(round(T_orb / dt_orb))
    every = int(round(1.0 / dt_orb))
    sub = max(1, every // 10)
    dt = dt_orb * (2 * np.pi / np.sqrt(MU / A_J ** 3))  # in years
    nsamp = nst // every
    A = np.empty((nsamp, N))
    Ee = np.empty((nsamp, N))
    LS = np.zeros((nsamp, N))
    logsum = np.zeros(N)
    binA = np.zeros(N)
    binE = np.zeros(N)
    nbin = 0

    pxJ, pyJ, p3J = planet_track(A_J, E_J, 0.0, 0.6, nst + 1, dt)
    pxS, pyS, p3S = planet_track(A_S, E_S, 0.0, 2.9, nst + 1, dt)

    def accel(X, Y, k):
        dxJ, dyJ = pxJ[k] - X, pyJ[k] - Y
        d3J = (dxJ * dxJ + dyJ * dyJ) ** 1.5
        dxS, dyS = pxS[k] - X, pyS[k] - Y
        d3S = (dxS * dxS + dyS * dyS) ** 1.5
        return (MUJ * (dxJ / d3J - pxJ[k] / p3J[k]) + MUS * (dxS / d3S - pxS[k] / p3S[k]),
                MUJ * (dyJ / d3J - pyJ[k] / p3J[k]) + MUS * (dyS / d3S - pyS[k] / p3S[k]))

    t0 = time.time()
    for k in range(nst):
        ax, ay = accel(X, Y, k)
        VX += 0.5 * dt * ax
        VY += 0.5 * dt * ay
        X, Y, VX, VY, ok = drift(X, Y, VX, VY, dt)
        alive &= ok
        ax, ay = accel(X, Y, k + 1)
        VX += 0.5 * dt * ax
        VY += 0.5 * dt * ay
        if (k + 1) % sub == 0:
            aa, ee = state_to_elem(X[:N], Y[:N], VX[:N], VY[:N])
            binA += aa
            binE += ee
            nbin += 1
            if (k + 1) % every == 0:
                i = (k + 1) // every - 1
                A[i] = binA / nbin
                Ee[i] = binE / nbin
                binA[:] = 0.0
                binE[:] = 0.0
                nbin = 0
                ddx = X[N:] - X[:N]
                ddy = Y[N:] - Y[:N]
                dvx = VX[N:] - VX[:N]
                dvy = VY[N:] - VY[:N]
                d = np.sqrt(ddx * ddx + ddy * ddy + dvx * dvx + dvy * dvy)
                d = np.maximum(d, 1e-300)
                logsum += np.log(d / D0)
                LS[i] = logsum
                sc = D0 / d
                X[N:] = X[:N] + ddx * sc
                Y[N:] = Y[:N] + ddy * sc
                VX[N:] = VX[:N] + dvx * sc
                VY[N:] = VY[:N] + dvy * sc
                if i % 500 == 0:
                    print(f"  [{tag}] orbit {i+1}/{nsamp}  {time.time()-t0:.0f}s", flush=True)
    wall = time.time() - t0
    np.savez_compressed(os.path.join(OUT, f"raw_{tag}.npz"), A=A, E=Ee, LS=LS,
                        a0=a0, e0=e0, alive=alive[:N] & alive[N:],
                        T_orb=T_orb, dt_orb=dt_orb, wall=wall)
    print(f"[{tag}] done in {wall:.0f}s", flush=True)


def moving_mean(x, W=81):
    c = np.cumsum(np.vstack([np.zeros((1, x.shape[1])), x]), axis=0)
    return (c[W:] - c[:-W]) / W  # out[j] = mean of x[j:j+W], centred at j+W//2


def first_hit(d, q):
    over = np.abs(d) > q
    any_ = over.any(axis=0)
    return np.where(any_, over.argmax(axis=0), -1)


def analyze(r, W=81):
    A, E, LS = r["A"], r["E"], r["LS"]
    T = r["nsamp"]
    fA, fE = moving_mean(A, W), moving_mean(E, W)
    dA, dE = fA - fA[0:1], fE - fE[0:1]
    lam_late = (LS[-1] - LS[int(0.5 * T)]) / max(1, T - int(0.5 * T))
    good = r["alive"] & np.isfinite(A).all(axis=0) & (A.min(axis=0) > 0.3) \
        & (A.max(axis=0) < 15.0) & (E.max(axis=0) < 0.99)
    qs = [1e-4, 3e-4, 1e-3, 3e-3, 1e-2]
    qe = [1e-4, 3e-4, 1e-3, 3e-3]
    return dict(tag=r["tag"], N=r["N"], T_orb=r["T_orb"], dt_orb=r["dt_orb"],
                wall_s=round(float(r["wall"]), 1), nsamp=T, good=good,
                lam_late=lam_late, lam_all=LS[-1] / T, LS=LS,
                dA=dA, dE=dE,
                hits={f"{q:g}": first_hit(dA, q) for q in qs},
                hitse={f"{q:g}": first_hit(dE, q) for q in qe},
                syn=np.ptp(A[100:500], axis=0), a0=r["a0"], e0=r["e0"])


def summarise(res, cut=None):
    g = res["good"]
    lam, a0 = res["lam_late"][g], res["a0"][g]
    out = dict(tag=res["tag"], N_good=int(g.sum()), wall_s=res["wall_s"],
               lam_median=float(np.median(lam)),
               lam_p90=float(np.quantile(lam, 0.9)),
               syn_amp_median_au=float(np.median(res["syn"][g])))
    if cut is not None:
        chaotic = (res["lam_late"] > cut) & g
        quiet = ~chaotic
        out["chaotic_frac"] = float(chaotic.sum() / max(1, g.sum()))
        for key, hd in (("a", res["hits"]), ("e", res["hitse"])):
            for q, h in hd.items():
                hit = (h >= 0) & g
                late = (h > 0.5 * res["nsamp"]) & g
                out[f"hitfrac_{key}_{q}"] = float(hit.sum() / max(1, g.sum()))
                out[f"lateflux_{key}_{q}_per_kilo_orbit"] = \
                    float(late.sum() / max(1, g.sum()) / (0.5 * res["nsamp"] / 1000))
                out[f"hitfrac_{key}_{q}_quiet"] = float((hit & quiet).sum() / max(1, quiet.sum()))
                out[f"hitfrac_{key}_{q}_chaotic"] = float((hit & chaotic).sum() / max(1, chaotic.sum()))
    bins = np.arange(2.0, 3.32, 0.02)
    bl, ba = [], []
    for lo in bins:
        m = (a0 >= lo) & (a0 < lo + 0.02)
        if m.sum() >= 3:
            bl.append(float(np.median(lam[m])))
            ba.append(float(lo + 0.01))
    out["lambda_bins_a"], out["lambda_bins_med"] = ba, bl
    return out


def spawn(tag):
    rng = np.random.default_rng(8269)
    if tag == "C1":
        a0 = 3.10 + rng.uniform(-0.004, 0.004, 256)
        e0 = np.clip(rng.rayleigh(0.01, 256), 0, 0.25)
        run_belt("C1", 256, a0, e0)
    elif tag == "C2":
        a0 = 2.502 + rng.uniform(-0.003, 0.003, 256)
        e0 = np.clip(rng.rayleigh(0.05, 256), 0, 0.25)
        run_belt("C2", 256, a0, e0)
    elif tag == "R1":
        a0 = rng.uniform(2.0, 3.3, 1024)
        e0 = np.clip(rng.rayleigh(0.07, 1024), 0, 0.25)
        run_belt("R1", 1024, a0, e0)
    elif tag == "R1f":
        a0 = rng.uniform(2.0, 3.3, 512)
        e0 = np.clip(rng.rayleigh(0.07, 512), 0, 0.25)
        run_belt("R1f", 512, a0, e0, T_orb=1000.0, dt_orb=1.0 / 200)
    else:
        raise SystemExit(f"unknown phase {tag}")


def analyze_all():
    an = {}
    for k in ("C1", "C2", "R1", "R1f"):
        z = np.load(os.path.join(OUT, f"raw_{k}.npz"))
        r = dict(A=z["A"], E=z["E"], LS=z["LS"], a0=z["a0"], e0=z["e0"],
                 alive=z["alive"], tag=k, N=len(z["a0"]),
                 T_orb=float(z["T_orb"]), dt_orb=float(z["dt_orb"]),
                 wall=float(z["wall"]), nsamp=z["A"].shape[0])
        an[k] = analyze(r)
    floor = float(np.median(an["C1"]["lam_late"][an["C1"]["good"]]))
    cut = 10.0 * max(abs(floor), 1e-6)
    S = {k: summarise(an[k], cut if k in ("C2", "R1") else None) for k in an}
    S["_config"] = dict(floor_lam_C1=floor, cut=cut,
                        C2_over_C1=S["C2"]["lam_median"] / max(abs(floor), 1e-9),
                        T_orb=5000, dt_orb=0.01, W_filter=81, d0=D0,
                        scene="planar restricted S-J-S, planets prescribed Kepler")
    gR, gF = an["R1"]["good"], an["R1f"]["good"]
    S["_conv"] = dict(
        lam_med_1k_dt100=float(np.median(an["R1"]["LS"][999][gR] / 1000)),
        lam_med_1k_dt200=float(np.median(an["R1f"]["LS"][999][gF] / 1000)),
        hit1e3_q1e3_dt100=float(((an["R1"]["hits"]["0.001"] >= 0) & (an["R1"]["hits"]["0.001"] < 1000) & gR).mean()),
        hit1e3_q1e3_dt200=float(((an["R1f"]["hits"]["0.001"] >= 0) & gF).mean()))
    g = an["R1"]["good"]
    times = np.unique(np.logspace(0, np.log10(an["R1"]["nsamp"] - 90), 40).astype(int))
    curves = {q: [float(((h >= 0) & (h <= t) & g).mean()) for t in times]
              for q, h in an["R1"]["hits"].items()}
    S["_curves_R1"] = dict(times=times.tolist(), curves=curves)
    # filtered-a deviation magnitude distribution (end of run), quiet vs chaotic
    lamR = an["R1"]["lam_late"]
    cha = (lamR > cut) & g
    qui = (lamR <= cut) & g
    endA = np.abs(an["R1"]["dA"][-1])
    S["_enddev_R1"] = dict(
        quiet_median_au=float(np.median(endA[qui])), quiet_p90_au=float(np.quantile(endA[qui], 0.9)),
        chaotic_median_au=float(np.median(endA[cha])) if cha.any() else None,
        chaotic_p90_au=float(np.quantile(endA[cha], 0.9)) if cha.any() else None)
    np.save(os.path.join(OUT, "bodies_R1.npy"), np.vstack([
        an["R1"]["a0"], an["R1"]["e0"], an["R1"]["lam_late"],
        an["R1"]["hits"]["0.001"], an["R1"]["hits"]["0.0001"]]).T.astype(np.float32))
    np.save(os.path.join(OUT, "dA_series_R1.npy"), an["R1"]["dA"][:, ::16].astype(np.float32))
    with open(os.path.join(OUT, "metrics.json"), "w") as f:
        json.dump(S, f, indent=1, default=float)
    print("FLOOR", floor, "CUT", cut, " C2/C1", S["_config"]["C2_over_C1"])
    for k in ("C1", "C2", "R1"):
        print(json.dumps({kk: v for kk, v in S[k].items()
                          if not kk.startswith("lambda_bins")}, default=float))
    print("_conv", json.dumps(S["_conv"]))
    print("_enddev", json.dumps(S["_enddev_R1"]))


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "analyze"
    if phase in ("C1", "C2", "R1", "R1f"):
        spawn(phase)
    else:
        analyze_all()
