Working...
Check complete. **Grade: gold** — written to `lab/results/20261012-0311-second-20261012-0138-taleb-74a1-4ec3/check.md`.

**What I verified:**

1. **Reproduction, byte-exact.** Clean rebuild, all nine probe cases + `cargo test` (10/10): every substantive line of `run-log.txt` regenerates identically modulo wall-clock times. The nine physics sources are byte-identical to `adce00d6`; `/tmp/orig-probe.rs` is a verbatim prefix of the shipped probe, so `probe-second.diff` is exactly the two additive cases. Only nit: "all ten sources" counts the adapted `Cargo.toml`.

2. **Provenance.** `predictions.md` 03:21:44 → disp2 03:22:08 → blob 03:25:41; probe.rs's touched mtime restored to its original nanosecond value. The model column and all quoted slopes/fractions/ratios reproduce exactly from the stated parameter-free formula; ladder deviations −9.8%…+6.2%, all inside the pre-registered ±10%; the one slope edge miss (0.927 vs 0.92) is disclosed and model-consistent.

3. **My attacks.** (a) ρ=1e-3 crossover on my own scene: model/measured 0.949–0.997 — the crossover formula generalizes beyond the author's ρ. (b) e=0.3 shared-shape ladder, brute-verified: 1350/1350 blob contacts found, zero above ρ. (c) Mixed shapes (random e≤0.02, ϖ) — the author's admitted kicked-tube blind spot: **0 missed** but the window already sits at the n²/2 ceiling, so sub-ρ near-tightness is a shared-shape result; sound, and the silver's occupancy gate catches it (my max_k ≈ n−1). (d) A tube-crossing construction seeded no contacts — weak test, not counted.

4. **Novelty/goal fit.** New measurements (unsaturated transition, blob safety, prediction-4 re-adjudication), absent from HISTORY and the board; it makes the 6 Oct gold's adopted certificate's gating rule cheap to choose — the board's top scaling risk.

Nothing else in the run folder was changed; no git writes.
