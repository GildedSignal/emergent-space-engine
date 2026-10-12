Grade: silver

**Abstract.** Claim: at canonical μ=1e-3 the belt's (E,L) key process is diffusive below q ≈ element range (order μ), so the exact memo cannot pay anywhere; compile load is uniform (top-5% ≈ 7% of keys); a separation-growth classifier ranks work (ρ = 0.74) where time-averaged resonance distance cannot (ρ = −0.05). I reproduced m1m, mu0, m3e3 and m3e4 **bit-for-bit** from the shipped `belt.py` (max diff 0.0 in every stored field) and re-derived every table row. Adversarial: μ=1e-6 is regular with range ∝ μ (mechanism confirms); T=6000 keeps churn@1e-5 = 100% and load uniform at both μ; e0=0.2 is more chaotic but the instrument NaNs there. Deletes smart-memo-key builds; hands B18b/H_live a floor (~1 key/orbit/body). Adoption cost ≈ none.

## Reasons

**Reproduction.** Clean reruns of the dossier's commands: m1m, mu0, m3e4, m3e3 all regenerate the stored JSONs exactly (max |Δλ̂| = 0, Δ anything = 0). Every dossier number I recomputed from the stored JSONs matches: P2 (44.6% / 5.4% / 50% mid), churn ≥ 0.5 = 81/100/100% at q = 1e-4/5/6, top-5% shares 7.0/5.4/5.4%, ρ = 0.737 / −0.738 / −0.052, median rel range 1.12e-2, seed-11 row 41/4/78/100/7.2, m3e4 row 34/39/46/98/10.7, m3e3 row 62/0/100/100/5.7. μ=0 control: revisit 1.000 everywhere, distinct2 = 1, λ̂ max 6.3e-4 (the disclosed shear bias).

**Predictions.** `predictions.md` (23:17:22) predates the decisive run (m1m.json 23:18:43); held-outs ran after and were disclosed as such (23:22–23:28). The author honestly reports P2/P3/P5/P6-d_res/P7 failing and P4's factor-3 clause failing; the kill criterion pre-anticipated the negative result. This is the pre-registration working as intended.

**Adversarial (mine).**
1. μ = 1e-6: fully regular (revisit 1.00 at 1e-4, 0.87 at 1e-5; median range 3.2e-5 ≈ μ) — the dead-zone mechanism (range ∝ μ) confirms at a third μ; the claim's scoping to canonical μ is honest.
2. Canonical μ, T = 6000: rev<0.05 = 0.42, rev>0.8 = 0.10, churn@1e-5 = 1.00, top-5% = 7.7% — the core claim holds at doubled horizon.
3. μ = 3e-4, T = 6000: the regular sea *grows* (rev>0.8: 39→50%), churn@1e-5 stays 0.97 — regime fractions are horizon-conditioned; single-horizon fractions (including the canonical ones) should not be read as asymptotic.
4. e0 = 0.2 (the author's own unrun P8 case): 77% chaotic, churn 97/100, load still uniform — direction as predicted, but λ̂ goes NaN for one body and the key cast emits a RuntimeWarning: the instrument does not survive its own predicted adversarial case cleanly.

**Record gaps (why silver, per this lab's own taste log: most silvers fall short on the record, not the physics).**
- `belt.py` was edited at 23:26:45, after the decisive run, and `m3e3.log` carries the pre-fix crash traceback (complex `a_mean` for hyperbolic bodies); the fix is undisclosed in the dossier. I proved it immaterial — the shipped file reproduces the pre-fix m1m/mu0 bit-for-bit — but an undisclosed mid-series edit is exactly the class the 5 October lesson flags.
- The "ejected/escaped" column (35/31/64/3) is not regenerable from the stored artifacts under any definition I tried (best proxies: 33/27/~50/~1); no definition is committed.
- Walls are misstated: "70–80 s each" vs 122.9/128.8 s in the held-out logs.
- "Co-orbital → 100% chaotic" rests on n = 1 body (bins 0.86–1.17 are empty); not disclosed. "Steady state" is generous with ~31% escaped at canonical μ.
- The ρ = 0.74 classifier headline runs on a λ̂ dynamic range of 6e-4 → 1.06e-3 (disclosed), i.e. near-binary saturated-vs-not; the ranking claim is weaker than it reads.

**Novelty.** H0212/H0213 (5 October) already measured the plane's exact memo hitting 0% on distinct kicks, and the 6 October gold killed memo deferral. What is new here: the belt scene (B18b, frozen H0214), the physical mechanism (element diffusion with range ∝ μ, verified at three μ), the uniform-load/no-concentration allocator fact, the H_live distinction-rate floor, the B12 slow-diffusion trap, and the averaged-resonance misallocation result (ρ = −0.05). No HISTORY entry measures belt key dynamics.

**Goal fit.** Board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" — this run measures that rate (~1 key/orbit/body at canonical μ). PRINCIPLES #3 "Compute only surprises" and #22 "the simulation decides; heuristics schedule" are both served; the negative result deletes a component path (smarter memo keys) rather than adding one.

## The one experiment that would make it gold

One committed regeneration pass: a single script that emits **every** dossier number from the shipped code — including a defined escaped count — plus an instrument hardened for e ≥ 0.2 (guard the key cast and λ̂), and one saturation-free check of the ranking claim (renormalized shadow pair or T = 3×10⁴) confirming ρ(λ̂, churn) ≈ 0.74. The physics is already gold-grade; the record is not.

## What the author missed

- Horizon dependence of regime fractions (my T = 6000 runs: regular share rises at both μ; the m1m numbers are T-conditioned).
- The instrument's failure at its own predicted e0 = 0.2 case (NaN λ̂, invalid key cast for escapers).
- The escaped column and the co-orbital zone statistic (n = 1) presented without the definitions/counts that would let a reader regenerate them.
- Per-kick key dynamics within one orbit (admitted in the lens note) — the per-orbit sampling bounds churn from below; the plane's 99%-per-kick is the upper bound, and the gap is unmeasured.
