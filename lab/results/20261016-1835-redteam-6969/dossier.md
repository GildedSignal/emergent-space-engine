# Run 20261016-1835-redteam-6969 — premise red-team: "ν only in the energy map" measured at the flank

## Claim

The two-body doll's premise "ν enters only through the energy map" (representation.md
L37, law.md L39) is **measurably false already at 100M and unlicensable below ~30M**:
at fixed real invariants (E, j), the 2PN truth precesses less than the doll by
+1.2% at p = 30M (ν = 0.25), scaling ≈ 1.8·ν·(M/p) and exactly linear in ν — while
in the inspiral band p ≲ 20M **no oracle the repo has (1PN by construction, 2PN by
its own +11–370% truncation floor) can vouch for the doll at all**, and B11's
tolerance (1% + 16/p) is wider than the effect everywhere, so no existing gate or
rung can fail on it.

## Bottleneck

Premise 1 of the lens order (two-body doll), the only SURVIVES entry in the topic
census, and the wiki's open direction 3 ("the EOB strong-field flank... the missing
licence for the merger scene the game sells"). This run turns the unmeasured flank
into numbers and names the guard that is missing. Not a 10× compute lever; a
correctness hole on Julien's approved scene (rotating holes, inspiral: law.md L32;
"we need to build towards GR that's the goal", CL 09-26).

## Evidence (float, 33 s, one core, ~50 MB; `python3 eob_flank.py flank.json`)

Machinery: one invariant quadrature dφ/dr over the allowed annulus, three
Hamiltonians through it — exact Schwarzschild (the doll, r3 v3's `eob-doll` with the
2PN-accurate energy map E_real = √(1+2ν(E_eff−1)), j identical), ADM 2PN (Buonanno–
Damour 1999 eq 10a–c, fetched), and ADM 1PN. Comparison at fixed real invariants:
doll orbit (p, e) → (E_eff, L) via the shipped `bound_constants`; truth at
(E_real(ν), L). Sources fetched live: Iorio arXiv:2107.07126 (eqs 9, 18, 19:
2PN periastron advance, three parameterizations), BD99 gr-qc/9811091 (eq 10).

- **C0 (positive control, both sides):** r-space quadrature vs the independent
  Darwin χ-integral (law.md's own dφ/dχ = √(p/(p−6−2e cosχ))), 21 orbits
  p ∈ [8,100], e ∈ {0.3,0.6}: max relative disagreement **2.2×10⁻⁸**.
- **A lesson that bit twice:** the closed form 2π(1/√(1−6M/p)−1) is NOT exact for
  e > 0 (it is the e = 0 epicyclic value); two independent integrals agree with
  each other and deviate from it by ∝ e²/p (e.g. +2.5×10⁻⁴ in k at p = 100, e = 0.3).
  Any check that uses it as "exact" inherits that bias.
- **C1 (the 2PN oracle's own floor, ν = 0, e = 0.3):** ADM-2PN vs exact: −0.25% @
  p=100, −1.2% @ 50, −11.6% @ 20, −59% @ 10. Consistent with a ~22(M/p)²
  truncation. **Licence region for a 2PN oracle: p ≳ 30M.**
- **The ν-induced doll error** (k_doll/k_2PN − 1 at ν=0.25 minus the same at ν=0;
  truncation cancels to leading order), ν = 0.25: **+0.48% @ p=100, +0.68–0.90% @
  50, +1.2% @ 30** (e = 0/0.3/0.6). Exactly linear in ν at p = 50: +0.18%, +0.45%,
  +0.90% for ν = 0.05/0.125/0.25 (ratios 1 : 2.5 : 5). Sign: the doll
  over-precesses. Fit ≈ +1.8·ν·M/p in the licensed band.
- **Below the licence line (p ≤ 20M), the floor swamps the signal** (ν=0 floor:
  +11% @ 20, +133% @ 10, +372% @ 8) — I can bound nothing there with this oracle,
  and the repo's 1PN oracle (r3 v3, `damour_deruelle`) cannot see 2PN terms by
  construction. **The inspiral band is unjudged by every instrument that exists.**
- **Circular binaries at fixed L:** the 2PN orbital frequency exceeds the doll's
  Ω = (M/p³)^{1/2} by ν-induced +0.108% @ p=100 and +0.18% @ 50 — the same size as
  B11's 0.1% period gate, which judges periods only where the next-term estimate is
  ≤ 5×10⁻⁴ (a ≳ 100M): the gate sits exactly at its own contamination edge.
- **Gate arithmetic:** B11/r3-v3 precession tolerance (1% + 16/p) is 1.63% at p=30,
  81% at p=20 — my measured ν-term (+1.2% at p=30) passes under it everywhere.
  **No rung or gate in lab/rungs/ or law.md can fail on this effect.**

## Predictions (predictions.md, written before the run)

- P1 (controls): C0 passed at 2×10⁻⁸. C1's magnitude at p=20 measured −11.6% vs my
  predicted ≲1% with ~5.6% expected truncation — right sign and growth, size 2× my
  estimate; this moved my licence line from p ≈ 20M to p ≳ 30M. **Held, with the
  licence line worse than predicted.**
- P3 (decisive): sign held (doll over-precesses in the licensed band); the 1%
  crossing measured at p ≈ 30–35 vs predicted 25–60 ✓; p=50 magnitude +0.9% vs
  predicted 0.5–8% ✓ (low end); linear in ν exactly ✓. My p=10 band (1–15%) is
  **not measurable** — the oracle floor there is 133%; the prediction presumed a
  licence the oracle does not have. Reported as not held, honestly.
- P4 (ISCO shift): **not measured** — my κ² scan did not converge; no ISCO claim.
- P2 (1PN sanity): the planned adm1-difference decomposition was unsound at p ≤ 20
  (1PN truncation artifacts leak into the ν-difference); replaced by the ν=0-subtracted
  adm2 difference, which cancels the floor to leading order. Disclosed.

## What would make it wrong

My ADM H₄ ν-coefficients rest on one fetched source (BD99 eq 10) validated only
through C1's floor-consistency, not against a second independent 2PN derivation;
a transcription error in a ν-coefficient would rescale the 1.8 coefficient (not
the ν-linearity, which is structural). The χ-integral control validates the
machinery, not the Hamiltonian. A checker with 3PN coefficients (or an EOB 2PN
Hamiltonian) should reproduce the ν-column at p ∈ {50, 100} before adoption.

## Cost of adopting / fit with PRINCIPLES

Adoption is a gate, not code: an **r3 v4** rung with a 2PN oracle, cases p ∈
[25, 200], ν ≤ 0.25, tolerance tied to the measured floor (≈ 22(M/p)² + 1%), and
negative control `nu-in-geometry` (a planted A = 1−2u+2νu³ EOB law must be
distinguished from the doll at p ≤ 50). Cost: one rung file, one oracle port (the
quadrature here is 150 lines of float). Fit: principle 2 ("error type over error
size" — the doll's error type at p ≤ 30 is a wrong ν-law, not a rounding);
principle 30 ("navigation, knowledge and dynamics those need to be perfect");
principle 9 (a KILL of the doll below 30M would kill a configuration, not the
dolls idea). What survives: the doll above p ≈ 40M at ν ≤ 0.25 is fine to ~0.5% —
the premise is *bounded*, not destroyed; "dolls all the way down" needs a second
mechanism (EOB ν-terms or a dense-order handoff) below that line.

## The lens

A red-team overweighting exotica would have chased the plunge; the most
player-visible failure is the boring one: an equal-mass binary's periastron drift
and orbital period are subtly wrong everywhere inside 100M, and no instrument in
the repo is licensed to notice. What this lens may have missed: the ISCO/plunge
error TYPE (not measured here), and whether the plane's integer law already
diverges from the float doll by more than these ν-terms (the integer law's own
gates would need the same 2PN licence).

## Files

`eob_flank.py` (instrument + grid), `flank.json` (all numbers), `predictions.md`,
`regen.sh`. Machine: shared Linux runner (8 vCPU), single process, 33 s.
