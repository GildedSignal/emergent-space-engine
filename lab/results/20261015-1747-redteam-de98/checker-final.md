Working...
Check complete. Summary of what I did and found:

**Grade: silver** — written to `lab/results/20261015-1747-redteam-de98/check.md`.

**Reproduction:** `bash regen.sh` → exit 0, 12 s, output **bit-identical** to the stored log (three independent runs agree). `work/patch.diff` empty. Every dossier number traced to `eob_data.json`.

**Verified independently:**
- **The rung arithmetic is exact**: r3 v3's frozen file samples p̄∈[20,1000] and its precession tolerance is (0.01+2·8M/p̄) = **81% at p̄=20M** — the "certifies only where trivially safe" claim holds against the oracle (1PN `damour_derelle`).
- **Closed the instrument's biggest gap**: the shipped ADM-side RK control (C1b) is dead code printing "?". My φ-parametrized RK of the ADM Hamilton equations matches the author's quadrature to **2e-12** at four labels; H_adm(ν=0) confirmed as the correct 2PN truncation of the exact isotropic test Hamiltonian (2PN shrinks the gap 5–26×). Both halves now validated.
- **ecfd's contradiction is genuine**: read from its branch — it matched *turning points* with a ν→0-exact resummed EOB; de98 matches *real invariants* with truncated ADM. Recording it as unadjudicated is correct.

**Adversarial (beyond the author's range):** p̄=200/400 — absolute error scales ν/p̄² cleanly (exponents 1.90–1.96); ν=0.05/0.2 off-grid — linear (5.4 vs 5.0); e=0.99 — exposed a silent false-PLUNGE mode (`doll_turning` grid caps at r=2000M; no shipped row crosses it); baselines converged (2e-8).

**Why not gold:** the adjudicating oracle (the run's own open direction 4) is missing; P1 failed as pre-registered **and** the reference was switched EOB→ADM after `predictions.md` without disclosure — the failure is partly baked into that swap. Also corrected on the page: "baseline <1.5% at p̄≥50" is false (measured 1.1–2.2%; clean ≥80, signal-dominant ≥120), and two quoted controls aren't regenerable ("4 digits" is 3). My attack scripts (`checker_attack*.py`) are in the run folder so every number I cite regenerates.
