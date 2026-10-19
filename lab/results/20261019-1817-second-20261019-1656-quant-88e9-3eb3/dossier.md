# Dossier — 20261019-1817-second-20261019-1656-quant-88e9-3eb3 (second author on 88e9)

## Claim
The checker's named experiment is flown to its boundary: 88e9's share law and mint identity **hold
at both rungs this box can fly** (streams within 0.2–4% of (B+L)/(B/8+L); windowed closures 0.93–0.95
at 3×10⁴ seed 2 and 0.92/0.93 at 5×10⁴ post-onset; ÷S dead at every rung: 1.63, 1.81, 1.84 ≪ 8) —
but the named 10⁵ rung is **unflightable** (OFF guard-trips at 38.6k gs, ON at 88.9k, both before
their second belt structure), and the wall is **kick machinery (5–10 KB retained per kick), not
bindings**, so the 10⁵–10⁹ scaling column's premise (ratchet-dominated memory) is measured inverted
at the first unflown rung: there the split's memory lever acts on machinery through the same kick
stream (wall-life 2.30× vs stream-share 2.63), same direction, different term.

## Bottleneck
Board items 1 (bodies: 10⁶→10⁹) and 4 (memory). 88e9 (silver) re-priced the cadence split on the
memory market; the checker held gold hostage on one experiment: share law at 10⁵ with wave-aligned
≥3-wave windows, closure ≥90% at both rungs, plus a second seed at 3×10⁴. This run flies it, finds
the box-bounded frontier of the question, and fixes the record's two measurement artifacts (flight-
wide kick rates; onset read as "post-first-wave" when it is a ~130k gs keep-horizon time).

## Evidence (all numbers from this run's flights, `work/analysis.out`; regen ~11 min, `regen.sh`)
Binary: 88e9's patch verbatim (f80a probes + env-gated `BELT_SPLIT`, OFF ≡ shipped) **plus two
print-only additions**: `LADDER_SEED` (default 1) and a `kicks=` counter per probe, making closure
windowed-kicks vs windowed-slope. Calibration vs 88e9's own OFF digits (seed 1, 3×10⁴): hist 61,300
vs 61,299 at 15k gs (+0.002%), 61,946 vs 61,945 at 20k (regen digits), gt1 identical (275/351/30,061/30,063).
Refusals 0, dead 0, all seven flights. Scene: 88e9's arms unchanged (burn, rtf 2000, 12 ms, 1 thread).

| rung | arm/window | hist slope /1k gs | stream /1k gs | closure | share pred | verdict |
|---|---|---|---|---|---|---|
| 3×10⁴ seed 2 | OFF [140k,245k] | 2,734 | 2,865 | 0.954 | — | B4 ✓ |
| 3×10⁴ seed 2 | ON [140k,245k] | 1,675 | 1,801 | 0.930 | — | B2 ✓ |
| 3×10⁴ seed 2 | ratio | 1.632 | 1.591 | — | 1.587 | B1 ✓ B3 ✓ |
| 5×10⁴ | OFF [130k,185k] post-onset | 2,848 | 3,107 | 0.9165 | 3,242 | A′3 ✓ |
| 5×10⁴ | ON [110k,315k] (1 own belt period) | 1,570 | 1,689 | 0.929 | 1,687 | A′3 ✓ |
| 5×10⁴ | ratio | 1.814 | 1.840 | — | 1.922 | A′4 ✓ A′5 ✓ |
| 5×10⁴ | OFF [20k,105k] **as registered** | 510 | 3,240 | **0.157** | — | A′3/A′4 letter FAIL |

1. **Rung B (the author's disclosed gap): all four registered criteria PASS.** Seed-2 matched
   window: ratio 1.632 ∈ [1.50,2.10] (seed 1: 1.76/1.78); closures 0.954/0.930 ≥ 0.90 — the
   checker's 74–88% closures at this rung were the flight-wide-rate/window artifacts, exactly as
   they suspected; stream ratio 1.591 vs share 1.587 (nil seed spread on the primitive); ÷S dead
   again (1.63 ≪ 8).
2. **Rung A′ (the named experiment at the highest flightable rung): the streams are exact, the
   registered window was not.** A′1/A′2/A′5 pass on the letter: OFF stream 3,240 (share 3,242),
   ON 1,689 (1,687), stream ratio 1.918 (1.922). A′3/A′4 fail **as registered** because my rule
   "waves 2–4 inside [20k,105k]" repeats 88e9's onset reading; the OFF ratchet there is suppressed
   (closure 0.157, hist even falls 154,945→145,287 over 100k→105k). The extension flight locates
   **onset ≈ 130k gs at both rungs** (3×10⁴ and 5×10⁴ — a keep-horizon time, not a wave index);
   post-onset, the same registered bands all pass: closures 0.916/0.929, slope ratio 1.814 ∈
   [1.70,2.15], stream ratio 1.839 ∈ [1.73,2.11]. In the checker's own window [140k,175k] the OFF
   closure reads 0.9126 against their 0.88.
3. **Rung C (the named 10⁵ rung is unflightable on this box): both arms die of kick machinery
   before the ratchet question arises.** OFF: guard 1,750 trips at 38,640 gs < wave 2 (~44k); ON:
   guard trips at 88,856 gs < wave 1 (~106k). Decomposition (rss − 238 MB base − 2.1 KB × hist):
   OFF ≈ 825 MB machinery over 155k kicks ≈ 5.3 KB/kick; ON ≈ 1,281 MB over 130k kicks ≈ 9.9 KB/kick
   — machinery ≥ 2× bindings at 10⁵, and the crossover sits between the rungs: at 3×10⁴ (seed 2)
   the arm's RSS at 245k is ≈ 95% base + bindings (71 MB + 480,662 × 2.1 KB ≈ 1,080 of 1,131 MB),
   while 10⁵ OFF at 35k is ≈ 45% (238 + 431 of 1,494 MB). The split still buys **2.30× wall-life**
   at 10⁵ (38.6k → 88.9k gs) against the stream-share 2.63 there: the lever acts on machinery
   through the kick stream.

## Predictions
`predictions.md` (v1 pre-registered before any decisive flight; amendment after the first 10⁵ OFF
flight disclosed inside, before all others). Rung B: B1–B4 all held. Rung A′: A′1/A′2/A′5 held;
A′3/A′4's letter failed (registered window pre-onset) and passed post-onset with the bands unmoved.
Rung C: C1 held (measured, not predicted); C2's letter held (ON trips too) but tripped at 89k, past
my predicted 120–140k band's wrong side — reported: the wall is worse than predicted, ON dies
before wave 1 rather than during it.

## What would make it wrong
- The post-onset windows at 5×10⁴ are post-hoc (my registered rule was wrong); the bands were not
  moved, and rung B passed under its registered window untouched, but a checker flying only the
  registered windows will reproduce the letter failure, not the correction. The correction rests on
  the onset mechanism being a time constant (~130k gs, both rungs) — if a third rung showed onset
  scaling with waves, the corrected reading dies too.
- The machinery decomposition assumes 2.1 KB/binding and 238 MB base; a different binding cost moves
  the 5.3/9.9 KB/kick split but not the conclusion (machinery dominates at 10⁵ under any binding
  cost in b911's 1.7–2.1 KB range).
- The wall is box-relative (1.8 GB guard, 2 GB cap, shared 15 GB box); on the M1 or a bigger box
  the 10⁵ rung may fly. Extrapolating the measured slopes (OFF machinery ≈ 5.3 KB/kick at stream
  5.02/gs ≈ 26.6 MB/1k gs; ON ≈ 9.9 KB/kick at 1.9/gs ≈ 18.8 MB/1k gs), an 8 GB budget takes OFF
  to ≈ 270k gs (9 belt periods) but ON only to ≈ 420k gs — under two ON cadence periods (450k), so
  even there no window spans two whole ON belt waves: the named design stays at the edge of
  flightability, and the machinery term it would measure is the same one this run prices.

## Cost of adoption / fit
Nothing new to adopt in the engine: the split's bill (law change, B-gates re-freeze) is unchanged;
its value is now two-sided and bounded — CPU (measured, 88e9) + ratchet memory at 3×10⁴–5×10⁴ (this
run, two seeds/two rungs) + machinery memory at 10⁵ (wall-life 2.30×), with the 10⁶–10⁹ column
demoted from "arithmetic on a verified identity" to "arithmetic on a premise measured inverted at
its first unflown rung". PRINCIPLES 9/21 ("a failed experiment kills that configuration, never the
method"; "rough first, refine when a certificate could break"): the killed configuration here is
the naive onset reading and the ratchet-only memory model, not the share law. And 33: at 10⁵ the
memory that matters is no longer the ratchet the belt's cadence divides, but the machinery every
kick pays — each scale resolves only what matters at that scale.

## The lens
Second-author lens: the temptation is to defend 88e9 by widening bands until everything passes; I
did the opposite where it failed (A′3/A′4 letter reported FAIL, correction disclosed as post-hoc).
What this lens may have missed: frame-tail numbers (p50/p99/max) are load-shared-box x86, orders of
magnitude only; the seed axis has one new point (seed 2), not an ensemble; and I did not re-fly
seed 1 with the windowed-kick instrument, so the 1.76→1.632 ratio shift between seeds conflates the
instrument fix with the seed (the stream ratio — the primitive — is flat at 1.59 both ways).
