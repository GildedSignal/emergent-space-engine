# Dossier — 20261013-0236-second-20261013-0037-system-174d-0f2a (second author on 20261013-0037-system-174d)

## Claim

The silver's missing experiment is done and the lever survives it: re-priced with **the law's own
regime-scaled tide cadence** — `plan_interval`'s `want` before the thrust clamp, i.e. `step_for`
(the probe now records it per kick as `clock_full`) — the tide behind a held burn costs **~0–24
events where the burst costs 377–1,085 kicks (45–377×)**, at every level and in both modes,
**including paced L15 at 8 s** where the silver's fixed-granularity counterfactual inverted
(31,286 events against ~1,000 burst items). The carry-the-burn lever is therefore adoptable within
one step, with the claim honestly re-scoped from "~0–10 field events" to **"~0–25 tide events per
burn, set by the dive the burn produces, not by the throttle level"** (L8 6, L12 23, L15 24, brake
5, turn-then-burn 1, coast 0; paced 8 s, seed 1).

## Bottleneck

`frame-cost` open direction 2 (the sweep's L8+ stutter) and through it `kick-jet`. The silver priced
the deletion only in demand mode and at L8–L12; the checker showed the fixed-granularity
counterfactual inverts at paced L15 (~31×10³ events vs ~10³ items). This run derives the correct
counterfactual from the shipped law itself and shows the deletion wins everywhere — the number the
integrator's item 2/3 fix builds needed before building.

## Evidence

All from shipped code plus the original probe extended by two counters (`clock_full`: the law's own
step for the tube this kick ran on, recomputed purely via `step_for`; `r_e6`: distance to the star).
Env-gated (`ES_WATERFALL`), counters only, no behaviour change. Reproduce with `regen.sh` (~2 min
including build; each flight ≤ 8 s wall).

**Instrument control, digit for digit.** Demand worst frames 42 (L8, frame 62) / 579 (L12, frame 60)
/ 1,036 (L15, frame 60) — the published waterfall counts. Composition unchanged: kick0 ≈ boundary ≈
kicks, opens 0, decides = script inputs. The fixed-granularity counterfactual prints 31,286 at paced
L15 8 s against the checker's 31,284 (their seed-7 count: my seed 7 prints 31,286-equivalent budgets
to 3 digits). Cross-seed: seed 7 gives 1,080 kicks → 24 law events (seed 1: 1,085 → 24); per-window
tide budgets median 8.687×10⁶ and max 1.490×10¹³ **identical at both seeds**; tide/burn ratio medians
identical to 3 digits (4.49×10⁻¹⁰ L8, 2.82×10⁻¹¹ L12, 3.52×10⁻¹² L15) — the physics converges; only
wall-clock-dependent counts vary (turn-flight crash frame 188–192).

**The decisive table (paced 8 s, seed 1).** n_law = Σ dt/clock_full over the thrust window — the
events the law's own cadence mints for the same flight:

| flight | burst kicks | worst-frame items | law-cadence events | win (kicks) |
|---|---|---|---|---|
| coast | 0 | 1 | 0 | — |
| forward L8 | 636 | 41 | 6 | 106× |
| forward L12 | 897 | 50 | 23 | 39× |
| forward L15 | 1,085 | 50 | **24** | **45×** |
| reverse L8 | 404 | 31 | 5 | 80× |
| turn+burn L8 | 377 | 33 | 1 | 377× |

Every thrust kick in every flight is burn-bound (`clock_full > step`; law-bound count 0) — P1 held
at 100%. Demand 4 s agrees (L8 3, L12 16, L15 24; worst frames 42/579/1,036), and the demand arm now
reaches the turn flight's burn (377 thrust kicks — closing the silver's undisclosed gap, P5).

**The per-event budget, measured as the checker asked (P3).** Integrated per law-cadence window (a
window closes at its opening kick's `clock_full` elapsed ticks; budget = the tide its kicks
accumulate): ~1.25×10⁸ median at L8 (recovering the coast operating point 5×10⁸, same order, by
construction), ~10⁷ mid-dive, and up to **1.5×10¹³ quanta per window through the plunge** — the
law's own phase rule scales the per-event budget ~10⁵× through the dive, so the checker's
conservative 5×10¹¹ (read off today's per-kick tides) understates the headroom.

**The mechanism correction the re-pricing buys.** The silver's inversion was an artifact of the fixed
divisor (the coast's 4.98×10⁸ quanta/event applied to the plunge's tide). With the law's own cadence
the picture inverts back and sharpens: on the L15 dive (r 1.24×10⁹ → 9.4×10⁷, β → 0.231, γ 1.028)
the burned conic becomes an escape passage and the law's cadence **coarsens** to ~2³² ticks — the
149 deep kicks that carry **100.0% of the flight's tide sum (1.56×10¹³ quanta)** contribute **0.02
of the 24 law events**. The tide the burst so finely samples near the plunge is, to the law, most of
one window of an escape transit — the same mechanics any coasting body on that conic already obeys
(PRINCIPLES 19, one law at every scale). The honest cross-seed, cross-regime tide/burn range is
median 10⁻¹⁰…10⁻¹² with a plunge tail to 1.5×10⁻⁴ (not the silver's unqualified "10⁹–10¹⁰ less";
the checker's "10⁸–10¹⁰" was the short-flight view).

## Predictions

`predictions.md` was written before the decisive runs (the smoke test that proved the probe decoded
`clock` and `r` had shown the 4 s law-cadence counts 2/11/24, disclosed there as instrument-familiar).
P1 held (100% burn-bound, predicted ≥ 95%). P2 held (24 ≤ 40 at L15 8 s; ≥ 39× everywhere). P3 held
(coast recovery within 4×; plunge budget 10¹³ ≥ the predicted 10¹¹). P4 held (seed 7 to 3 digits on
every deterministic number). P5 held (demand 4 s within 3× of paced; the turn flight burns). No
prediction failed.

## What would make it wrong, cost, fit

Wrong if: (a) the word margin the thrust step protects ("the velocity leaves its word") cannot be
held at readout by a ramp-carrying tube — unchanged from the silver, the integrator's to build;
(b) the near-periapsis tide window (up to ~10¹³ quanta in one event) is too coarse an impulse for
the law's own gates — but it is exactly what the shipped `step_for` delivers to any coasting body
on the same escape conic today, so this is the law's standing accuracy, not a new liberty (the
residue to bound at adoption: the impulse error of one such window, against the B-series gates);
(c) the n_law integral's assumption breaks — it reads `clock_full` from the *burned* conic each
kick; with the burn carried in the generator the tube between tide events evolves through the same
conics (the burn's rapidity integral is the same physics), so the cadence sequence is the same to
first order. The counterfactual's windows use the opening kick's clock, which through the dive
*coarsens* — so the count errs toward overcounting events (conservative for the claim). Adoption
cost: unchanged from the silver (a law change in the shipped code, the integrator's to take); this
run supplies the missing price. PRINCIPLES: "Compute only surprises … Nothing is evolved that can be
derived when looked at" (3); "you don't advance a ship tick by tick you just map where it wants to
go" (14); "Store the generator, not the generated" (6); "the same mechanics at all scales while not
doing the work" (19).

## The lens

The second-author lens (do the checker's named experiment exactly) may have missed: the read side
(a ramp-carrying tube read every frame per viewer — `frame-cost` direction 3's standing
counterweight, unmeasured here); the possibility that the tide's own carry cadence *should* be
finer than `step_for` near a compact mass for gate reasons (this run prices the law as shipped, not
as it might become); and the page-level judgement calls (conflict resolution ordering, run-line
deduplication of 32ab/64e4 duplicate entries) that the next checker should verify against the
committed page.
