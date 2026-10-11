Working...
Check complete. `check.md` written; nothing else in the run folder touched.

**Grade: silver** — real physics, partially broken record.

**What reproduced (scratch copy, `python3 falsifier.py`, 26 s):** every key the shipped `main()` writes regenerates **bit-for-bit** — 730/730 classification with 0 mismatches, all six accuracy sectors, negative control, near-radial table, horizon slopes, 24/24 kicks at 8.1e-12.

**What I confirmed beyond the author:**
- Independent 1461-seed classification sweep (L² across the barrier-existence boundary 12, δ down to 3e-9, starts hugging every root): **0 mismatches** — the root-structure rule is exact algebra.
- Near-radial anchored partner on my own grid (E²∈{0.5,0.9,0.99} × L down to 3e-7): 8–32 panels, ≤1.5e-11; literal pairing fails as claimed.
- Valley panel counts 43/83/133/205/3765: exact, via the shipped-but-never-called `separatrix_cost()`.

**Why not gold:**
1. **The documented command does not regenerate the stored metrics.json.** Two evidence blocks — the valley counts and the bound control — are written by no shipped code path. The bound-control block is dead code (apoapsis-start oracle hits `ev_turn` before `ev_plunge` on every seed; `eta_of_r` also returns `None` near-circular). My fair reconstruction gives 3.4e-8, not the stored 3.2e-12 — substance corroborated (converged at 8–16 panels, phase flow validated against parametrization-free quadrature), digits not. This is the taste log's named silver-killer.
2. **The P7 kick headline never probes the valley.** The 24 kicks sampled δ ∈ (1e-6, 1e-2) uniformly — worst recorded δ ≈ 4.4e-4. My valley kicks at 64 panels: δ=1e-6 → 1.8e-3, δ=1e-8 → 0.30. The "kick across the separatrix the plane refuses" holds only for kicks clearing Vmax by ≳1e-4.
3. P1 promised ≥2000 seeds, ran 730, undisclosed (my sweep closes the gap).

Novelty and goal fit are clean: ENVELOPE.md:94 and HISTORY:3176 record the plunge gap; the cosh extension of the law's own `space-darwin16-v1` machinery is new, and bound/plunge differ only in φ(η) — principle 19 satisfied in the strong direction. The one gold experiment: wire `separatrix_cost()` into `main`, fix or drop the bound control, and judge valley kicks (δ ≤ 1e-6) on the law's **fixed** integer cuts rather than adaptive float bisection.
