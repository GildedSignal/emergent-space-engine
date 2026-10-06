# Predictions — 20261006-0437-components-2222 (components lens)

Component: the encounter seam (`Encounters` trait, `crates/universe/src/encounter.rs`).
Decisive experiment: `cargo run --release -p emergent-universe --bin seam` — the shipped
exact scan (`PlayerNeighbourhood::find`, full integer tube readout per candidate) against
the certificates of `crates/encounters` (sorted U-window + cone + exact per-pair passages),
on (A) the plane's own doll population and (B) a belt grown at fixed linear density in a
shipped root doll (n = 192 → 12288, half-width ∝ n), plus phased near-partners so some
checks hold real encounters. Written before the run; nothing below was tuned on these cases.

1. **The scan is linear in the doll population** with a per-candidate cost of 2–20 µs
   (a `binding_at` + integer Kepler `cartesian` readout per candidate). The certificates'
   per-candidate work is ~0.05–0.5 µs (float arithmetic on cached elements). So the idiot
   index is ≥ 40× per candidate even before scaling, and grows with n.
2. **At fixed belt density the certificates' per-check cost is flat in n** (q-candidate-degree's
   regime: work tracks real encounters, not the population): I expect ≤ 10 µs per check at
   n = 12288, against a scan cost of n × per-candidate (tens of ms). If the certificate cost
   grows ∝ n instead, the seam swap does not hold the board's answer and this configuration
   is killed (the method is not: a skin/doll split may still).
3. **Zero misses**: every pair the exact scan reports (linear `hit` at the true per-pair
   reach) appears among the certificates' sub-ρ minima. The belt here is uniform
   (σ_e ≈ 0.02, no co-orbital clumps), so taleb-09b5's concentrated-regime misses (cone
   candidates in a-clumps) should not appear; if they do, the seam needs the train
   certificate as the fallback and I will say so.
4. **The plane's real check** (Home's doll, ~10 bodies) costs 20–300 µs per player event
   today; the certificate path ≤ 5 µs including the build (Sorted::new is n log n but paid
   per element change — the slack skin of q-skin, not per check; I measure both the query
   and the rebuild so the neighbour's cost is visible, not hidden).
5. Expected misses of my own extraction (a real risk, stated): the float element extraction
   from one cartesian readout must reproduce each tube's position to < 1e-6 relative; if it
   does not, all certificate numbers are void until the conversion is fixed (I check this
   first and report the worst error).

Kill criteria: any scan-found pair missed by the certificates (at the true per-pair reach),
or certificate per-check cost ∝ n at fixed density, kills the swap configuration, not the
method. A plane-scene extraction error > 1e-6 voids the run.
