#!/usr/bin/env python3
"""Real-kick ledger — second author on run 20261007-0621-scout-6e10.

The checker's named experiment, cheapest decisive part: the mix (smooth fraction,
sigma scales) of REAL kicks on B18b's belt scene, and whether real flyby kicks sit
in a low-order birth-feature basis (its A1). The plane's b-h-live build is queued and
the belt is not wired into the plane yet (b-belt-wire also queued), so the real kicks
are produced by integrating the scene under the plane's own force model
(crates/universe/src/force.rs `field`: the secondary's differential pull + the
origin's fall, no truncation), fixed-step velocity-Verlet at 700 steps/orbit (the
plane's cadence regime), each body for 10 of its own orbits = one ledger epoch.
The original run's scene constants, entropy convention (differential entropy per
component at the quantum, sum of the two) and 12-term basis are reused verbatim
(orig_h_live_ledger.py).

Modes (each a separate command, < 60 s):
  control  Jupiter off: the integrator's own noise floor on dz. -> ctrl.npz
  main     the real run + the program ladder. -> real_kick_ledger.json

Deterministic: seeded. ~2 x 45 s, < 300 MB.
"""
import json
import sys

import numpy as np

MODE = sys.argv[1] if len(sys.argv) > 1 else "main"
rng = np.random.default_rng(20261008)
C2PI = 2 * np.pi
R = {}

# ---------------- scene (the original run's / B18b proportions) --------------
N = 1 << 15
A0, A1 = 2.0, 3.6
GM = 4 * np.pi ** 2
AJ, ECCJ, MU = 5.2, 0.05, 1e-3
GMJ = GM * MU
NJ = np.sqrt(GM / AJ ** 3)

a = A0 + (A1 - A0) * rng.random(N)
e0 = 0.1 * np.sqrt(-2 * np.log(1 - rng.random(N)))
w0 = C2PI * rng.random(N)
M0 = C2PI * rng.random(N)
lam0 = (M0 + w0) % C2PI            # initial mean longitude
n = np.sqrt(GM / a ** 3)
P_orb = C2PI / n
T_win = 10 * P_orb                 # one epoch of the original's ledger
STEPS = 7000                       # 700 steps per orbit, 10 orbits
hstep = T_win / STEPS

Q24, Q16 = 0.6 * 2.0 ** -24, 0.6 * 2.0 ** -16


def dh(r, q):
    s = float(np.std(r))
    return 0.0 if s <= 0 else max(0.0, float(np.log2(s * np.sqrt(2 * np.pi * np.e) / q)))


def kepler_E(M, e, iters):
    E = M + e * np.sin(M)
    for _ in range(iters):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E


def state(a_, e_, w_, M_):
    """Heliocentric (x, y, vx, vy) from elements (2D)."""
    E = kepler_E(M_, e_, 8)
    c, s = np.cos(w_), np.sin(w_)
    xo = a_ * (np.cos(E) - e_)
    yo = a_ * np.sqrt(1 - e_ ** 2) * np.sin(E)
    nn = np.sqrt(GM / a_ ** 3)
    denom = 1 - e_ * np.cos(E)
    vxo = -nn * a_ * np.sin(E) / denom
    vyo = nn * a_ * np.sqrt(1 - e_ ** 2) * np.cos(E) / denom
    return (c * xo - s * yo, s * xo + c * yo,
            c * vxo - s * vyo, s * vxo + c * vyo)


def jupiter_warm(t, Ew):
    """Jupiter's position at per-body time t; Newton warm-started from Ew."""
    M = NJ * t
    E = Ew
    for _ in range(3):
        E = E - (E - ECCJ * np.sin(E) - M) / (1 - ECCJ * np.cos(E))
    return AJ * (np.cos(E) - ECCJ), AJ * np.sqrt(1 - ECCJ ** 2) * np.sin(E), E


def ecc_vec(x, y, vx, vy):
    r = np.hypot(x, y)
    v2 = vx * vx + vy * vy
    rv = x * vx + y * vy
    c = (v2 - GM / r) / GM
    d = rv / GM
    return c * x - d * vx, c * y - d * vy


def integrate(mu_j):
    """Velocity-Verlet under Sun + (optionally) Jupiter, per-body step hstep."""
    x, y, vx, vy = state(a, e0, w0, M0)
    t = np.zeros(N)
    Ew = np.zeros(N)               # Jupiter starts at its perihelion (M_J0 = 0)

    def accel(x, y, xJ, yJ):
        r = np.hypot(x, y)
        r3 = r * r * r
        ax = -GM * x / r3
        ay = -GM * y / r3
        if mu_j:
            dx, dy = xJ - x, yJ - y
            d = np.hypot(dx, dy)
            d3 = d * d * d
            rJ = np.hypot(xJ, yJ)
            rJ3 = rJ * rJ * rJ
            ax = ax + mu_j * dx / d3 - mu_j * xJ / rJ3   # pull + origin fall
            ay = ay + mu_j * dy / d3 - mu_j * yJ / rJ3
        return ax, ay

    xJ = yJ = np.zeros(N)
    if mu_j:
        xJ, yJ, Ew = jupiter_warm(t, Ew)
    ax, ay = accel(x, y, xJ, yJ)
    for _ in range(STEPS):
        vx = vx + 0.5 * hstep * ax
        vy = vy + 0.5 * hstep * ay
        x = x + hstep * vx
        y = y + hstep * vy
        t = t + hstep
        if mu_j:
            xJ, yJ, Ew = jupiter_warm(t, Ew)
        ax, ay = accel(x, y, xJ, yJ)
        vx = vx + 0.5 * hstep * ax
        vy = vy + 0.5 * hstep * ay
    return x, y, vx, vy


def fit(X, rh, rk):
    coef, *_ = np.linalg.lstsq(X, np.column_stack([rh, rk]), rcond=None)
    res = np.column_stack([rh, rk]) - X @ coef
    return res[:, 0], res[:, 1]


h0, k0 = e0 * np.cos(w0), e0 * np.sin(w0)

if MODE == "control":
    xc, yc, vxc, vyc = integrate(0.0)
    hc, kc = ecc_vec(xc, yc, vxc, vyc)
    ctrl = float(np.max(np.hypot(hc - h0, kc - k0)))
    np.savez("ctrl.npz", ctrl=ctrl)
    print(json.dumps({"control_jupiter_off_maxdz": ctrl}, indent=1))
    sys.exit(0)

# ---------------- the real run -----------------------------------------------
if MODE == "integrate":
    x, y, vx, vy = integrate(GMJ)
    hT, kT = ecc_vec(x, y, vx, vy)
    np.savez("int.npz", hT=hT, kT=kT)
    print(json.dumps({"integrated": True, "max_absdz": float(np.max(np.hypot(hT - h0, kT - k0)))}))
    sys.exit(0)

saved = np.load("int.npz")
hT, kT = saved["hT"], saved["kT"]
dz_tot = (hT - h0) + 1j * (kT - k0)

R["control_jupiter_off_maxdz"] = float(np.load("ctrl.npz")["ctrl"])
sig = dict(total_h=float(np.std(dz_tot.real)), total_k=float(np.std(dz_tot.imag)))
for i, idx in enumerate(np.array_split(np.argsort(a), 3)):
    sig[f"a_third_{i}_h"] = float(np.std(dz_tot.real[idx]))
    sig[f"a_third_{i}_a_mid"] = float(np.mean(a[idx]))
R["sigma"] = sig
R["dz_total_bits_q24"] = round(dh(dz_tot.real, Q24) + dh(dz_tot.imag, Q24), 2)

# crossers: aphelion beyond Jupiter's perihelion (real deep-encounter tail)
cross = a * (1 + e0) > AJ * (1 - ECCJ)
R["crossers"] = int(cross.sum())
if cross.sum() > 10:
    R["crosser_median_absdz"] = float(np.median(np.abs(dz_tot[cross])))
R["absdz_percentiles"] = {p: float(np.percentile(np.abs(dz_tot), p))
                          for p in (50, 99, 99.9)}
zsc = (dz_tot.real - dz_tot.real.mean()) / dz_tot.real.std()
R["gaussianity_h"] = dict(skew=float(np.mean(zsc ** 3)), exkurt=float(np.mean(zsc ** 4) - 3))

# ---------------- program 1: the true Laplace–Lagrange form ------------------
def b31(al_arr):
    """Laplace coefficient b_{3/2}^{(1)}(alpha): grid + interpolation."""
    ag = np.linspace(al_arr.min() * 0.98, al_arr.max() * 1.02, 513)
    psi = (np.arange(1024) + 0.5) / 1024 * C2PI
    vals = np.array([np.trapz(np.cos(psi) / (1 - 2 * c * np.cos(psi) + c ** 2) ** 1.5,
                              psi) / np.pi for c in ag])
    return np.interp(al_arr, ag, vals)


al = a / AJ
g_th = n * MU * b31(al) / 4.0
best = None
for scale in (0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3):
    ph = np.exp(1j * g_th * T_win * scale)
    z0 = h0 + 1j * k0
    X = np.column_stack([(ph * z0).real, (ph * z0).imag,
                         ph.real, ph.imag, np.ones(N)])
    rh, rk = fit(X, dz_tot.real, dz_tot.imag)
    rss = float(np.mean(rh ** 2 + rk ** 2))
    if best is None or rss < best[0]:
        best = (rss, scale, rh, rk)
_, g_scale, rh, rk = best
dz_kick = rh + 1j * rk
H_kick = dh(rh, Q24) + dh(rk, Q24)
R["ll_program"] = dict(g_scale_chosen=g_scale, bits_q24=round(H_kick, 2),
                       sigma_h=float(np.std(rh)), sigma_k=float(np.std(rk)))

# ---------------- program 2: the original's low-order basis (A1) -------------
aprime = (a - A0) / (A1 - A0)
B_low = np.column_stack([
    np.ones(N), aprime, aprime ** 2, e0, np.cos(w0), np.sin(w0),
    np.cos(M0), np.sin(M0),
    aprime * np.cos(M0), aprime * np.sin(M0),
    aprime ** 2 * np.cos(M0), aprime ** 2 * np.sin(M0)])
rl, kl = fit(B_low, rh, rk)
H_low = dh(rl, Q24) + dh(kl, Q24)
R["b_low"] = dict(n_features=12, bits_q24=round(H_low, 2),
                  recaptured_frac=round(1 - H_low / H_kick, 3))

# ---------------- diagnostic: generic harmonics in the birth longitude -------
cols = [B_low]
for j in range(1, 17):
    cols.append(np.column_stack([np.cos(j * lam0), np.sin(j * lam0),
                                 a * np.cos(j * lam0), a * np.sin(j * lam0)]))
B_harm = np.column_stack(cols)
rhm, khm = fit(B_harm, rh, rk)
H_harm = dh(rhm, Q24) + dh(khm, Q24)
R["b_harm16"] = dict(n_features=B_harm.shape[1], bits_q24=round(H_harm, 2),
                     recaptured_frac=round(1 - H_harm / H_kick, 3))

# ---------------- program 3: the synodic (event) basis -----------------------
cols = []
for m in range(10):
    tm = (0.0 - lam0 + C2PI * m) / (n - NJ)          # m-th conjunction time
    mask = ((tm > 0) & (tm < T_win)).astype(float)
    base = np.exp(1j * (lam0 + n * tm)) * mask       # conjunction longitude
    for wgt in (1.0 + 0j, np.exp(1j * w0), np.exp(-1j * w0), e0 + 0j):
        cols.append(np.column_stack([(base * wgt).real, (base * wgt).imag]))
B_syn = np.column_stack(cols)
rs, ks = fit(B_syn, rh, rk)
H_syn24, H_syn16 = dh(rs, Q24) + dh(ks, Q24), dh(rs, Q16) + dh(ks, Q16)
R["b_synodic"] = dict(n_features=B_syn.shape[1], bits_q24=round(H_syn24, 2),
                      bits_q16=round(H_syn16, 2),
                      recaptured_frac=round(1 - H_syn24 / H_kick, 3))
sig["synodic_residual_h"] = float(np.std(rs))

# ---------------- ledger consequences ----------------------------------------
R["belt_stock_1e9"] = dict(
    every_body_scarred_from_epoch1=True,
    synodic_q24=dict(bits_per_body=round(H_syn24, 2), gb_per_1e9=round(H_syn24 / 8, 2)),
    synodic_q16=dict(bits_per_body=round(H_syn16, 2), gb_per_1e9=round(H_syn16 / 8, 2)),
    no_program_q24=dict(bits_per_body=R["dz_total_bits_q24"],
                        gb_per_1e9=round(R["dz_total_bits_q24"] / 8, 2)),
    low_order_q24=dict(bits_per_body=R["b_low"]["bits_q24"],
                       gb_per_1e9=round(R["b_low"]["bits_q24"] / 8, 2)))

# ------------- post-hoc (NOT pre-registered): richer program ladder ----------
ladder = {}
for Jmax, Lmax in ((1, 2), (2, 2), (3, 3)):
    cols = []
    for m in range(10):
        tm = (0.0 - lam0 + C2PI * m) / (n - NJ)
        mask = ((tm > 0) & (tm < T_win)).astype(float)
        for j in range(1, Jmax + 1):
            for l in range(-Lmax, Lmax + 1):
                f = np.exp(1j * (j * (lam0 + n * tm) + l * w0)) * mask
                cols.append(np.column_stack([f.real, f.imag, (f * a).real, (f * a).imag]))
    X = np.column_stack(cols)
    rj, kj = fit(X, dz_kick.real, dz_kick.imag)
    Hj = dh(rj, Q24) + dh(kj, Q24)
    ladder[f"fourier_j{Jmax}_l{Lmax}"] = dict(n_features=X.shape[1], bits_q24=round(Hj, 2),
                                              recaptured_frac=round(1 - Hj / H_kick, 3))
R["posthoc_richer_ladder"] = ladder

print(json.dumps(R, indent=1))
with open("real_kick_ledger.json", "w") as f:
    json.dump(R, f, indent=1)
