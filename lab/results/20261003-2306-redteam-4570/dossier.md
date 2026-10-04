# Dossier — premise red-team of representation.md (run 20261003-2306-redteam-4570)

## Claim

The view gather's per-emitter cache is Newtonian where the game is relativistic:
its warm-guess slope is clamped to [0.5, 1.5] and its fast-path acceptance window
is `1 − speed`, but the true arrival rate is `1/(1 + n·β)` — the inverse Doppler
factor — so on B15's own 0.9c stream every stream emitter costs 2–3 tube readouts
per frame forever (measured 1.96–2.98 vs 1.01 for static), at root speeds ≥
0.9999c the one-readout path is unreachable, and two one-line relativistic
constants restore ~1.0 readouts everywhere with identical ticks.

## Bottleneck

The plane's #2 measured bottleneck (HANDOFF, 1 October): the view gather is 83%
of a light frame. Relativistic content (the 0.9c stream is in B15's frozen
scene) currently pays 2–3× the readout cost of slow content; the fix deletes
that overhead — order of magnitude: the gather's per-emitter cost on streams
falls ~2–3×, no new component. Also: premises 4 and 5 of the design have **no
rung** (r5 and r6 are named in representation.md §7 but absent from
`lab/rungs/`; law.md lists them as open), so nothing frozen would have caught
this or the dense/sparse door below.

## Evidence

Faithful Python port of `crates/universe/src/view.rs::crossing` +
`ViewCache::guess/put` (integer-tick Newton, acceptance window
`−(1 − speed − 1e-4)`, bracket fallback, 64-readout cap, slope clamp [0.5,
1.5], cold guess = t_now), uniform-motion emitters in the root frame, c = 1,
1 tick = 4.925 µs = 1.47 km. Oracle: g is strictly monotone (dg/dt = 1 + n·β
> 0), so the answer is exactly floor(real root), found by bisection.

- `python3 gather_falsifier.py` (0.5 s): warm mean readouts/emitter/frame over
  100 frames — static 1.01; 0.9c transverse 1.96–1.97 (max 6); 0.9c head-on
  2.01–2.98; 0.9c receding 1.96; 0.99c 2.01–2.05; 0.9999c transverse 2.05.
  Moving observer (0.9c lateral): 2.02. Correctness: 270 cold/foreign-guess
  (±10⁵ ticks) cases, 0 wrong ticks, 0 dropped, worst 4 readouts. Acceptance
  window analytic: empty at root speed ≥ 0.9999 (measures −1.1e-17).
  One-crossing monotonicity: 10⁵-case sweep, min dg/dt = 2.6e-4 > 0.
  True root-advance rate for approachers: 10 at 0.9c, 100 at 0.99c, 1000 at
  0.999c — the clamp caps at 1.5.
- `gather_fix.py` (slope clamp widened): 0.9c head-on 2.98 → 1.02.
- Combined fix (acceptance `−(1 + n·β) − ε` + unclamped slope, same script
  variant): all geometries and speeds 1.01–1.05, correctness 0/25 wrong.
- Tick quantization of the emission event: apparent angular error 1.1 px per
  tick at 1470 km for 0.9c transverse (1080p, 90° FOV); crosses 1 px at
  D* ≈ 1600 km — player-visible only inside relativistic dogfights.

## Predictions

`predictions.md` was written before the decisive run. P1 held (2+ readouts on
all 0.9c+ content, warm); P2 held (window empty ≥ 0.9999c, cost only — zero
correctness loss, exactly as predicted); P3 held (D* ≈ 1.6e3 km); P4 held
("any cache gives the same view": 0/270 wrong); P5 held (0 monotonicity
violations in 10⁵). One refinement: head-on cost is dominated by the slope
clamp, not the window (my analytic sub-claim that the window governs head-on
was wrong; the measurement corrected it). Two scene errors were found and
fixed during the run (pre-first-light path; post-flyby emitters — a 0.99c
approacher is inbound-visible only in a 1% distance band, itself a
demonstration of how narrow the seen-inbound window is at high β).

## What would make it wrong

The port uses uniform motion; real tubes have n·β varying along the orbit, so
the stored slope tracks a measured average rather than an exact rate — if
orbital curvature made the relativistic extrapolator oscillate (perigee swings),
the fixed acceptance could cost more than measured. The bracket fallback bounds
this: correctness is provable (acceptance ⇒ last tick with g ≤ 0) independent
of the guess, and the 64-cap covers pathological seeds. Cost of adopting: two
constants in `view.rs` (`put`'s clamp; `crossing`'s window), both already
computed nearby (1 + n·β is the arrival rate and the inverse Doppler the
colour path uses). Fit with PRINCIPLES: principle 1 (cheapest compute is
compute not done — one readout, not three), principle 3 (the view is derived
at observation: only the observation's own constants should appear), principle
26 (steal what works: the Doppler factor is already in the code).

## Ranked attacks (the lens deliverable)

Ranked by how likely the player is to see the failure:

1. **Newtonian cache in a relativistic view (premise 5, measured above).** The
   player at high c watching the stream pays 2–3× gather cost per frame — the
   headline experience costs the most on the plane's #2 bottleneck. Rung that
   should have caught it: **none — r6 does not exist.** Proposed criterion:
   warm readouts ≤ 1.2 per emitter at |β| ≤ 0.9999, all geometries, moving
   observer included; ticks identical to the cold oracle for any cache;
   negative control: the shipped constants (clamp 1.5, window 1 − speed) must
   fail on the 0.9c stream.
2. **Dense/sparse bit-identity has no rung (premise 4).** One engine test
   exists (H0207: a battle bit-identical lockstep vs sparse), but nothing
   frozen attacks it: foreign caches, simultaneous same-cell contacts ordered
   by provenance vs time, radix-key collisions. Player-visible as a battle
   replayed differently from how it played. Proposed r5: replay one battle's
   event graph in both orders with permuted caches → identical digest;
   negative control: provenance-free serialization must differ.
3. **The two-body doll is unbounded in the doc (premise 1).** B11 judges only
   seeds with next-term 5/a² ≤ 5×10⁻⁴ (a ≳ 100M); by the gate's own estimator
   a tight binary at a = 10M carries ~5% next-term error, at ISCO ~14%, and
   representation.md still says "dolls all the way down" with no handover to
   the dense order or a plunge chart. Not falsified here (no trustworthy 2PN
   oracle in this container); flagged with the gate's own numbers. Rung: B11's
   excluded band needs a designed fallback or an explicit "not judged" bound.
4. **representation.md is a stale second home for truth (premises 2, 3, 6 as
   written).** §1 still teaches the Minsky in-cell map as "the primary
   in-cell solution" — killed 30 September (law.md:20, band-centre tangent
   slope error in turning-point cells; replaced by `space-darwin16-v1`); §2's
   joint-refraction framing carries the killed river (H0205); §3 still
   describes the killed kick layer as live; §6 says kicks cost "~50 ns,
   incremental" against the measured 29 µs (580×, kicks the engine's dominant
   cost); §7 names r5/r6 that do not exist. A builder reading the design
   implements dead physics. No rung catches doc drift; `history check`
   enforces budgets only. Fix: rewrite representation.md in place (AGENTS:
   specs are rewritten in place and hold no change logs).
5. **Emission-tick quantization at dogfight range (premise 5, minor).** ~1 px
   per tick inside ~1600 km at 0.9c; deterministic; principle 28 covers it
   (the view is an instrument). Below threshold beyond ~10⁴ km.

Premises that survived, reported as such: one crossing per tube without
lensing (proved: dt_arr/dt_e = 1 + n·β > 0; 10⁵-case sweep, min 2.6e-4);
"any cache, however stale or foreign, gives the same view" (0/270 wrong,
worst 4 readouts); exact-tick correctness of the gather at every speed tested
including 0.99999c.

## The lens

A premise red-team overweighting the player's eye found its strongest result
in cost, not wrongness: the gather is *correct* everywhere I attacked it
(the bracket fallback is genuinely well built — the answer is provably the
last tick with g ≤ 0, independent of the guess). What the lens may have made
me miss: everything the player sees through gravity rather than light
(retarded gravity, the Fermi-frame GR tide) — E9's own red-team is queued
next in this window and covers it; and attack 3 rests on an estimator, not a
measurement, because no 2PN oracle is reachable from first principles in this
container without literature risk.
