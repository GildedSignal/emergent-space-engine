# Dossier — the seam between the encounter certificate tiers (lab run 20261010-0306-taleb-8af8)

**Claim.** The co-orbital certificate's adopted premise — "every real encounter lies within partner
rank 4 along the orbit" (gold 20261006-0346-taleb-09b5, now build `b-coorbital-cert`) — is not a
constant but the law **rank ≈ 0.2–0.5 · ρ·n/arc measured at the encounter epoch** (median; max ≈
30× the median), rank measured at setup covers almost nothing under internal shear, and the
fleet⊕belt seam makes the cone tier pay m·n_cross candidate setups of which **94% never produce an
encounter**, with belt-body degree growing ∝ fleet size — so the build contract must size k from the
dimensionless density, add a shear-driven refresh number, and route cross-family pairs to an
arc-envelope (the queued skin), not to the cone.

**Bottleneck.** "Candidate work at scale … work must track real encounters" (HANDOFF risks, board
focus, `q-candidate-degree`); the top scaling risk re-enters through the tier seam, which the gold's
fleet-only scenes could not see.

**Evidence** (this tree, `crates/encounters` extended with `make_fleet` + a `seam` subcommand; Linux
x86 cloud box, shared, 4 threads; orders of magnitude only). Fleet: m bodies, a ∈ [1, 1.005],
σ_e = 2e-3, **aligned periapses**, mean longitude uniform in an arc; belt: n bodies, a ∈ [1.02, 1.5],
σ_e = 5e-2; ρ = 5e-3; 20 orbits; truth = conservative advancement over the radial superset (Halley),
method = the shipped cone tier; `dup = 0` and `outside_cone = 0` on every scene (events distinct,
superset sound). Raw JSON: `work/seam-raw.jsonl`. Reproduce (each line ≤ 60 s):

```
cargo build --release -p emergent-encounters
./target/release/encounters seam cost                      # degree vs fleet size
./target/release/encounters seam scene mixed-arc0.1 300 0.1 700 0.005 20
./target/release/encounters seam scene ring 300 6.283185307179586 0 0.005 20
./target/release/encounters seam scene graded 400 <arc> 0 0.005 20   # arc ∈ {2π,1,0.3,0.1,0.03}
```

1. **The rank law** (partner's rank among all N bodies by circular mean-longitude distance; graded,
   fleet-only, N = 400, ρ·n/arc = 0.32 / 2 / 6.7 / 20 / 67):

   | arc | 2π | 1.0 | 0.3 | 0.1 | 0.03 |
   |---|---|---|---|---|---|
   | rank@enc median | 0 | 1 | 3 | 7 | 12 |
   | rank@enc p95 / max | 2 / 6 | 7 / 23 | 18 / 68 | 44 / 164 | 115 / 356 |
   | frac rank@enc ≤ 4 | 99.9% | 85.5% | 59.6% | 39.7% | 26.5% |
   | rank@setup median | 14 | 69 | 115 | 143 | 170 |
   | frac rank@setup ≤ 4 | 27.1% | 7.9% | 4.0% | 2.5% | 1.6% |

   The gold's "rank 4" is reproduced exactly where ρ·n/arc ≪ 1 (my ring control: max 4) and fails
   progressively as concentration rises: a fixed k = 4 certificate silently drops 60–74% of real
   encounters exactly in the regime it exists for. And rank@setup ≤ 4 holds for at most 27% even at
   ring density: with fleet-internal shear (here Δa up to 5e-3), phase ordering reshuffles well
   within the horizon, so neighbours must be re-taken at a refresh cadence set by shear, not once at
   setup. Two dimensionless numbers govern the certificate, and the contract names neither.
2. **The seam cost** (`seam cost`, belt n = 1000 fixed, arc 0.1): fleet-body candidate degree =
   222 / 422 / 1122 / 3122 at m = 100 / 300 / 1000 / 3000 — i.e. m + 123 cross pairs; belt-body
   degree grows 436 → 792 with m (the quadratic is mutual). Cross-family: 25,985 candidate pairs,
   1,488 real encounters, **94.3% of cross setups never hit** (stable across arcs). Setup pairs per
   cross encounter ≈ 17 here; candidates are orbit-geometry, encounters scale with ρ and horizon, so
   at game ρ = 1e-5 this is ~10⁴ setups per encounter — work does not track encounters at the seam,
   even after the phase certificate absorbs all fleet-internal pairs.
3. **Completeness at the seam** (against my expectations, see Predictions): the shipped cone tier
   missed **0** encounters on every scene, including 53,610 fleet-internal encounters at arc 0.1 and
   133,810 at arc 0.03; false reports ≤ 8 per 10⁵ (terrace-scale). The trigger between tiers is a
   **cost** decision in this regime, not a correctness one; the gold's 4–6% window-tier misses did
   not reproduce at these parameters (their formation must sit at other da/horizons — the miss
   regime remains unmapped, which is itself a hole in the trigger's spec).

**Predictions** (`predictions.md`, written before the runs): P1 (mutual degree growth, 94%-scale
setup waste, ρ-independence) **held**; P3's rank law **held** (median ≈ ρ·m/arc within a factor 2–5,
monotone; cross-family rank@setup ≈ uniform — measured medians 700–725); P2's completeness half
**failed**: no fleet-internal misses anywhere and no silent-miss zone — the tier is complete across
the whole graded range, so the trigger is cost-driven, not miss-driven. P3's "cross-family rank@enc
≤ 4" also failed (median 70–141): even at the encounter epoch, cross partners are not phase-local.

**What would make it wrong.** My fleet has aligned periapses and ρ = 5e-3 (chosen so fleet-internal
encounters exist inside 20 orbits; conjunction needs Δa ≳ 2π/(1.5T) ≈ 3.3e-3, contact needs Δa ≲ ρ).
Tighter convoys (smaller da) shear slower, pushing rank@setup down and refresh out — but then
fleet-internal encounters vanish below any horizon, so the gold's evidence could only ever sit at
one end of the law. The rank instrument reads correctly on the ring control (spacing 2π/300 ≫ ρ ⇒
rank 0, max 4). Misses are counted with the crate's own matchup (tol 1e-3, window-excluded edges).
If the checker's independent truth disagrees on the terraced false reports, they are truth-resolution
artifacts (r8 v3's lesson), not method claims — none of my conclusions rests on them.

**Cost of adoption, fit with PRINCIPLES.** Nothing to build: amend `b-coorbital-cert`'s contract
before it freezes — (a) k = ⌈c·ρ·n/arc⌉ + tail margin (max/median ≈ 30 measured), certified not
tuned; (b) a refresh number Δn_max·T_refresh/spacing; (c) cross-family pairs excluded from both
tiers and given the arc's sheared longitude envelope (b-encounter-skin's job, with the 94% waste
number as its target). "Gates judge a representation; they never size it" (AGENTS): a k=4 baked into
tests would size it. "Candidate work must track real encounters" is the board's own bar; the seam
violates it by ~10²–10³ at game ρ.

**The lens (Taleb).** This lens looked for the fragility between regimes rather than inside them, and
it found a hidden dimensionless variable where a constant was adopted. What it may have missed: the
speed side — my ρ is 500× the game's, chosen to make encounters measurable in one run; the
extrapolation ∝ 1/ρ is argued, not measured, and the miss regime map (where the window tier does
drop contacts) still has no data. Nothing here says the phase certificate is the wrong
representation — only that its constant was a fortune read off one point of a law.
