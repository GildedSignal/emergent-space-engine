# Dossier — 20261019-0325-taleb-90b7

## Claim

The formation burst law is priced on shipped code, and generic formations are NOT a
standing allocator ruin: a fleet crossing is a **one-shot 3× episode** (worst 64-chronon
window 2.8-3.4× the box's late mean, lasting ~2.8·extent chronons, once), after which the
merged cloud is flat forever; **recurrence (a standing shock train) requires the head-on
swap symmetry** — matched transverse velocity AND aligned columns — which survives
arbitrary *timing* dispersion (σₓ) but is killed by one quantum of transverse structure
(σy ≥ q/256 OR position jitter ±q); in the exactly-aligned limit single chronons carry
**n/2 contacts** (top-1% of chronons carry 21% of all contacts), forever at constant
amplitude.

## Bottleneck

Board item 4 (smoothness/allocator) feeding item 2 (encounter work at 10⁹): the wiki's
only unpriced half of the dense-order record (chaos-shadowing open direction 2, checker2's
fleet arms: Fano₁ 96-128, "both allocator-visible, both unpriced"). Gain: deletes the
standing-formation tail as a generic allocator fear (one class of guards never needs
building), names the one configuration that does need a guard (integer-aligned crossings),
and hands the belt/formation wiring a dimensionless trigger: transverse velocity equality.

## Evidence

Shipped `Chronon` + `Law::RelativisticV1`, Q = 2²⁰, `worlds::galaxy` fleet conventions
(unit-mass bouncers, radius q, spacing 6q, drift ±q/4 = 0.25c, jitter ±q, dispersion σ per
component). Scene: two n/2 fleets, gap extent/2, Bounce box W = 2.5·extent,
extent = 6·⌈√(n/2)⌉ light-chronons; the box re-crosses them. 38 flights (seeds 1-2),
n ∈ {400, 1600, 6400}, horizons 2048/4096/8192 (≈6 crossings per rung), every flight ≤ 27 s;
regenerates in ~4 min (`./regen.sh`; deterministic — rerun digest-identical).

The regime table (worst over seeds; `work/table.txt`, `work/analysis.json`):

| n | arm | verdict | maxc/n | maxW/mean_late | F64_late | conc (top-1%×) | excess contacts/n |
|---|---|---|---|---|---|---|---|
| 400-6400 | aligned (σ=0, no jitter) | **train** | **0.487-0.499** | 2.6-2.8 | 437-7035 | 21.4-21.5 | 17.8-68.7 |
| 1600, 6400 | σₓ=q/256, columns | **train** | 0.069-0.076 | 2.7 | 1635-6950 | 2.8-3.0 | 34.7-70.1 |
| 1600 | σₓ=q/16, columns | smeared→one-shot | 0.066 | 2.4 | 2.9 | 2.5 | 11.1 |
| 400-6400 | σᵧ=q/256 (±jitter) | one-shot | 0.057-0.059 | 3.3 | 1.1-1.3 | 3.2 | 11.8 |
| 1600 | jitter ±q alone, σ=0 | one-shot | 0.057-0.059 | 3.3 | 0.9-1.0 | 3.3 | 11.5-11.8 |
| 400-6400 | isotropic σ (jitter on) | one-shot | 0.051-0.070 | 2.8-3.4 | 0.7-8.5 | 2.8-3.9 | 4.8-25.6 |
| 400-6400 | thermal control | — | 0.021-0.035 | 1.28-1.39 | 0.8-1.4 | 1.4-2.6 | 0.9-2.0 |

Key facts, each from the table plus the window series in `work/`:
- **One-shot law (any transverse structure):** a single crossing burst, worst window
  2.8-3.4× the late mean, width 2.8-2.9·extent ch (the interpenetration time; ~2× wider
  than a train crossing — the merged streams pile up), ~0.4·⌈√(n/2)⌉ excess contacts per
  body; afterwards flat: extended horizon 8192 (2× the grid's) shows no second burst
  (re-meet would fall at ~5100 ch), late rate 1.20× thermal (x-anisotropic heat), F64_late
  ≤ 8.5 vs thermal 0.8-1.4. Momentum conservation: the merged cloud has zero net drift and
  never re-crosses.
- **Train law (σᵧ=0, jitter=0):** bursts of 2.6-2.7× mean every 320/640/1344 ch (n =
  400/1600/6400) with silent gaps (windows at 0.0-0.2× mean), amplitude constant:
  last/first 0.87-0.99 over 6 crossings; σₓ=q/256 changes nothing structural (0.905-0.959
  over 6), σₓ=q/16 smears the train away in ~3-4 crossings (arrival-time diffusion through
  random pairing). Per crossing the sweep cost is the same ~0.4·⌈√(n/2)⌉ contacts/body as
  the one-shot — the regimes differ in whether it repeats, not in unit cost.
- **The comb (exactly aligned):** single chronons carry n/2 contacts in teeth every 4 ch
  (n=1600: 654-794 across a 256-ch burst), concentration 21.4-21.5× at every n, F64_late
  437→1815→7035 with n; the wiki's checker2 fleet Fano₁ 96-128 is this first crossing.
- **Ops vs contacts (the honest allocator caveat):** at n=6400 the burst window costs
  2.085M charged ops vs 1.592M quiet (1.31×) — the O(n) walk dominates ops, so a
  walk-budgeted scheduler barely sees the crossing; the 3× (and the comb's 21×) lives in
  the contact/response stream, which is what event-driven modes and response work pay.

## Predictions

`predictions.md` was written before the decisive grid. Scored honestly: P1's spine held
only for σ=0 and σₓ-only (the train is real and undecaying there); its own kill branch
fired for isotropic σ — "sustained" dies at the first quantum of transverse structure, and
the axis decomposition (σₓ vs σy) that explains this was not foreseen. P2 half-refuted:
0.5·n per chronon holds ONLY aligned (0.05-0.07·n for any dispersion — an 8× drop that is
itself the finding); top-1% share 21% (not >50%). P3 held for thermal (0.8-1.4) and trains
(437-7035) but the σ=q/256 isotropic arm lands at 0.7-1.5, not >100 — F64_late separates
the regime (train vs merged), not "has dispersion". P4 half-held: width is geometric
(∝ extent, σ-independent), sub-linear in n. P5 held (burst ops/contact 70-170 vs quiet
285-390 — no blow-up on simultaneous batches). P6 held (seed 2 verdicts and digits within
±15% everywhere). P7 partially checked (walls 6.6k vs 99k contacts at n=1600; not priced
as a train).

## What would make it wrong

The verdicts ride on transverse structure ≥ 1 quantum (jitter ±q or σy ≥ q/256) — a
formation mechanism that holds transverse velocity exactly equal while crossing (wings on
integer velocities, which the engine's quantized conventions make representable: galaxy's
own drifts are exact multiples of q/4) sits in the train regime and my σₓ arms show that
regime does not decay. Second, the one-shot conclusion is for trapped boxes (walls
re-reflect the streams); in unbounded space a pair crosses once by geometry — same one-shot
exposure, no recurrence question either way. Third, ops-based allocator conclusions
under-react (1.31×): if the production scheduler budgets ops, not response work, it will
underprovision crossing seasons by the 3×/21× contact factor.

## Cost of adoption, fit with PRINCIPLES

Zero code: a measurement plus one guard recommendation — the belt/formation wiring gets a
dimensionless trigger (transverse-velocity equality between crossing formations ⇒ expect a
train; anything else ⇒ one 3× crossing season of duration 2.8·extent). "Compute only
surprises" (3): the crossing is the surprise, the rest is flat; "regimes are chosen by
dimensionless numbers" (4); "one law at every scale" (33): the same swap condition decides
at every n flown (16×). Via negativa: this deletes a feared generic tail (no batch-shaping
machinery needed for formation crossings) and keeps exactly one named guard.

## The lens

Taleb looked for ruin and found the ruin is conditional — the barbell keeps the paranoid
end (the aligned comb, 21× concentration, forever) and frees the middle (generic fleets:
one bounded episode). What the lens may have missed: the convexity lives in the response
stream, not the walk (an ops-only allocator under-reacts — an instrument lesson, not a
physics one); mixed fleet+thermal scenes (a fleet crossing a live belt — the game case)
and the wall-reflection train are unflown; the natural next rung takes them with this same
harness and the F64_late instrument.
