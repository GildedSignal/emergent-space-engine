# Predictions — 20261007-1334-quant-7334 (held out before the decisive run)

Question: what is the live memory (H_live) of a quiet belt — the entropy of the scar field
(deviation from the birth program) after game time under Sun + Jupiter-like secular forcing
and mutual encounters — and its growth per game-second at 10⁹ bodies?

Scenes (not tuned before writing this):
- Main: N = 16,384, a ~ U[1, 1.5] AU, e₀ Rayleigh σ = 0.01, angles uniform; μ_J = 9.54×10⁻⁴,
  a_J = 5.2 AU, e_J = 0.048. WH drift-kick, dt = 1/32 yr, T = 100 yr.
- Tail: same but σ_e = 0.1 (crossing orbits), T = 30 yr.

Cases held out (no tuning on them after this file is written):

- **P1 (secular scars everything).** Before any re-inference, at the store's native grids
  (ω quantum 2⁻²⁴ turns, Δa/a quantum 2⁻²⁸), the scarred fraction reaches ≥ 90% within 10 yr:
  the parent+tide secular drift moves every body off its birth tube. Naive per-body storage is
  then ~N × 20–40 bits, i.e. the naive ledger at 10⁹ is already ~4 GB class.

- **P2 (shared structure compresses it ≥ 30×).** The scar field after subtracting a
  smooth-in-a model (the re-inferred program: 64 a-bins, per-bin median per column) leaves a
  residual with per-body entropy ≤ 1.5 bits at the 2⁻²⁴ grid, and the residual grows slower
  than linearly in t over 100 yr (log-like or flat), because linear secular theory is regular:
  deviations are a smooth function of birth state + the shared ephemeris, so a generator re-derives
  them. If instead the residual grows linearly at a fixed grid, information is really being
  created (diffusion), and I report the belt as unscalable at that grid.

- **P3 (the tail is where the money is).** The p99.9 per-body residual is ≥ 4× the median
  residual entropy, concentrated in the high-e tail; in the σ_e = 0.1 scene the residual per body
  is ≥ 3× the main scene's at the same grid and grows linearly (encounter shot noise:
  sparse, independent, heavy deltas that no shared generator re-derives).

- **P4 (encounters are the only true information source in the quiet belt).** The encounter
  scar rate per body per orbit in the main scene is ≤ 10⁻³ (r8's belt measured ~427 real
  encounters over 20 orbits); each such scar carries ~tens of bits (full-width ΔE, Δω rows).
  At 10⁹ this stays ≤ a few MB per belt-orbit — the quiet belt's H_live is encounter-dominated
  and tiny; 8 GB is not threatened by the quiet belt within a session.

Kill criteria for the whole approach: if the compressed/residual field at the coarse grid
(2⁻²⁰ turns) still exceeds 10 bits/body by 100 yr with linear growth, H_live ∝ N×t at the law's
grids and the 10⁹ belt does not fit: that is the finding, reported with the N and the hours at
which 8 GB dies.
