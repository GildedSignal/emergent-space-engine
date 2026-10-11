# Dossier — run 20261011-2028-dynamics-7807 (dynamics lens)

## Claim

The Binet-cone candidate tier's cost is decided by one dimensionless number, the
thermal crossing depth κ = σ_e·ā/Δa — the candidate fraction of all pairs
collapses onto **frac = min(4.27·κ + f₀(ρ), 1)** across N (1024–16384), ρ
(0.003–0.01) and seeds (sd ≤ 0.0015), with the half point at **κ\* ≈ 0.20**
(κ̂\* ≈ 0.84 in the U-sort's own statistic κ̂ = mean‖(V,W)‖/std(U), computable in
O(N) from the array the engine already keeps) — and the belt's own measured
dynamics (elastic-encounter runaway, secular stirring) drive κ monotonically
*through* κ\*, so the U-sort cone tier is a designed-in instability, not a tail
case: a main-belt-like belt is born at frac 0.45, half the quadratic budget, and
fleets are the same phenomenon at κ → ∞ (a cold tight band, σ_e = 0.01,
Δa/a = 0.0015, already has frac = 0.9995). Second finding: a planar **tangential
cliff** at κ ≈ 0.35–0.44, where the close-encounter rate jumps 9–14× per 1.5× in
κ (near-tangent coplanar crossings, v_rel → v·Δa/2a) — the same κ where the
impulsive-conjunction representation loses its domain (ec74): two walls, one
number.

## Bottleneck

The board's top scaling risk (5 October): "candidate pairs per body grow with N
at a fixed distribution (O(N²)); candidate work must track real encounters."
q-candidate-degree answered the **N axis at fixed distribution** (work per
encounter constant at fixed density); taleb-09b5 answered **concentration**
(fleets). Unmeasured: the **temperature axis** — belts heat (today's dynamics
runs: elastic encounters run away, 6565; secular stirring e ∝ t^0.4, 79ef), and
heating widens the cone. Expected gain: the certificate switch becomes a rule
decided by one local number (no "fleet" category), and encounter-cost gates
(B10/B15/B18b) gain the dimensionless parameter they must pin — without it,
transfers between scenes are meaningless (79ef's checker found exactly this for
thickness). It deletes the implicit assumption that the two-tier cone is the
belt's steady-state certificate.

## Evidence (machine: Linux x86, 8 vCPU shared, load 1.5–3.0; single-threaded
numpy, < 1 GB; run.log timestamps in this folder)

Instrument `cone_phase.py` mirrors the shipped rule exactly
(`crates/encounters/src/pairs.rs`: candidate iff |ΔU| − ‖Δ(V,W)‖ < eps_u(ρ),
eps_u = 1.5ρ(1+κ₀)/rmin²; belt ensemble per `belt.rs`: uniform a, Rayleigh e
truncated 0.5, uniform angles). Candidate counts are exact. Encounter rates are
mean-field over the section's circle rotation (conjunctions once per synodic
period, phase equidistributed): rate = 2ρ·|n_i−n_j|/(v_rel·T_i) per crossing,
exact Kepler v_rel at the crossing; co-orbital full sections (equal periods)
rated by epicyclic alignment (approximation, flagged). Focusing neglected.

Commands (this folder): `python3 cone_phase.py formation | nscal | sweep |
analyze` (sweep ≈ 105 s, others ≤ 35 s) → `metrics.json`, `sweep.json`,
`formation.json`, `nscal.json`.

- **Collapse (P1).** frac_pairs(κ, ρ=0.01): 0.059, 0.077, 0.105, 0.146, 0.205,
  0.291, 0.409, 0.561, 0.727, 0.866, 0.949, 0.983 for κ = 0.010…1.019 (N=4096,
  3 seeds). c = frac/κ = 4.27 ± 0.05 below the knee; f₀(ρ) = 0.017 at ρ=0.003
  vs 0.059-cκ at ρ=0.01 (ρ-floor resolved only down to κ=0.01). N=1024/4096/16384
  at κ=0.10: frac = 0.3427/0.3410/0.3401 — collapse to 3 digits.
- **Boundary (P2).** frac = ½ at κ\* = 0.196 (ρ=0.01) and 0.237 (ρ=0.003; 21%
  above — the ρ-floor, marginally outside my predicted 20%). A main-belt-like
  birth (σ_e = 0.07, the q-secular/B18b scene) has κ = 0.143, frac = 0.45.
- **W and the controls (P4, P6).** Setups per real encounter W = k̄/λ: at ρ=0.01,
  W = 375→776 (peak at κ=0.036)→303 at κ=0.29, then 38, 3.7, 1.3 — the belt's
  native range pays 300–2900 setups per encounter (r8 v2's belt 0: 1.7×10⁶
  candidate pairs / 427 encounters ≈ 4×10³, same order). W is N-independent at
  fixed κ: 711/646/656 (κ=0.10) and 0.67/0.76/0.75 (κ=2.0) for N=1024/4096/16384;
  λ per body ∝ N exactly (both total sides O(N²) at fixed density —
  q-candidate-degree's answer extends over the whole κ axis).
- **Formation (P5).** Δa/a ∈ {0.15, 0.015, 0.0015} × σ_e ∈ {0.01, 0.07, 0.2}:
  frac = 0.296…0.9995; the tight band is all-pairs at every temperature,
  cold included. taleb-09b5's fleet case is κ → ∞ of the same cone-swallowing.
- **Tangential cliff.** λ per body per orbit (ρ=0.003): 0.06, 0.30, 0.82, 1.67,
  2.63 (κ ≤ 0.29, ~∝κ^1.2), then 22.6 (κ=0.44), 322 (κ=0.67), 933 (κ=1.02).
  Mechanism checked on the pairs: rates are median 4×10⁻⁵ but max ≈ 60 — the
  near-tangent coplanal tail (two crossings, v_rel at its Δa floor) dominates
  the mean above κ ≈ 0.4. Planar is the plane's native case (2-D dolls); 3-D
  thickness dilutes λ (79ef's checker: e₀=0.3 sat 29× below the e-only
  collapse) but *widens* the radial-overlap cone, so W only gets worse.
- **Instrument incident (disclosed).** The first decisive run had a rate bug: a
  sampling rescale (×total/sampled) and a missing |n_i−n_j| factor that let the
  near-tangent tail inflate λ by the N² of the sample ratio. The pre-registered
  N-scaling control (P6) failed (W: 1656→389→98), which caught it. Both fixed;
  every number above is from the corrected instrument; predictions were not
  edited (same file, written before the first decisive run).

**The trajectory (orders of magnitude, citing measured exponents).** 8269
(today): a quiet belt's proper elements are a bounded attractor — κ stays put
without elastic coupling. 79ef (silver, reproduced bit-for-bit): stirred e ∝
t^0.4 ⇒ κ ∝ t^0.4 ⇒ a belt measured at κ₀ reaches κ\* = 0.196 in
(κ\*/κ₀)^2.5 × its current age: 2.3× for the main-belt-like κ₀ = 0.14. 6565
(silver, runaway confirmed bit-for-bit: e 0.01→172): an elastically coupled
belt needs e ×10 ⇒ κ ×10 ⇒ tens to hundreds of orbits. So the boundary is
crossed by the belt's own laws in every elastic regime, and never in the quiet
regime — the switch must be live from birth either way.

## Predictions

`predictions.md`, written before the first decisive run (P1–P6 above). Held:
P2 (κ\* = 0.196 ∈ [0.15, 0.25]; the ρ-independence clause missed by 1 point:
21% vs 20%), P4 at ρ=0.01 (peak 776 at κ=0.036, inside [300, 3000] and
[0.05, 0.3] — marginal on the low edge; at ρ=0.003 the peak sits below the
grid), P5 exactly, P6 after the fix it was written to catch. Failed: P3's
shape — λ is monotone in κ (no minimum at κ~0.1–0.2; the co-orbital floor
falls with κ instead of rising), the steep branch's α ≈ 4.7 sits just above
my [1.5, 4], and λ ∝ ρ only for κ ≳ 0.19 (the cold co-orbital rate saturates
in ρ). P1's form held; c = 4.27 missed my [2, 4] band by 7%.

## What would make it wrong

- 3-D belts: the cone becomes radial overlap of inclined orbits — more
  candidates, fewer real encounters (W worse); κ\* itself is planar-exact and
  the plane's law is planar, so this bounds applicability, not the result.
- λ uses uniform-phase averaging of the section's rotation; resonant islands
  concentrate event times but not the long-run rate; the exact per-pair check
  would settle any doubt.
- Focusing is neglected (fine for ships/small bodies; wrong for planet-scale
  ρ-encounters).
- The aging trajectory borrows 79ef/6565 exponents (both silver; the memo
  lesson says cross-run constants share harness risk — but only the *time* to
  reach κ\* borrows them; the boundary itself is measured here, in-run).
- e truncated at 0.5 in the generator: the κ ≥ 0.67 rows are conservative.

**Cost of adoption:** small and already half-paid — the switch certificate is
taleb-09b5's phase-neighbour O(n·k) tier (adopted for fleets); the increment is
(a) track κ̂ = mean‖(V,W)‖/std(U) per doll (O(N) per rebuild, O(1) maintained),
(b) switch certificate class at κ̂ ≈ 0.5 (frac ≤ 0.3), hard-fail above κ̂ ≈ 0.84,
(c) pin κ̂ in every encounter-cost gate (B10/B15/B18b), as 79ef's checker
already demanded for thickness — κ̂ *is* that demand, generalized to one number
that also covers fleets. **Gate we lack:** none of the frozen gates pins κ̂, so
today a heated or clumped belt silently re-enters the O(N²) tier the board
names as the top scaling risk.

**Fit with PRINCIPLES:** #4 — "no object categories: regimes are chosen by
dimensionless numbers" (fleet and hot belt are one regime of κ; the certificate
class is a function, not a label); #18/#19 — the right number makes the switch
trivial ("the right representation always just feels right"); #12 — the cliff
is exactly a p99 event-source, invisible in means.

## The lens

Dynamics read of an engineered component: the quiet belt is a bounded attractor
in κ (8269), elastic coupling is a drift through a measured phase boundary, and
the boundary is where two walls coincide (candidate budget, encounter-representation
domain). What the lens may have missed: the queue level (Kingman tails, frame
impact of the switch itself) and the birth transient (ec74's burst) — both
upstream of the tier, both now parameterized by the same κ̂.
