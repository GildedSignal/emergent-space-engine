Working...
Check written to `lab/results/20261007-0621-components-8306/check.md` — **Grade: gold**.

**What I did** (~25 min, all processes ≪ 2 GB):

1. **Reproduced** from the clean tree — no patch.diff (0 B; the repo is untouched, the work is a standalone `jet-bench` against `crates/space`). All dossier commands run: deterministic stream rows match bit-for-bit (corr e=0.9 → 0.077 compiles/kick, 6.1e-7; peters 5.02/kick; rand 8.1e-7); cost split reproduced at +8–9% on the shared runner with identical ratios (compile = 36% of the ~14 µs rebind tail).
2. **Grounded the premise in the crate:** `Rebinding::from_state` really does `fit_key` + `Orbit::compile` per call (binding.rs:353), and `ShapeKey` is (k, q→0) so p-only kicks hit the memo — the shipped 1.0 compile/kick claim is real.
3. **Adversarial cases (7 of my own):** plane kicks, rand ε=10⁻⁵, seed variation, e=0.95/0.97, the unrecorded ε=10⁻⁷-safety row — all hold. **One boundary found:** a 10× longer coherent stream at e=0.9 walks past the floor (5.7e-5, 57×) as e drifts toward 0.995 — the author's declared blind spot, now measured; the crate fails closed beyond it.
4. **Novelty:** law.md line 35 adopts the jet with a *global* C from gold df81; this run's measured correction (C is an anchor property, 0.33–140+; global C breaks the floor 89×) amends an adopted rule on the real integer compiler.
5. **Predictions:** mtime ordering consistent with pre-registration before scan/streams; the disclosed global-C failure and the P7 self-falsification are recorded in the txt lineage.

Gold because: reproduced, held-out predictions held, shows an adopted premise wrong (global C) with controls on both sides, and is adoptable in one surgical step — with the separatrix boundary caveat I added for the integrator.
