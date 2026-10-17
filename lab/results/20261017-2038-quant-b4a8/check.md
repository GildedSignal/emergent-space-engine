Grade: silver

**Abstract.** The calendar page's falsifier resolves against its premise, reproduced: the
bulk (11,700/11,700 doll-0 ships; held at seeds 2–3 and 10× N) runs the chained clock, not
`aligned` — next-due is carried per-body state (0/11,700 on-grid; every step changed in 3
fires, not ~18 — the 18 counted the locals' kicks; id-prediction off ~0.7 steps), so no
id-derived fixed class exists for a class-major store: the calendar axis is a ~33–40-bit
next-due word rewritten per fire (~5.9 h game). Gain: deletes 25ce's form-(d) premise;
adoption is design-only. Not gold: the comb half overstates — the settled tail is a
decaying train (dues confined to 41% of the span; max 17 vs Poisson ~9), and the comb is
not aligned-only: 8ffc/f82a measured 57× genesis trains on this same law.

## Reproduction

- `git apply work/patch.diff`, `cargo run --release --example calendar`: **bit-identical**
  to `regen.log` (third independent run incl. the runner's): kicks 206,554, boundaries
  194,155, every census line equal. regen.sh ≤ 60 s as claimed (21 s run + warm build).
- All five code anchors verified in shipped code: `step.rs:554` (`plan_interval_inner` →
  `on_clock()`), `step.rs:601-603` (doll 0, Ship|Player), `step.rs:715-718` (`rec.step =
  full`; next kick at `t + full`; boundary `t + full/2`), `ext.rs:98-103` (`ticks` with
  `dt_carry`, at least one tick — no absolute grid on this path), `step.rs:107`
  (`aligned`, the non-clock path). `key_of` returns the body's earliest plan item — a fair
  "next due".
- `predictions.md` predates the instrument and dossier (mtimes 6 m vs 1 m; log order
  consistent). P1 (law split) and P4 (no grid, no id-closed-form) held. P2/P3 (battalions,
  standing train) failed and are reported as failures, not buried. **P5 (burst ≥ 50×) also
  failed (measured 10×)** — the number is in the table but its prediction outcome is never
  labelled.

## Adversarial cases (mine; the author's census instrument plus a per-body fires counter and a support/density readout, env-driven seeds/N/order; tree restored after)

1. **Seeds 2, 3** (same config): 100% clock, largest battalion 1 at genesis and after 3
   fires, 0/11,700 on-grid, 11,700/11,700 steps changed, 0 chain-predictable, dues mean
   1.62/max 15. All claims hold.
2. **One decade up in N** (extra 120,000, seed 1 — outside the author's range): belt
   119,700, 100% clock; genesis distinct firsts 119,663, **largest battalion 2** (37
   collisions ≈ birthday-expected ~24 — no comb); after 3 fires all steps changed, 0
   chain-predictable, largest battalion 2, dues mean 16.62/max 83 (5×). The core holds at
   10× N; "largest shared next tick = 1" is N-dependent (birthday), not a law constant.
3. **Belt fires**: min = p50 = max = **3** fires per belt body. The dossier's "~18 fires"
   is 206,554 (whole-universe kicks, locals-dominated) ÷ 11,700 — a misattribution. The
   step-change claim is *stronger* as measured: every step changed after 3 fires.
4. **Order::Dense**: census identical to Sparse — `Order` selects the fleet battle's
   stepper, not the body-schedule law. A null case; noted so no one counts it as a regime
   probe.

## Where the claim overstates (page corrected in place)

- **"Poisson-consistent, no comb"** is wrong at the tail. The settled dues occupy 7,143
  frames = **41% of the max-step span** (~17,400 frames): 2.4× the uniform density; max 17
  where Poisson(1.64) over 7,143 bins expects ~9; p99 9 vs ~4. The author's mean divides
  by bins *touched*, not by the span — the denominator hides the concentration. What the
  census shows is a **decaying genesis train**, exactly what kick-cadence gold 8ffc
  measured on this same law ("shearing past ~5 intervals") — and the author's own G0 line
  shows it: firsts confined to 891 frames = 5% of the span ≈ **20× support concentration**
  (3294/8ffc/f82a measured 57× on the tighter nladder draw).
- **"The comb is real only where `aligned` runs"** is false as a law statement. The clock
  law's genesis-locked train is real and measured on the clock population (8ffc: two-comb
  train, ~1 event/body/interval; f82a: 57× → 1.0× deleted by the stagger at 10⁵). True
  only as: no shared-exact-tick battalions and no K=1 comb, **on this wide-draw
  population** (step spread [4.3, 5.9]×10⁹ ticks). The consequence "the stagger is not a
  belt-scale lever on the shipped law" inherits the overstatement; the author's own
  Contradictions note scopes populations correctly — the claim and Refuted entry do not.
- **"≈ 4.4 game-days"** is an arithmetic slip: 2.07×10¹⁰ ticks × TICK_SECONDS
  (4.9255×10⁻⁶ s) = 28.3 h = **1.18 game-days**. (2³² ticks ≈ 5.9 h is correct.)

## Novelty

Resolves the calendar page's own open direction 1 against its premise, including the prior
checker's "the shipped law is `aligned`" read. No H entry covers it. The clock chain's
mechanics are known (kick-cadence cites the same lines), but the next-due-derivability
census and the store-class consequence are new. Not a repetition.

## Goal fit

Board question 1 (28 → 10⁹ bodies) via the store-class decision; deletes 25ce's form-(d)
premise ("the class of a body is id-derived and fixed … the bulk never re-keys"). Fits
PRINCIPLES: "a failed experiment kills that configuration, never the method"; "The
simulation decides; heuristics schedule" — the belt's own energies set its stagger; and
"Compute only surprises" — the calendar moves only where fires happen.

## The one experiment to gold

Run this same census instrument on the **phase-locked nladder coast population** (where
8ffc/f82a measured the 57× train) and across a swept orbit-draw spread, establishing the
law-scoped rule the page actually needs — **train lifetime vs the population's step
spread** (and whether a compact-store belt with quantized periods sits on the combing side
of it). That turns "no comb, on this draw" into the general statement the store-class
decision is taken against; with it, and the fires/tail corrections folded in, this run is
gold.

## What the author missed

- The tail-vs-support denominator (bins touched vs step span) — the one reading a quant
  lens exists for, and the residual 2.4× train is the run's own most interesting number.
- The fires misattribution: `stats.kicks` is global; the belt's own fires were never
  counted (a one-line counter from the census gives 3).
- Standing gold on the same law (8ffc/f82a/3294's trains) was reconciled in Contradictions
  but contradicted in the Claim and Refuted — the page now says both, which is how errors
  propagate.
- The 4.4-game-day arithmetic and the unlabelled P5 outcome (failed at 10× vs predicted
  ≥ 50×).
- Well done and worth keeping: pre-registered predictions with honest P2/P3 failures,
  controls passing on both sides, exact code anchors, a reusable census instrument, and a
  clean reproducible regen.
