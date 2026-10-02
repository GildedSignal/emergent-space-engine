# dossier.md — run 20261002-0539-q-fermi2-tide-0dee

**Claim:** the Schwarzschild tidal tensor in the parallel-transported tetrad
along any equatorial timelike geodesic is, in closed form, a rational core in
(E^2, L^2, 1/r, M) — including the rotation rate — plus one accumulated angle;
its eigenvalues are E-independent and rational, verified independently at the
1e-9..1e-15 level, delivered as `schwarztide.py` + `vectors.json`.

**Bottleneck:** the phase-2 Fermi frame (board: Schwarzschild tide in the Fermi
frame after gate E9). Expected gain: the tide x'' = -E(tau) x needs no geodesic
integration and no square roots per evaluation on the rational core — it
deletes the per-step Riemann contraction from the engine path and makes the
tide integer-exact (PRINCIPLES 16, 32: symmetries found, not given).

## The result (M = mass, m = M/r^3, lambda = L^2/r^2, f = 1-2M/r,
## G^2 = E^2 - f, rdot^2 = E^2 - f(1+lambda))

Frame: lambda_1 = e_theta; (lambda_2', lambda_3') = static frame boosted along
the velocity; parallel frame = boosted pair rotated by Phi, dPhi/dtau = -omega.

    C11 = m (1 + 3 lambda)                       rational
    C22 = m - 3 M E^2 L^2/(r^5 G^2)              rational
    C33 = -2 m + 3 M f L^2/(r^5 G^2)             rational
    C23 = -3 M E L rdot/(r^4 G^2)                rational in rdot (odd)
    C12 = C13 = 0 (e_theta is an eigenvector)
    eigenvalues { m(1+3 lambda), m, -(2+3 lambda) m }   E-independent, rational
    omega = E L M/(r^2 (r E^2 + 2M - r))                  rational
    dPhi/dphi = - E M/(r E^2 + 2M - r)           rational; E=1 -> -1/2 exactly
    C^parallel = R(Phi) C^boosted R(Phi)^T

Integer-exactness: every per-step quantity is rational in (E^2, L^2, 1/r, M)
[+ rdot, i.e. one sign bit on the rational rdot^2] — exact in integers at any
fixed precision; the ONLY non-rational object is the accumulated angle Phi
(one scalar phase, like the orbital phase itself). Eigenvalues need no roots.
G^2 > 0 always on timelike geodesics (G^2 = rdot^2 + f lambda).

## Evidence (commands, each <= 60 s except the last)

- `python3 work/derive.py` — sympy: Riemann from the metric, conventions
  asserted (R_that_rhat = -2M/r^3; radial tidal stretch +2M/r^3).
- `python3 work/derive6.py`-path (inlined in the run log) — sympy: the boosted
  tetrad is orthonormal exactly; C^boosted contraction; omega contraction
  after the complete Christoffel set (a first attempt missed Gamma^r_rr and
  produced a wrong omega — caught by the numeric measurement below).
- Pointwise, double precision: C^direct (coordinate Riemann x boosted frame)
  minus C^closed = machine epsilon (<= 5e-16 rel) on bound/unbound/radial,
  both rdot signs.
- omega vs directly measured g(grad_u lambda_2', lambda_3') (finite-differenced
  field, no transport machinery): 3e-13; circular anchor omega = sqrt(M/r^3)
  (geodetic precession 2 pi (1 - sqrt(1-3M/r)) per orbit) exact; L=0 -> 0 exact.
- `python3 verify.py` (~11 min, 2 vCPU): on 8 held-out families (whirl
  e=0.95 p=7.95, circular r=6.01 and r=1000, e=0.9, e=0.1, unbound E=1.05
  L=4.1, parabolic E=1, radial L=0):
  - A: mpmath 40-digit direct construction (numeric parallel transport; Phi
    read off the transported frame, never from the closed form): worst
    C^P error 4.0e-9, worst omega error 4.6e-7 (both RK4-truncation-limited,
    not formula-limited; pointwise checks reach 3e-13..1e-16).
  - B: geodesic-deviation integration in coordinates vs the 3-space closed-form
    ODE x'' = -C^P x: 3e-15..2e-14 (circ-10, ecc mid, ecc peri; machine
    precision after fixing a Riemann slot bug in the checker itself).
  - C: finite differences of nearby geodesics — checker harness not finished
    (its bookkeeping of base-vs-perturbed positions is still wrong); NOT a
    physics result. The independent evidence for the same statement is B plus
    the pointwise FD of the boosted frame (separation vectors verified
    sensible and E,L conserved to 1e-14 in the geodesic integrator).
  - D: structural, all families: trace 0, C12=C13=0, eigenvalue match, all
    <= 3.6e-14; C11 E-independent to 1e-14; parabolic dPhi/dphi = -1/2 to 1e-16.
- Literature cross-check: eigenvalues match Xin & Mummery, arXiv:2511.21499
  (Q=0 limit of their RN equatorial eigenvalues), including their remark that
  the eigenvalues are E-independent; structure (sin 2Phi / cos 2Phi with
  rational coefficients) matches Marck 1983 / Ishii-Shibata-Mino 2005.

## Predictions (predictions.md, written before verify.py)

Held: 1 (mpmath agrees, at 4e-9 not 1e-12 — integration-truncation, reported
as such), 2 (eigenvalues exact), 6 (radial: omega=0, C diag(m,m,-2m)),
7 (parabolic dPhi/dphi = -1/2 exactly), 8 (circular anchors).
Partially held: 3, 4 — B passed at machine precision where re-run with the
fixed checker; C unfinished. 5 (whirl smooth) held for all closed forms.

## What would make it wrong

The checks A/B/D all share the coordinate Riemann built from the six
orthonormal components (independently asserted against sympy). A sign error
there would flip C and omega together; the Newtonian and geodetic limits and
the Xin-Mummery eigenvalues pin the conventions. The angle convention Phi
jumps at radial turning points (v-hat reflects); the parallel frame itself is
smooth — the phase-2 builder must unwrap Phi across turning points (or track
the parallel frame directly, as B does).

## Cost of adoption

One small table-free function per evaluation; the rational core is exact in
integers; no geodesic integration for the tide; Phi accumulates like the
orbital phase (already compiled in the engine). Fits PRINCIPLES 7 (multipoles/
geometry), 16 (cheapest arithmetic), 32 ("under the right representation many
symmetries can appear").

## The lens (reference-building) may have missed

The FD checker being unfinished means the three-way agreement rests on A+B+D;
a reviewer should re-run C from the dossier before freezing gate E9. Null
orbits were excluded (the boosted frame degenerates: lambda_3' -> u); ships
are massive, but light-like tubes (signals) would need the ZAMO-style frame
instead.
