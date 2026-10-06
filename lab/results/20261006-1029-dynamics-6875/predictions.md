# Predictions — dynamics run 20261006-1029-dynamics-6875

Written BEFORE the decisive runs. Original derivation first; then one amendment made
after a 20-orbit N=60 debug pilot (code correctness only), before any sweep ran.

**Question.** The encounter design assumes a steady state: "judge steady-state work per
orbit (→ 0), with each pair paid once per element change" (r8 v2 next step). But element
changes are endogenous: every conjunction kicks elements, kicks change the overlap
(candidate) set, and the overlap set decides who meets whom. Treat the belt as a closed
dynamical system left alone: does its event/work process settle, drift, or avalanche?

**Model (first order in e, exact discrete events, no ticks).** N bodies, a uniform in
[1, 1.5] (the r8 belt), Rayleigh σ_e = 1e-2, GM = 1. Conjunction when mean longitudes
cross; miss distance b from first-order epicyclic positions; impulse α = 2 Gm/(b v_rel²)
rotating v_rel (pair momentum and |v_rel| exact); Gauss update of (a, e-vector). Pairs
whose radial ranges do not overlap are outside the certificate (the two-tier design's
premise); they enter/leave incrementally when a member is kicked. Certificate cost =
reschedules (pair-rebuild count). Strength swept as gm = G(2m).

**Predictions (hot, focused regime — as amended below):**

- **P1' (heating law).** v_rel ~ n a σ_e, b ~ a σ_e ⇒ α ∝ gm/σ³, δe ∝ gm/σ²; conjunctions
  per body per orbit ∝ σ_e². So d σ_e²/dt ∝ σ_e²·(gm/σ_e²)² ⇒ **σ_e ∝ t^{1/4}**
  (log-log slope 0.25 ± 0.08). (Original pre-pilot derivation, kept for the record,
  assumed v_rel ≈ v_kep and rate const, giving 1/3.)
- **P2 (certificate budget).** Overlap-pair count ∝ σ_e ⇒ grows **∝ t^{1/4}**, saturating
  only at κ = 2aσ_e/W ~ 1 (the co-orbital transition of the 6 Oct gold), unreachable
  inside these runs.
- **P3' (encounter yield flat, work per encounter grows).** rate ∝ σ_e², P(b < ρ) ∝ 1/σ_e²
  ⇒ physical encounters (b < ρ = 1e-3) per orbit **flat**; work per real encounter
  ∝ overlap/encounters ∝ **t^{1/4}**. The "→ 0" steady state does not exist at fixed
  birth parameters; σ_e must be capped at birth (the belt program's tail) for it to exist.
- **P4 (clustering).** Conjunction counting statistics stay Poisson-like (Fano factor of
  per-orbit counts within 0.7–1.4) — synodic geometry, not state-amplified. If Fano > 2
  appears, this fails and there is a clustering gate we lack.
- **P5 (avalanche).** One injected player kick (tangential δv ~ 5× typical v_rel) causes
  an excess of reschedules of order the victim's immediate overlap degree, decaying
  within a few orbits: **branching ratio b < 0.15**, no amplification cascade. If excess
  grows or persists, the p99 frame risk is real and needs a gate.
- **P6 (conservation).** Σ 1/a_i and Σ momentum stay at their initial values to numerical
  precision (the kick rotates v_rel, never changes |v_rel|); drift is reported per run.

Calibration disclosed: gm ∈ {5e-8, 1.5e-7} gives α_typ ∈ {0.05, 0.15} at σ_e = 1e-2;
α capped at 0.5 (the strong tail under-kicks slightly). Runs: N = 200, 2 000 orbits,
seeds {0,1,2}; gm = 0 control must hold every quantity fixed (the null). Avalanche pair:
same seed, injection at orbit 1000 vs no injection.

Kill criterion: if P1' is contradicted (σ_e saturates on its own below κ/3, or grows with
slope > 0.5), the feedback model is wrong and the dossier reports that as the result.
