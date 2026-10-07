# Predictions — 20261007-1801-fermi-bb60 (written before the decisive run)

All constants come from repo evidence (none tuned on this machine); the only new measurements are three micro-benchmarks on this Linux/x86 box, reported per core, orders of magnitude only.

## Micro-benchmarks (this box, single core)

- P1 — integer fold floor (two fixed-point u64 updates with u128 products + one binary-heap push/pop, the designed kick's arithmetic + queue reschedule): **100–1,000 ns per op**.
- P2 — sequential bandwidth on 1 GiB: **5–30 GB/s** single-thread.
- P3 — random 16-byte read-modify-write over a 1 GiB array (a tube update in a 16 GB store): **50–200 ns per op**, i.e. ≥ 30× dearer than sequential, giving ≤ 2×10⁷ such updates/s/core.

## Budget decomposition at N = 10⁹, M1 (8 GB, ~10¹⁰ ops/s, 60 GB/s, ~5 effective performance cores, 4 GiB state budget, RTF 100, 3,600 s session)

- P4 — claim check: re-deriving the board's "about 190 cores at 10⁹" from 32.5 kicks/orbit (K1), a 5,400 s low orbit, and the plane's 29 µs kick lands within **2× of 190** (I compute ≈ 175; H0190's own economics row extrapolates to 600 — same wall, one order).
- P5 — adversarial scene (all 10⁹ bodies strong-tide low-orbit, unaveraged K1 cadence, today's 29 µs events): compute is **over budget by ≥ 10³×**; even with a free 200 ns fold it stays **≥ 10× over** — unaveraged 10⁹ strong-tide bodies are dead on compute alone.
- P6 — same scene with K2 averaging (0.285 kicks/orbit, 114×) and a ≤ 1 µs fold: compute **≤ 3 effective cores at RTF 100**, i.e. fits.
- P7 — galaxy scene (10⁹ belt/population bodies + 10⁶ fleet ships strong-tide + player): every wall — compute, bandwidth (sequential and random-access), memory, H_live — holds with **≥ 2 orders of margin**, even charging every one of the 10⁹ far bodies the full K2-averaged LEO kick rate (an unmeasured, generous upper bound; the true belt rate is a lead).
- P8 — H_live: with kicks folded into tubes (rebinding with remainder carried), net new state is encounters + contacts + decisions ≈ **≤ 10 bits/s wall** at 10⁹ — bounded by ≥ 5 orders. Scars-instead-of-folds stays bounded below a strong-tide population of ~10⁷ (≈ 0.6 GB/hour at 10⁷), and breaks (≥ 34 GB/hour) only at ≥ 10⁸ strong-tide bodies — the fold-vs-scar choice matters only on that frontier.
- P9 — any per-tick full-state sweep at 10⁹ (16 GB of tubes) at 60 Hz demands ~10¹² B/s: **≥ 10³× over** the M1's bandwidth; event-driven is not a preference, it is the only architecture inside 3 orders (principle 14 quantified).

## What would falsify the decomposition

- P1 measuring > 10 µs/op (the fold is not µs-cheap → averaging alone cannot save 10⁹ strong-tide bodies at RTF 100).
- P3 measuring < 10× dearer than sequential (then the random-access wall I claim in P5/P6 is overstated).
- Any wall in P7 within one order of its budget (then the "≥ 2 orders of margin" headline is wrong).
