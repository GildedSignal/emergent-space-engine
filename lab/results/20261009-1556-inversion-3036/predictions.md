# Predictions — 20261009-1556-inversion-3036 (written before the decisive run)

Question: does the phase-neighbour certificate adopted from gold `20261006-0346-taleb-09b5`
("every real encounter lies within partner rank 4 along the orbit, so a phase-neighbour
certificate at O(n·k) replaces the quadratic tier") compose to **two formations on crossing
orbits**, and to a lone crosser through a formation?

Scenes (all μ=1, ρ=1e-3, groups given with true labels — generous to the certificate;
any per-group concentration number that fires on the gold's single formation fires on each
group here by construction, since the per-group spreads are identical):

- **S1** single formation (positive control, the gold's scene): n=250, a∈U[1,1.0001],
  e Rayleigh 3e-4, ϖ tight, λ in a 0.25 rad arc. Horizon 1 orbit.
- **S2** two formations, same period (a=1 both), B eccentric e=0.5 crossing r=1 at two nodes;
  both arcs centred on one node at t=0 (a rendezvous). Horizon 1 orbit.
- **S2b** as S2 but a_B≈1.05 (detuned period; node phases drift). Horizon 20 orbits, n_B=100.
- **S3** the player: S1's fleet plus one body on the e=0.5 crossing orbit timed to pass
  through the fleet's arc.

Truth: the crate's own `truth_pair` (r8 v2 truth: rigorous conservative advancement,
Halley vs Newton solver paths). Tiers measured: phase cert (rank ≤ 4 in mean longitude per
group), the cone tier (`is_candidate`), and a time-sorted node-event certificate as a cure.

## Predictions (held-out: nothing below has been run)

- **P1 (positive control).** On S1 the phase cert misses **0** intra-fleet encounters, and the
  cone tier's intra candidate set is ≈ n²/2 (all pairs; nearly identical orbits) — reproducing
  the gold's premise and its quadratic setup. If P1 fails, my implementation is broken: VOID.
- **P2 (the inversion, misses).** On S2 real cross encounters exist (order 10²–10³) and the
  phase cert, scoped per group exactly as adopted, generates **zero** cross candidates:
  cross misses = **100%**. Intra misses stay ≈ 0.
- **P3 (the inversion, quadratic).** On S2 the cone tier admits essentially **all** n_A·n_B
  cross pairs (crossing orbits ⇒ cone hit): per-body candidate count grows with the other
  fleet's size — the board's top scaling risk, alive in the fleet-battle scene. At 10⁶+10⁶
  that is ~10¹² cross candidate pairs, order 10 TB of pair list: the gold's 40 TB blowup
  returns through the scene the game actually has.
- **P4 (rate).** Cross-encounter rate per pair per node meeting ≈ (2ρ/|Δv|)/(arc-time spread),
  order 5·10⁻³ at these spreads: real cross encounters ∝ n_A·n_B, so per-encounter work is
  constant while absolute setup is quadratic (consistent with q-candidate-degree's fixed-density
  claim; the failure is the absolute per-body candidate growth).
- **P7 (dilution corollary of P4).** S2c = S2 with both arcs widened 10× (same n, same ρ):
  real cross encounters drop ~10×, the cone tier's cross candidate count is unchanged (still
  ~all n_A·n_B pairs), so work per encounter grows ~10× — the cone tier violates "candidate
  work must track real encounters" under dilution in the crossing scene. The node cert's
  candidate count drops ~10× (tracks).
- **P5 (cure).** A time-sorted node-event certificate (per group-pair crossing longitudes from
  Binet, exact per-body passage ticks, candidate iff node-passage times within a window
  ~ safety·ρ/|Δv|) finds **all** cross encounters on S2, S2b and S3 with cross candidates
  ∝ (n_A + n_B), not n_A·n_B.
- **P6.** S2b: node phases drift; cross encounters still occur over 20 orbits; the phase cert
  still misses 100% of them.

Kill criteria: if S2 yields zero real cross encounters the scene failed to contain the
phenomenon (retune arcs, disclose). If the node cert misses any truth cross encounter with
safety 2, the cure as sketched is wrong and I report it broken rather than widen it silently.

Calibration disclosure: S1's spreads copied from the crate's own `coorbital` verify spec
(σ_e=3e-4, a∈[1,1.0001], ρ=1e-3); arc chosen so mean spacing ≈ ρ. Nothing else tuned.
