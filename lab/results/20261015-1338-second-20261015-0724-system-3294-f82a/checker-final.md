Working...
Check complete. **Grade: gold** — written to `check.md`, one page correction applied.

**What I did:**

1. **Reproduced** via the runner's regen (exit 0) plus 11 of my own flights. Every deterministic number is exact: baseline = 3294 to the digit (29,143/29,143 fired, all dv ≥ 2⁷, wave-1 246.6/1,101.7 s, 10⁵ 99,712/99,712); dimensionless belt impulse 2⁻²³ (p01 2⁻²⁴, p99 2⁻²⁰) at both scales; stagger rate 1.000 in seven independent arm-runs with distributions unchanged; digest hashes `d5bc72b7`×3 / `5f3e8b42`×2 exactly as claimed.
2. **Adversarial cases (3+, one beyond the author's domain):** a quiet-load 10⁴ coast repeat (the regen's tail flip under load 2.8 was noise — the author's numbers reproduce at load ~1.1); **10⁵ burn, never run by the author** — the held pile stays (it's the player's doll's, confirming the decomposition) but the worst frame drops **820 → 35.5 ms (23×)**, extending the tail-deletion to the scale that matters; a 2× horizon — the staggered train holds 0.49–0.50·I through wave 5 while baseline shears 3×/wave; over-flown digest guard verified working.
3. **Predictions** verified pre-registered (file times 13:49 → flights 14:00+); prediction 1 failed by one octave in the strengthening direction and was reported as failed; the sharp structural prediction (0.494·I) held to three digits.
4. **Corrected the page** once: the "9–11 octaves" was the floor-kick/grid-kick ratio mislabeled as distance-to-binding; the honest number is 2⁷× finer than the grid, 16–18 octaves finer than the floor — substance unchanged and understated.
5. **Recorded differences:** burn digests were stable in my regen (author's disclosure over-conservative); stagger total fires track the wall-bounded horizon (rate always 1.000); 10⁴ max/over comparisons are load-noise both ways.

Gold because: a gold-record premise (the "one dial" tail third) is refuted by direct intervention, the worst-frame metric moves 23× at 10⁵ burn and held 154→1 at 10⁵ coast, and the change is a 15-line env-gated, bit-identical-off constant — adoptable in one M1 step (the B-gate delta flight, which can't run in this lab). Scratch files removed from the run folder; nothing else touched; no git operations.
