# Predictions — 20261018-2155-scout-9fd1 (written BEFORE the decisive run)

Topic: encounters, the epoch rule's adoption dial (08d0's named follow-up: the pooled
multi-seed knee curve and the eps dial). All on the toy frozen in `epoch_knee.py`
(constants wiki-sourced: w = 23 ticks, d ∈ [1.5,6]·10⁵, j₀ mean ≈ 10⁶ ⇒ dd ≈ C/j₀-scale
drift; quantum kick p50 relative size κ ≈ 0.08·dd per kick, from e87d's δd p50
2.4·10⁴ ticks at d ~ 3·10⁵). Integer-valued float64 (all magnitudes < 2⁵³, add/sub
exact); floats explore, the design rule is stated in integers at the end.

Cases NOT tuned on (the decisive grid, run once):

- **P1 (positive control).** E = 1 (exact re-certify every kick): 0 leaks at every κ arm.
- **P2 (negative control).** No re-arm (never armed): leak fraction of hits = 1.0, and the
  per-pair per-kick hit hazard ≈ E[1/j₀] ≈ 7·10⁻⁷ (the toy's uniform-phase scale, to be
  compared with the belt's w/C = 1·10⁻⁶).
- **P3 (the mechanism — the run's headline).** The knee E_knee (largest pooled-zero E)
  scales ≈ 1/κ²: doubling the quantum (κ ×2) divides the knee by ≈4, halving it multiplies
  by ≈4, within a factor 2 per octave. [Mechanism: the certificate's information horizon is
  the drift random-walk decorrelation time; ballistic drift would give 1/κ.]
- **P4 (the above-knee law).** Leak-per-pair-per-kick above the knee rises ≈ linearly in E
  with slope within 2× of the P2 hazard (08d0's Ew/C law, reproduced independently).
- **P5 (held-out point).** At the base κ, E = 96: pooled leak CI upper bound < 2·10⁻⁵ per
  pair per kick (zero or near-zero expected if the pooled knee ≥ 128).
- **P6 (grazer clustering).** Leaks concentrate: the top decile of pairs by hit count
  carries ≥ 50% of leaks at every E above the knee (the grazer law, 08d0's checker).

Kill criteria: P1 failing (instrument unsound) ⇒ VOID. P3 failing with 1/κ-scaling instead
⇒ the diffusion mechanism is wrong and the dossier reports the ballistic law. If the base-κ
knee lands outside [32, 512], the toy's κ anchor is off the belt's — report, rescale to the
measured belt κ, do not tune to fit.
