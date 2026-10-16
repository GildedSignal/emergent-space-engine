# Predictions (written before the decisive sweep + chain)

Target: representation.md §3 — "Perturbations … are kicks on E and L. A cycle's
derivatives are stored with it, so a kick updates the cycle by a multiply-add."
Instrument floor: quadrature ~1e-11 (strong field), multiply-add floor
~1.5e-6·eps at weak field (derivative roundoff). Calibration already confirmed
kappa_E -> 15/8 (Kepler) on the t/tau channels and the 1PN kappa_L on the
advance channel at p=1000, so those are NOT predictions anymore.

Kick parameterization: eps_E = fraction of the binding energy (1-E), eps_L =
fraction of L. Channels: dphi (advance), dt (radial period), dtau (proper).
delta = p - (6 + 2e) is the distance to the Schwarzschild separatrix.

## P1 — bulk domain (held-out: the tau channel and the e-dependence)

For p >= 20, e <= 0.9, every channel: error <= 5·eps². So an encounter-class
kick (eps = 1e-2) errs <= 5e-4, a tide-class kick (2^-23 ~ 1.2e-7) errs below
1e-13 (instrument floor). The premise SURVIVES the bulk belt.

## P2 — separatrix family (the attack)

The dt channel's kappa grows as delta shrinks, err_t ≈ A·eps_E²·delta^(-alpha)
with alpha in [1, 3]. The r1 period bar (0.1%) breaks at eps_E = 1e-2 for
delta <= 0.5, and at eps_E = 1e-3 for delta <= 0.05-ish. Held-out sub-case: the
dphi channel stays BELOW the dt channel everywhere near the separatrix (the
advance diverges more slowly than the period; the 1PN calibration already shows
kappa_L_phi < kappa_L_t at p=20).

## P3 — the chain (Peters inspiral, stale vs refreshed derivatives)

From p0=20, e0=0.3, nu=0.25, kicks sized by Peters' secular rates per cycle:
- The multiply-add with derivatives NEVER refreshed (stale) mispredicts the
  merger time or cycle count by > 1% (the first-order term itself is evaluated
  with stale slopes as (E,L) walks a large fraction of the domain).
- Refresh-every-64 holds the merger time to < 0.1%.
- The final cycles near the separatrix dominate the error either way: the
  last ~10 cycles contribute more error than all earlier cycles combined.

## P4 — tau vs t (held out: instrument-understanding check)

kappa_tau <= kappa_t for every (p, e): proper time has no (1-2M/r)^-1
amplification, so the clock channel is never the worst one.

## P5 — monotonicity in e (held out)

At fixed p (>= 10), every channel's kappa is monotone increasing in e on
e in [0, 0.99] — no interior bump, i.e. no surprise benign middle that would
suggest a different law than "curvature grows toward the boundary orbits".

## Kill criteria (pre-registered)

- If P1 holds and P2 shows the 0.1% bar crossed at eps_E >= 1e-3 within
  delta <= 0.5: the premise is domain-limited, not wrong — "multiply-add
  certified on the bulk, breaks on the separatrix family; a recompile trigger
  is required and is derivable from the measured kappa map".
- If P1 FAILS (some bulk cell errs > 5·eps²·10 = 5e-3 at eps = 1e-2): the
  premise is wrong beyond the separatrix — stronger claim, dossier headline.
- If P2's kappa is flat in delta (alpha ~ 0): the attack dies on the
  separatrix too; the premise survives outright and the kappa map is the
  certificate (a negative result worth as much).
- Chain: if stale-derivatives holds merger time to < 0.1% everywhere, the
  design's "derivatives stored with the cycle" needs no refresh rule at all —
  premise survives fully.
