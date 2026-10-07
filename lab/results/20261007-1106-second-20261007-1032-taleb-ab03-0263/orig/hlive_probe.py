#!/usr/bin/env python3
"""H_live probe: distinctions per game-second created by the plane's real dynamics.

Scene anchored to the plane (crates/universe/src/scenario.rs): star, Giant (Jupiter-like,
mu=2^-10, a=4.94 AU, e=0.05), belt test particles 2.0-3.5 AU (B18b shape: banded a, Rayleigh
e sigma=0.1, uniform angles) + Giant-crossers 5.5-6.5 AU. Solar-normalized: GM=4*pi^2 AU^3/yr^2.
1 play-hour at rtf 100 = 3600*100 s = 0.0114 yr.

Law-matched split: drift is exact Kepler (the program covers it: a frozen birth state plus
exact drift predicts the unperturbed belt forever); kicks carry the Giant (direct + indirect
term). Scars = quantized tube-column deltas (E Q48, L Q32 over the belt's birth span; omega and
mean anomaly u32 over 2pi) vs the program. Smooth control: subtract a smooth-in-a median drift
(the physics g(a) a real program would hold).
"""
import numpy as np, json, time, os

TAU = 2 * np.pi
GM = 4 * np.pi ** 2
MU = 2.0 ** -10
AJ, EJ = 4.94, 0.05
HOUR = 3600.0 * 100 / 3.156e7  # play-hour in yr at rtf 100

rng = np.random.default_rng(20261007)
N_BELT, N_CROSS = 65536, 4096
N = N_BELT + N_CROSS

def birth():
    a = np.concatenate([2.0 + 1.5 * rng.random(N_BELT), 5.5 + 1.0 * rng.random(N_CROSS)])
    e = np.concatenate([np.sqrt(-2 * 0.1 ** 2 * np.log(1 - rng.random(N_BELT))),
                        np.sqrt(-2 * 0.1 ** 2 * np.log(1 - rng.random(N_CROSS)))])
    e = np.clip(e, 1e-6, 0.45)
    w = rng.random(N) * TAU          # periapsis angle
    lam = rng.random(N) * TAU        # mean longitude
    return a, e, w, lam

def kepler_E(M, e):
    E = M + e * np.sin(M)
    for _ in range(8):
        f = E - e * np.sin(E) - M
        E = E - f / (1 - e * np.cos(E))
    return E

def elem_to_cart(a, e, w, lam):
    n = np.sqrt(GM / a ** 3)
    E = kepler_E((lam - w) % TAU, e)
    c, s = np.cos(E), np.sin(E)
    den = 1 - e * c
    xo, yo = a * (c - e), a * np.sqrt(1 - e * e) * s
    vxo, vyo = -a * n * s / den, a * n * np.sqrt(1 - e * e) * c / den
    cw, sw = np.cos(w), np.sin(w)
    return (cw * xo - sw * yo, sw * xo + cw * yo,
            cw * vxo - sw * vyo, sw * vxo + cw * vyo)

def cart_to_elem(x, y, vx, vy):
    r = np.hypot(x, y); v2 = vx * vx + vy * vy; rv = x * vx + y * vy
    a = 1.0 / (2.0 / r - v2 / GM)
    ex = (v2 / GM - 1.0 / r) * x - (rv / GM) * vx
    ey = (v2 / GM - 1.0 / r) * y - (rv / GM) * vy
    e = np.clip(np.hypot(ex, ey), 1e-9, None)
    w = np.arctan2(ey, ex)
    cosE = np.clip((1 - r / a) / e, -1, 1)
    sinE = np.clip(rv / (e * np.sqrt(GM * a)), -1, 1)
    E = np.arctan2(sinE, cosE)
    lam = w + E - e * sinE
    return a, e, w, lam % TAU

def giant_path(t):
    nJ = np.sqrt(GM * (1 + MU) / AJ ** 3)
    gx, gy, _, _ = elem_to_cart(np.array([AJ]), np.array([EJ]), np.array([0.7]),
                                np.array([(0.3 + nJ * t) % TAU]))
    return gx[0], gy[0]

def run(a0, e0, w0, lam0, mu, dt, T, epochs, track_cross=False):
    a, e, w, lam = a0.copy(), e0.copy(), w0.copy(), lam0.copy()
    n0 = np.sqrt(GM / a0 ** 3)
    out = {}
    mind = np.full(N, 9e9) if track_cross else None
    steps = int(round(T / dt))
    t = 0.0
    for st in range(steps):
        lam = lam + np.sqrt(GM / a ** 3) * dt
        x, y, vx, vy = elem_to_cart(a, e, w, lam)
        gx, gy = giant_path(t + 0.5 * dt)
        dx, dy = gx - x, gy - y
        d = np.hypot(dx, dy)
        if track_cross:
            np.minimum(mind, d, out=mind)
        rJ = np.hypot(gx, gy)
        k = GM * mu * dt
        vx += k * (dx / d ** 3 - gx / rJ ** 3)
        vy += k * (dy / d ** 3 - gy / rJ ** 3)
        a, e, w, lam = cart_to_elem(x, y, vx, vy)
        t += dt
        for E_ in list(epochs):
            if abs(t - E_) < 0.5 * dt and E_ not in out:
                out[E_] = snapshot(a, e, w, lam, a0, e0, w0, lam0, n0, t)
    if track_cross:
        out["mind_giant"] = mind
    return out

def snapshot(a, e, w, lam, a0, e0, w0, lam0, n0, t):
    dE = -GM / (2 * a) - (-GM / (2 * a0))
    dL = np.sqrt(GM * a * (1 - e * e)) - np.sqrt(GM * a0 * (1 - e0 * e0))
    dw = np.angle(np.exp(1j * (w - w0)))
    dlam = np.angle(np.exp(1j * (lam - (lam0 + n0 * t))))
    return dict(t=t, a=a.copy(), dE=dE, dL=dL, dw=dw, dM=dlam - dw)

# quanta from the belt's birth span (the doll's exponent is set by its content)
a0, e0, w0, lam0 = birth()
qE = 2.0 ** 48 / abs(-GM / (2 * 3.5) + GM / (2 * 2.0))
L = np.sqrt(GM * a0 * (1 - e0 ** 2))
qL = 2.0 ** 32 / (L[:N_BELT].max() - L[:N_BELT].min())
qW = 2.0 ** 32 / TAU

def bits(dq, width):
    q = np.abs(dq)
    b = np.where(q >= 1, 1 + np.log2(np.clip(q, 1, 2.0 ** width)), 0.0)
    return b

def col_bits(s):
    return dict(E=bits(s["dE"] * qE, 48), L=bits(s["dL"] * qL, 32),
                w=bits(s["dw"] * qW, 32), M=bits(s["dM"] * qW, 32))
def smooth_resid(col, a0v):
    # subtract the smooth-in-a median drift (a physical g(a) program), interpolated per body
    o = np.argsort(a0v)
    bs = np.array_split(o, 128)
    centers = np.array([a0v[b].mean() for b in bs])
    med = np.array([np.median(col[b]) for b in bs])
    fit = np.interp(a0v, centers, med)
    return col - fit

RES = {"3:1": 2.501, "5:2": 2.824, "7:3": 2.958, "2:1": 3.117}
def res_dist(a):
    return min(abs(a - r) for r in RES.values())

report = {"hour_yr": HOUR, "N": N, "N_belt": N_BELT, "N_cross": N_CROSS,
          "load": open("/proc/loadavg").read().strip(),
          "mem": os.popen("free -m | awk 'NR==2{print $2, $3, $4}'").read().strip(),
          "GM": GM, "mu": MU}

t_start = time.time()

# control: mu = 0
ctrl = run(a0, e0, w0, lam0, 0.0, 0.05, 1.0, [1.0])
cb = col_bits(ctrl[1.0])
report["control_mu0_maxbits"] = float(max(cb[c].max() for c in cb))
report["control_mu0_scarred"] = int(sum((cb[c] >= 1).sum() for c in cb))

# fine run: play-hours; coarse run: years
fine = run(a0, e0, w0, lam0, MU, HOUR / 8, 0.05, [HOUR, 2 * HOUR, 0.05])
coarse = run(a0, e0, w0, lam0, MU, 0.0625, 20.0, [0.1, 0.25, 0.5, 1.0, 2.0, 5.0, 10.0, 20.0],
             track_cross=True)

rows = []
prev_scar = None
for tag, snap in sorted([(f"{t:.4f}yr", s) for t, s in fine.items() if isinstance(t, float)] +
                        [(f"{t:.4f}yr", s) for t, s in coarse.items() if isinstance(t, float)],
                        key=lambda kv: kv[1]["t"] if isinstance(kv[1], dict) else 0):
    if not isinstance(snap, dict) or "dE" not in snap:
        continue
    cb = col_bits(snap)
    tot = cb["E"] + cb["L"] + cb["w"] + cb["M"]
    scarred = tot >= 1
    scar = scarred[:N_BELT]
    k = int(scar.sum())
    ef = 2 + np.log2(N_BELT / k) if k else 0.0
    per_body_belt = tot[:N_BELT] + np.where(scar, ef, 0.0)
    # smooth-program residuals (belt only)
    sr = {c: smooth_resid(snap[c], a0)[:N_BELT] for c in ("dE", "dL", "dw", "dM")}
    cbS = dict(E=bits(sr["dE"] * qE, 48), L=bits(sr["dL"] * qL, 32),
               w=bits(sr["dw"] * qW, 32), M=bits(sr["dM"] * qW, 32))
    totS = (cbS["E"] + cbS["L"] + cbS["w"] + cbS["M"])
    # resonance attribution of the tail (belt only)
    rd = np.array([res_dist(x) for x in a0[:N_BELT]])
    tail = np.argsort(totS[:N_BELT])[-max(1, N_BELT // 100):]  # top 1% by irreducible bits
    reab = {}
    if prev_scar is not None:
        for c in cb:
            now0 = (cb[c][:N_BELT] < 1)
            reab[c] = int((prev_scar[c] & now0).sum())
    prev_scar = {c: cb[c][:N_BELT] >= 1 for c in cb}
    rows.append(dict(
        t_yr=snap["t"], play_hr=snap["t"] / HOUR,
        frozen_mean=float(tot[:N_BELT].mean()), frozen_p50=float(np.median(tot[:N_BELT])),
        frozen_p99=float(np.percentile(tot[:N_BELT], 99)), frozen_max=float(tot[:N_BELT].max()),
        scarred_frac=k / N_BELT,
        ef_bits=float(ef), total_bits_per_body=float(per_body_belt.mean()),
        smooth_mean=float(totS.mean()), smooth_p50=float(np.median(totS)),
        smooth_p99=float(np.percentile(totS, 99)), smooth_max=float(totS.max()),
        col_mean={c: float(cb[c][:N_BELT].mean()) for c in cb},
        tail_mean_res_au=float(rd[tail].mean()), tail_within_05AU=float((rd[tail] < 0.05).mean()),
        reabsorbed=reab,
        GB_per_hr_per_1e9_frozen=float(tot[:N_BELT].mean() / 8e9),
        GB_per_hr_per_1e9_smooth=float(totS.mean() / 8e9),
    ))

cross_mind = coarse.get("mind_giant")
cross_enc = int((cross_mind[:0] >= 0).sum()) if cross_mind is not None else None
last = [r for r in rows if abs(r["t_yr"] - 20.0) < 0.07]
report["crossers_min_d_AU"] = float(cross_mind[N_BELT:].min()) if cross_mind is not None else None
report["crossers_within_Hill034"] = int((cross_mind[N_BELT:] < 0.34).sum()) if cross_mind is not None else None
report["rows"] = rows
report["wall_s"] = time.time() - t_start
with open(os.path.join(os.path.dirname(__file__), "hlive.json"), "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=1))
for r in rows:
    print(f"t={r['t_yr']:8.4f}yr ({r['play_hr']:7.3f} play-hr) frozen mean/p99/max bits "
          f"{r['frozen_mean']:6.2f}/{r['frozen_p99']:6.2f}/{r['frozen_max']:7.2f} "
          f"smooth {r['smooth_mean']:5.2f}/{r['smooth_p99']:6.2f}/{r['smooth_max']:7.2f} "
          f"scarred {r['scarred_frac']:.4f} tail<0.05AU {r['tail_within_05AU']:.2f} "
          f"reab {r['reabsorbed']}")
