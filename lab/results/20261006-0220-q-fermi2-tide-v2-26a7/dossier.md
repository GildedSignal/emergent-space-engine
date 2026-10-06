# dossier.md — run 20261006-0220-q-fermi2-tide-v2-26a7

**Claim:** the Fermi phase-2 tide reference now regenerates end to end from
shipped code — `verify.py` (v2) re-runs in 16 min and writes its own
`vectors.json` (18 families, near-ISCO re-admitted and passing every gate), the
omega derivation (`work/derive5.py`) regenerates `work/omega_expr2.txt` byte
for byte (2 s; the shipped derive5 was still missing Gamma^r_rr), `derive6.py`
is deleted, and the closed kernel agrees with the red-team's corrected kernel
−w(3γ²−1), +w to 1e-15 at the formula level and as the h→0 limit of their
geodesic-pair measurement at r = 6 and 3.1.

**Bottleneck:** the phase-2 Fermi frame (board item: "the Schwarzschild tide in
the Fermi frame, after gate E9"). The gain is not new physics but a
*trustworthy* freeze input: 0dee was silver solely because its record did not
regenerate; this run removes that defect, so E9's owner can adopt the kernel
without re-deriving it (PRINCIPLES: "Certificates need independent,
adversarial checks").

## Evidence (all commands ≤ 60 s unless noted, from this run folder)

- `python3 verify.py` — **the decisive run** (15m55s, 1 core, exit 0; log in
  `run.log` excerpt below, full numbers in `vectors.json`, 44 KB):
  18 families = the shipped 16 **plus circ-6.01 (re-admitted by the relative
  rdot² guard) and circ-6.02**, both with full 1/8-dynamical-time windows.
  Worst errors, gated value → tolerance:
  | check | worst | where | tol | status |
  |---|---|---|---|---|
  | A C^P (mpmath transport) | 4.00e-9 | parabolic/far | 1e-8 | pass (the shipped instrument floor, unchanged) |
  | A omega (Richardson h) | 1.20e-9 | ecc-e0.1/peri | 1e-9 | **2 entries 1.2× over** (see below) |
  | B.coord (shipped check) | 8.66e-3 | parabolic/far | 2e-2 | pass; refinement probe ratio 0.500 |
  | B.frame (new) | 8.54e-8 | circ-1000, parabolic/far | 1e-9 | **2 entries over** (see below) |
  | C finite-diff | 7.9e4 | diagnostic, not gated (known-broken launch bookkeeping, disclosed since 0dee) |
  | D structural | 3.6e-14 | all | 1e-12 | pass |
  | X.redteam kernel | 1.2e-12 | 4 radii | 1e-12 | pass |
- The four recorded failures are tolerance placement, not physics, and each is
  closed by a measurement in this run:
  - omega: 1.163e-9 / 1.195e-9, **flat under window-transport refinement**
    (nsteps 150/600/2400 identical to 4 digits — probe in `work/omega-floor`),
    h⁴-structured Richardson residue; the raw (pre-Richardson) errors were up
    to 2.13e-7, so the fix bought 178×; gate belongs at 2e-9 (measured floor).
  - B.frame: 8.0e-8 at n=1200 substeps on the τ=277 window, **4th-order in n**
    (8.04e-8 → 5.45e-9 → 3.53e-10 at n = 1200/2400/4800, ratios 14.7/15.5);
    n=4800 (41 s) passes 1e-9. Machine precision (2e-16…8e-15) on every window
    ≤ 60 of proper time.
- `python3 base/verify.py`-equivalent (`base/` holds the shipped code; its
  `vectors.json` regenerated, 11m08s): reproduces 0dee's checker exactly — A
  4.00e-9 / omega 4.56e-7 / B 8.66e-3, circ-6.01 dropped by the `< 0` rdot²
  guard (its exact-circular rdot² is −1.1e-16 in float64; at 40 digits mpmath
  it is −1e-40 → mpc crash in `msqrt`, found and clamped in v2).
- `python3 crosscheck_redteam.py` (10 s) — the red-team kernel cross-check:
  - formula level: `tide_boosted` C22 = −w(3γ²−1), C33 = +w, γ² = f/(1−3M/r),
    at r ∈ {3.1…1000}: worst rel diff 1.3e-13 (r=1000 round-off), typical
    1e-15; radial factor (3γ²−1)/2 = 1.5000 at r=6 and 16.0000 at r=3.1 —
    exactly the red-team checker's h→0 numbers;
  - static orthonormal Riemann from `riemann_down`: R_r̂φ̂r̂φ̂ = −M/r³ (their
    root-cause sign fix), R_θ̂φ̂θ̂φ̂ = +2M/r³ (their 3D note), R_t̂r̂t̂r̂ = −2M/r³,
    all ≤ 7e-18;
  - measurement level: their `eeff.py` geodesic-pair machinery (no Riemann
    code, no closed form), hspan and eps halved together to h₀/64:
    r=6: radfac 1.5579 → 1.4984 (closed 1.5000); r=3.1: 18.517 → 16.0077
    (closed 16.0000); eigenvalue diff ≤ 1.6e-2 at h₀/4 → 1.4e-3 at h₀/64,
    monotone, matching their checker's 16.12 at their smallest window.
- `python3 work/derive5.py` (2.3 s) — prints omega = E·L·M/(r²(rE²+2M−r)),
  dΦ/dφ = −EM/(rE²+2M−r), E=1 → −1/2, L=0 → 0, and writes
  `work/omega_expr2.txt` **identical to the shipped one** (diff clean). The
  shipped derive5 could not do this: its substitution loop left un-cancelled
  sqrt(r³rdot²) terms (a monster), because (a) it too omitted Γ^r_rr and
  (b) its reduction was pattern-substitution, not algebraic. v2 uses the
  correct chain rule d/dτ = ṙ·∂_r + (d(rdot²)/dr/2)·∂_ṙ + (d(G²)/dr·ṙ/2G)·∂_G
  and exact mod-square polynomial reduction. `work/derive6.py` is not shipped
  (deleted; it differentiated without any chain rule).

## Predictions (predictions.md, written before the decisive run)

Held: 1 (all families pass A C^P, B.coord, D, X; near-ISO full windows), 3
(circ-6.01/6.02 windows 11.57/11.60, errors at circular floor), 4 (radial,
parabolic −1/2, E-independence anchors), 5 (cross-check, run before and
untouched by v2). Missed, disclosed: 2 — Richardson omega reached 1.2e-9 not
≤1e-10, and 1's sub-claim "B.frame ≤ 1e-9" fails on the two longest windows at
n=1200 (truncation, 4th order in n, measured to 3.5e-10 at n=4800). The B.coord
refinement ratio came out 0.5004, at my pre-registered 0.5 boundary: the probe
reads as truncation-like, not round-off — the 2e-2 gate holds either way but
the checker's "coordinate round-off floor" wording is not what the probe shows.

## What would make it wrong

The B.frame truth side shares the coordinate Riemann with check A (independently
asserted against sympy in `work/derive.py`, and now against the red-team's
static components); a sign error there would move A, B and X together — the
geodesic-pair measurement (crosscheck level 3) is the one path that uses no
Riemann at all, and it lands on the same kernel. The near-ISCO admission
rests on the round-off tolerance being the right reading of rdot² = −1e-16 on
an exact zero; if 6.01/6.02 ever drift below −1e-12·scale the guards drop them
again (visible as invalid-sample failures, not silent). The Phi jump at radial
turning points remains asserted, not tested (0dee's open caveat; unchanged
here — windows are clamped away from turning).

## Cost of adoption

None new: same `schwarztide.py` (byte-identical to 0dee), verify.py v2 replaces
the record-generating path (16 min, 1 core), B.frame at n=4800 on long windows
adds ~1 min if 1e-9 is wanted there. Fits PRINCIPLES 2 ("'Exact' means
deterministic and reproducible") and the lab rule "numbers the shipped code
cannot regenerate" — now it can.

## The lens (second-author) may have missed

I did not fix check C (left diagnostic, as the directed question scoped); the
omega residual's h-scaling below h=5e-4 was inferred (ns-flat measured, h⁴ not
re-measured at h/2); the long-arc whirl and the turning-point Phi unwrap (0dee
checker's "free" extra tests) were again left on the table — time went to the
named experiment; and B.coord's floor story is now *truncation-like*, which the
next run should settle with an h-refinement of the coordinate integrator.
