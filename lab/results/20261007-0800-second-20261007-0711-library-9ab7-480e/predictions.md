# predictions.md — run 20261007-0800-second-...-480e (second author on 20261007-0711-library-9ab7)

Written before the decisive sweep, after only 2000-frame pilots (which showed: at
rtf=1, m=48 the plane resolves ~1.01 items/frame, 99% fleet slices; at rtf=16 ~1.8
items/frame with kicks ×23, boundaries ×208, encounters ×15; at m=400 leavers ×21,
opens ×6.6; budget-of-one and unlimited runs give the same digest — the instrument
is neutral).

## The experiment (the checker's named one)

Log the shipped plane's own per-event work (item count and wall µs per item, per
frame, per kind) on the shipped configurations (`scenario::plane`, `Config::default`,
`Order::Sparse`, threads 1), then estimate the event-size tail exponent (Hill plot on
the continuous streams; direct order statistics on the integer demand stream) and the
bench-vs-hour hazard (55-s bench windows at 60 fps vs the worst frame in an hour of
frames), across seeds.

Streams: S1 demand = items resolved per frame (deterministic, digest-pinned);
S2 cost = per-item wall µs (top-1 per frame, exact for pooled top-N ≤ frames);
S3 = per-frame wall ms. Configs: A rtf=1 m=48 (the shipped default, 15 seeds ×
60 000 frames + 1 seed × 216 000 frames = one hour of play); B rtf=16 m=48
(4 × 60 000; the fly page's clamp); C rtf=1 m=400 (4 × 60 000; the bench's clamp).

## Pre-registered predictions, with kill criteria

- **P1 (demand tail, config A).** The per-frame demand stream at rtf=1 is thin or
  bounded: pooled max/p99.9 < 3 and no α̂ ≤ 3 plateau (Hill at the top 0.5–2% of a
  jittered copy, or the extremes directly). *Kill:* max/p99.9 > 3, or an α̂(k)
  plateau ≤ 3 stable in k.
- **P2 (cost tail, config A).** The per-item cost tail is wide but **bounded by
  construction**: the largest item is a compile-class rare event (a kick recompile,
  a doll open) whose size the engine knows; max/p99.9 ∈ [3, 30] with a stable
  ceiling across seeds (seed-wise maxima within 3× of each other). *Kill:* maxima
  scale with run length (no ceiling), or seed maxima differ > 3×.
- **P3 (bench vs hour, config A).** On the shipped record the 55-s bench p99.9
  sizes the hour's worst frame within 3× (the light-tailed regime of the original
  probe: 1.3–1.7). *Kill:* the hour-max / median-bench-p99.9 ratio > 3, i.e. the
  matched-percentile hazard lands on the shipped plane.
- **P4 (rtf=16, direction only).** Compressing time fattens the demand tail:
  max/p99.9 and burst depth grow with rtf. The hazard, if anywhere, lives where
  the player fast-forwards.
- **P5 (m=400, direction only).** A fleet at the bench clamp fattens the demand
  tail at rtf=1 less than rtf=16 does (leavers/opens grow, but the per-frame
  cadence stays ~1 slice/frame).

## Decision rule (the checker's, pre-committed)

α_eff ≤ 3 with no bound on the shipped rtf=1 stream → the claim holds on the
shipped record (adopt the tail-exponent line in plane.md's measured list and the
utilization policy). Bounded or thin (α_eff > 3, or a construction ceiling with
stable seed maxima) → **clean refutation on the shipped record**: percentiles
stand today, lesson 5 survives, and the fat-tail machinery is deferred to where
P4/P5 show it returns (fast-forward, fleet scale).

## What would make the run itself wrong

The shared CI box's timing noise contaminating S2/S3 (mitigated: deterministic S1
decides; timing is orders of magnitude only, per lab rules); the scenario's fleet
battle ending early (leavers exhausted) so the hour run stops seeing events
(check: event-rate vs frame index); a warm-up transient mistaken for a tail
(reported with and without the first 300 frames).
