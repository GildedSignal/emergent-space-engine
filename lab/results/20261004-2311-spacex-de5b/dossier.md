# Dossier — 20261004-2311-spacex-de5b (spacex lens)

## Claim

Neither WHFast symplectic correctors (0× — they repair an error term the split's gate
observables never see) nor a 4th-order Yoshida split (1.33× on the tuning scene, 3× worse on
the close pass) buys the hoped-for 4× kick cut for the plane's drift-plus-tide split: the
plane's 64 kicks/orbit plain DKD is already near its own minimum, because the binding
behaviour is apsidal precession under eccentricity pumping, not the Jacobi error these
schemes reduce — so the lever is the precession gate's representation (r9's lesson, again),
plus one deletion available today: a per-observable kick cadence (energy-only bodies run at
16/orbit, 2–4× fewer kicks), since the J gate alone passes at 16 while only apse-tracked
moons need 64.

## Bottleneck

Board #1 (1 October): "fewer kicks per orbit at the same behaviour (correctors, higher-order
splits): kicks dominate the engine's cost". The queue item `q-correctors` asked exactly this
(gold bar: measured 4× cut with an integer path named). Expected gain: 4×+ fewer kicks.
What it deletes if true: 3/4 of all kick events. What it deletes as false: the corrector
work item itself, and the assumption that the cadence is set by the split rather than by
the gate.

## Evidence

Float replica of the plane's law (`crates/universe/src/step.rs`: DKD, step = 1/64 of the
radial period in mean anomaly; drift exact, kicks = the tide): Jupiter-mass planet
(mu_p = 1e-3) forced circular at 1 AU; moons planetocentric; kick = star tide (+ a second
planet's tide in the pass scene). Schemes: `dkd` (the plane), `dkd3`/`dkd5` (WHFast 3rd/5th-
order corrector, REBOUND's exact coefficients, applied at outputs only), `y4` (Yoshida-4,
3 kicks/step), `euler` (negative control). Behaviours: Jacobi max-error ≤ 1e-4 (B12),
apsidal precession within 10% of the dkd@512 reference (B14/r9), bound/escape class matches
the reference (B14), final elements within 1%/10% after a 2.2-Hill-radius planet pass (B13).
50 planet orbits; 2–19 moon orbits per planet orbit; prograde moons unstable beyond ~0.49
r_H (real CR3BP), so the sweep is prograde 0.2–0.45 and retrograde 0.5–0.85.

Minimum kick-evaluations per moon orbit passing all gates (scene-level = max over moons):

| scheme | s1 tuning | s2 held out | s3 pass | s3 detail |
|---|---|---|---|---|
| dkd    | 64 | **FAIL** (retro@0.6 never passes ≤64) | 16 | |
| dkd3   | 64 | **FAIL** | 16 | ret0.5 needs 32 (dkd needs 8) |
| dkd5   | 64 | **FAIL** | 16 | idem |
| y4     | 48 | 96 | 48 | admissible where dkd is not |
| euler  | FAIL | FAIL | FAIL | control |

- The corrector is correctly implemented (verified: displaces the state by 5.7e-5 ≈ the
  eps·dt scale at K=8) and changes **no gate outcome anywhere**; the split's Jacobi error is
  already O(eps² dt²) (measured dt² scaling, 2e-5 at K=8), so the O(eps·dt²) term the
  corrector kills does not exist in these observables.
- y4's J error scales dt⁴ as advertised (×~60 per halving; 7e-10 at K=64) — and it still
  buys almost nothing, because J is not the binding gate: **J alone passes at 16/orbit for
  dkd on every s1/s2 moon** (2–4× deletion available today for bodies nobody tracks).
- The binding gate is apsidal precession on e-pumped moons: dkd's precession error at
  K=8..64 on e10-0.4 is 0.26/1.42/0.49/0.00 (noise-seeded, not convergent until 64), while
  y4 locks exactly at K=16. On retro@0.6 dkd never converges ≤64; y4 locks at 32.
- Reference sanity: dkd@512 vs @2048 agree on precession to <0.05% on every bound moon
  (including the pass scene); drift unit test: energy exact to 2e-14 over 1000 orbits;
  euler fails at least one moon on every scene at every K (though the easiest moon passes
  its J gate at K≥16 — my prediction 6 was too strong).

Reproduce (Linux, ~9 s total, float replica):

```
cd lab/results/20261004-2311-spacex-de5b
rustc -O -o kickcorr kickcorr.rs && ./kickcorr && python3 summarize.py
```

## Predictions

`predictions.md` written before reading any held-out scheme row (harness tuned on s1 only).
Outcome: 3 confirmed (corrector no-lever; s3 all pass at 16; reference convergence), 1
roughly right (y4 1.3×), 3 wrong — dkd's s1 minimum is 64 not 32 (the precession of
e10-0.4 binds, which *strengthens* the finding); dkd FAILS retro@0.6 outright rather than
passing at 32; euler passes the easiest moon at high K. The wrong ones were all in the
direction of the finding being stronger than predicted.

## What would make it wrong

- A different precession gate (secular frequency analysis instead of LSQ on the apse angle,
  r9's Clairaut lesson) could dissolve the precession wall; then dkd relaxes below 64 and
  the "64 is minimal" half of the claim weakens. That is the named next experiment.
- The replica is float and 2D-coplanar, no SyMBA sub-steps, no integer quantization; the
  plane's real kick (rebinding, sub-quantum carries) could bind at a different K. Integer
  check belongs to `q-correctors`' follow-up on the real law.
- y4 and the correctors are not exactly representable in the integer law (w1 = 1/(2−2^{1/3}),
  corrector coefficients irrational): adopting either costs bit-exactness or needs rational
  approximations whose cancellation is no longer guaranteed. dkd remains the only fully
  integer path — an independent reason not to adopt, beyond the measured 0×/1.33×.

Cost of adoption: zero for the negative (deletes the corrector plan item); the
per-observable cadence is a one-line policy in `step.rs` (a body with no apse observer
takes H = P/16): ~2–4× fewer kicks for untracked bodies, behaviours unchanged by the J and
class gates that already cover them.

## Fit with PRINCIPLES

- "A failed experiment kills that configuration, never the method" (#9): the corrector
  configuration is killed for this split; the method (cheaper kicks by representation
  change) moves to the gate.
- "Compute only surprises" (#3) / "No work for no reason" (#14): bodies whose apse nobody
  observes pay 64/orbit today for a behaviour nobody reads — a deletion, not an
  optimization.
- "Behaviours matter, not continuum fidelity" (#2): the J gate passes at 16; only the
  precession behaviour forces 64 — the split is not the cost driver, the observable is.
- "Steal what works, from skin in the game" (#26): REBOUND's corrector, exactly, with its
  literature coefficients — measured before judged.

## The lens

SpaceX's delete-first instinct found the two deletions (don't build correctors; split the
cadence), but the lens initially underweights what the data showed: the cost is set by a
*gate's representation*, not by machinery — closer to Julien's "the right question, then
the representation" (#18) than to idiot-index arithmetic. A hardware-rich lens also wants
to blow up the pass scene harder; the m20 = 4.56 pass at 2.2 r_H was chosen to stay inside
the plane's regime (SyMBA handles closer), which bounds what this run can say about deep
encounters.

## Grade suggested

Silver-to-gold: it is reproduced by two commands, it kills a queued configuration
(q-correctors' premise) and names the next experiment (the precession gate by frequency
analysis; the integer check). Not gold by the letter: no 10× was moved, and three
predictions failed (though all toward the stronger conclusion).
