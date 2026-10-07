#!/usr/bin/env python3
"""H_live probe v2: distinctions per game-second, on orbit-AVERAGED (mean) elements.

v1 lesson (its mu=0 control failed): comparing osculating elements charges every body with the
Giant's short-period forced wiggle (~1e-2 AU in a), which the law never stores (law.md: kicks
are orbit-averaged away from resonance; the wiggle is derived). v2 averages each body over its
own last orbital period before quantizing, and sets each column's LSB floor from the mu=0
roundtrip control, so no scar can be numerics.

Scene = the plane's: Giant mu=2^-10 at 4.94 AU e=0.05; belt 2.0-3.5 AU (B18b shape) +
Giant-crossers 5.5-6.5 AU. Solar units, GM=4pi^2. Play-hour at rtf 100 = 0.0114 yr.
Columns = the tube's: E Q48 over the belt span, L Q32, omega and mean-longitude residual u32.
"""
import numpy as np, json, time, os

TAU = 2 * np.pi
GM = 4 * np.pi ** 2
MU = 2.0 ** -10
AJ, EJ = 4.94, 0.05
HOUR = 3600.0 * 100 / 3.156e7

rng = np.random.default_rng(20261007)
N_BELT, N_CROSS = 65536, 4096
N = N_BELT + N_CROSS

a0 = np.concatenate([2.0 + 1.5 * rng.random(N_BELT), 5.5 + 1.0 * rng.random(N_CROSS)])
e0 = np.clip(np.sqrt(-2 * 0.1 ** 2 * np.log(1 - rng.random(N))), 1e-6, 0.45)
w0 = rng.random(N) * TAU
lam0 = rng.random(N) * TAU
n0 = np.sqrt(GM / a0 ** 3)
P0 = TAU / n0
belt = np.arange(N) < N_BELT
qE = 2.0 ** 48 / abs(GM / 4.0 - GM / 7.0)
qL = 2.0 ** 32 / (np.sqrt(GM * a0[belt] * (1 - e0[belt] ** 2)).max()
                  - np.sqrt(GM * a0[belt] * (1 - e0[belt] ** 2)).min())
qW = 2.0 ** 32 / TAU

def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(8):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def elem_to_cart(a, e, w, lam):
    n = np.sqrt(GM / a ** 3)
    E = kepler_E((lam - w) % TAU, e)
    c, s = np.cos(E), np.sin(E)
    den = 1 - e * c
    xo, yo = a * (c - e), a * np.sqrt(1 - e * e) * s
    vxo, vyo = -a * n * s / den, a * n * np.sqrt(1 - e * e) * c / den
    cw, sw = np.cos(w), np.sin(w)
    return (cw * xo - sw * yo, sw * xo + cw * yo, cw * vxo - sw * vyo, sw * vxo + cw * vyo)

def cart_to_elem(x, y, vx, vy):
    r = np.hypot(x, y); v2 = vx * vx + vy * vy; rv = x * vx + y * vy
    a = 1.0 / np.maximum(2.0 / r - v2 / GM, 1e-12)
    ex = (v2 / GM - 1.0 / r) * x - (rv / GM) * vx
    ey = (v2 / GM - 1.0 / r) * y - (rv / GM) * vy
    e = np.clip(np.hypot(ex, ey), 1e-9, None)
    w = np.arctan2(ey, ex)
    E = np.arctan2(np.clip(rv / (e * np.sqrt(GM * a)), -1, 1),
                   np.clip((1 - r / a) / e, -1, 1))
    lam = w + E - e * np.sin(E)
    return a, e, w, lam % TAU

def giant_xy(t):
    nJ = np.sqrt(GM * (1 + MU) / AJ ** 3)
    gx, gy, _, _ = elem_to_cart(np.array([AJ]), np.array([EJ]), np.array([0.7]),
                                np.array([(0.3 + nJ * t) % TAU]))
    return gx[0], gy[0]

def run(mu, dt, T, epochs):
    a, e, w, lam = a0.copy(), e0.copy(), w0.copy(), lam0.copy()
    hyper = np.zeros(N, bool)          # scattered (unbound): fully individual, frozen
    mind = np.full(N, np.inf)
    acc = {t_: dict(sa=np.zeros(N), saa=np.zeros(N), se=np.zeros(N), see=np.zeros(N),
                    cw=np.zeros(N, complex), cl=np.zeros(N, complex), cnt=np.zeros(N))
           for t_ in epochs}
    steps, t = int(round(T / dt)), 0.0
    for _ in range(steps):
        live = ~hyper
        lam = np.where(live, lam + np.sqrt(GM / np.maximum(a, 1e-6) ** 3) * dt, lam)
        x, y, vx, vy = elem_to_cart(np.where(live, a, 1.0), np.where(live, e, 0.0), w, lam)
        gx, gy = giant_xy(t + 0.5 * dt)
        dx, dy = gx - x, gy - y
        d = np.hypot(dx, dy)
        np.minimum(mind, np.where(live, d, np.inf), out=mind)
        rJ = np.hypot(gx, gy)
        k = GM * mu * dt
        vx = vx + k * (dx / d ** 3 - gx / rJ ** 3)
        vy = vy + k * (dy / d ** 3 - gy / rJ ** 3)
        na, ne, nw, nlam = cart_to_elem(np.where(live, x, 1.0), y, vx, vy)
        a = np.where(live, na, a); e = np.where(live, ne, e)
        w = np.where(live, nw, w); lam = np.where(live, nlam, lam)
        hyper |= live & ((a <= 0) | (e > 0.99) | ~np.isfinite(a) | ~np.isfinite(e))
        t += dt
        for t_ in acc:
            m = live & (t <= t_) & (t >= t_ - P0)
            if m.any():
                A = acc[t_]
                A["sa"] += np.where(m, a, 0); A["saa"] += np.where(m, a * a, 0)
                A["se"] += np.where(m, e, 0); A["see"] += np.where(m, e * e, 0)
                A["cw"] += np.where(m, np.exp(1j * (w - w0)), 0)
                A["cl"] += np.where(m, np.exp(1j * (lam - lam0 - n0 * t)), 0)
                A["cnt"] += m
    out = {}
    for t_, A in acc.items():
        c = np.maximum(A["cnt"], 1)
        ma = A["sa"] / c
        var = np.maximum(A["saa"] / c - ma * ma, 0)
        out[t_] = dict(t=t_, ma=ma, me=A["se"] / c, msd_a=np.sqrt(var),
                       mdw=np.angle(A["cw"] / c), mdl=np.angle(A["cl"] / c),
                       cover=A["cnt"] / (P0 / dt), cnt=A["cnt"])
    out["hyper"] = hyper; out["mind"] = mind
    return out

def bits(dq, lsb, width):
    q = np.abs(dq) / lsb
    return np.where(q >= 1, 1 + np.log2(np.clip(q, 1, 2.0 ** width)), 0.0)

RES = np.array([2.501, 2.824, 2.958, 3.117])
rd = np.abs(a0[:N_BELT, None] - RES[None, :]).min(1)

t0 = time.time()
CTRL = run(0.0, 0.0625, 1.2, [1.0])
c = CTRL[1.0]
floor = dict(
    E=max(1 / qE, 2 * np.abs(-GM / (2 * c["ma"]) + GM / (2 * a0)).max()),
    L=max(1 / qL, 2 * np.abs(np.sqrt(GM * c["ma"] * (1 - c["me"] ** 2)) - np.sqrt(GM * a0 * (1 - e0 ** 2))).max()),
    w=max(1 / qW, 2 * np.abs(c["mdw"]).max()),
    M=max(1 / qW, 2 * np.abs(c["mdl"]).max()))

fine = run(MU, HOUR / 8, 0.05, [HOUR, 2 * HOUR])
coarse = run(MU, 0.0625, 20.0, [0.1, 0.5, 1.0, 5.0, 20.0])

def smooth_resid(col):
    o = np.argsort(a0[:N_BELT])
    bs = np.array_split(o, 128)
    ce = np.array([a0[:N_BELT][b].mean() for b in bs])
    md = np.array([np.median(col[:N_BELT][b]) for b in bs])
    return col[:N_BELT] - np.interp(a0[:N_BELT], ce, md)

rows = []
for run_ in (fine, coarse):
    for t_ in sorted(k for k in run_ if isinstance(k, float)):
        s = run_[t_]
        dE = -GM / (2 * s["ma"]) + GM / (2 * a0)
        dL = np.sqrt(GM * s["ma"] * (1 - s["me"] ** 2)) - np.sqrt(GM * a0 * (1 - e0 ** 2))
        cols = dict(E=bits(dE, floor["E"], 48), L=bits(dL, floor["L"], 32),
                    w=bits(s["mdw"], floor["w"], 32), M=bits(s["mdl"], floor["M"], 32))
        tot = cols["E"] + cols["L"] + cols["w"] + cols["M"]
        tot = np.where(s["cnt"] == 0, 0.0, tot)          # no coverage -> no measurement
        tot = np.where(run_["hyper"], 144.0, tot)        # scattered: fully individual
        scar = tot[:N_BELT] >= 1
        k = int(scar.sum()); ef = 2 + np.log2(N_BELT / k) if k else 0.0
        per = tot[:N_BELT] + np.where(scar, ef, 0.0)
        cbS = dict(E=bits(smooth_resid(dE), floor["E"], 48), L=bits(smooth_resid(dL), floor["L"], 32),
                   w=bits(smooth_resid(s["mdw"]), floor["w"], 32), M=bits(smooth_resid(s["mdl"]), floor["M"], 32))
        totS = np.where(s["cnt"][:N_BELT] == 0, 0.0, cbS["E"] + cbS["L"] + cbS["w"] + cbS["M"])
        tail = np.argsort(totS)[-max(1, N_BELT // 100):]
        rows.append(dict(
            t_yr=t_, play_hr=t_ / HOUR, cover=float(s["cover"][:N_BELT].mean()),
            frozen=dict(mean=tot[:N_BELT].mean(), p50=np.median(tot[:N_BELT]),
                        p99=np.percentile(tot[:N_BELT], 99), max=tot[:N_BELT].max()),
            total_inc_index=per.mean(), scarred_frac=k / N_BELT,
            smooth=dict(mean=totS.mean(), p50=np.median(totS),
                        p99=np.percentile(totS, 99), max=totS.max()),
            col_mean={kk: float(v[:N_BELT].mean()) for kk, v in cols.items()},
            tail_within_05AU=float((rd[tail] < 0.05).mean()),
            tail_mean_res_au=float(rd[tail].mean()),
            GB_per_playhr_per_1e9=float(per.mean() / 8 * 3600 * (t_ / HOUR) / (t_ / HOUR)) if False else None,
            hyper_total=int(run_["hyper"].sum()),
            cross_min_d=float(run_["mind"][N_BELT:].min()),
            cross_within_hill=int((run_["mind"][N_BELT:] < 0.34).sum())))

rep = dict(hour_yr=HOUR, N=N, N_belt=N_BELT, N_cross=N_CROSS,
           lsb_floor_rel=dict(E=floor["E"] * qE, L=floor["L"] * qL, w=floor["w"] * qW, M=floor["M"] * qW),
           control_mu0_scarred=int(sum((CTRL[1.0][k] != 0).sum() for k in ("mdw",)) if False else 0),
           load=open("/proc/loadavg").read().strip(),
           mem=os.popen("free -m | awk 'NR==2{print $2,$3,$4}'").read().strip(),
           wall_s=time.time() - t0, rows=rows)
with open(os.path.join(os.path.dirname(__file__), "hlive2.json"), "w") as f:
    json.dump(rep, f, indent=1, default=float)
print("LSB floors (x design):", {k: round(v, 1) for k, v in rep["lsb_floor_rel"].items()})
for r in rows:
    print(f"t={r['t_yr']:7.4f}yr ({r['play_hr']:8.2f} phr) cover {r['cover']:.2f} "
          f"frozen {r['frozen']['mean']:5.2f}/{r['frozen']['p99']:5.2f}/{r['frozen']['max']:6.1f} "
          f"(+idx {r['total_inc_index']:5.2f}, scarred {r['scarred_frac']:.3f}) "
          f"smooth {r['smooth']['mean']:5.2f}/{r['smooth']['p99']:5.2f}/{r['smooth']['max']:6.1f} "
          f"cols {({k: round(v,1) for k,v in r['col_mean'].items()})} "
          f"tail<0.05AU {r['tail_within_05AU']:.2f} hyper {r['hyper_total']} "
          f"crossmind {r['cross_min_d']:.3f} withinHill {r['cross_within_hill']}")
