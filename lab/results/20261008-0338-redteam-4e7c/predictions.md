# Predictions (written before the decisive run)

Attack: the encounters design (law.md "Finding encounters"; crates/encounters) is Kepler-native —
closed ellipses, sections at longitude passages, "an exact integer circle rotation", candidate
certificates "valid until a kick". In a GR doll every orbit is a rosette: apsidal advance Δϖ ≈
6πM/p per radial period, carried by the drift (not a kick), so (E, L) — the law's own bookkeeping —
never change while the geometry rotates.

Falsifier: mini-belts (N = 30, p ≈ 30M and a p ≈ 300M variant, e ~ 0.2, ρ = 1e-4·p, 60 orbits, no
kicks) integrated on the exact Schwarzschild Binet law u″ + u = M/L² + 3Mu² (the doll's own law),
against a faithful Python emulator of the crate's premise fed perfect osculating elements and the
exact GR radial period (most favorable to the design). Truth = dense distance scan, encounter =
local minimum < ρ with dip quantum 1e-6·ρ (r8 v4's definition). Plus one deliberately excluded pair
(cone gap > eps at t = 0, radial ranges overlapping).

Held-out predictions:

1. **Newtonian control** (same pipeline, u″ + u = M/L²): missed_fraction = 0 and false_fraction = 0.
   If this fails, my emulator is a strawman and the run is VOID.
2. **GR, p ≈ 30M (Δϖ ≈ 0.63 rad/orbit):** missed_fraction ≥ 0.2 pooled over crossing pairs; the
   conjunction-time error of the one-frequency model grows roughly linearly in conjunction index and
   exceeds the encounter dip duration within ~5–20 conjunctions.
3. **Excluded pair (cone says non-crossing at t = 0, no kicks ever):** the truth records ≥ 1
   encounter below ρ; the crate predicts none (excluded until a kick) → missed = 100% for that pair.
4. **GR, p ≈ 300M:** differential precession 10× slower per unit Δp; over 60 orbits I expect
   missed_fraction ≈ 0–0.05 (the boundary of the kill is p-dependent, scaling like Δϖ̇_rel·horizon
   vs the arc width).
5. **Certificate invalidation rate** is set by differential precession Δϖ̇_rel ≈ 6πM·Δp/p² per
   orbit (not by kicks): at p = 30M, Δp = 0.6M, that is ~0.013 rad/orbit → every near-tangent pair's
   cone status flips within ~500 orbits even with zero kicks.
