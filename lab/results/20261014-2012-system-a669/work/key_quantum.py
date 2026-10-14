#!/usr/bin/env python3
"""The ladder belt's kick stream against the tube key's own quanta (SI replica).

Mirrors the shipped kick path (crates/universe/src/step.rs `kick`, level 0):
at each cadence tick, read the exact state, a = the secondaries' Newtonian pull
at that instant, dv = h * a, apply, re-fit. The question: how often does the
quantized key (E Q48 on scale 1, L Q32) actually flip, per kick and under
coarsening — i.e. is the per-kick `Orbit::compile` (binding.rs:422, called
unconditionally by `Rebinding::from_state`) forced by the key's own fineness?

All constants from shipped code: roster from crates/universe/src/scenario.rs
PLANETS (mass octaves of the star, periapsis in root units, e_q48), root unit
1.477 km, cadence from Config::step_log2 = 7 over the shortest secondary
(measured 2.814e4 s, cf45). Belt band from `ladder_ship`. E quantum
c^2 * 2^-48 (f0a2's SI anchor of `Key::new`'s Q48-on-scale-1).
"""
import numpy as np

AU = 1.495978707e11
ROOT = 1477.0            # m, one root length unit (scenario.rs)
C = 2.99792458e8
GM = ROOT * C * C        # the star's GM: M = 1.477 km geometric
YR = 3.15576e7

# scenario.rs PLANETS: (name, mass_log2, periapsis_root, e)
PLANETS = [
    ("Cinder", -21, 35_600_000, 0.1),
    ("Home",   -18, 99_300_000, 0.02),
    ("Giant",  -10, 500_000_000, 0.05),
]
SEC = [(n, 2.0 ** ml, p * ROOT / AU * AU, e) for (n, ml, p, e) in PLANETS]  # (name, mu, periapsis_m, e)

H = 2.814e4              # s, the root doll's step (cf45 p50 on shipped main)
NKICK = 120_000          # ~107 yr, ~21 Giant synods at 2.5 AU
Q_E = C * C * 2.0 ** -48 # 319.3 m^2/s^2, one Q48 of E on scale 1
Q_V = C * 2.0 ** -48     # the velocity-carry quantum (step.rs quantize)

rng = np.random.default_rng(20261014)
NB = 64
a = (2.0 + rng.random(NB)) * AU
e = rng.rayleigh(0.07, NB)
e = np.where(e > 0.4, rng.rayleigh(0.07, NB), e)          # re-drawn above 0.4
varpi = rng.random(NB) * 2 * np.pi
M0 = rng.random(NB) * 2 * np.pi

def kepler(M, e):
    E = M.copy()
    for _ in range(8):
        E = E - (E - e * np.sin(E) - M) / (1 - e * np.cos(E))
    return E

def state(a, e, varpi, M):
    E = kepler(M, e)
    c, s = np.cos(E), np.sin(E)
    r = a * (1 - e * c)
    x = a * (c - e); y = a * np.sqrt(1 - e * e) * s
    n = np.sqrt(GM / a ** 3)
    vx = -a * n * s / (1 - e * c); vy = a * n * np.sqrt(1 - e * e) * c / (1 - e * c)
    ca, sa = np.cos(varpi), np.sin(varpi)
    return ca * x - sa * y, sa * x + ca * y, ca * vx - sa * vy, sa * vx + ca * vy, r

def sec_state(t):
    out = []
    for (name, mu, peri, ep) in SEC:
        aa = peri / (1 - ep)
        n = np.sqrt(GM * (1 + mu) / aa ** 3)
        # periapsis angle/phase from PLANETS are fixed; randomising the belt phase
        # samples the geometry anyway. Keep the shipped ordering, angle 0.
        x, y, vx, vy, r = state(np.array([aa]), np.array([ep]), np.array([0.0]),
                                np.array([n * t]))
        out.append((name, mu, x[0], y[0]))
    return out

t = 0.0
E_word = np.zeros(NB, dtype=np.int64)
L_rel = np.zeros(NB)                    # L/L_doll, doll = naive root reading
flips = np.zeros(NB, dtype=np.int64)
dE_all, dL_all, dv_all = [], [], []
E0_word = None
syn_net, syn_abs = [], []
syn_per_syn = ((1/ ( (2.5) ** 1.5 ) - 1 / (5.196) ** 1.5)) ** -1 * YR  # Giant synod at 2.5 AU
K_PER_SYN = int(syn_per_syn / H)

for k in range(NKICK):
    x, y, vx, vy, r = state(a, e, varpi, M0)
    En_birth = En_birth if k else (0.5 * (vx*vx + vy*vy) - GM / r)
    ax = ay = 0.0
    for (name, mu, sx, sy) in sec_state(t):
        dx, dy = sx - x, sy - y
        d2 = dx * dx + dy * dy
        ax = ax + mu * GM * dx / (d2 * np.sqrt(d2))
        ay = ay + mu * GM * dy / (d2 * np.sqrt(d2))
    dvx, dvy = H * ax, H * ay
    vx, vy = vx + dvx, vy + dvy
    v2 = vx * vx + vy * vy
    En = 0.5 * v2 - GM / r                       # Newtonian specific energy (dominant mass only)
    Lz = x * vy - y * vx
    word = np.floor(En / Q_E).astype(np.int64)
    if E0_word is None:
        E0_word = word.copy()
    flips += (word != E_word)
    E_word = word
    L_rel = Lz / (GM / C)                        # L in units of GM_*/c (the naive doll reading)
    dE_all.append(vx * dvx + vy * dvy)           # dE = v.dv at the kick
    # re-fit the kicked state onto new Kepler elements (the rebind): the walk accumulates
    v2b = vx * vx + vy * vy
    Enb = 0.5 * v2b - GM / r
    a = -GM / (2 * Enb)
    hh = x * vy - y * vx
    evx = (vy * hh) / GM - x / r; evy = (-vx * hh) / GM - y / r
    ee = np.hypot(evx, evy)
    varpi = np.arctan2(evy, evx)
    cosn = (evx * x + evy * y) / np.maximum(ee * r, 1e-30)
    cosn = np.clip(cosn, -1, 1)
    sinn = (evx * y - evy * x) / np.maximum(ee * r, 1e-30)
    nu = np.arctan2(sinn, cosn)
    Ea = 2 * np.arctan2(np.sqrt(np.maximum(1 - ee, 0)) * np.sin(nu / 2),
                        np.sqrt(1 + ee) * np.cos(nu / 2))
    e = ee
    M0 = Ea - e * np.sin(Ea)
    dL_all.append((x * dvy - y * dvx) / np.maximum(Lz, 1.0))
    dv_all.append(np.hypot(dvx, dvy))
    if k and k % K_PER_SYN == 0:
        syn_net.append((En - En_birth).copy())
    # advance the body's own Kepler mean anomaly one step (the compiled drift)
    M0 = M0 + np.sqrt(GM / a ** 3) * H
    t += H

dE = np.array(dE_all); dL = np.array(dL_all); dv = np.array(dv_all)
E_final = np.array(syn_net)

print("== the belt's kick stream (shipped roster, h=2.814e4 s, %d kicks x %d bodies) ==" % (NKICK, NB))
print("per-kick |dv|  p01/p50/p99: %.2e / %.2e / %.2e  m/s" % tuple(np.percentile(dv, [1, 50, 99])))
print("per-kick |dE|  p01/p50/p99: %.2f / %.2f / %.2f  Q48 quanta" % tuple(np.percentile(np.abs(dE) / Q_E, [1, 50, 99])))
print("per-kick |dL|/L p01/p50/p99: %.2e / %.2e / %.2e  (relative)" % tuple(np.percentile(np.abs(dL), [1, 50, 99])))
print("velocity-carry gate (step.rs:424): |dv| in quanta of 2^-48 c, p01 = %.1f -> early-return fraction %.1e%%"
      % (np.percentile(dv, 1) / Q_V, 100 * np.mean(dv < Q_V)))
print()
print("== P1: L-axis flips ==")
qmax_rel = 2.0 ** -32 / 0.25     # the COARSEST quantum the shipped L range (L>=1/4) allows
qmin_rel = 2.0 ** -32 / 4096
print("dL/L per kick vs the shipped L range's own quantum extremes:")
print("  vs coarsest legal (2^-32/0.25 = %.2e): median multiplicity %.0f quanta/kick" % (qmax_rel, np.median(np.abs(dL)) / qmax_rel))
print("  vs finest   legal (2^-32/4096 = %.2e): median multiplicity %.1e quanta/kick" % (qmin_rel, np.median(np.abs(dL)) / qmin_rel))
print("  naive root-doll reading L/L_doll p50 = %.3e (out of the documented [0.25,4096]: the belt's tube"
      " cannot use it; every legal scaling is finer)" % np.median(L_rel))
print("P1 verdict: L flips on 100%% of kicks at every legal scaling" if np.percentile(np.abs(dL), 1) > qmax_rel
      else "P1 FAILS: some kicks are sub-quantum in L even at the coarsest legal scaling")
print()
print("== P2: E-axis flips (Q48, absolute) ==")
ff = flips.mean() / NKICK
print("E-word flip fraction: %.3f (P2 predicted 0.25-0.60)" % ff)
print()
print("== P3: synodic cancellation and the coarsening run length (E axis) ==")
if E_final.size:
    drift = (E_final[-1] - E_final[0]) / Q_E
    print("E-word drift birth->end (107 yr): p50 %.1f quanta, max |.| %.1f" % (np.median(drift), np.max(np.abs(drift))))
print("|sum dE| per synod / sum|dE| per synod (median over bodies):")
first_syn = np.array(syn_net[0]); last_syn = np.array(syn_net[-1])
per_syn_net = np.abs(last_syn - first_syn); per_syn_abs = np.abs(dE[:K_PER_SYN]).sum(axis=0)
print("  cancellation ratio p50 = %.4f (P3 predicts <= 0.05)" % np.median(per_syn_net / per_syn_abs))
print()
print("== the coarsening dial (what a per-population coarser key deletes) ==")
print("  k   q_E x 2^k    E-flip frac   mean run length (kicks)")
for kk in range(0, 13):
    w = np.floor(dE.cumsum(axis=0) / (Q_E * 2.0 ** kk)).astype(np.int64)
    f = (np.diff(w, axis=0) != 0).mean()
    # run length: kicks per flip
    print("  %2d   2^%-2d        %.4f        %.1f" % (kk, kk, f, (1.0 / max(f, 1e-12))))
print()
print("== P4: kick size vs belt radius ==")
inner = a < 2.4 * AU; outer = a > 2.6 * AU
print("  |dE| p50 inner (<2.4 AU) %.3f vs outer (>2.6 AU) %.3f quanta; ratio %.2f (Giant-dominated -> < 1)"
      % (np.median(np.abs(dE[:, inner])) / Q_E, np.median(np.abs(dE[:, outer])) / Q_E,
         np.median(np.abs(dE[:, inner])) / np.median(np.abs(dE[:, outer]))))
