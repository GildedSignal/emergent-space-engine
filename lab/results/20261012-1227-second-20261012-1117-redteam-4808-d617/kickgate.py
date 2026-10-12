"""E1: the frozen kick-train gate (B-sep) at p -> p_crit+.

For e in {0.5, 0.9, 0.99}, margin mu in {2, 1, 0.3, 0.1, 0.03}: a train of
10^3 kicks, dL/L = 1e-4, alternating signs (zero mean).  Multiply-add (the
design's law.md jet: exact offset plus stored derivatives at the compile
anchor) vs exact GR, against the frozen budgets:
  A (law floor, per kick): |residual| <= 1e-6 * dphi_cycle
  B (player-visible, per 10^3 kicks): |drift| <= 5e-3 rad
Also: random-sign trains, and the re-anchor control (trigger = 730 quanta).
"""
import numpy as np, sys
sys.path.insert(0, '.')
from cycle import *

rng = np.random.default_rng(4808)   # prior run's id, for continuity
S = 1e-4                             # dL/L per kick
NK = 1000
FLOOR_REL = 1e-6                     # darwin16 compile error scale (law.md:3)
TRIGGER_QUANTA = 730.0               # law.md "Not adopted" entry: sqrt(floor/C)

def jet_err(L, La, fam, dphi_s, dd_s):
    """dphi_jet(L; anchor La) - dphi_exact(L)."""
    dj = dphi_s(La) + dd_s(La) * (L - La)
    return dj - dphi_s(L)

print("e   mu     p      dphi     gain   resid/kick(+/-)      A:per-kick  B:drift/1e3  verdict")
for e in [0.5, 0.9, 0.99]:
    for mu in [2.0, 1.0, 0.3, 0.1, 0.03]:
        p = 6 + 2 * e + mu
        up, L0 = seed_from_pe(p, e)
        fam = build_family(up)
        from scipy.interpolate import CubicSpline
        dphi_s = CubicSpline(fam["L"], fam["dphi"])
        dd_s = CubicSpline(fam["L"], fam["ddphi"])
        # derivatives/gain/residual by central differences on the exact family
        Lp, Lm = L0 * (1 + S), L0 * (1 - S)
        d0, dp, dm = dphi_s(L0), dphi_s(Lp), dphi_s(Lm)
        d1 = (dp - dm) / (2 * (Lp - L0))
        resid_p = dp - (d0 + d1 * (Lp - L0))
        resid_m = dm - (d0 + d1 * (Lm - L0))
        gain = abs(d1) * L0 / d0
        # alternating train (jet anchored at compile point = L0)
        rk = np.where(np.arange(NK) % 2 == 0, resid_p, resid_m)
        drift_alt = np.abs(rk).sum()          # |sum| of one-signed residuals
        # random-sign train with re-anchoring (shipped rule)
        Ls = np.empty(NK); L = L0; La = L0; n_re = 0; drift = 0.0; maxoff = 0.0
        for k in range(NK):
            L = L * (1 + S * rng.choice([-1.0, 1.0]))
            if abs(L - La) / La > TRIGGER_QUANTA * S:
                La = L; n_re += 1
            drift += jet_err(L, La, fam, dphi_s, dd_s)
            maxoff = max(maxoff, abs(L - La) / La)
        okA = max(abs(resid_p), abs(resid_m)) <= FLOOR_REL * d0
        okB = drift_alt <= 5e-3
        print(f"{e:.2f} {mu:5.2f} {p:6.2f} {d0:8.4f} {gain:6.1f} "
              f"{resid_p:+.2e}/{resid_m:+.2e}  {'PASS' if okA else 'FAIL':>8}"
              f"  {drift_alt:9.2e} {'PASS' if okB else 'FAIL':>6}"
              f"  {'SAFE' if (okA and okB) else 'UNSAFE'}")
        if mu == 0.3:
            print(f"      random-sign: drift={drift:+.2e} rad  re-anchors={n_re}  "
                  f"max offset={maxoff:.2e} vs trigger {TRIGGER_QUANTA*S:.1e}")
