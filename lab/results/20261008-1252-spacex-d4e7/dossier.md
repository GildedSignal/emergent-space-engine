# Dossier: H_live of a secular belt — a step, not a rate; the wall is the generator's

Run: `20261008-1252-spacex-d4e7` (lens: SpaceX). All numbers below regenerate from the
commands in Evidence, on this machine, each run ≤ 60 s.

## Claim

Under the plane's own kind of perturbation (orbit-averaged secular kicks from a Jupiter),
a belt's live distinguishing information is **not a rate but a step**: the naive store
scars to its full ~84 bits/body within ~100 orbits and then stays flat to 10⁵ orbits, so
10⁹ bodies hit the 8 GB wall once, immediately, by amplitude-vs-quantum — while a
closed-form secular generator holds the same belt at ~0 bits growth, and the synthetic
kick model (`Pop::kick` magnitudes) mispredicts the level 1.8× low *and* the shape
(unbounded growth vs flat).

## Bottleneck

HANDOFF risk #2 / board "fitting 10⁹ in 8 GB … decided by distinctions created per
game-second" — the number that decides whether a billion bodies fit, previously "not
measured yet". This run measures it for the secular regime (the bulk of a smooth belt's
dynamics), in the law's own quanta and the shipped codec. Expected gain: it deletes the
naive scar store (84 bits/body → ~0) by naming the generator the belt already implies;
it re-sizes the b-h-live build's budget; and it kills synthetic-kick-model budgeting.

## Evidence

Scene: belt of m bodies, Darwin p uniform [2048, 3072) Q16, e₀ Rayleigh σ=0.04, ϖ₀
uniform, birth order p-sorted (B18b's banded belt); one exterior perturber a_J=5120,
μ=9.55e-4, e_J=0.048. Times in orbits of the inner edge. Scar columns δE (Q48), δL
(Q32), δϖ (u32) — the law's own `Key::darwin` quanta — encoded by the shipped
`shipmem` block codec in 256-member blocks. δt_p excluded: under secular dynamics a is
constant, so periapsis times advance as an exact affine program (0 bits).

Arms — A: scars vs birth (no generator); B: scars vs an RK4 Laplace–Lagrange generator
at one shared step per reference orbit (the plane's averaged cadence); C: the synthetic
kick model (random walk, ±2¹⁰ quanta/orbit, `Pop::kick` magnitudes). Truth for A/B:
closed-form restricted Laplace–Lagrange (verified: forced e = (b₂/b₁)e_J =
0.0235–0.0342 across the band, cross-checked by independent scipy quadrature to 4
digits; precession g = 1.0–3.8e-3 rad/orbit, cycle 6.3e3–1.7e3 orbits).

bits/body (total, δE+δL+δϖ) and the GB it makes at 10⁹ bodies:

| T (orbits) | A naive | B RK4 gen | C kick model |
|---|---|---|---|
| 0 (control) | 0.13 GB (~0) | — | — |
| 100 | 82.0 bits / 9.54 GB | 0.9 / 0.10 GB | 46.3 / 5.39 GB |
| 1 000 | 82.2 / 9.57 | 2.1 / 0.25 | 51.5 / 6.00 |
| 10 000 | 83.7 / 9.74 | 6.6 / 0.77 | 57.0 / 6.63 |
| 100 000 | 83.9 / 9.77 | 13.8 / 1.61 | 61.7 / 7.18 |

Column detail at T=1e5 (arm A): E 30.5, L 20.2, ϖ 33.2. Birth base in block form for
context: E 31.2 + L 26.0 + ϖ 32.2 ≈ 89 bits (the gold's program form is 0.126
bits/body, unmerged). Controls: T=0 encodes to 0.03/0.03/1.09 bits (the 1.09 is
float→u32 angle round-trip noise); seed 2 reproduces every number to ±0.02 GB; m=2¹⁸
(arm A) gives 9.64 GB at 1e5 — bits/body are m-independent, so block-span shear is not
the driver; the birth-phase-dependent oscillation is.

Reproduce (each ≤ 60 s, release, 3 MB RSS):

```
cargo build --release -p emergent-shipmem --example hlive
$CARGO_TARGET_DIR/release/examples/hlive 4096 0x5eed1234          # main table, ~9 s
$CARGO_TARGET_DIR/release/examples/hlive 4096 99                  # seed control
$CARGO_TARGET_DIR/release/examples/hlive 262144 0x5eed1234 A      # size control, ~1 s
```

Instrument: `crates/shipmem/examples/hlive.rs` (this run's patch); outputs saved in
`work/hlive-*.txt`.

## Predictions (predictions.md, written before the run)

- **P1 half-held.** Flatness held exactly (9.74 → 9.77 GB from 1e4 → 1e5 orbits). The
  level and timescale did not: E measured 30 bits vs predicted 38–48, and the step
  completed by T≈100, not 1e4 — both trace to one wrong constant, the e_F control
  (b₂/b₁ is 0.49–0.71 at α ∈ [0.4, 0.6], not the ~1.45 I guessed; the integrals
  themselves verified two ways). The control window [0.03, 0.15] was missed low
  (0.0235); disclosed, physics verified.
- **P2 half-held.** L 19–20 vs predicted 25–33 (same wrong constant); ϖ saturates ≤ 32+
  zigzag, held.
- **P3 falsified, and the failure is the second result.** The per-orbit RK4 generator
  leaves 13.8 bits/body at 1e5 orbits (prediction: ≤ 2). Cause, verified by magnitude:
  RK4 phase error accumulates linearly, T·(g·dt)⁵/120 ≈ 9e-8 rad ≈ 62 ϖ-quanta ≈ 6 bits,
  measured 7.7. An *integrator*-style generator leaks; a *compiled-cycle* generator (the
  law's own pattern — compile once from constants, then additions only, as the tube's
  cycle memo already does) leaks nothing by construction. Cadence is a 32× lever per
  halving.
- **P4 held.** The kick model reads 46 bits at T=100 (vs the truth's 82) and grows
  without bound (62 at 1e5, ≈ log of a random walk): wrong low on level, wrong on shape.
- **P5 held.** Arm A total 84 bits = 9.8 GB at 10⁹ (predicted 80–110), breaking 8 GB but
  flat in T: the wall is set by quantum-vs-amplitude, not by a rate. Arm B's "≤ 2 bits"
  half failed per P3 above.

## What would make it wrong

- The truth is single-planet, planar, linear secular theory. Real belts add mean-motion
  resonance pumping (r4 v3: first-order kicks over-pump e ~2× near resonance), secular
  resonances, encounters and their scars, and chaos. Those are *not* derivable from a
  smooth generator and are the true H_live; this run bounds only the smooth bulk. If
  resonance/encounter residue dominates at belt scale, the "step then flat" claim holds
  only for the secular component — the named next experiment measures the residue.
- Orbits, not game-seconds: the mapping to the plane's RTF is B18b's pending belt rung.
- The block codec is the shipped store; the (unmerged) gold program form would
  reabsorb part of arm A's ϖ column, moving 84 down somewhat — the direction of every
  claim is unchanged.
- One perturber's g and zf are doll constants here; a real system's multi-frequency
  secular response is still closed-form (eigenmodes) but the generator's exactness in
  *integer* law arithmetic is unproven — my float generator's 1e-15 floor is not the
  law's floor.

## Cost of adoption, and fit with PRINCIPLES

Adoption = one change to the b-h-live build: the belt store's base is the birth program
plus a **compiled secular cycle per doll** (the perturbers' g(a), zf held as doll
constants; each body's (E, L, ϖ)(T) re-derived on read, ~20 flops, or folded into the
tube's existing cycle additions). No scar layer for the secular bulk; the naive
84-bit/body store is deleted. Cost: the generator must be law-exact (integers) and
red-teamed — my own sign bug (found, fixed, disclosed) silently produced a
worse-than-nothing generator; the check is the T=0 control plus cross-generator diffs.

- "Compute only surprises … Nothing is evolved that can be derived when looked at" (#3):
  the secular response is exactly derivable-by-looking; evolving it into scars is the
  compute-not-done violated in memory.
- "Store the generator, not the generated" (#6): the secular cycle is the generator the
  belt already has.
- "A fix signals the wrong representation" (#19): the wall was never a cadence problem;
  it was the absence of the generator native to the dynamics.

## The lens

SpaceX's delete-first found the deletable 84 bits; its named blind spot bit once: the
wrong-sign generator (a "deleted certificate" analogue) passed silently until the T=0
control caught it — controls on both sides are what make deletion safe. What the lens
may still have missed: the idiot index here is infinite (0 bits of physical information
vs 84 stored), and such ratios tempt one to stop at the secular floor; the game's real
memory question lives in the irreducible residue (resonances, encounters), which this
lens under-weights because no part of it can be deleted.

## Grade suggestion

Silver. Real, reproduced (two seeds, two sizes, every number regenerable in ≤ 60 s),
predictions pre-registered with one falsified for a verified cause. One named
experiment from gold: measure the *residue* — the bits a correct compiled secular
generator cannot re-derive on a belt with resonance overlap and real encounters — which
is the number the b-h-live build and B18 need.
