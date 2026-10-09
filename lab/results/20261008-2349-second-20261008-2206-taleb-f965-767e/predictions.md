# Predictions (second author, written before any gate2 run)

Question: the checker named the experiment that keeps 20261008-2206-taleb-f965 from gold —
"member-extremal crossing arcs (or families clamped to ε≈ρ) closing the wedge/belt hole, then
the 10⁶-fleet pair-count at game ρ". Does the named fix close the hole soundly, at what cost,
and does gated pair-work track (ρ+ε) where cone setups track n²?

Method `gate2` (built this run, on the run's own scripts): families and the intra-family
rank+cadence path unchanged from v1; the inter-family layer replaces the representatives'
single crossing longitude with a member-extremal ARC per family pair (box over-approximation
of the Binet-difference ball of radius eps_a+eps_b: skip a pair only when |du|−r ≥ 2·E; arc
half-width = acos-range/2 + asin(E/r_lo), clamped at π), sampled at centre and both endpoints;
the join window per sample is the exact Kepler sweep time of arc-half/2 for the slowest member
of each family plus v1's GATE_S·(ρ+E)/|Δv_rep| margin; the exact check pays `sections()` once
per joined pair (amortized) and walks each deduped hit window with `run_section` (the crate's
own certified machinery — no capped-resolution uniform scans).

Scenes: the run's S1–S8 unchanged; the checker's adversarial cases rebuilt as A1 (pure fleet,
10× a-spread, 50 orbits), A2 (wedge at ρ = 1e-5), A4 (fleet × tight cold belt a ∈ [0.995,1.005],
σ_e = 3e-3; n reduced 550 → 180 to bound machine time — same a-range and σ_e, so the family
degeneracy ε ≫ ρ is preserved); pair-count scaling S9 at ρ ∈ {1e-4, 1e-9} with the fleets'
own ε ≈ 1e-3 and with ρ-tight fleets (ε ≈ 2e-8), n_side 75…600, counts only (no truth).

Predictions, each falsifiable:

- H1 (the hole closes): gate2 missed = 0 on S4 (v1: 21), S7 (41), A2 (1), A4 (3). Any
  remaining miss kills the arc repair as a certificate.
- H2 (regression): gate2 missed = 0 on S1, S1b, S2, S3, S6, S8 (v1 already 0; arcs only widen
  the searched longitudes).
- H3 (wedge cost): gate2 evals on S4/S7 within ~5× of the cone's (~17–19 M); hits grow ~5–20×
  over v1's ~6.9 k (three samples, sweep-widened windows).
- H4 (belt degeneracy): on A4 most belt family pairs' arcs clamp at half = π (near-concentric
  families, r < E), and gate2's evals exceed the cone's by ≥ 10× there — the family gate is
  structurally wrong for loose populations; the cone tier stays (restriction (a) re-confirmed
  at family level).
- H5 (slack is ε, not ρ): at game ρ = 1e-9, gate2's hits with ε ≈ 1e-3 fleets stay at the
  ρ = 1e-4 level (the window is ε-dominated); with ρ-tight fleets (ε ≈ 2e-8) hits fall with
  (ρ+ε) — roughly 3–4 orders of magnitude below the ε-fleet value at ρ = 1e-9 — while cone
  candidates are identical at every ρ (crossing fleets: cone_gap ≪ 0 regardless of ρ).
- H6 (10⁶ extrapolation): cone setups ×4 per fleet doubling (n_side²: ~2.5×10¹¹ setups at
  10⁶ bodies); gate2 pair-work grows ~×2 per doubling (linear in n per crossing family pair),
  and its per-encounter slack is ≈ S·(ρ+ε)/ρ — bounded only when families are ρ-tight. The
  adoptable form of restriction (c) is therefore arcs AND ρ-tight families together (the
  engine's fleet programs), not arcs alone.

Kill criteria: any gate2 miss on a scene it claims to certify kills the member-extremal arc
repair (then only "families clamped to ε≈ρ before any family-level gate" survives); if gate2's
hits at game ρ do not fall with (ρ+ε) for tight fleets, the "work tracks real encounters"
claim dies and only the veto survives.

Timing note: A4's degenerate arcs widen joins by ~2·π/2 sweep time; if the full A4 gate2 run
exceeds ~10 minutes it is stopped and reported partial with the count of degenerate arcs.
