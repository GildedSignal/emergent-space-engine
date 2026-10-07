# Dossier — 20261007-0933-second (second author on 20261007-0842-fermi-fc22)

## Claim

The checker's named experiment is done: on a live belt built from the shipped machinery with the far quantum in force, the flux model reproduces the measured element-word-write rate with no fitted constants (ratios 1.05–1.47, exponents N^1.07, m^1.13), the 32× closes as a cross-section-form artifact (the rung belt is planar, the model's P6 used the 3-D tube) plus a rate remembered from a different belt (6.0× × 5.3×), and the original claim then **holds in 3-D** (18 KB/game, ~50× margin) but is **refuted for planar belts** — every belt the engine ships today — where the same anchored machinery gives ~209 MB/game and 31 writes/s at 10⁹ at the dossier's own belt parameters: ~200× the claimed ≤ 1 MB.

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; the checker's "one experiment to gold": count element-word writes and recertifications per game-second on a live belt, reconcile against the flux model, closing the 32× with an engine-side measurement.

## Evidence

Machine: GitHub Actions runner, Linux x86, 8 vCPU, load 0.2–0.9, ~13 GB free. All commands from the repo root; each ≤ 40 s except the m=10¹⁹ rung (352 s, backgrounded).

Record regeneration (the silver's gap "results the shipped code cannot regenerate" does not exist here):
- `python3 lab/results/20261007-0933-second-20261007-0842-fermi-fc22-a7d0/ledger.py` → `ledger-out.json` **bit-identical** to the author's (0.4 s).
- `cargo run --release -p emergent-universe --example plane -- 100` → `bytes/body 2349`, N = 28 — exact.

**Part A — the 32× (shipped `verify`, massless planar rung belts, exact truth).**
`cargo run --release -p emergent-encounters -- verify a` → `verify-a.json`. Encounters per body per orbit: 1.75×10⁻⁴, 6.8×10⁻⁴, 1.89×10⁻³, 4.96×10⁻³ at σ_e = 10⁻³…3×10⁻² (ρ = 10⁻⁴) — exactly linear in σ_e. The 2-D strip form at the belts' own geometry (σ_n = N/2πāw, w = 0.5) is 1.4–1.9× over measured (one empirical constant, v_rel,eff ≈ 0.6 σ_e); the 3-D tube form (P6's, true width) is σ_e-independent and lands 4.3×–123× under, ∝ σ_e. **The 32× = 6.0× (tube form + width guess on the s1e-2 belt: measured 1.89×10⁻³ vs P6's 3.14×10⁻⁴) × 5.3× (the remembered 10⁻² belongs to a ρ = 10⁻³ or σ_e = 3×10⁻² belt, not this one).** The gap was never a wrong rate constant.

**Part B — the live belt, far quantum in force** (`sim/`, a standalone crate on the shipped `make_belt`/`Body`/`cone_pairs`/`pair_events`; no crate files touched). Belt: planar, a ∈ [1, 1.5], σ_e = 10⁻²; drift = exact Kepler (the law's tube); every pair event with b < b_cap = 10·b_q applies a symmetric hyperbolic impulse (saturated at |δv| = v_rel below b_90, clamped at contact radius), elements re-derived from state; quantum crossings of the accumulated kick vector at q = 10⁻⁶·v_kep counted with reset (the ledger model's own quantity). Commands: `cd lab/results/<this folder>/sim && cargo build --release` then `/home/glmlab/lab-target-0/release/livebelt <N> <m_kg> 20 1e-6 10 20261101 1e-2 1 1.5 2` → `sim-rungs.json`:

| N | m (kg) | crossings/body/orbit | model 4σ_nμ/q·2π | ratio | kicks/crossing |
|---|---|---|---|---|---|
| 2000 | 10¹⁸ | 6.75×10⁻³ (270) | 6.44×10⁻³ | 1.05 | 1.5 |
| 4000 | 10¹⁸ | 1.42×10⁻² (1133) | 1.29×10⁻² | 1.10 | 2.1 |
| 4000 | 10¹⁹ | 1.90×10⁻¹ (15178) | 1.29×10⁻¹ | 1.47 | 5.1 |

No fitted constants; scaling measured N^1.069, m^1.127. Regime signature: mean |δv| at crossing ≈ 5q and the planar rate is v_rel-independent and linear in m (no Coulomb log) — planar relaxation is threshold-dominated; the sub-quantum walk adds the 1.05→1.47 drift. Contacts 0–5 per run (negligible); no kick reached the saturation branch (b_90 ≪ b_min). Recertification cost, shipped: `cargo run --release -p emergent-encounters -- kick` → `kick.json`: 813 pairs/kick, 16.5–19.6 ms per recertification (n = 10⁴, ρ = 10⁻⁴, 1000-orbit horizon), slack certificates skip 57–95% of pairs at quantum-scale kicks.

**The claim at 10⁹** (`python3 lab/results/<this folder>/ledger2.py` → `ledger2-out.json`), the dossier's own belt (a = 2.5 AU, w = 1.3 AU, N = 10⁹, m = 10¹⁵ kg, q = 10⁻⁶ v_kep, 300-h game, 50 bits/write):
- **3-D:** 18 KB/game, 0.0027 writes/s — the claim holds with ~50× margin.
- **Planar:** 3.10×10⁻⁸ /body/s → 0.0335 crossings/body/game, **209 MB/game, 31.0 writes/s** — the "≤ 1 MB per game" headline fails by ~200×; recert compute ≈ 0.5–0.6 CPU-s/s at the shipped ms-per-recert (the known 12.6× slack skin would cut it to ~4%). Memory pressure is tier-level (scars stay bounded, one word per body); it is the ledger/bandwidth term that breaks.

## Predictions

`predictions.md`, written before `verify a` and the sim. Held: PA2-strip (within 2×), PA3 (linear in σ_e), PB1 (1.42×10⁻² in [4×10⁻³, 4×10⁻²]), PB2 (ratios 1.05–1.47 in [1/3, 3], flat within 2×; m^1.13 ∈ 1±0.25, N^1.07 ∈ 1±0.15), PB3 (threshold-dominated, mean crossing kick ≈ 5q), PB4 (planar 209 MB/game and 31 writes/s against the predicted 100–300 MB, ~30/s; 3-D ≤ 1 MB ✓). Missed: PA1 (measured 1.89×10⁻³, 6% below my [2×10⁻³, 1.2×10⁻²] band) and PA2's tube band (actual 4.3–123×, not 30–200×: the tube/strip ratio 4H/πρ is ∝ σ_e, not constant — my band was built on one belt's H).

## What would make it wrong

- The 10⁹ planar number is extrapolated on measured exponents from N = 2000–4000 (the exact pair machinery cannot enumerate 10⁶ candidates per window in 60 s; the shipped `scale`/`kick` experiments cover n to 10⁵ for the machinery, not the physics). A super-linear term in N (collective effects, resonances) would raise it further, not lower it.
- The 3-D ledger (P1) keeps its model status: Part B anchors the kick/crossing machinery in the planar regime; the 3-D cross-section is pinned only in direction (Part A). Its ~50× margin absorbs a factor-3 error; a lnΛ-scale miss would need >10×.
- Windows re-scan all candidate pairs; events of untouched pairs stay exact (Kepler), events of same-window kicked partners use pre-kick timing (staleness O(δv/v) ≪ b_cap). b_cap = 10·b_cap misses ~10% of the sub-q walk (inside the stated ratios).
- Gameplay distinction sources (wrecks, marks) remain outside physics, as in the original run.

## Cost of adopting

None to build; two design consequences. (1) Keep the kill of the scar-ledger track **in 3-D**; for planar belts — everything shipped today — the far quantum 10⁻⁶·v_kep does not hold the ledger at 10⁹: a planar 10⁹ belt needs either the coarse far quantum (rate ∝ 1/q), a 3-D store, or an accepted ~31 writes/s / ~200 MB-per-game ledger line in B18. (2) B18's belt rung (2²³, planar, per-body mass to be stated by the design) is the cheapest place to falsify this directly: predicted ledger rate there = 4σ_nμ/q, with the measured 1.05–1.47 correction band.

## Fit with PRINCIPLES

- "The memory floor is information-theoretical" — the floor's dynamics term is now measured, not modeled, in the regime the engine actually runs.
- "A fix signals the wrong representation" — the 32× was not a wrong constant but the wrong cross-section for the geometry measured; fixing the number without fixing the form would have been the bandaid.
- "Compute only surprises" — the write rate is threshold-dominated (1.5–5 kicks per crossing): almost every kick below the quantum is reabsorbed and never stored, as designed.

## The lens

The second-author lens inherits the checker's framing ("the plane or shipmem at 10⁶") and had to replace it: the plane is 28 bodies, shipmem has no dynamics, so the live belt had to be built on the encounters machinery at N where exact enumeration is possible. What it may have missed: collective/resizeant behaviour absent at N = 4000 with 20-orbit horizons, and the 3-D sub-quantum walk's lnΛ constant, which no planar measurement can anchor.
