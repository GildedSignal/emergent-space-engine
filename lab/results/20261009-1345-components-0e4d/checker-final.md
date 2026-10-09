Working...
Check complete: `Grade: silver`, written to `lab/results/20261009-1345-components-0e4d/check.md`. Tree restored (scratch tests removed, patch re-appliable from `work/patch.diff`); nothing else in the run folder touched.

**What held:**
- Parts B/C reproduce **bit-for-bit** (488,004 / 945,208 entries at 2²⁰, ladder 610,178/697,679, crossover 61,721→5,587→863, weak 989/1,025, sizes and knot counts exact) — the memory-bomb measurement is solid.
- Predictions pre-registered (13:59:21 < 14:00:50); #1 and #4 held exactly; #2 and #3 failed with the author's own kill criteria firing and both self-reported.
- My adversarial probes **strengthened** the core: the waste band is real (a p 65536–98304 belt pays the same 488,004 entries at q≈1.5×10⁻⁵, 20× below the tolerance), formations collapse it (3,212 entries), and a factor-16 belt widens it (880k codes at 2²⁰).

**What broke:**
- **Part A (the floor table) does not regenerate from the shipped patch**: evidence says scale-11 → 3/256 over, shape-10 → 213/256; the shipped code prints 15/256 and shape-10 → **0/256**. Deterministic across reruns, so the recorded table came from other code — the exact "unregenerable record" defect from the taste log.
- Fresh 2048-key sampling still confirms both axes near-tight (scale-11 fails 8.5–9.3%, shape-10 fails 51%), but the 256-key max-statistic misstates tail rates, and the 12/12 margin is 1.7×, not the recorded 2.9×.
- Gate labels: "B1/B2" don't exist in the frozen list — the tolerances are G1/G2's.

Gold path: the compactness-quantum sweep on the confirmed waste band with a regenerable, ≥2048-key record — collapses ~488k→~1k entries per belt on that band in one `orbit.rs` change.
