Grade: silver

**Abstract.** Claim: a scar is a bounded state-delta saturating at ~one key word per scarred body, so floor = 0.13 + f_x×35 bits/body and 10⁹ fit in 8 GB (4.4 GB worst). Reproduced bit-identically (C7, C8; C1 identical on all physics numbers); predictions.md genuinely predates every decisive run (mtimes). I extended the chain 5×: saturation holds (log2|kE| 33.84→34.08 over 2000 steps, decelerating; second seed identical; at 10⁻² M☉ survivors sit at 35.1, 18.6% escape). But the saturated (kE,kL) **pair** costs 70.1 bits (p90 71.8) on the author's own grid — the 35-bit headline counts E only; 35 holds by construction on law.md's 32-bit joint (E,L) key, not on the instrument used. Premise kill (no event log) is real; the floor constant is key-packing-dependent and Δt_p unmeasured. Adoption: one experiment.

## Reasons

**Reproduction.** Clean scratch tree, empty patch.diff, `python3 scar_floor.py cfg_cN.json out_cN.json` / `chain.py`: out_c7, out_c8 bit-identical; out_c1 identical on every shared field (author's file predates the `poisson_var_mean` field — code evolved after C1, additive, undisclosed but harmless). All commands ≤ 12 s, ≤ a few hundred MB. Dossier numbers spot-checked against outputs: C1 0.1597/0.998, C7 33.79→33.84/25 enc/0 escapes, C8 0.73425/33.10, C3 zero, ship–ship 0.0162 key units at 10⁶ kg·1 km — all match.

**Predictions.** mtime 11:16:05; every decisive config (C2–C8) later; smoke/C1 before, declared as calibration. Scoring in the dossier is honest: C3 exact-zero hit, C5 ×1.18, C6 0.7%, ship–ship hit; C2 15× and C4 15–50× misses traced to one named error; the failed Poisson control (var/mean 5.15) correctly demoted from prediction to finding (conjunction locks cluster encounters — so the event-log cost model was the wrong model). Prediction 7b (C2 < 30 bits/body at 10⁴ orbits) only passes under the saturation hypothesis; on the pair-grid it is ~50 bits.

**Adversarial (mine, on the author's exact code extended with kL).**
- Long horizon, N=2000×2000 steps: log2|kE| 33.85→34.08 (slope −4× from the first half, +0.056 bits/500 steps and decelerating; random-walk benchmark +1.41 bits). Saturation is real, not a window artifact.
- Seed 72 = seed 71 (33.837 vs 33.841 at step 400).
- m_p = 10⁻² M☉ (10× the grid): 18.6% escape (leave the store), survivors bounded at kE 35.1 / pair 72.2. Extremes do not break the bound.
- Mechanism exposed: in-belt fraction collapses to 0.2% by step 400 (0.15% at 2000) — saturation works by **evacuating the feeding band**; the belt self-destructs in ~10³ orbits at this secondary mass. The "self-limiting rate" (0.018/or) is a transient decay, not a steady state. The per-body bound survives regardless (a delta cannot exceed the key width), which is the load-bearing half.
- Impulse regime: at 2 r_H with 10⁻³ M☉ the deflection is θ ≈ 0.5–1.9 rad — outside the small-angle impulse approximation, and sub-Hill-speed shepherding is unmodelled. Rates and f_x are regime-specific; the bound is not.

**Novelty.** No scar-half floor exists anywhere: law.md §13 has the store shape (program + scars, Opus, H0210-era); components-98bc measured only the program half (0.126 bits/body, quoted, disclosed); H0173's ~4 bits/collision is the lattice-contact regime, correctly cited as different. This run supplies B18's missing floor law. Goal fit is exact: focus item 5, plane.md line 36 verbatim, PRINCIPLES #24 ("the memory floor is information theory"), #6 (the scar is a delta against the generator).

**Why not gold.** The headline constant conflates two grids. The instrument quantizes E and L each at 32 bits (64-bit total) and measures only kE; on it the saturated scar is ~70 bits/scarred body → worst case 0.13 + 70 ≈ 8.8 GB at 10⁹ — **over** budget. The 35-bit figure is true only on law.md's 32-bit joint (E,L) tube key, where |Δkey| ≤ 33 bits by construction — i.e., the floor constant is set by the law's key width (a design choice this run never measures), while the physics contribution is f_x and the saturation. Adopting `floor = 0.13 + f_x×35` into B18 as-is gates on a number whose own run contradicts by 2×. The 64-bit Δt_p field (the Tube's timing word) is unmeasured; the ~8-bit proxy may understate by tens of bits.

## The one experiment that makes it gold

Re-measure the saturated scar on the store's native representation: chained runs (≥ 2 seeds, m_p ∈ {10⁻³, 10⁻²}, ≥ 2000 steps) with the scar as Δ of the per-band quantized 32-bit joint (E,L) tube key plus the Δt_p field, reporting floor = 0.13 + f_x × (key width + index + measured timing bits). Then the B18 floor is representation-native and the 8 GB worst-case verdict is honest in both directions.

## What the author missed

1. kL is never measured in the chained runs; the pair costs 2× the headline, and the key packing (32-bit joint vs per-component) alone decides whether the 10⁹ worst case is 4.4 GB or 8.8 GB.
2. Saturation's mechanism is belt evacuation (in-belt → 0.2%): the scene is a transient that empties, so the measured 0.018/or "chained rate" is not a steady-state number for a maintained game belt; only the per-body bound transfers.
3. The transient-growth claim "≈ 4–5 bits per distinguishable encounter" is a cross-entropy consistency remark, not a measured slope (measured: ~0.03 bits/encounter once saturated; H_cond 2.1 bits per correlated kick).
4. Post-saturation drift is small but nonzero (+0.65 bits over 1600 steps); the per-band rebasing named in the lens section is what makes the bound exact and belongs in the floor law, not a caveat.
5. out_c1.json could not have been regenerated by the shipped scar_floor.py (poisson_var_mean field) — regenerated numbers match, but the shipped-code-regenerates-the-record rule (5 October taste log) demands a rerun or a note.
