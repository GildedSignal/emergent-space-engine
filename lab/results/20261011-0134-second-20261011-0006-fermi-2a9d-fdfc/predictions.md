# Predictions (written before the decisive run)

Question (the checker's named gold experiment): as a **totals comparison** — re-fit +
canonical relabelling of unobserved bodies (label cost = 0) versus entropy-coded frozen
program, both under a realistic 1/b² encounter tail at belt rate — what actually bounds
H_live, and does the relabelled floor hold at 10⁹ scale with m sized from the spread?

Model (the author's, unchanged): N = 2²⁰, one element column, λ = 1, diffusion
s = 1 cell/orbit, encounter rate r = 2.135×10⁻³/body/orbit (r8 v2 belt 0), T = 8192,
checkpoints at every power of two. Jump laws (median-matched |Δ| = 100 cells, physical
cap 10⁴ cells, symmetric sign):

- **G** (control): the author's Gaussian, J = 100. Must reproduce their results.json
  run 1 bit for bit (same seed, same draw order).
- **T1** (physical areal 1/b impulse): P(|Δ| > x) = (Δ_min/x)² on [Δ_min, 10⁴],
  Δ_min = 100/√2 (median 100). Clip mass 5×10⁻⁵. **E[Δ²] = 5.45×10⁴** (5.5× the
  Gaussian's J²).
- **T2** (the checker's literal law, |Δ| = K/U², U ~ U(0,1)): K = Δ_min = 25 (median
  100), clipped at 10⁴ (a 5% point mass at the cap = grazing encounters saturating).
  **E[Δ²] = 6.67×10⁶** — the checker's 6.6×10⁶ reconstructs exactly once the clip pile
  at the cap is counted (1.67×10⁶ continuous + 5×10⁶ in the pile).

## Held-out predictions (no retuning after this file)

**P0 — tail moments** (1-verification by 10⁷-draw MC inside the script): T1 E[Δ²] ∈
[5.2, 5.7]×10⁴, median ∈ [95, 105]; T2 E[Δ²] ∈ [6.5, 6.9]×10⁶, median ∈ [95, 105].

**P1 — reproduction**: G matches all 14 author checkpoints to <10⁻⁹ bits (frozen
2.1395 → 10.7868; resid m=256: 2.2532 → 6.3162; label 1.7555 → 10.7853; ever_hit 1.0;
H_delta 2.1047938061630695).

**P2 — frozen/label under the tails** (CLT form H ≈ ½log₂t + C with
C = log₂(4.13·σ_orbit), σ²_orbit = s² + r·E[Δ²]):
- T1: C = 5.49 → frozen(8192) = 11.99 ± 0.6 bits; slope over [2048, 8192] ∈ [0.42, 0.60]
  bits/doubling; 16-bit label deadline 2.1×10⁶ orbits (range [10⁶, 4.5×10⁶]).
- T2: finite variance ⇒ asymptotic C = 8.95 (deadline 1.8×10⁴), but pre-asymptotically
  the 5% cap-pile makes the marginal a mixture (59% of bodies carry ≥1 cap jump by
  t = 8192): frozen(8192) ∈ [15.0, 16.5] bits, slope ∈ [0.9, 1.6] bits/doubling,
  16-bit deadline ∈ [6×10³, 1.5×10⁴] orbits. **This adjudicates the checker's "~10⁴"
  against the author's 1.2×10⁷.**
- Label tracks frozen within 0.15 bits at both tails (λ = 1), as in G.

**P3 — the relabelled floor** total(t) = min_m [resid(t, m) + 32m/N], m ∈ {256, 1024,
4096, 16384, 65536, 262144}:
- G: floor(8192) ∈ [2.8, 3.8] bits at m* = 65536; T1 ∈ [3.8, 5.2]; T2 ∈ [7, 12] with
  m* ∈ {65536, 262144} (heavy tail needs more knots; program cost 32m/2²⁰ starts to
  bind at m = 262144: 8 bits).
- Bounded in t: floor(8192)/floor(1024) ≤ 1.5 for every law (growth is table
  resolution, absorbed by sizing m with the spread; m*(t)/σ̂(t) roughly flat).
- At 10⁹ bodies (program cost 1024× cheaper, = 32m/2³⁰ ≤ 0.008 bits): floor =
  resid(262144) ≤ 8 bits/body for G and T1, ≤ 9.5 for T2. **This is the adoptable
  number the checker asked for.**

**P4 — the totals verdict**:
- No-relabelling re-fit total (resid(m*) + label + program) ≥ frozen total at every
  checkpoint, every law — the checker's refutation extends to both tails.
- Relabelled total < frozen total for t ≥ 128 in every law, with the gap growing
  (½log₂t-ish; faster under T2).

**P5 — the budget restatement at 10⁹, 3 walking columns** (arithmetic on measured
constants, budget2.py):
- The 62-bit record format breaks at t = 0 (7.75 GB): the format is the problem, not
  time — retiring the author's "~350 orbits" framing.
- Entropy-coded frozen: 4.05 GB (G) / 4.5 GB (T1) / 5.97 GB (T2) at t = 8192; it
  breaks 8 GB at ~1.8×10¹⁰ (G), ~3.5×10⁹ (T1), **~5.7×10⁷ orbits (T2)** — the
  checker-heavy tail breaks it inside a 10¹⁰-year universe.
- Relabelled re-fit: flat ≈ 3 × floor ≈ 24 bits = 3.0 GB under T2, never breaks.
- So the binding deadline is the **relabelling law decision** (16 bits/column of label
  at ~10⁴ orbits under T2, ~2×10⁶ under T1), not the gigabyte line; and the author's
  "not urgent" survives only under the Gaussian tail. Which tail the engine really has
  is b-h-live's first measurement (the engine's own kick sizes in cells).
