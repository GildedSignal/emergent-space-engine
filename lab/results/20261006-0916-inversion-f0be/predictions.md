# Predictions — inversion-f0be (written before any run)

Question (one sentence): the gold `20261006-0346-taleb-09b5` replaces the quadratic tier with a phase-neighbour "train" (sort by longitude, watch k≈4, rebuild on overtakes), triggered by the Binet-clump number — at what scene does that train itself break, and is that scene inside the trigger's selected regime?

The attack follows the gold's own "what would make it wrong": *"e-spread ≫ ρ could break phase-order = distance-order (rank inflation)"* and *"it needs a proof that co-orbital sub-ρ contact implies rank ≤ k under stated invariants, which I did not write."* The invariant it silently needs is local phase spacing s ≳ ρ/k; neither the Binet-clump trigger nor the rank measurement (deepest case: phalanx σ_λ=0.01, n_c=200 → spacing ≈ 1.25ρ) ever probed s < ρ.

**Instrument** (independent numpy, not the taleb binary): exact Kepler toy, a=1 all bodies (tighter than the gold's 1e-5 half-width — generous to the train: no drift, exactly periodic, one orbit = the whole horizon), ρ=1e-4 as in the gold. Truth contacts: λ-gated candidate set (λ-rank ≤ 2 at some sample OR sampled d < 4ρ) + two-stage refinement (steps ΔM/8, ΔM/128; ΔM = 2π/4096). Rank at contact = min over both directions of (a) distance-rank, (b) longitude-rank, at the refined closest-approach time, under *perfect* continuous maintenance (the train's best case). Misses = contacts with λ-rank > 4.

## Scenes

- **S1 control (must reproduce the gold):** n_c=200, e~Rayleigh(0.001), ϖ~U(−0.1,0.1), M₀~N(0, σ_M=0.01) wrapped — their deepest phalanx. Predict: max rank ≤ 4, misses 0. If this fails, my instrument is broken → VOID, no claim.
- **S2 jam curve (low e):** n_c=512, e~Rayleigh(0.001), same ϖ, σ_M ∈ {0.02, 0.01, 0.005, 0.002} → peak nearest-neighbour spacing s ≈ 2.5·σ_M/n_c = {0.98, 0.49, 0.24, 0.10}·ρ.
- **S3 dwell compression (high e):** n_c=512, e = 0.9 + Rayleigh(1e-5) (one transfer ellipse, element-tight: the Binet trigger fires), σ_M ∈ {0.16, 0.08, 0.04, 0.02, 0.01}. Apoapsis dwell compresses λ-spacing by (1+e)^1.5/√(1−e) ≈ 8.3 and the contact gate shrinks by r_apo = 1.9 → net ~4.4×.
- **S4 maintenance cost:** e = 0.3 + Rayleigh(0.05), ϖ~U(−0.1,0.1), M₀ uniform (no jam — pure maintenance), n_c ∈ {128, 256, 512, 1024}. Overtakes/orbit = Kendall distance of the λ-ring between consecutive samples, summed (Σ|Δrank|/2, exact).

## Pre-registered predictions

1. **S1:** max rank ≤ 4, 0 misses (control passes).
2. **S2 (the decisive curve):** misses appear between s = ρ and s = ρ/4; at s = ρ/10 the max rank exceeds 10 and the k=4 train misses > 20% of true contacts. The missed contacts are deep inside ρ (d_min ~ s, i.e. 6×–10× inside), like the gold's window-tier misses.
3. **S3:** the miss onset moves to σ_M larger by ≈ 4.4× (between 3× and 6×); at σ_M = 0.01 the max rank exceeds 30; the missed contacts' anomalies cluster at apoapsis (|f − π| < 0.5 for the majority).
4. **S4:** overtakes/orbit ≈ c·n_c^α with α ∈ [1.7, 2.3] (wiggle amplitude ≈ |∂λ/∂e|·σ_e ≈ 0.1–0.2 rad ≫ spacing 6e-3 rad at n_c=1024); at n_c=1024 overtakes exceed 10× the watch itself (n_c·k). Correctness is intact here (rank at the few contacts ≤ 4): the wiggle breaks the *cost* claim O(n_c·k), not the watch.
5. **Held-out (risky, half-structural):** in mixed-e scenes (S4's few contacts), contacts between different-e bodies concentrate near quadrature |f ∓ π/2| < 0.4 rad (∂r/∂e = 0 there: the radial coordinate is e-blind at quadrature — the geometry the 1-D ring silently relies on).

Kill criteria for my claim: if S2 at s = ρ/10 still gives max rank ≤ 4 and 0 misses, the spacing invariant is not needed and the train is stronger than I argue (dossier says so). If S4's exponent is ≈ 1 with overtakes < n_c·k, maintenance is not quadratic and that prong dies.

Known instrument risks I accept and will report: same-a exact periodicity undercounts failure (real fleets drift); candidate capture can in principle miss a dip narrower than the coarse step (mitigated by the λ-rank ≤ 2 rule; S1 validates against the gold's published number).

## Addendum (disclosed, written after instrument debugging, before the decisive runs)

Instrument bugs found by the dense cross-check and fixed BEFORE the decisive runs:
1. the pipeline ignored the bodies' initial phases M0 (scanned a stacked fleet);
2. the refinement solved body j at body i's phase;
3. local-minima detection excluded the t=0/2π boundary;
4. 512-node scans missed dips narrower than the node step at e=0.9.
After the fixes the pipeline matches an independent dense scan (65536 and 1M
samples/pair) exactly: 4=4 contacts (low-e scene), 2=2 (high-e scene).
Scene trims for time (after registration, before runs): S2 {0.01, 0.005, 0.002}
(0.02 dropped; S1 at spacing 1.25rho brackets the safe side), S3 {0.04, 0.02,
0.01} (0.08, 0.16 dropped), S4 n in {128, 512, 1024} (256 dropped). LB gate T
512->256 with the 30-rho margin (the verified miss case had minLB 5.65e-4,
margin 5x below the gate).
