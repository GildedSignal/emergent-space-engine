# Dossier — run 20261011-2028-second (second author on 20261011-1917-redteam-fb64)

## Claim

The checker's named experiment is done and it decides BOTH ways: the silver
run's strong-field rows (r_e = 6, 8) were **correct all along** — the
checker's "converged" corrections there (delay 30.9→38.6, err_fix 9.9e-3→9.6e-2
at the ISCO) were themselves artifacts of a still-under-converged table, as
proven by an independent u-space Gauss–Legendre quadrature at every sampled
b — while the real corruption (A_t linear-interpolation error up to +414 M at
nearly-radial out-family columns, confirmed) DID reach the record at
r_e ≥ 20 (err_design −21%, err_fix −40% at 20 M); and the missing experiment
— the image-resolved delay memo at r_e = 8 — now exists and reaches the
player floor with 1,900× margin (median 7.6e-7 rad, 16/16 frames under one
pixel) where the per-family memo cannot (median 6.8e-2 rad, 47 px), provided
the memo is keyed in the light tube's own sweep parameter, not b.

The silver claim itself — the view's gather omits gravitational arrival
delay; bodies within ~60 M render 1–97 px wrong; the fix is one memo column
— **survives the converged record unchanged in every verdict**, with P8's
fate exactly as the silver author honestly reported (held at r_e = 6 and
≥ 60, failed at 8 and 20).

## Bottleneck

Not a board number: a correctness hole in the view (principle 30), already
argued by the silver run. This run closes the record: the one non-
regenerable number is regenerated (and vindicated), and the named prototype
converts "the correction must be image-resolved" from inference to
measurement.

## Evidence

All numbers regenerate from shipped code in this folder; each command is
single-threaded numpy on the shared 8-vCPU runner (load ~2, < 300 MB RSS).
`python3 attack.py calibrate|sweep` regenerate the SILVER record bit-
identically (verified `==` against the branch JSONs before any change).

**1. The oracle converged and validated (`python3 attack2.py quad`, 62 s).**
Decisive table: dφ = 7.5e-4 + 128 substeps re-integrating the arrival step.
Independent referee: u-space GL24×40 with sin²ψ substitution at turning
points and grazing launches (different parameterization AND rule than the
RK4-in-φ). At EVERY arrived column of every scene:

| r_e | original A_t rel err (abs) | fixed A_t rel err (abs) | A_phi err |
|---|---|---|---|
| 6 | 5.6e-2 (1.2 M) | 1.8e-6 (4.0e-5 M) | 1.8e-7 |
| 20 | 1.3e-1 (7.9 M) | 4.4e-6 (2.8e-4 M) | 2.3e-7 |
| 1000 | 1.2e-1 (414 M) | 5.8e-6 (1.8e-2 M) | 2.3e-7 |

The checker's finding (linear arrival interpolation inflates nearly-radial
out-family columns, b ≲ 0.15 r_e) is CONFIRMED and larger at the extreme
(+414 M vs their +24 M). RK4 4th-order scaling verified (halving dφ drops
the worst column 13.7×).

**2. Adjudication of the checker's corrections (`python3 attack2.py sweep2`,
58 s).** Three oracle constructions — silver (dφ=3e-3, linear), checker-style
(dφ=7.5e-4, linear), mine (dφ=7.5e-4, substeps) — agree to 4 digits on every
scene metric at r_e = 6 and 8. The scene's crossing solves query mid-b
columns (primary roots at r_e = 6: b ≈ 5.2–5.3 M), where even the silver
table matches the quadrature to ≤ 4e-3 M (measured directly at the primary
roots). The corrupted small-b nodes (b ≲ 1 M) are never interpolated
against. The checker's r_e = 6/8 corrections therefore do not reproduce
under ANY of the three tables, and the quadrature sides with the silver
values. At r_e = 20 the corruption DOES leak into the memo curves:

| r_e | metric | silver | converged (this run) |
|---|---|---|---|
| 6 | delay / err_design / err_fix | 30.87 / 8.52e-2 / 9.93e-3 | 30.87 / 8.52e-2 / 9.93e-3 (unchanged) |
| 8 | delay / err_design / err_fix | 12.30 / 9.03e-2 / 2.35e-2 | 12.30 / 9.03e-2 / 2.35e-2 (unchanged) |
| 20 | delay / err_design / err_fix | 4.42 / 1.52e-2 / 1.30e-3 | 3.95 / 1.20e-2 / 7.83e-4 (−11% / −21% / −40%) |
| 60 | err_fix | 3.86e-5 | 3.91e-5 |
| 200 / 1000 | err_fix | 1.69e-6 / 1.60e-7 | 1.03e-6 / 1.90e-8 |

phi0 robustness (results-phi0.json): the corrected 20 M row stays at
err_fix 3.9e-4–1.3e-3 over four phases (always above 1e-4, straddling the
floor); the 8 M row stays 1.3e-2–5.4e-2. Weak-field calibration on the
converged oracle: err_design 6.3e-7 (passes), planted negatives fail at
3.2e-5/45× and 6.9e-3/11,000× — both sides still controlled.

**3. P8 re-derived on the converged record** (`sweep2` prints it):
"err_fix < err_phase/10 at every r_e ≤ 20" — held at 6 (ratio 0.071) and
20 (0.105 vs 0.1: marginal fail by 5%, honest coin-flip territory), failed
at 8 (0.499). "err_fix < 1e-4 at r_e ≥ 20" — failed at 20 (7.8e-4), held at
60/200/1000 (3.9e-5, 1.0e-6, 1.9e-8). This is the SAME verdict structure
the silver author reported. The delay remains the dominant term: the
per-family fix collapses err_phase by 14× / 2.0× / 9.5× / 39× / 227× /
1,160× at r_e = 6 / 8 / 20 / 60 / 200 / 1000 (err_fix/err_phase in
results-sweep2.json: 0.071 / 0.499 / 0.105 / 0.026 / 0.0044 / 0.00086).

**4. The image-resolved delay memo prototype (`python3 attack2.py imgmemo`,
37 s).** One tracked image per scene (continuity in (σ, branch, α) within
0.35 rad, 16 frames spanning one orbit), memo keyed per image = arrival
family + winding segment + α-window ±0.35 rad. Three crossing solves, same
seed (warm = previous frame's converged time for the tracked image; cold =
te_flat on jumps), same target (the tracked image's own retarded position):

| r_e | per-family (shipped memo) | image-resolved, b-keyed | image-resolved, A_phi-keyed |
|---|---|---|---|
| 6 | med 6.6e-2, max 3.1e-1 | med 3.1e-2 | **med 3.1e-5, max 8.7e-4, 16/16 ≤ floor** |
| 8 | med 6.8e-2, max 3.5e-1 | med 4.2e-2 | **med 7.6e-7, max 3.5e-4, 16/16 ≤ floor** |
| 20 | med 5.0e-2, max 2.1e-1 | med 1.9e-2 | **med 7.3e-7, max 1.2e-3, 16/16 ≤ floor** |
| 60 (control) | med 3.0e-3 | med 2.2e-3 | med 1.8e-7, max 3.8e-3, 15/16 ≤ floor |

Floor = 1.45e-3 rad (one pixel, 1080p vertical 90° FOV). The checker's
named demonstration — reach the floor at r_e = 8 where per-family provably
cannot — holds with 1,900× median margin, including the 4 cold-seeded
(tracking-jump) frames. Mechanism, measured: the b-parametrized memo FAILS
because the arrival family folds in b near the photon ring (bend(b) non-
monotone: 23°→6.5° with a 10° knot at the ring edge; the self-consistent
b-map is non-contractive and clamps); the tube's own sweep parameter
(A_phi, monotone per branch) inverts without folds and carries the exact
identity G(te*) = te* + dt* + (D(te*) − D_tube(α*)) − t_obs = 0 — the solve
is a bracketed bisection (the checker's own prescription) on a smooth G.
One instrument bug found and fixed en route, disclosed: the angular closure
needs σ·A_phi = 2πk − φ0 − ωt; I first inverted the σ=+1 expression for
both signs (the σ=−1 chains failed at 1e-2; after the sign fix they hit
1e-7–1e-9, which is what localized the bug).

## Predictions

In [predictions.md](predictions.md), written before the decisive runs.
Held: Q2 (original's A_t > 1 M error in every scene's b range), S2, S3
(within stated bands), I1–I3 (the prototype reaches the floor at 6, 8, 20 —
the run's central held-out claim), I5 (jumps ≤ 35%: 4/16 at r_e = 8).
Partially held: Q1 (rel clause ≤ 5.8e-6 ✓; abs clause 1e-3 M fails at
r_e = 1000's extreme nearly-radial column, 1.8e-2 M), I2's tail prediction
(the tail stays below floor: max 8.7e-4 — conservative). Failed, and the
failures are the run's findings: **S1** — my [REPRO] prediction that the
checker's r_e = 6/8 corrections would reproduce: they do NOT (the double-
check refuted the correction; see adjudication); **S4** — "r_e ≥ 60 rows
change < 2%": err_fix moved −39%/−88% at 200/1000 (absolutely immaterial at
1e-6/1e-8 vs the 1.45e-3 floor, but the prediction as written was wrong);
**S5** — P8 at r_e = 6 holds, not fails; **I4** — sharper than predicted:
not only does the flat-b ablation fail, the b-keyed memo itself fails; only
the A_phi-keyed memo works. Instrument fixes after writing predictions,
disclosed: the referee quadrature needed GL24×40 (GL16×8 under-resolved the
grazing columns, masquerading as 5.8e-5 table error), and decisive tables
moved to dφ = 7.5e-4 per the checker's prescription.

## What would make it wrong

(a) The quadrature shares a bug with the RK4 table — unlikely: different
parameterization (u vs φ), different rule (GL vs RK4), and it agrees with
the table to 5.8e-6 while DISAGREEING with the checker's corrected values;
plus the weak-field control and both planted negatives still pass/fail on
cue. (b) The scene-query argument (small-b corruption never interpolated)
could break for other observer geometries — r_o = 4 r_e, equatorial,
static observer only; a scene whose primary images sit at b ≲ 0.15 r_e
(observer nearly behind the hole) would inherit the silver bug; the fix
(substep arrival) is in the shipped table regardless. (c) The prototype's
tracking uses the oracle's root set for image identity — a runtime tracker
must maintain (σ, branch, k, α) itself; 4/16 frames jumped and still hit
the floor cold-seeded, but longer sequences near caustics are untested.

## Cost of adoption

Unchanged from the silver, plus one key decision: the doll's memo column
must be keyed by the light tube's sweep parameter (A_phi/α), not b — "b =
L/E parameterization" (law.md §Motion.6) folds near the photon ring and
cannot serve multi-image scenes. The crossing solve is a bracketed
bisection (≈ 40 G-evaluations, each 2 interp + 1 chord: same cost class as
the design's Newton). No new component; no law change; integers keep
deciding canonical outcomes.

## Fit with PRINCIPLES

Principle 2 ("'Exact' means deterministic and reproducible"): the record now
regenerates from shipped code, both the silver rows and the corrected ones.
Principle 34 ("the oracles are guards, not shepherds"): the checker's
correction was itself unguarded — this run is the second finder, and it
refutes the correction's strong-field half while confirming its weak-field
half. Principle 10 ("Measure before claiming"): the "must be
image-resolved" inference is now a measured 10⁵× separation at the same
tracked image. Via negativa: the b-keyed memo variant is deleted from the
proposal.

## The lens (what this lens may have made me miss)

A second author inherits the checker's framing; I nearly baked their
"converged" values into my predictions as [REPRO] ground truth — only the
pre-registered prediction format exposed the conflict when the numbers
refused to reproduce. Untested here: Kerr (frame dragging reshapes but does
not remove the delay), moving observers (aberration compounds retardation),
the tracker over many orbits through caustic mergers, and the gather's cost
(r6's original sketch). The prototype's tubes are compiled from the same
RK4 family as the oracle (quadrature-validated at the columns used, but a
fully independent tube compiler would sever the last shared-harness link).
