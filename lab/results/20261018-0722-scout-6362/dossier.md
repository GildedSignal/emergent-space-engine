# Dossier — 20261018-0722-scout-6362

## Claim

The contact skip's open design question ("a real fix needs the contact root |d| = reach,
irrational normal: an integer-law design question", 1648) has a one-step answer: the contact
root's normal decomposes on the lattice's own integer data as **n·R = P − s·w** with P
rational, **w·P = 0 exactly in integer arithmetic**, and s = √D/|w|² the only irrational
(D integer, D ≥ 0 iff hit) — so the exact root-normal impulse is the closed form
**Δw = 2√D·P/R² − 2D·w/(|w|²R²)**, needing **one integer square root and one divide per
component**, no carried irrational state; verified in float/integer at 99.99+% impulse
recovery (worst 99.4452% over 200,000 adversarial random integer pairs), angle ≤ 2.2×10⁻³
rad, and zero fires on misses — against the shipped rule's measured **0%** on every
crossed-in-bin arm.

## Bottleneck

Not a scoreboard row: the board's own units anchor. Bottleneck 5 sizes the position quantum
by "the worst case, a near-c 50 cm missile"; 8144 measured that this object **cannot
collide at all** (v\* = 3.4×10⁻² c for a 0.5 m vs 50 m pair: "at its design speed it never
collides") — the representation's worst case is the one body the contact law ignores.
Gain: not compute (the fix touches 0.1–2.7% of detected contacts at fleet speeds, 1648's
measured skip fractions) — it deletes the bin-convention hole (a correctness class) and
restores the design's anchor object, at ~one isqrt + two divides per crossing. What it lets
us delete: the "integer-law design question" itself — the last open half of contact-speed
open direction 1.

## Evidence (all numbers regenerate: `python3 contact_fix.py`, 1.1 s, table.txt)

Instrument: `contact_fix.py` — standalone, integer lattice data in the shipped constants'
class (R = 2048 quanta reach [1648's gas], c = 2²⁰ quanta/chronon [8144's Q], k = 20
fractional bits, ticks/chronon = 2²⁰). Oracle: reflection of the relative velocity about
the exact float root normal; rule: the same reflection from the isqrt-quantized closed form
(operator shared, so the SR form of v1 cancels — the toy measures normal/timing recovery).

Grid arms (b/R ∈ {0, ¼, ½, 39/40}, ρ = |w|/R ∈ {3, 30, 300, 512}, β ≤ 1.0, τ\* = ½
mid-bin; `table.txt`):

| quantity | result |
|---|---|
| shipped recovery (the skip, 8144 reproduced in-toy) | **0%** on all 16 arms |
| integer-rule recovery | 99.9855–100.0007% (worst = predicted worst case b = 39R/40, ρ = 3) |
| impulse angle error | ≤ 1.10×10⁻⁴ rad |
| w·P_num = 0, integer-exact | True on every arm **and every one of 200,000 random pairs** (asserted) |
| D ≥ 0 iff crossing | True everywhere; miss control b = 1.5R never fires |
| τ− root tick (ceil at 2²⁰ sub-ticks) | position error ≤ 1.87 quanta vs bin-end application's up to 1.05×10⁶ quanta (R·ρ): the impulse is identical; only the application tick's position offset differs |

Random sweep (n = 200,000 arbitrary integer (d, w): non-axis-aligned, odd values, both
senses, 2,207 crossed-in-bin, 143,248 misses, 9,829 already-inside): recovery min
**99.4452%** / p1 99.9920% / median 100.0000%; angle max 2.177×10⁻³ rad, p99 1.109×10⁻⁴;
**zero** fires on the 143,248 misses.

Overflow (arithmetic, worst shipped magnitudes |w| = 9.4×10⁵ quanta/chronon, d = 10⁶
quanta): max intermediate ~2^120 — u128 carries 7 bits headroom at k = 20 (k = 16 buys
16 bits); real detection-window d ≲ R + |w| gives ~2^114.

## Predictions

`predictions.md`, written before the decisive run. **All four held:** P1 identity exact in
integers everywhere incl. miss; P2 shipped 0% on every crossing arm; P3 integer recovery
≥ 99% with angle ≤ 5×10⁻³ rad on every arm, worst case exactly where predicted (grazing ×
ρ = 3); P4 bin-end position cost ~R·ρ quanta (measured 1.05×10⁶ at ρ = 512) against the
root-tick's ≤ 1.9 — the schedule choice, not the rule, owns the position offset. No kill
criterion fired. Instrument bugs found and fixed during the run (a 2²⁰ scaling slip and a
splice) were corrected before any number was recorded; `table.txt` is the final run only.

## What would make it wrong

1. **The shipped v1 operator.** The toy shares the reflection operator between oracle and
   rule, so what is proven is the **normal and TOI** recovery. If `Law::RelativisticV1`'s
   Householder normal mixes 4-momentum terms (f50d read N = (d·P_s, E_tot·d)), the closed
   form must be re-derived in that algebra; the spatial decomposition (n·R = P − s·w,
   w·P = 0) still carries, but the "one isqrt" claim must be re-verified on the shipped
   operator. This is the named adoption gate.
2. **The detection window.** I assume the crossed-in-bin class is detected with the bin's
   start-state (d, w) available (the law solves the detection quadratic — 8144). If
   detection carries only the bin-end state, P must be formed from the back-projected
   integers (same algebra, sign flip; untested here).
3. **Multi-pair bins** (1648 measured ≤ 1.6% contamination): the fix inherits the shipped
   batch convention; near-simultaneous roots need ordering (event-driven MD's known failure
   mode). Untested in the toy (single pair).

Cost of adoption: one branch at the receding gate (resolve when D ≥ 0 instead of skip — the
gate keeps its other job, stopping second hits), one u128 isqrt helper. Digest moves (a law
change); r5's frozen scenes are exchanging-regime by construction (8144), so the rung needs
the crossed-in-bin scene 1648 named — the criterion already stands ("a crossed-in-bin
head-on pair at closing 0.9c must exchange the exact v1 impulse; the shipped skip is the
negative control").

Fit with PRINCIPLES: #30 "what really matters is navigation, knowledge and dynamics those
need to be perfect" — a near-c missile that passes through everything is a dynamics hole in
the design's own anchor object; #16 "physics loves e while we love 2" — one isqrt, shifts,
one divide; #2 "error type over error size" — the residue is a bounded sub-tick offset,
not compounding; #19 — the rule is the event at its own time, not a finer bin (no
sub-chronon stepping, no threshold tuning).

Prior art, fit-ranked (scout lens; **UNVERIFIED at the source** — this run had no network
access; all from the author's training, to be source-checked before freeze): (1)
**event-driven molecular dynamics** (Alder & Wainwright 1959; Lubachevsky's parallel
event-driven scheme; Rapaport's) — hard spheres at arbitrary speeds, collisions scheduled
at the exact time-of-impact: same structure, and the practitioners paid for being wrong
about ordering; (2) **game-physics continuous collision detection** (Box2D `b2TimeOfImpact`,
Bullet's CCD sweeps) — the same quadratic resolved at the root, shipped in millions of
games; (3) **Shewchuk's robust predicates** — exact integer-coordinate geometry; here the
needed identity (w·P_num = 0) is algebraic, so no adaptive arithmetic is required.
Rejected: sub-chronon refinement (pays everywhere for a 0.1–2.7% class — PRINCIPLES 1,
compute not done) and doing nothing (fleet speeds are safe, but the missile is the units
design's own worst case).

## The lens

The scout lens searched for a mechanism elsewhere and found an old one (event-driven MD),
but it could not verify sources at the network layer this run, and it measured the fix in
a toy rather than on the shipped `Chronon` stepper (the lattice crate's reference stepper
would host the real gate: build risk on this box within the window). It also chose a
correctness-class question over the composed CPU/memory rows — those are engineering-bound
(Carlson port, split-16 legality flight, store wiring) and a scout hour adds less there;
the checker may disagree with that weighting. The page's own held-out domain (f50d's pump,
r5's scenes) was not re-flown.
