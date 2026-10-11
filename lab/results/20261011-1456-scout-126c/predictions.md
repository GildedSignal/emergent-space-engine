# Predictions (written before the decisive run)

Candidate under test: **extended Darwin variables** (Blanco 2026, arXiv:2604.28140):
r̃ = 1/(f + A·φ(η)), φ = cosh(η−η₀) for plunge sectors, f/A from the real parts of
the roots of R(r̃) = Ẽ² − (1−2/r̃)(1+L̃²/r̃²); phase flow dτ/dη = |dr̃/dη|/√R;
Gauss–Legendre 4-point panels in η, exact terminal by root-finding r̃(η) = r_surface.

Cases below were NOT tuned on: they are the sectors and boundaries the parameterization
must survive for the b-plunge-tubes build.

## P1 — classification (root structure vs brute-force integration)
Sector from root structure (outer / direct / inner / bound-branch) agrees with a
DOP853 brute-force trajectory classification on ≥ 2000 seeds stratified near every
boundary (separatrix V_max, E²=1, V_min), with **0 mismatches** after excluding ties
(|Ẽ²−V_crit|/Ẽ² < 1e-9). Rationale: the classification is exact algebra; the oracle
is numerically decidable away from ties.

## P2 — terminal-event accuracy
For terminals r_s ∈ {2.001, 3, 6} (and mid-branch starts), with a FIXED uniform
panel layout of ≤ 48 GL4 panels:
- median relative error on (Δφ, Δτ, Δt) ≤ 1e-10 (oracle DOP853 rtol 1e-12),
- p99 ≤ 1e-8,
- near-separatrix seeds (|Ẽ²−V_max| down to 1e-8) degrade: I predict cost grows
  ~log(1/δ) but accuracy still ≤ 1e-6 at ≤ 96 panels.

## P3 — cost vs the bound control
Panels needed for 1e-9 relative on the plunge branch within 2× the same machinery
on a bound half-cycle (apo→peri) of comparable radial span. Bound control expected
~16–32 panels (the compiler's proven ground).

## P4 — negative control (the phase variable is load-bearing)
GL panels in r directly (no turning-point absorption) across the apoapsis of an
outer plunge: error stays > 1e-2 or non-convergent at any practical panel count
(the 1/√R singularity at the turning point).

## P5 — near-radial and L = 0
- L̃ ≥ 1e-6·L_scale: cost flat, accuracy holds (R barely feels L̃²; dφ/dη ~ L̃ is
  small and smooth).
- L̃ = 0 exactly: the (f, A) form breaks (double root at r̃ = 0) → confirms the
  lens's separate radial path (cycloid/τ-panels) is required; I predict the
  cosh-form errors or construction fail here, and that this is the ONLY sector
  needing it.

## P6 — horizon terminal (hole)
At r_end = 2+2e-9: Δτ, Δφ finite and accurate vs oracle; Δt log-divergent with
local slope dt/d ln(1/(r−2)) → 2/E·(1/√(R(2)/E²))... i.e. t ≈ −(2/Ẽ)·ln(r−2)·(Ẽ/√R(2))·...
predict the measured slope matches −2·Ẽ/(√R(2)·1) = −2 (since R(2) = Ẽ²) within 1%:
t ~ −2 ln(r−2). This is the ledger rule (τ-terminal), not a coordinate clock.

## P7 — kick across the separatrix (the plane's actual refusal)
A bound orbit kicked at periapsis phase into the plunge sector, continued by the
paper's C² rule (cos to last apoapsis, then cosh−2), matches an oracle that
integrates through the kick (state-continuous, (E,L) jumped): terminal (φ, t, τ)
within the same 1e-8 envelope. If this fails, the continuation is only kinematic,
not usable mid-orbit.

## Kill criteria
- p99 terminal error > 1e-6 at ≤ 96 panels in any decidable class → KILL (not panel-grade).
- Any classification mismatch > 0.5% → KILL of the root test.
- Panels-to-1e-9 > 10× bound control → downgrade (real but expensive).
