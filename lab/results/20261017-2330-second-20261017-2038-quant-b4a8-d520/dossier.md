# Dossier — 20261017-2330-second-20261017-2038-quant-b4a8-d520 (second author on 20261017-2038-quant-b4a8)

## Claim

The checker's named experiment, done, **refutes the last comb premise the calendar page held open
(od 4)**: on the shipped chained clock a quantized-period belt does **not** sit on the combing side —
shared exact (a, e) never yields shared ticks, because the step is a function of *position*
(`y = U_P(x) + c`, the secondaries' potential at the body, `step.rs:611-618`, `704-716` — not of
the orbit constants) — and the step spread the train's shear was attributed to is **draw-invariant
(8–10% on every draw, [2,3) AU through [2.999,3), quantized or not)**, so the genesis train is one
law-level object: **C50 = 40–58× at birth on every population (the shipped wide draw itself: 58.2× —
f82a/3294's "57×" is not a tighter-draw artifact), shearing at ~2.7% of the step per fire to
C50 ≈ 2× by ~8 fires, with no exact-tick battalions anywhere (largest = 1 body, all arms, all
generations, N up to 11,700)** — the calendar axis at belt scale is a decaying genesis wave common to
every clock population, not a comb, and the only lever on it is the genesis stagger (f82a), which
decouples the phase-lock at birth instead of widening the draw or quantizing periods.

## Bottleneck

Board question 1 (bodies 28 → 10⁹) via the calendar page's store-class decision. Not a speedup: it
closes the page's open directions 2's checker question ("the general rule — train lifetime vs the
population's step spread — is unmeasured on one instrument") and direction 4 (the compact-store
quantized-period belt, "the one population where the chained clock could still comb — unmeasured"),
and deletes a wrong number the page now carries: the "[4.3, 5.9]×10⁹ ticks" step spread (37%) that
b4a8's record and both checkers repeated — an artifact of the census's `2^ilog2` step labels; the
measured spread on the same population is min 5.2995×10⁹, max 5.9021×10⁹ (10.5% min–max, 7.8% p1–p99).

## Evidence

All numbers from shipped code (`crates/universe`) + `work/patch.diff` (a pure refactor: it extracts
the belt draw into `scenario::{BeltDraw, belt_ship}` and adds `plane_belt`; the control line proves
`plane_belt(SHIPPED) ≡ plane_extra` bit-identically at N = 3,000). Linux x86, release. One census per
fire generation g = 0..8 (settle to first_max + g·1.03·step_max), 8 arms, seed 1. Per-body fires at
the census (m_med) = g + 0.99, i.e. **the belt fires about once per "generation"** — b4a8's "~18
fires" (whole-universe kicks ÷ belt bodies) stays corrected at every horizon. Full raw:
`raw-train.txt` (regen), endpoints in `raw-endpoints.txt`, the w2999 full curve in
`raw-w2999-full.txt`; rule table from `rule.py`.

Command per arm (≤ 60 s each; the whole sweep = `regen.sh`, ~8 min):
```
cd crates/universe && cargo run --release --example train shipped   # 51 s, N = 12,000
cd crates/universe && cargo run --release --example train w2999     # 53 s
```

| Arm (draw, N belt) | σ_step p1–p99 | C50 g=0 | C50 g=8 | largest battalion (all g) | kicks |
|---|---|---|---|---|---|
| shipped [2,3) AU, 11,700 | 7.8% | **58.2×** | 2.2× | 1 | 503,014 |
| w2000 [2,3), 2,700 | 7.9% | 57.9× | 2.1× | 1 | 421,885 |
| w2400 [2.4,3), 2,700 | 8.4% | 49.4× | 2.1× | 1 | 421,848 |
| w2800 [2.8,3), 2,700 | 9.2% | 43.1× | 2.0× | 1 | 421,987 |
| w2950 [2.95,3), 2,700 | 9.9% | 41.4× | 2.1× | 1 | 422,280 |
| w2999 [2.999,3), 2,700 | 10.1% | 40.8× | 2.2× | 1 | 422,286 |
| q32e16 (32 a-classes × 16 e-levels), 2,700 | 8.0% | 55.8× | 2.1× | 1 | 421,925 |
| q1024e16 (1024 × 16), 2,700 | 8.3% | 54.8× | 2.0× | 1 | 421,804 |


The rule table (all arms, full curves; `rule.py` over `raw-train.txt`):

| arm | σ p1–p99 | C50 g=0 | g=1 | g=2 | g=4 | g=8 | wave slope (% of step/fire) | L (C50≥2) | largest battalion |
|---|---|---|---|---|---|---|---|---|---|
| shipped | 7.80% | 58.2 | 14.6 | 9.8 | 5.9 | 2.2 | 2.81% | 8 | 1 |
| w2000 | 7.85% | 57.9 | 14.5 | 9.7 | 5.8 | 2.1 | 2.88% | 8 | 1 |
| w2400 | 8.41% | 49.4 | 12.4 | 8.3 | 5.0 | 2.1 | 2.83% | 8 | 1 |
| w2800 | 9.18% | 43.1 | 10.8 | 7.2 | 4.4 | 2.0 | 2.85% | 8 | 1 |
| w2950 | 9.86% | 41.4 | 10.4 | 6.9 | 4.2 | 2.1 | 2.66% | 8 | 1 |
| w2999 | 10.09% | 40.8 | 10.3 | 6.8 | 4.1 | 2.2 | 2.61% | 8 | 1 |
| q32e16 | 8.05% | 55.8 | 14.0 | 9.4 | 5.6 | 2.1 | 2.95% | 8 | 1 |
| q1024e16 | 8.34% | 54.8 | 13.7 | 9.2 | 5.5 | 2.0 | 3.03% | 8 | 1 |

Every arm decays on the same law: wave width grows 2.6–3.0% of the median step per fire
(median step 5.71×10⁹ ticks ≈ 28,140 game-s ≈ 3294's 28,141.5 s belt interval), C50 falls
below 2× just past g = 8 everywhere, and the shipped draw's C50 curve (58.2, 14.6, 9.8,
7.3, 5.9, 4.9, 4.2, 3.0, 2.2) brackets every other arm within ~1.5× at each generation.
Cross-check to b4a8's record: the shipped arm's g = 3 dues max = **17** — b4a8's settled
S1 max, to the digit (its mean 1.64 was over bins touched; over the step span the same
census reads μ = 0.69, p99 = 5).

Controls, every arm, both ends: planets+moon 4/4 and locals 300/300 exactly on the `aligned` grid;
refused 0; the refactor control IDENTICAL; the shipped arm's genesis census equals b4a8's record to
the digit (firsts in 891 frames, 11,700 distinct steps and first-kick ticks). **Reproduced
bit-identically twice** (the live run and `regen.sh`): every arm's kick, boundary, handoff, lost
and refused count equal (shipped 503,014 kicks; w-arms 421,804–422,286; q-arms 421,804/421,925),
every census line identical.

Mechanism, from shipped code: `project` sets `p_t = U_P − H_D` (`step.rs:611-618`), so the clock's
argument is `y = H_D + p_t + c = U_P(x) + c` — the *planets'* potential at the body's position — and
`full = ticks(time(y, ds))` (`step.rs:704-705`). Two bodies with identical (a, e) at different angles
have different y, hence different steps: the q-arms make this measurement — 32 shared (a, e) classes
carrying 2,700 bodies still show **2,700 distinct steps** (≤ 224 possible if steps were orbit-derived)
and no battalion at any generation. The spread across angles (drawn uniformly, identically in every
arm) is the 8–10% the sweep sees; the a-width of the draw moves it barely at all.

## Predictions

`predictions.md` written before any sweep arm ran (the smoke w2999 ran after, on the same committed
instrument). P2 **held** (58.2× against "within a factor 2 of 57×" — and it resolves that 57× as the
*shipped* draw's own genesis train). P5 **held** (refactor control identical; grid controls pass;
genesis census = b4a8's to the digit). P1 **wrong in mechanism**: no Kepler a^1.5 — the a-width is
not the step-spread dial at all; the "floor" is the whole spread (draw-invariant 8–10%). P3 **refuted
in form**: lifetime is not W0/σ — it is spread-independent (~8 fires to C50 2× on every draw); the
wave shears at a fixed ~2.7%/fire. P4 **refuted in its combing half, as its own alternative clause
allowed**: quantized classes never battalion (no combing side to sit on); they ride the same decaying
wave as every continuous draw. Direction 4 closes either way, as pre-registered.

## What would make it wrong, cost, fit

- A *law* change that derives `full` from orbit constants ((a, e) classes) would re-open od 4 by
  construction; on the shipped law the step's position dependence is anchored in code and measured
  (q-arms' 2,700 distinct steps).
- The genesis stagger (f82a) remains the one measured lever on the wave (57×→1.0×); my arms do not
  fly it — nothing here contradicts it, and the stagger's question moves from "belt-scale lever?" to
  "the only lever".
- Stirred/driven belts and the burn's interaction are unflown here (coast only); 8ffc's two-comb
  (boundary combs) is a different comb than this page's kick comb and untouched.
- Cost of adopting: none in code; the calendar page's od 4 closes and its step-spread number is
  corrected (10.5% min–max, not 37%). Fit: PRINCIPLES "a failed experiment kills that configuration,
  never the method" (the killed configuration is the quantized-period comb premise, not the compact
  store); "The simulation decides" (the wave is the belt's own U_P geography, present on every draw).

## The lens

The second-author lens ran the checker's experiment exactly and read the sweep flatness as the
result: the dial that was supposed to move the phenomenon does not move it. Missed by construction:
no wall-clock cost per frame of the wave at 10⁹ (the frame's dues are counted, not priced); the
middle generations g=1..7 were kept for w2999 and verified by regen for all arms, but the live
monitoring run lost them to a tee path error before regen re-ran — reported, not buried.

Wall time: 0.06 seconds
