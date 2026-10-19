# Predictions (written before the flights)

Lens: library. Bottleneck: nladder (28 → 10⁹); the page's freshest measured fact (7b6f,
gold, checker note) is that at 2×10⁵ the next wall is COMPUTE: "at 2×10⁵ the first kick wave
costs 1.2–1.3 s frames on this box (max_ms 1,286–1,312, over=35–133) — the next wall at that
rung is compute, not memory." That observation has never been decomposed: is there ebb (idle
frame budget) to harvest, and is the spike a burst of arrivals or a per-frame drift?

Probe: shipped `nladder` flights, burn, rtf 2000, 12 ms budget, ~25 s wall each, at
N = 10⁵ and N = 2×10⁵ (sequential, Linux box, timeout-capped; print-only). The shipped
`ladder:` line already reports p50/p99/max engine ms, over-count, and the worst frames with
their event counts — the decomposition is read, not patched.

Cases NOT tuned on (first flights of this rung on this box):

- **P1 (the ebb exists):** at both rungs, engine p50 ≤ 3 ms — ≥ 75% of the 12 ms budget is
  idle outside the waves. (Ground: at 3×10⁴–10⁵ the pages record "frames mild", over counts
  of 66–102 out of 200–336k frames.)
- **P2 (the spike is clustered, not smeared):** over-budget frames cluster into ≤ 3 windows;
  the first window alone holds ≥ 50% of the over-count.
- **P3 (the spike is arrival-driven):** the worst frame's event count is ≥ 20× the p50
  frame's event count at the same rung (a burst of due work, not uniformly slower frames).
- **P4 (the spike scales with K):** max_ms(2×10⁵) / max_ms(10⁵) ∈ [1.5, 8] (7b6f checker:
  ~1.3 s at 2×10⁵; taleb-6138: 322 ms at 10⁵ → ~4×; I predict the same order, not exact).

If P1 and P2 hold, the allocator decision changes: the wave is harvestable from the ebb
(known-due work moved into idle frames), and the cheapest next rung is a compute-ahead arm,
not a cheaper kick. If P1 fails (p50 near budget), no ebb exists and the only lever is
deleting arrivals (stagger); that would invert the lesson order (delete-first becomes the
only lesson).

What would make the probe void: RSS growth on this shared box forcing an early stop before
the first kick wave (mitigation: 25 s wall cap, timeout, sequential flights; wave onset at
gs ≈ 11–16k ≈ 8–11 s wall at rtf 2000).
