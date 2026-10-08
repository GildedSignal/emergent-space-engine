# Predictions — run 20261008-0148-second-20261008-0041-redteam-ecfd-90ec

Second author on 20261008-0041-redteam-ecfd. The checker's gold path is a
record correction, not a new physical experiment: (i) the oracle-distance
range must regenerate from the shipped JSON, (ii) prediction 1 must be
restated as failed-low. Tuned on: the shipped `falsifier-out.json` (reproduced
bit-identically, 1.4 s) and hand arithmetic on its columns. Held out: the two
decisive additions below have NOT been run.

## Deterministic corrections from the shipped record (not predictions)

C1. Oracle-distance ratio |rel_oracle_vs_shipped| / |rel_shipped_vs_GR2PN| at
    e=0.6: at ν=0.25, min ≈ 34 (p̄=1000), max ≈ 718 (p̄=50); at ν=0.1,
    ≈ 42–1820. The dossier's "5–170×" regenerates under no definition tried.
C2. Sign-flipped law (2·shipped − GR2PN(ν=0.25)) vs B11's tolerance
    (0.01+16/p̄, verified `xtask/src/behave/binary.rs:18`): deviation
    |a_flip/a_1pn − 1| reaches 0.317 at p̄=20 (not |4.5/p̄| = 0.225);
    margin tol/dev ≈ 2.55 at p̄=20 rising to ≈ 5.9 at p̄=1000. Corrected
    claim: B11 passes the sign-flipped law with ≥ 2.5× slack everywhere
    (the dossier's "≤ tol/3.6 everywhere" was wrong at strong field).

## Held-out predictions (decisive runs)

P1 (offset artifact is the weak-field floor). The nudged start [up, −1e-9]
puts the exact integrator 1e-9/|u''(up)| past the turning point — a phase
offset of ≈ 1.68e-6 rad at p̄=1000 (|u''(up)| ≈ 5.96e-4), i.e. −8.9e-5
relative on the advance, while the EOB side's offset is ~1e-13 (du/dφ =
F·u²·pu/(jA) shrinks it by up²/j ≈ 8e-8). Prediction: an artifact-free
rerun (start exactly at the periastron, integrate to the aphelion event,
advance = 2·Δφ_half − 2π, both integrators) collapses the p̄=1000 rows:
|rel(ν=0.01)| from 9.0e-5 to < 1e-5 (c₂-scaled ≈ −2.4e-6); rel(ν=0.1)
from −1.06e-4 to −2.3e-5 ± 50%; rel(ν=0.25) from −1.32e-4 to −5.8e-5 ± 30%
(c₂ gap 0.0579 × u). Control: at p̄ ≤ 100 the artifact-free numbers agree
with the stored nudged numbers to < 1e-6 relative (artifact ≤ 4e-8 there).

P2 (Rust transfer). The shipped integer law's compiled advance
(`Orbit::compile` via `QuantizedMemo::get`, judge-boundary quantization of
xtask's Space adapter) at (p, e=0.6) matches the falsifier's exact-ODE
advance at the same semi-latus/eccentricity labeling to < 0.05% at every
grid point — then the +0.36% GR bound transfers to the shipped Rust law.
If it instead matches the closed form 2π(1/√(1−6/p)−1) (0.23% away at
p=50), the key convention differs and no transfer is claimed.
Kill: |a_rust − a_ex|/a_ex ≥ 0.36% at any grid point → the 2PN bound binds
only the design; report as the new limiting fact.

## Kill criteria for the corrected record itself

- If the artifact-free rerun leaves |rel(ν=0.01, p̄=1000)| > 3e-5, the floor
  story is wrong; the weak-field rows must be reported unexplained, and only
  the p̄ ≤ 100 verdict stands.
- If the c₂ fit (p̄ ∈ {30,40,60,80}) moves by more than ±0.01 under the
  artifact-free method, the c₂-based conclusions carry an instrument error
  and the dossier says so.
