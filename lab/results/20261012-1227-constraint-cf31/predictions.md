# Predictions (written before the decisive probe)

The claim to test: **the light-cone crossing search is the constraint inside the view gather**
(61–74% of every frame's CPU on the plane as flown), not the engine.

Probe: replace each body's `crossing(...)` Newton search (readouts at retarded ticks) with a
single read at the presented tick `t_now` (no light delay). Everything else identical. This
changes the view's content (positions are no longer retarded) but not the engine digest.

Held-out cases (not tuned on — the runs so far only measured the intact system, rtf 1/100/1000):

1. **rtf=100, 20 s:** view_gather p50 falls from ~3.6 ms to **under 0.6 ms** (≥ 5× drop).
   If it stays above ~1.5 ms, the cost is not the crossing search but the per-body plumbing
   (binding_at walk, push closure, allocations) and the constraint statement is wrong as named.
2. **rtf=1000, 20 s:** view_gather p50 falls from ~6.0 ms to **under 0.9 ms** (the readouts/seen
   ~2 factor at rtf 1000 should vanish with the search: exactly one read per body).
3. **rtf=1, 12 s:** view_gather p50 falls from ~2.4 ms to **under 0.4 ms**.
4. **Constraint moves:** with the crossing gone, the engine becomes the largest share of the
   frame at rtf ≥ 100 (engine p50 ≥ view_gather p50 there). At rtf=1 the frame becomes
   JSON/wire-dominated (the engine is only ~0.14 ms there).
5. **Digest unchanged** by the probe (the view is a pure read): same cut_tick, same digest at
   every rtf as the intact runs.
6. **Per-body floor:** with the search gone, the bodies loop still costs **3–15 µs per body per
   frame** (one `state_rate` up the doll chain + push). If it is ~0, the search was the whole
   cost and even the read is free — that would instead point at the Newton iteration as the
   only lever.
