# Dossier — 20261017-2038-quant-b4a8 (quant lens)

## Claim

The calendar page's falsifier resolves **against** the page: the shipped belt (the 10⁹ bulk:
doll-0 ships) runs the **chained clock**, not `aligned` — 100% of 11,700 belt bodies, next-due
≡ carried per-body state (every body's step changed after ~18 fires; the id-prediction is off
by p50 0.67 steps), so **no id-derived fixed class exists to lay a class-major store against**
— but the page's feared comb is absent on this law (largest shared next tick = 1 body; dues per
frame max/mean 10×): the comb is real only where `aligned` runs (planets, moon, doll locals:
100% grid-locked, same-step bodies on identical ticks).

## Bottleneck

Board question 1 (bodies: 28 → 10⁹) via the calendar page's store-class decision (its open
directions 1 and 3). Expected gain: not a speedup — it deletes the page's form (d) premise
("the class of a body is id-derived and fixed... the bulk never re-keys") and re-aims the
compact-store design: the calendar is a per-body next-due word that moves at every fire
(~5.9 h game per fire at the belt), not a static class; and it retires the stagger as a
belt-scale lever (the belt self-staggers; measured, no battalions).

## Evidence

All numbers from shipped code (`crates/universe`), Linux x86, release, warm build, single
run 21 s; reproduced bit-identically twice (kick count 206,554 both).

Command (≤ 60 s):
```
cd crates/universe && cargo run --release --example calendar
```
Scene: `plane_extra(Config::default(), seed 1, Sparse, threads 1, members 16, extra 12,000)`
— the merged N-ladder's own population (300 locals + 11,700 belt), settle to 3 max steps
(2.07×10¹⁰ ticks ≈ 4.4 game-days). Frame = 338,375 ticks (60 FPS at rtf 100).

| Measurement | Number |
|---|---|
| Belt bodies on the clock law (`ext`, `kick_clock` chain) | 11,700/11,700 = 100% |
| Aligned control (3 planets + moon + 300 locals): dues ≡ 0 or S/2 mod S | 4/4 and 300/300 at genesis, 300/300 after settle |
| Belt dues on any grid {0, S/2} after settle | 0/11,700 |
| Distinct first-kick ticks at genesis | 11,700 (largest "battalion" = 1 body) |
| Distinct steps at genesis | 11,700 (all ≈ 2³² ticks ≈ 5.9 h; per-body integers, not powers of two) |
| Bodies whose step changed after ~18 fires | 11,700/11,700 (p50 |Δstep|/step 2.6×10⁻⁴) |
| Phase error vs id-prediction (first + m·step) after ~18 fires | p50 2.86×10⁹ ticks ≈ 0.67 steps; p99 2.94×10⁹ |
| Belt dues per frame | mean 1.64, p99 9 (5×), p99.9 11, max 17 (10×) — Poisson-consistent, no comb |
| Events | kicks 206,554, boundaries 194,155, handoffs 5, lost 8, refused 0 |

Code anchors: the law split is `step.rs:554` (`plan_interval_inner` → `on_clock()` at
`step.rs:601`: doll-0 ships → `plan_clock`), the chain is `kick_clock` at `step.rs:715-718`
(`insert(plan, Item{t: t + full})`, `full` a per-body whole-tick count from the body's energy
with a fractional carry, `ext.rs:98` — no absolute grid on this path); `aligned`
(`step.rs:107`) serves the planets, moons and doll locals only.

## Predictions

`predictions.md` written before the run. P1 (law split) **held** (100% clock; controls
on-grid). P4 (no grid, no closed form) **held** (0/11,700 on-grid; step changes everywhere).
P2 and P3 (genesis train ≥ 10% battalions; standing train) **failed**: the ladder belt has
**no** battalions — 11,700 distinct first-kick ticks, largest shared next tick 1 body. The
f82a "57× standing train" the calendar page inherits is not this population: on the shipped
chained clock the belt self-staggers (per-body steps spread fires by construction). The comb
the page's K-dial sizes lives only on the `aligned` class (measured exactly grid-locked
there). Reported as held-out failures, not buried.

## What would make it wrong

- A different belt (the compact store's "phase-locked belt", quantized orbits, shared exact
  periods) could re-create battalions on the clock chain: shared (anchor, full) ⇒ shared
  ticks. My census covers the shipped ladder belt only, not that population.
- `settle`-driven censuses could differ from frame-driven ones (deadline ordering). Mitigated:
  genesis census is pre-settle; controls pass on both sides; refused = 0.
- The chain could be re-anchored somewhere I did not drive (handoffs: only 5 in this window).
  Handoffs/decisions are the hot set's own path and stay carried state by construction.

## Cost of adopting, fit with PRINCIPLES

Adoption is a design consequence, not code: the compact store's calendar axis must carry a
per-body next-due word (~step-span bits, ~33-40) that is rewritten at every fire — it cannot
be a static hash class; conversely no stagger is needed at belt scale (the comb is an
`aligned`-population artifact). Fits "Compute only surprises" and "The simulation decides;
heuristics schedule": the belt's own dynamics (per-body energy → per-body step) are the
stagger. Fits "a failed experiment kills that configuration, never the method": what dies is
the calendar page's `aligned`-only reading and its fixed-class store premise, not the
class-major store itself (which now keys on a carried next-due word).

## The lens

The quant lens priced the tails (per-frame dues, battalions, controls on both sides) but read
the law from the doc comment first — `aligned` — and nearly measured the wrong population;
the census-by-kind/doll split (who runs which law) is what made the refutation clean. Missed:
wall-clock cost per fire event (not needed for the claim); the fired-vs-unfired kick split
(not exposed by the shipped API).
