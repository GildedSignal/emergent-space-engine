#!/usr/bin/env python3
"""Follow-up diagnostics for the twin result (chosen after seeing it - post-hoc, labeled).

The secular twin leaves ~all of the belt's mean-element drift unexplained (var expl ~0),
the synodic window does not remove it, and clones show no chaos. Candidate mechanism:
small-divisor (near-resonant) quasiperiodic envelopes of the mean elements. Two probes:

  (D) bounded vs diffusive: full field to 60 yr on a 16,384-body subset; rms/median |ma-a0|
      and E-bits vs t (5/20/40/60). Quasiperiodic envelope -> saturates; diffusion -> keeps
      climbing ~log t. Also per-body |ma-a0| correlation between epochs (persistent structure).
  (E) resonant-angle absorption: bin medians of dE over (a, theta_res) where theta_res is the
      deterministic phase of each body's nearest p:q commensurability with the Giant
      (continued fractions, q<=8), compared against (a, synodic phase) bins of the same shape
      (the checker's form, 5.1% absorbed) and an (a) only null.
"""
import numpy as np, json, time, os

TAU = 2 * np.pi
GM = 4 * np.pi ** 2
MU = 2.0 ** -10
AJ, EJ = 4.94, 0.05
NJ = np.sqrt(GM * (1 + MU) / AJ ** 3)
LAMG0 = 0.3

rng = np.random.default_rng(20261007)
N_BELT, N_CROSS = 65536, 4096
N = N_BELT + N_CROSS
a0 = np.concatenate([2.0 + 1.5 * rng.random(N_BELT), 5.5 + 1.0 * rng.random(N_CROSS)])
e0 = np.clip(np.sqrt(-2 * 0.1 ** 2 * np.log(1 - rng.random(N))), 1e-6, 0.45)
w0 = rng.random(N) * TAU
lam0 = rng.random(N) * TAU
n0 = np.sqrt(GM / a0 ** 3)
NS = 16384
A0, E0, W0, L0, N0 = (v[:NS] for v in (a0[:N_BELT], e0[:N_BELT], w0[:N_BELT], lam0[:N_BELT], n0[:N_BELT]))
P0 = TAU / N0

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
    gx, gy, _, _ = elem_to_cart(np.array([AJ]), np.array([EJ]), np.array([0.7]),
                                np.array([(LAMG0 + NJ * t) % TAU]))
    return gx[0], gy[0]

t0 = time.time()
EP = [5.0, 20.0, 40.0, 60.0]
acc = {t_: dict(sa=np.zeros(NS), cnt=np.zeros(NS)) for t_ in EP}
a, e, w, lam = A0.copy(), E0.copy(), W0.copy(), L0.copy()
dt, T = 0.0625, 60.0
steps, t = int(round(T / dt)), 0.0
for _ in range(steps):
    lam = lam + np.sqrt(GM / np.maximum(a, 1e-6) ** 3) * dt
    x, y, vx, vy = elem_to_cart(a, e, w, lam)
    gx, gy = giant_xy(t + 0.5 * dt)
    dx, dy = gx - x, gy - y
    d = np.hypot(dx, dy)
    rJ = np.hypot(gx, gy)
    k = GM * MU * dt
    vx = vx + k * (dx / d ** 3 - gx / rJ ** 3)
    vy = vy + k * (dy / d ** 3 - gy / rJ ** 3)
    a, e, w, lam = cart_to_elem(x, y, vx, vy)
    t += dt
    for t_ in EP:
        m = (t <= t_) & (t >= t_ - P0)
        acc[t_]["sa"] += np.where(m, a, 0)
        acc[t_]["cnt"] += m
print(f"[{time.time()-t0:6.1f}s] 60-yr subset run done")

ma = {t_: acc[t_]["sa"] / np.maximum(acc[t_]["cnt"], 1) for t_ in EP}
dE = {t_: -GM / (2 * ma[t_]) + GM / (2 * A0) for t_ in EP}

# (D) bounded vs diffusive
qE = 2.0 ** 48 / abs(GM / 4.0 - GM / 7.0)
# floor from the shipped control (mu=0 worst |dE| over the belt was floor_E*0.132 of design):
FLOOR_E = 7.565315045294554 / qE       # = shipped lsb_floor_rel['E'] / qE, identical construction
rowsD = []
prev = None
for t_ in EP:
    bitsv = np.where(np.abs(dE[t_]) / FLOOR_E >= 1, 1 + np.log2(np.clip(np.abs(dE[t_]) / FLOOR_E, 1, 2.0 ** 48)), 0.0)
    med = float(np.nanmedian(np.abs(ma[t_] - A0)))
    row = dict(t_yr=t_, med_da_AU=med, rms_da=float(np.sqrt(np.nanmean((ma[t_] - A0) ** 2))), nan=float(np.mean(~np.isfinite(ma[t_]))),
               E_bits_mean=float(bitsv.mean()), E_bits_p50=float(np.median(bitsv)))
    if prev is not None:
        ok = np.isfinite(ma[t_]) & np.isfinite(ma[prev])
        row["corr_da_with_prev"] = float(np.corrcoef(ma[t_][ok] - A0[ok], ma[prev][ok] - A0[ok])[0, 1])
    rowsD.append(row)
    prev = t_

# (E) resonant-angle absorption at t=20
tR = 20.0
ratio = N0 / NJ
best = None
for q_ in range(1, 9):
    p_ = np.round(ratio * q_).astype(int)
    err = np.abs(ratio - p_ / q_)
    key = np.where((p_ >= 1) & (err < 0.06), err, 99)
    if best is None:
        best = (key, q_, p_)
    else:
        repl = key < best[0]
        best = (np.where(repl, key, best[0]), np.where(repl, q_, best[1]), np.where(repl, p_, best[2]))
keyerr, qb, pb = best
theta_res = (qb * L0 - pb * LAMG0 + (qb * N0 - pb * NJ) * tR) % TAU
theta_syn = (L0 - LAMG0 + (N0 - NJ) * tR) % TAU
val = dE[tR]

def absorbed(theta):
    ia = np.clip((A0 - 2.0) / 1.5 * 64, 0, 63).astype(int)
    ith = np.clip(theta / TAU * 32, 0, 31).astype(int)
    b = ia * 32 + ith
    med = np.zeros(64 * 32)
    cnt = np.zeros(64 * 32)
    np.add.at(cnt, b, 1)
    np.add.at(med, b, val)
    med = np.where(cnt > 0, med / np.maximum(cnt, 1), 0.0)
    # empty bins -> fall back to the a-only median of their a-strip
    ia_only = np.zeros(64)
    cnt_a = np.zeros(64)
    np.add.at(cnt_a, ia, 1)
    np.add.at(ia_only, ia, val)
    ia_only = np.where(cnt_a > 0, ia_only / np.maximum(cnt_a, 1), 0.0)
    med = np.where(cnt > 0, med, ia_only[np.repeat(np.arange(64), 32)])
    return float(1.0 - np.var(val - med[b]) / np.var(val))

resE = dict(
    a_theta_res=absorbed(theta_res), a_theta_syn=absorbed(theta_syn),
    a_only=float(1.0 - np.var(val - ia_only[ia]) / np.var(val)) if False else None)
# a-only null, properly
ia = np.clip((A0 - 2.0) / 1.5 * 64, 0, 63).astype(int)
ia_only = np.zeros(64); cnt_a = np.zeros(64)
np.add.at(cnt_a, ia, 1); np.add.at(ia_only, ia, val)
ia_only = np.where(cnt_a > 0, ia_only / np.maximum(cnt_a, 1), 0.0)
resE["a_only"] = float(1.0 - np.var(val - ia_only[ia]) / np.var(val))
# shuffle null for the 2D binning (same shape, permuted theta)
rng2 = np.random.default_rng(11)
nulls = [absorbed(rng2.permutation(theta_res)) for _ in range(5)]
resE["a_theta_res_null"] = float(np.mean(nulls))
# how many bodies got a q<=8 commensurability within 0.06
resE["frac_with_resonance"] = float((keyerr < 99).mean())
resE["q_hist"] = {int(q_): int((qb == q_).sum()) for q_ in range(1, 9)}

rep = dict(subset=NS, floor_E_rel=float(FLOOR_E * qE), bounded_vs_diffusive=rowsD,
           resonance_absorption=resE, wall_s=time.time() - t0)
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "followup.json"), "w") as f:
    json.dump(rep, f, indent=1, default=float)
print(json.dumps(rep, indent=1, default=float))
