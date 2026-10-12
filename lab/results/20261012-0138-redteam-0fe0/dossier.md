# Dossier — red-team of docs/representation.md (run 20261012-0138-redteam-0fe0)

## Claim

The design's six load-bearing premises were attacked in the lens's order; the one already
falsified is in the design text itself (§1's in-cell Binet/Minsky rotation is dead in the
live law), the two-body doll's ν claim is exact for the relative motion but silently
stops being the field its members feel, the view has no correctness gate at all — and the
central determinism premise (both orders, identical bits) **survived** the attack it had
never faced: a relativistic body crossing a battle, bit-identical across lockstep and
sparse orders at β = 0.88, with the negative control firing.

## Bottleneck

Bottleneck 0 of the board (the representation). The attack targets what B8's evidence
base actually covers before the law freezes on it. Gain: not orders of magnitude — this
is a red-team; its product is which premises may be built on and which must be fixed
before more is built on them.

## Evidence

Machine: GitHub Actions linux runner, 8 vCPU, 15 GB, load 1.24, 1 GB used, shared (state
recorded per PRINCIPLES; timings are Linux/x86, orders of magnitude only).

### The falsifier (premise 4: "two evaluation orders … with identical bits")

`crates/engine/tests/redteam_flyby.rs` (copy in this folder; run
`cargo test -p emergent-engine --test redteam_flyby -- --nocapture`, 11 s; output in
`flyby.out`). The shipped identity ladder (`crates/engine/tests/identity.rs`) covers only
battles whose bodies all move at fleet speed q/8..q/32 (β ≤ ~0.18, one speed class per
scene). The falsifier keeps the shipped s1 scene bit-for-bit (100 bodies, q = 1024,
seed 2, div 8, same rng draw order — my v0 digest `1f8e2ebdefd6` equals the shipped s1
digest) and appends interceptors of mass 1, radius q/2, aimed to cross the engagement
zone at t = 480:

| variant | contacts | epochs | lockstep | sparse | rebuilds | digests |
|---|---|---|---|---|---|---|
| v0 none (control = shipped s1) | 216 | 33 | 1.25 s | 0.04 s | 3 | equal |
| v1 one at β 0.88, along a fleet row | 230 | 33 | 1.26 s | 0.04 s | 2 | equal |
| v2 one at β 0.74, diagonal | 217 | 33 | 1.27 s | 0.04 s | 2 | equal |
| v3 two opposing at β 0.88, same row | 233 | 33 | 1.28 s | 0.04 s | 2 | equal |

World, log and tide digests equal in both orders on every variant (`Outcome` equality,
asserted). The interceptors really collided (contacts +14/+17). The negative control
fired per variant: one chronon of epoch shift in one order breaks equality; shifted in
both, they agree again — the instrument can see a difference. Cost surprise, in the good
direction: sparse is ~30× faster than lockstep and the fast body adds no grid re-forms
(2 vs 3 rebuilds), so the p99/allocator fear of one fast body churning the sparse
structure of a battle did not materialise at this scale (100 bodies, 4096 chronons).

Why identity holds here, and what this proves: the lattice law is discrete-time by
construction (contacts are exact integer bin meets at ticks), and c = |k| < q is the
no-tunneling guarantee — a body advances less than one cell per tick, so it meets every
cell on its path; there are no mid-tick contacts to disagree about. That is the design's
own "c = 1 cell per cell-update" being load-bearing for contact completeness, which
representation.md states as a cost rule but never as the completeness argument for
bit-identity. **What B8 gains:** the scene class the ladder lacked (speed heterogeneity,
relativistic closing speeds, a near-c pair contact) now passes. **What it does not
prove:** handoffs of a relativistic body out of the frame's size rule in both orders
(the interceptor stays inside the extent rule here), and cross-doll simultaneity
(HANDOFF's open risk, root-clock keys in flight) — neither is exercised by this scene.

### Premise 5 (the view): my cheapest attack ran and the premise survived it

`view_newton.py` (`python3 view_newton.py`, 0.04 s; output in `view_newton.out`):
Newton on the past-light-cone root, warm-seeded at 60 FPS, emitter on a circular orbit
at β up to 0.999 — the root function's derivative degenerates to −(1−β_radial) when the
emitter runs at the observer, yet iterations stay at 3.0 per frame (mean = p99 = max) at
every β: the frame-to-frame seed is too good for the flat slope to matter. The cost
premise of §2's gather is robust in flat space. Not measured, stated as derivation: at a
lensing fold (an image pair born as a source crosses a caustic) two roots merge with
F′ = 0 and the newborn image has no seed; nothing in the design finds the second root.
That is a behaviour gap, not a cost gap.

## The ranked attacks (the lens's order 1–6, re-ranked by player visibility)

1. **Bit-identity at relativistic speed heterogeneity (premise 4)** — attacked, survived;
   numbers above. Rung that should have caught a failure: r5/B8; it now has the scene
   class. Residual exposure named (handout of a fast body, cross-doll simultaneity).
2. **The design text is falsified by the repo itself (premise 2).** representation.md §1
   still presents Binet cells with Minsky's two-addition rotation as "the primary
   in-cell solution"; law.md §1 replaced it with `space-darwin16-v1` after the in-band
   map's turning-point slope error. Any builder reading the design builds a killed
   configuration. Rung: r1 (it caught it — the builder's own test, not a rung). Fix:
   rewrite §1 to the live law; cost: an hour of text.
3. **No gate judges what the player sees (premise 5).** r6 judges iterations and samples
   (cost); B16 judges one doll's deflection against a boosted oracle; nothing judges the
   composed image — multi-doll deflection composition along one light path, colours under
   composed redshift × aberration, image birth at caustics. Player-visible exactly at the
   game's selling points (fly at 0.99c past a binary). Rung: none. Proposed: an oracle
   image gate (float64 geodesic-integrated photons vs the gather, positions and colours,
   N seeds, weak-field and one compact scene).
4. **The two-body doll's ν claim is exact for the pair, silent about members (premise
   1).** At 1PN the EOB map is exactly Schwarzschild for the relative motion with ν only
   in the energy map (true; r3 v3 and B11 confirm) — but the doll also supplies the
   field members feel, and the 1PN tidal field of a moving pair carries
   velocity-dependent ν terms that a Schwarzschild tide in M = m₁+m₂ does not. B11
   judges the pair's precession and periods, never a member inside a ν > 0 doll.
   Player-visible near compact binaries (the game has them); second-order elsewhere.
   Rung: none; extend B11 or the B14 scene with one member-in-a-pair case.
5. **Premise 3's load-bearing evidence is single-checked.** The re-anchor rule that
   keeps jet-updated cycles bounded (`√(floor/C)`, run 20261006-0346-redteam-df81) is
   recorded in law.md as "graded gold by one checker; the second never ran" — under
   arch-v3 §3 gold needs two. Not a new attack; a verification hole on the premise that
   kicks plus derivatives do not compound.
6. **Costs ≈ 0 (premise 6): standing risks, cited not re-derived.** H_live (distinctions
   per game-second) unmeasured (HANDOFF); the light cone keeps growing (Julien). My
   rebuild measurement above removes one small unknown (fast-body churn).

## Predictions

`predictions.md` was written before the run. P1 (identity holds) held on all variants —
the premise survives. P2 partially wrong: rebuilds do occur (2–3) but are not
interceptor-driven, and sparse is 30× faster, not slower; the p99 exposure did not
appear. P3 held: relativistic contacts happened (+14/+17, including a near-c head-on
pair). Held-out honestly: I predicted the p99 exposure would be visible at this scale;
it was not.

## What would make it wrong

The falsifier scene is one battle geometry, one seed, 100 bodies, a flat-ish frame (the
extent rule dominates the orbit rule, as in shipped stress scenes), and interceptors
inside the extent rule the whole run. A failure needing a handoff, a container, threads
≠ 1, or GPU/Metal paths would not show here. The ν-tide and caustic arguments are
derivations, not measurements; the caustic one in particular should be measured before
the view is built (it shapes the gather's root-finder, not just its cost).

## Cost of adopting

Nothing to adopt from the surviving premise beyond adding the flyby scene class to the
identity ladder (the test file is in this folder, ~60 lines net). The doc fixes (§1
rewrite, B11/B14 extension, the view gate proposal) are integrator decisions.

## Fit with PRINCIPLES

"Gates are frozen before the first run and never weakened after … Gates judge a
representation" — B8's evidence base did not cover the player's headline action; this
run adds it before any freeze leans on it. "A test that cannot fail is a control" — the
epoch-shift plant fires on every variant. "Measure before claiming" — the p99 fear I
came with was measured away in the good direction.

## The lens

A premise red-team overweighted exotic relatives (near-c flybys) and the falsifier
confirming B8 is the least surprising result here; the durable findings are the stale
§1 text, the missing view gate, and the single-checked re-anchor gold — none of which
needed a run. The blind spot the lens warns about cut both ways: the genuinely
player-visible failures (what the composed view shows near a binary) are exactly the
ones with no code to attack yet.
