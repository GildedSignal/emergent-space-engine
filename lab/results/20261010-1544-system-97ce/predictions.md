# Predictions (written before the decisive run; plumbing run passed unseen)

Scene: 384-ship smooth belt (banded p 2.1–3.3 AU, Rayleigh e σ=0.1, uniform angles) in the star's doll, one Jupiter-like planet (5.2 AU, mass 2⁻¹⁰), 2 planet periods (~24 game-years), cadences 2⁷ and 2⁴ kicks/period.

The claim under test: the event stream (work) and the distinction stream (kicks whose rounded Δv changes a velocity quantum — live information) are two measurements of one scalar, and they separate: the event rate is set by cadence (a schedule choice), the distinction rate by physics (how fast the perturbation crosses the state's own quantum).

1. **Event rate scales with cadence; distinction rate does not.** At 2⁷ vs 2⁴, events per ship orbit drop ~8×; kicks with dv≠0 per ship orbit stay within a factor ~2 (prediction: not proportional to cadence — if it *is* proportional, the quantum-crossing count is numerical noise, not information, and the distinction notion dies).
2. **The waste factor is large at fine cadence.** At 2⁷ = 128 kicks/orbit I expect ≥ 5× more computed kicks than quantum-changing kicks for this belt (typical belt perturbations from a 2⁻¹⁰ planet at ≥ 2 AU separation are tiny per step). Fraction dv≠0 prediction: 1–30%.
3. **dv histogram is concentrated at ±1 quantum** (classes 0 and 1 dominate; ≥5 rare): the per-distinction information is ~2–3 bits (which component, which sign), not a wide distribution.
4. **Boundaries are pure work:** boundaries ≈ kicks in count (every step ends), all of them distinctions-free. Total work per distinction ≥ 2× the kick ratio alone.
5. **Memory extrapolation at 10⁹:** with the measured distinction rate D per body per game-second and h ≈ 2–3 bits/distinction, H_live from kicks = 10⁹·D·h bits/s. I predict this comes out < 1 MB/s (the belt's perturbation stream is weak), i.e. the kick stream is NOT what threatens 8 GB — the live record per diverged body is (≈ sizeof of tube+remainder ≈ 30–50 B × 10⁹ = 30–50 GB unless the population is re-programmed). If instead D·h lands > 100 MB/s, the kick stream itself is the memory killer and the two bottlenecks bind at the same cadence lever.
6. **Wall cost:** order 10 ms–100 ms per ship orbit per body at 2⁷; the two runs' ns/event within 3× of each other (same machinery).

Kill criteria for my own claim: if dv≠0 scales ∝ cadence (1 fails), or the histogram is flat across classes (3 fails), or D·h exceeds the live-record cost at every horizon (5's structure inverts), the "one scalar, two faces" reading is wrong and I report which.
