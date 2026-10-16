# Predictions — 20261016-0117-second-20261016-0023-scout-1652-d86c (second author)

Written before the decisive flights. The experiment (the checker's named one): fly the deletion —
the `h.len() > 1` floor in `PlainBodies::prune`/`droppable_until` dropped behind `ES_DROP_FLOOR=1`
(same binary, same build; the floor is the shipped path when unset) — on the scout's belt scene
(`plane_extra`, seed 1, 48 members, N = 10⁴ → 10,028 bodies), coast and burn, cuts at
15/20/32/48/60k game-s, `settle(cut)` before every read. Instrument: per-call-site retired serves
(view vs engine, an in-view flag set only around gathers — fixing the checker's defect (i)) plus
retired **misses** (queries with `t < event_time` that no segment covers), the scout's
`history_window` census, a warm gather loop, and a full `seen` dump per cut for baseline-vs-deletion
view comparison.

Decision rule, registered before the flights:

- **D1 (the fork).** If any digest at any cut differs between floor-on and floor-off (coast or
  burn): the floor is law-load-bearing; the claim closes the other way and the page records a
  refutation of the deletion. If every digest is bit-identical: the deletion is outcome-free and the
  standing-memory claim is judged on D2/D3.
- **D2 (degradation bound).** The view degradation is bounded iff, at every cut, (a) the set of seen
  ids is identical between floor-on and floor-off (no emitter vanishes), and (b) every seen body's
  position shift |Δoffset| is smaller than its own physical radius (the shift stays inside the
  body's disc, so no view at any zoom that resolves the body can see it move). Otherwise the
  degradation is unbounded-at-this-scale and reported as such.
- **D3 (the cut).** Standing history at steady cuts (32k–60k) drops from ~1.05 segs/body to
  ≤ 0.15/body under the floor-off build (the ~10× standing cut the scout priced).

## The cases I have not tuned on, and what I expect

- **P1 (digests).** Every digest bit-identical across the toggle, coast and burn, at every cut.
  Rationale: the engine's `binding_at` queries are all at `t ≥ oldest`-ish ticks (encounter capture,
  handoffs, kick sources), and `Universe::prune`'s guard `before = (now − keep).min(oldest − 2²⁶)`
  only forgets segments strictly older than any such query can need — the floor protects nothing the
  guard does not already protect. This is the claim's load-bearing prediction: a single digest move
  kills the deletion.
- **P2 (engine serves).** Engine-side retired serves occur between gathers (the checker saw
  7,040–22,591 per interval) and their count is **identical** across the toggle at every cut (no
  engine query ever lands in a pruned era) — the engine never reads what the deletion removes.
- **P3 (view serves and misses).** View serves exist with the floor on (the scout's 714–21,561 per
  gather) and **drop to near zero** with the floor off at steady cuts; the view-miss counter picks
  up the difference (the same queries now refused). Just past the wave (15k) the in-window segments
  are still served in both builds, so the delta there is small.
- **P4 (degradation, the honest risk).** I expect (a) to hold at most cuts — a vanished emitter
  needs its retarded read to fall entirely before its oldest retained segment, which for most bodies
  still holds at `d/c` behind now — but I am not confident: bodies whose `keep` window (p50 2.8 ks)
  is far shorter than their view lag (the scout measured served eras at the full kick interval,
  28.1 ks) may lose the containing segment entirely and vanish. For (b) I expect shifts of order the
  pending half-kick over the read gap (the tube-alone error the ramp exists to remove): belt kick
  impulses are ~2⁻²³ of orbital speed, so |Δoffset| should be ~10⁻³ light-seconds or smaller — but
  whether that is inside every body's radius depends on the body (a ship's radius is far smaller
  than a planet's). I register 50/50 on D2 holding as stated; either way the max/p99 shift in
  light-seconds and the vanished-id count are the reported numbers.
- **P5 (the cut).** D3 holds: ~1.05 → ≤ 0.15 segs/body at 32k–60k; at 15k (just past the wave) both
  builds still hold ~1 segment/body (the in-window transient).
- **P6 (warm loop).** Warm gathers (30 iterations, one persistent cache) serve fewer retired reads
  per gather than the first (the crossing memo shortens Newton walks), in both builds; the per-gather
  warm serve count with the floor off is ≤ the floor-on count at every cut.

Kill criterion for the claim (registered): D1 fails → the deletion is refuted (the floor is a law
requirement, not a memory pin). D1 holds but D2 fails (emitters vanish or shifts exceed the body's
own disc) → the deletion is outcome-free but not view-free: the standing cut survives only behind a
view change (the tube-alone fallback is already the shipped behaviour for unreadable steps, but a
vanished emitter is a new visible artefact) — reported as a blocker, not an adoption.
D1+D2+D3 hold → the ~10× standing cut is adopted within one step (one predicate in `prune` +
`droppable_until`).
