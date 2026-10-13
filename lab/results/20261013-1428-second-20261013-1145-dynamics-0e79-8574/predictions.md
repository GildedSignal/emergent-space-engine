# Predictions — frozen 2026-10-13 ~14:4x UTC, before building or running any new flight

The second checker kept 20261013-1145-dynamics-0e79 from gold on two record defects (regen.sh
cannot regenerate the four crash rows; the frozen pre-registration text is unrecoverable — it
exists only in the final publish commit 7ae64ed6, so I state it unrecoverable rather than
reconstruct it) and named the unflown cheap flights: the Λ\* r-dependence, the nose-sense brake,
and the refusal-storm decomposition. These are my predictions for those flights, written before
the probe exists.

## P1 — the record (the named experiment)

One committed flight list with D levels [0, 2, 4, 5, 6, 8, 15] regenerates all 22 rows of
grid.txt + grid-d.txt bit-identically on physics columns. Expected because each flight is an
independent deterministic world (fresh plane, seed 1, settle-only inputs at fixed check cadence)
and determinism is already witnessed for 19 of the 22 rows by the run's own second invocations
and both checkers. If any row differs, the run's record is worse than reported and I report which.

## P2 — Λ\* vs r (the apoapsis brake)

Raise the ship to apoapsis ≈ 2R and ≈ 4R (forward L2 cut by osculating apoapsis, nose tracked to
v during the coast-out, then a held fixed-nose reverse brake at levels spanning Λ), compute Λ at
hold start with g(r_apo) = g_start·(1.099/r_apo)². Two competing rulers:

- **Λ-hypothesis (the claim):** fate is ordered by Λ, not level. Predicted: at apo ≈ 2R
  (Λ ≈ 1.7·2^L·(r_apo/1.099R)² ≈ 4·0.427·2^L): L1 (Λ ≈ 3.4) crashes, L2 (Λ ≈ 6.8) crashes or
  grazes, L3 (Λ ≈ 14) escapes or grazes, L4 (Λ ≈ 27) escapes. At apo ≈ 4R (Λ ≈ 13·0.427·2^L):
  L0 (Λ ≈ 5.6) crashes, L1 (Λ ≈ 11) borderline, L2 (Λ ≈ 23) escapes, L4 (Λ ≈ 90) escapes. The
  boundary Λ\*(apo) lands within ~2× of the start-orbit Λ\* ∈ (6.8, 13.6) at both radii.
- **Level-hypothesis (the alternative):** what crashed at the start orbit crashes anywhere —
  L4 crashes at both apoapses. This would refute Λ as the ruler across r and I would say so.

Confound I accept and name: the apoapsis brake is also an eccentric brake (e ≈ 0.3–0.6) at lower
initial speed, so r and e move together; this flight decides whether Λ survives the move, not
which of r/e carries it.

## P3 — nose sense / attitude (the tracking brake)

From the start orbit, hold reverse while re-pointing the nose along v every check (bang-bang
turn keys, band ±2.5°; the turn tier runs at 2⁻³⁰ turns/tick ≈ 4.1°/min, and v rotates ≈ 4–5°/min
in the fall, so the tracker is marginal by construction).

- **Misalignment reading (my prediction):** the fixed nose's cost is that thrust stops opposing
  v once v rotates; a tracking brake should escape at Λ well below the fixed-nose Λ\* ≈ 7–14.
  Predicted: L4 (Λ 6.8, crashes fixed) escapes tracked; L5 (Λ 13.6, grazes fixed) escapes
  tracked cleanly; L2 (Λ 1.7) is marginal — thrust is only 1.7× local weight, I predict escape
  but with low confidence; L0 (Λ 0.43 < 1) still crashes: tracking cannot beat thrust < weight.
- **Turn-rate-limited reading (the alternative):** v's rotation outruns the 2⁻³⁰ turn tier in the
  fall (the lag column grows past ~30°), the brake stops opposing v, and L4 still crashes. Then
  the fixed nose is not the cost — the turn tier is — and "attitude control" cannot rescue a
  held brake at any level: that would be a new wall for the turn tier, reported as such.

## P4 — the refusal storms

Re-fly off45/off90 with per-check refusal logging, bucketed by phase (pump/turn/hold) and by
doll-change vs same-doll checks. Prediction: the storms are a held-burn phenomenon, not a turn
phenomenon — ≥ 80% of the 12.7–13.4k refusals accrue in phase ≥ 3 (the off-axis held burn), and
within it they cluster at doll-change (rekey) checks, starting only after γ grows past ≈ 2 (the
A/B θ = 0 pumped flights show zero refusals at the same γ, so the off-axis component — the
transverse motion crossing doll boundaries — is what rekeys). If instead most refusals fire in
the turn phase, the turn owns them and the `range` defect report widens. Frame-time cost: not
measured — the shared 8-vCPU runner gives no stable timing; stated, not fudged.

## Scorecard (after the canonical 38-flight run; the predictions above untouched)

**P1 — HELD (22/22).** One committed list (D levels [0,2,4,5,6,8,15]) regenerates every row of
grid.txt + grid-d.txt bit-identically on physics columns (regen.sh; per-row name-keyed diff).
The named experiment is done: the record defect is closed on the shipped tree at f00a04ec.
The frozen pre-registration of 1145 stays unrecoverable (only the post-run scorecard was ever
committed, 7ae64ed6) — stated, not reconstructed.

**P2 — FALSIFIED in both readings, and the Λ constant itself was wrong.**
First the constant: μ̃ measured from the shipped code (β²·r on the circular start orbit,
8.845×10⁻¹⁰ in Home radii = 2⁻¹⁸ of the star's μ exactly; v_c = 8.51 km/s, T = 5,172 s, both
confirmed by the record's own coast row) gives surface g = 12.47 m/s², local weight at the
start orbit = 10.33 m/s² — not the 8.11 both checkers verified (they assumed an Earth-mass
Home; it is 1.27 Earth mass). Corrected ladder Λ(L) = 0.3355·2^L: 0.34/1.34/5.37/10.7/21.5/
85.9/1.10×10⁴. The level bracket L4-crash/L5-escape is unchanged; Λ* ∈ (5.37, 10.7).
Then the map: from apoapsis 1.445R, L1 (Λ 1.16) crashes at 7.83 km/s and L4 (Λ 9.26) lives;
from 1.665R, L1 (Λ 1.54) crashes, L4 (Λ 12.3) lives; from 2.228R, L1 (Λ 2.75) LIVES (dip
1.4586R only) — as does every E flight at Λ ≥ 2.75 up to 78.7. Crash at Λ 5.37 from 1.099R
against alive at Λ 2.75 from 2.228R falsifies Λ as the ruler across r (and L4 living from
1.445R up falsifies the level reading). Λ* falls with the brake's start radius by ≥ 2–4×
between 1.099R and 2.228R. My predicted crashes at E2R-L1/E4R-L0 did not happen.

**P3 — FALSIFIED in the predicted reading; the turn-rate alternative confirmed.** The tracking
brake does not move the boundary: L4 tracked still crashes (9.14 km/s, world 6:27) and L5
tracked lives — the same L4/L5 bracket as the fixed nose. The lag column is the mechanism:
24.6° at L0, 47.5° at L2, 144.2° at L4, 163.5° at L5 — the band controller saturates the
turn tier (2⁻³⁰ turns/tick = 4.08°/min) while v rotates ≈ 24°/min in the terminal fall, so the
nose cannot follow and thrust stops opposing v. Attitude control at the shipped turn rate
cannot rescue the basin; the wall is the turn tier's rate, not the fixed-nose assumption.

**P4 — half held.** 100.0% of both storms (13,386 / 12,762) accrue in the held-burn phase
(≥ 80% predicted) — but the rekey clustering is FALSIFIED: 0% fire at doll-change checks.
The storm is a steady per-check tax: refusals on 91% of all checks through the burn, ~6.5 per
check, γ between 1.7–2.4 (off45) and 3.2–5.0 (off90), doll constant ("star"), first refusal
at γ 2.10 / 3.19. Every θ = 0 pumped flight shows zero refusals at the same γ — the off-axis
burn state (nose 45–90° off v), not γ and not the doll edge, refuses the kicks. Frame-time
cost unmeasured, as disclosed.
