# Predictions (written before the decisive runs)

Question: encounters wiki open direction 1 (cd3b, 20261018): "the one missing constant —
pairs re-checked per kick on the live anchor at 10⁹-scale occupancy (fe6b's 0.0346·n law)";
does the row close?

Instrument: new `examples/churn.rs` on the shipped `emergent_encounters` tier
(`Sorted`/`reach`/`is_candidate`, the shipped U-scan), plus the shipped `kick` experiment
re-specced to the belt mix. Replica element tier (a,e floats), band [2,3) AU, Rayleigh
σ_e = 0.07 (make_belt's own cap 0.5), ρ = 1e-4 AU, quantum kick eps = 2⁻²³ ≈ 1.19e-7
(the belt quantum, 8ffc/3294), horizon 1000 orbits (shipped kick default). NOT the live
velocity word — anchor condition stated in the dossier.

- **P1 (the density law).** At fixed band [2,3), candidates re-checked per kick grow
  ~linearly in N over 10⁴→10⁶: fitted exponent ∈ [0.9, 1.15]. Structure: the U-window is
  set by e/p + e_max/p (dispersion), not by any cell bound, so window ∝ density × reach.
  Kill: exponent ≤ 0.8 would mean fe6b's law does not transfer to the belt mix.
- **P2 (the fixed-density control).** At fixed areal density (band width grown with N so
  density = the 10⁶-in-[2,3) anchor's 4×10⁴/AU²), candidates/kick are flat: ratio
  cand/kick(3×10⁵)/cand/kick(10⁶) ∈ [0.6, 1.6]. "O(1) at fixed density" is true but does
  not describe 10⁹ bodies in the fixed band (density 4×10⁷/AU², 10³× the anchor).
- **P0 (dispersion control).** Candidates/kick at fixed N scale with σ_e roughly as the
  reach law: cand(σ=0.07)/cand(σ=0.01) ∈ [2.5, 12] at n=10⁵.
- **P3 (the slack arm, shipped `kick` at the belt mix, quantum eps).**
  slack_skippable_fraction ≥ 0.9, slack_skip_violations = 0, changed_fraction ≤ 0.15.
  Kill: violations > 0 at the quantum eps would kill stored slack at belt kicks (and
  contradict b509's slack reading at fleet scale).
- **P4 (the composed 10⁹ verdict, rtf 100, kick rate 2/body/interval shipped / 0.25 after
  split 8, pair price 1.02 µs arm / measured exact).** Naive candidate rescan per kick
  (what the tier does today on a kick): ≥ 10² cores — the row does NOT close on the
  candidate scan. Slack-deferred re-arm (only changed/newly-armed paid, cd3b's mint row
  ≤ 1.9 cores separate): ≤ ~10 cores — the row then closes with the stream's own cadence
  lever.

Seeds: decisive 20261050 (the shipped kick spec's seed family), held-out 777.
