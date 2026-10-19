# Dossier — 20261018-2312-dynamics-84b2 (dynamics lens)

**Claim.** The dense order's "breathing mode" — checker2's unpriced N-scaling lead on
834e — is the genesis shock's acoustic ringdown of the box, and its Fano growth is the
identity **Fano_w = w·ν·n·m²** with the relative modulation m bounded at 1.3-2.4%: no
coherence grows with N, no ratio tail grows with N, and the mode decays — the steady
state stays anti-bunched and flat at every n flown.

**Bottleneck.** Smoothness and the allocator (the board's #4): 834e's checker2 left
"the breathing mode's N-scaling (Fano₆₄ 1.2 → 33.4 from n = 400 → 6400)" as
allocator-visible and unpriced, with the live danger that a dense formation's contact
work bunches worse as the game scales toward 10⁹. This run prices it: the danger is
bounded by construction (m ≤ 2.4%, per-window max/p50 ≤ 1.12 inside the worst block),
which **deletes the need for any batch-shaping or dephasing machinery for thermal dense
scenes** — the simplest falsifying probe killed the configuration, not the method. It
also corrects the record: "a long-lived coherent breathing mode" (834e current best) is
a decaying transient whose *lifetime and period scale with the box* (T ≈ 5.7-9·side
chronons, lifetime ~3-6 blocks at side 120-170), so fixed-burn measurements see more of
it at larger n without anything growing.

**Evidence** (shipped `Chronon` + `Law::RelativisticV1`, Q = 2²⁰, `worlds::gas` genesis
mirrored bit-identically, fill 0.7 = the touching lattice, vmax 2¹⁶ units ⇒ ρ ≥ 11, no
skip boundary; burn 1024, horizon 8192, seeds 1-3; harness
`crates/lattice/examples/breathe.rs`, analysis `analyze.py`/`summary.py`):

N-ladder (seed ranges; identity = mean₆₄·m² with m = mean relative std of the 64-window
counts; blocks = F64 in successive 2048-chronon blocks, seed 1):

| n | side | F1 | F64 | mean₆₄ | m | identity | p99/p50 (chronon) | b0 max/p50 | T_early | share | blocks |
|---|------|----|----|--------|---|----------|--------------------|------------|---------|-------|--------|
| 400 | 43 | 0.77-0.80 | 1.76-2.20 | 4070 | 2.16% | 1.89 | 1.286 | 1.052 | 341 | 0.01 | [2.4, 1.8, 3.0, 1.7] |
| 800 | 60 | 0.77-0.79 | 1.89-2.65 | 8804 | 1.59% | 2.22 | 1.182 | 1.031 | 256 | 0.01 | [2.5, 3.0, 2.2, 1.3] |
| 1600 | 85 | 0.80-0.81 | 2.39-3.20 | 17461 | 1.26% | 2.79 | 1.128 | 1.034 | 409 | 0.02 | [3.8, 3.1, 3.1, 1.5] |
| 3200 | 120 | 0.86-0.90 | 6.38-7.94 | 35457 | 1.44% | 7.38 | 1.094 | 1.077 | 682 | 0.16 | [24.5, 2.4, 2.2, 1.7] |
| 6400 | 170 | 1.34-1.36 | 38.18-39.05 | 69032 | 2.37% | 38.73 | 1.106 | 1.115 | ≥1024 | 0.37 | [117, 19.5, 7.3, 2.7] |

1. **The identity holds at every n** (each column reproduced by mean₆₄·m², e.g.
   69032·0.0235² = 38.18). Checker2's 33.4 at n = 6400 is reproduced (38.18, seed 1;
   their 1.2 at n = 400 reads 1.8-2.2 here — same order, same law). The N-growth of
   Fano₆₄ is counts ∝ n under bounded modulation; m never exceeds 2.4% and shows no
   trend (1.3% at 1600, 2.4% at 6400 — phase/scatter, not growth).
2. **The spectral "transition" between 1600 and 3200 is statistical emergence**: the
   mode's share grows 0.01 → 0.37 exactly as the Poisson noise floor 1/√mean₆₄ falls
   (1.57% → 0.38%) past the fixed ~2% oscillation. Nothing dynamical switches on.
3. **The mode is a decaying ringdown, not an attractor**: blocks fall 117 → 2.7 at
   n = 6400 (lifetime ≈ 4-6×10³ chronons ≈ several box periods), 24.5 → 1.7 at 3200;
   long horizons (400 and 1600 at 3-4× the horizon, 32k chronons) never see it return —
   last-block F64 = 1.4-2.6 (the anti-bunched baseline), whole-run per-64-window
   max/p50 ≤ 1.093.
4. **The period is the box's, not the cage's**: T_early/side = 7.9, 4.8, 5.7, ≥6.0
   (sides 43 → 170; the 800 arm is noise-dominated) — acoustic scaling against the cage
   alternative (T ≈ 22-45 chronons, side-independent; measured cage rattle from V-rows
   peaks at periods 7-21). Effective phase speed ≈ 0.3-0.6c: the touching lattice's
   contact network carries pressure ~10× faster than its particles (⟨|v|⟩ ≈ 0.044c).
   Mode *shape* unmeasured: genesis-id band binning dies at maxdisp 25-37 lc (bodies
   migrate up to 58% of the small boxes), band correlations ≈ 0 — the temporal law
   carries the result, the spatial claim is not made.
5. **Held-out dephasing (P5), honest miss**: mass spread {1,2,4} at n = 6400 (seed 1)
   does not kill the mode — it strengthens it: m 2.91% vs 2.35%, F64 65.98 vs 38.18,
   share 0.46, blocks [188, 50, 20]. The ringdown is the box's acoustic response,
   robust to cage detuning — which *confirms* the acoustic reading of (4) while
   refuting the pre-registered identical-cages mechanism. The radius half fails the
   same way: radii {0.75,1} leave the mode standing (m 3.19%, share 0.23, block0
   F64 39.1; F64 34.6 vs 38.2 — the small fall is the lower contact rate of smaller
   discs, mean64 33934 vs 69032, not lost coherence). The 12800 octave was still
   queued at the run's time limit; `regen.sh` includes it.

Reproduce: `lab/results/20261018-2312-dynamics-84b2/regen.sh` (applies
`work/patch.diff`, runs the ladder + dephasing + long arms with `-P 6`, prints
`summary.txt`; ~6-10 min wall on this 8-vCPU machine; single arms:
`breathe 6400 0.7 65536 1 1024 8192 0` ≈ 2 min, `breathe 400 0.7 65536 1 1024 8192 0` ≈ 2 s).

**Predictions** (`predictions.md`, written before the decisive runs):
- P0 calibration: held in order (33.4 ↔ 38.18 at 6400; 1.2 ↔ 1.8-2.2 at 400 — both «
  the 6400 value, same identity).
- P1 (F1 ∝ n, global coherence): **refuted** — F1 flat 0.77-0.90 through 3200; the
  1.34 at 6400 is the ringdown inside the window (identity at w = 1), not coherence
  growth; both pre-registered mechanisms (global sync, independent cages) were wrong —
  the measured law is bounded modulation under ∝n counts.
- P2 (allocator): **held** — per-64-window max/p50 ≤ 1.08 at every n ≤ 3200 and 1.115
  at 6400's worst block (inside the ±35% band of the n = 400 value); per-chronon
  p99/p50 ≤ 1.29 (worst at the smallest n, small-count granularity; ≤ 1.19 from 800 up,
  under the 1.25 line).
- P3 (mechanism): acoustic half **held** (T ∝ side across a 4× side range); "single
  sharp peak" only above the noise floor at n ≥ 3200 — itself a finding (emergence,
  see 2); the band-correlation half was unmeasurable (binning died, see 4).
- P4 (attractor vs transient): **decided for transient** — decay by > 2× was the
  registered line; measured 117 → 2.7 (> 40×), and no return at 3-4× horizons.
- P5 (held out): mass half **refuted** (strengthened, see 5); radius half pending.

**What would make it wrong.** The m-bounded claim is measured on one genesis family
(the monodisperse touching lattice at fill 0.7, one speed, β ≤ 0.09) and one law; a
genesis that *sustains* a global oscillation (a driven wall, a coherent fleet's
wall-ram — checker2's Fano₁ 10-129 formations) sits outside it, and the 12800 octave is
extrapolated by the identity, not yet flown. The acoustic-speed reading infers c_eff
from measured periods on 3 solid points; a direct mode-shape measurement (positions,
not genesis ids) could still surprise. If a checker finds m growing past ~5% at some
n ≫ 6400 or at higher β, the bounded-modulation conclusion dies and the allocator
needs the batch-shaping this dossier deletes.

**Cost of adoption.** Zero code: this is a deletion of a feared requirement (no
dephasing, no batch shaping, no N-dependent margin for thermal dense scenes) plus a
measurement rule — price rate modulation as m = relstd, never raw Fano, so arms compare
across n (raw Fano conflates ∝n counts with coherence). One line of 834e's current
best is corrected ("long-lived coherent breathing mode" → genesis ringdown, T ∝ side,
lifetime ∝ side).

**Fit with PRINCIPLES.** "Compute only surprises" and "the cheapest compute is compute
not done": the ringdown is a one-off startup cost that self-extinguishes — paying any
steady-state machinery against it is work for no reason. "A test that cannot fail is a
control": P1/P5 were written to fail and did, which is what makes the identity
credible. "Fat tails: judge behaviours over many seeds and look at the worst cases":
the allocator letter is quoted from the worst block of the worst arm, not the mean.
"Rough first": orders (T ∝ side over 4×, m bounded over 16× in n), no polishing of a
scene family the N-ladder may replace.

**The lens.** The dynamics lens went looking for an attractor and found a transient —
its own declared blind spot ("long-run behaviour can hide a transient that ruins a
frame" cut the other way: here a transient mimics a long-run mode). What the lens may
have missed: the *coherent fleet* burst law (checker2's other unpriced half, bulk-drift
formations) is a genuinely different dynamical object — a driven, sustained bunching —
and this run's m-instrument, not raw Fano, is the tool for it; also the ringdown's
*absolute* batch cost at genesis (max_batch = n, 834e's genesis shock) is the number an
allocator actually pays at scene start, and it deserves the m-style pricing more than
the steady state ever did.
