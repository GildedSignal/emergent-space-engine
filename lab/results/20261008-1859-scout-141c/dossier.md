# Dossier — 20261008-1859-scout-141c (lens: scout)

**Claim.** The arrival rate of distinguishable gravity news at one body grows as R² with the
light-cone radius R under the naive per-source cursor channel, but only as log R (one arrival
quantum per octave shell per receiver) once sub-quantum events accumulate into shell aggregates
— so the growing light cone is a budget choice about the news quantum Q, not a wall; the channel
must be owned by cells (O(log R) accumulators per cell), never per body.

## Bottleneck

The board's named risk "the light cone keeps growing (there will always be a point where we
cannot handle the universe anymore); budgets (4 GiB, 30 FPS, one hour, 20 GiB) open, not
dropped" — the one risk with **no queue item** (b-news-gravity builds the in-system cursor
mechanism, not the scaling law; b-h-live measures distinctions, this bounds what a body must
*consume*). Expected gain: the naive channel is 130× over the quantized one at 3.5 decades and
the ratio is unbounded (∝ R²/log R); this deletes the per-(body, source) cursor as a
galaxy-scale structure and replaces it with cell-owned octave accumulators.

## Requirements, as numbers (tied to PRINCIPLES)

- 30 FPS ⇒ 33 ms/frame, p99 (P12, smoothness); one hour of play; 10⁹ bodies in 8 GB (P24: the
  memory floor is information). Fixed surface density as N grows = the board's 5 October
  scaling risk.
- News = surprise events only; smooth motion is compiled away by generators (P3, P14: compute
  only surprises, no ticks). Events below one quantum accumulate (P6 verbatim: "influences
  below one quantum accumulate").
- c = 1 ⇒ arrival time = t_event + r; nothing past c (P23).

## Candidates found (ranked by fit, not popularity)

1. **PDES conservative synchronization** (Chandy–Misra–Bryant; Time-Warp): regions compute
   lazily against lookahead = light-crossing time; the null message ("nothing changed up to t")
   bounds the future. Known failure: null-message overhead explodes when granularity is too
   fine — our accumulator IS the aggregated null message, and the quantum Q is its granularity.
   (Overhead literature verified to exist; specific laws UNVERIFIED.)
2. **Retarded-potential FMM / wave-equation FMM** (plane-wave expansion grouping, multirate
   updates): far groups are updated through coarse channels at pair light-crossing rates — the
   octave shell is that channel. (Verified the method exists; its cost law UNVERIFIED at source.)
3. **Cosmology on-the-fly light cones** (GADGET-4/Arepo): the cone is swept in nested shells;
   their failure mode is box replication (repeated structures aliasing into shells) — our
   analogue is shell aliasing, a certificate must bound it.
4. **Exchange market-data feeds** (depth updates quantized to ticks, aggregated by level;
   skin in the game): the tick = quantum, levels = shells. UNVERIFIED at source.
5. **Game LOD impostor refresh** (update rate falls with level): practice agrees; weakest fit
   (no causality).

## Evidence (commands each ≤ 60 s; total 0.64 s on this Linux/x86 host)

```
cd lab/results/20261008-1859-scout-141c && python3 news_scaling.py   # writes news_scaling.json
```

2D disk, G=c=1, Keplerian Ω=a^-1.5, surface density ρ=1/π held fixed, r₀=1, event size
s(a)=δ/a² (δ=1), Poisson rate λ=10⁻² per source; arrival = tₑ+a; binned exact Poisson
(constant size per bin), quantum channel: s≥Q fires individually, else accumulates per octave
shell and fires floor(Σs/Q).

- **Naive channel: exponent 2.0 exactly.** Rate 0.536 → 3.29×10⁴ over R=4→1024
  (=λN(R)); slope 0.602 log₁₀ per octave = α(R)=2.0.
- **Quantum channel: log in R.** Q=10⁻³: 76.0, 120, 164, 209, 253 at R=64…1024 — +44 per
  octave, flat increments (analytic prediction λ·1.5πδρ/Q = 47/octave; the ~6% deficit is the
  r_cut cutoff). Fitted top-decade power slope 0.11 (an artifact of fitting a log with a
  power law); at every Q the increments per octave are constant, i.e. the law is
  ν(R) = c₀ + c₁·log₂(R/r₀).
- **Q sweeps (P4):** Q=10⁻² ⇒ r_cut 10, +4.5/octave; Q=10⁻⁴ ⇒ r_cut 100, +440/octave —
  r_cut=√(δ/Q) as predicted, absolute rate ∝ 1/Q, exponents unchanged (0.076–0.19 ≪ 2).
  r_cut is exactly where quantum = naive stops (R=16 for Q₂, R=128 for Q₃: visible in the
  tables).
- **Head-to-head at R=1024:** 3.29×10⁴ vs 253 (Q₁, 130×), vs 32.6 (Q₂, 10³×), vs 1.8×10³
  (Q₃, 18×). The ratio grows as R²/log R — unbounded in the naive channel's favour.
- **Smooth-disk control (P1):** even the naive channel converges without events
  (1.24–1.30 across R=4…1024, slope −0.008) because per-source change rate ∝ a⁻⁷ᐟ²;
  aggregate shell sums 0.55–0.66, only ~2× below naive — the inner few sources dominate and
  cannot cancel (where aggregation does NOT help; the engine already pays those directly).
  Grid check of the closed form at R=16: 0.749 vs analytic 0.741 (1%).
- **Cataclysms (P5, held out):** rare size-≥Q-everywhere events add exactly their total rate
  (0.048–0.051 vs Λ=0.05) to both channels, independent of R — bounded by the universe's own
  event rate, not by the cone.
- **Coherent m=1 mode (P6, held out):** a lopsided disk's aggregate field amplitude grows
  ∝ ln R, so its quantized rate grows linearly in octaves (12.5, 14.2, 16.1 at R=256, 512,
  1024) — the log is a physical channel, not an artifact.
- **Adversarial bursts:** fully correlated, synchronous firings give quantum rates identical
  to the spread case to 3 digits (76.03/119.9/164.2/208.7/253.1) — bunching sums sizes before
  thresholding, so the count is bounded by Σs/Q; correlation cannot inflate the channel.
- **Seeds (5):** std ≤ 0.15% for R ≥ 32 (12% at R=4, ~6 counts).

## Predictions

All six frozen in `predictions.md` before the decisive sweep (P1–P6 above) **held**, including
both held-out cases and the kill criterion's non-trigger (no positive exponent anywhere in the
quantum channel). The analytic per-octave constant matched within 6%.

## What would make it wrong

- The 1/a² event-size falloff is load-bearing: multipoles above monopole fall faster (then the
  law only tightens); a game mechanic whose *distinguishable* news falls slower than 1/a² per
  shell (e.g. observability that grows with distance) would restore a positive exponent.
- A receiver whose certificate demands Q so fine that r_cut approaches the universe's radius
  (Q ≲ δ/R²) is back on the naive channel by choice — measured: Q₃ at R ≤ 128 equals naive.
- The toy is one central observer; an observer embedded in a clump changes c₀ (its
  neighbourhood), not the log law. Unverified: non-central observers, anisotropic shells.
- Not the engine: the plane's real event stream may have event-size distributions where the
  accumulator's linearity in Σs hides cancellation (vector directions). I measured magnitudes;
  directional cancellation only lowers the rate further.

## Cost of adoption and fit

Adoption is a design input, not a patch: (1) b-news-gravity's per-(body, source) cursors stay
**inside r_cut** (system scale) and hand over to cell-owned octave accumulators beyond it;
(2) the accumulator is the aggregated null message — its quantum Q must be set by the
*receiver's certificate floor*, never by the sender's precision (the CMB lesson, and our Q₃
row shows the cost of getting it wrong); (3) memory Fermi: 1 AU → 5×10⁴ ly is 31.6 octaves ⇒
~32 channels/cell; 10⁷ cells × 32 × 8 B ≈ 2.6 GB against the 4 GiB budget — fits cell-owned,
never body-owned (10⁹ × 32 × 8 B = 256 GB). PRINCIPLES: P6 verbatim ("influences below one
quantum accumulate"); P3 (compute only surprises); P7 (multipoles are the mechanism, "for
gravity and for causality regions alike"); P23 (nothing past c).

## The lens (what scout may have missed)

Scout optimizes for the best *known* structure; I did not invent a representation, I measured
the law the existing design implies. Missed by construction: whether the *view* channel
(photons, the 83%-of-a-light-frame gather) obeys the same law (it should — same cone, same
1/a²-class falloff for brightness — but b-readout-cost owns it and I did not measure it), and
whether H_live's distinction budget can *afford* 32 accumulators per cell (b-h-live owns it).

## Grade (author's self-assessment)

Silver-shaped: real, reproduced cheaply, held-out predictions held, but a float toy — the
named experiment to gold is running the two channels on the plane's own event stream at N
bodies (the accumulator wired into crates/universe's news cursor), which this run's 60 minutes
did not reach.
