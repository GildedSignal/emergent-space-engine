# Check 2 (second checker, blind to the first) — rung kepler-pass

Machine: cloud container, Linux x86_64, 4 vCPU, load 0.05, 1.1/16 GB used, cold. Rung file `lab/canaries/kepler-pass.md` sha256 `454758ed…41bb581`, committed (6b22aee) and unchanged; `work/patch.diff` is empty, so the tree is the author's scripts as committed.

## Abstract

The canary reproduces exactly and the verdict is **PASS**. Rerunning the author's `kepler_rung` gives bit-identical `metrics.json`, `summary.txt`, `win_leapfrog.txt` and `ener_euler.txt` (at `-O2` and `-O0`). My independent implementation, written from the rung spec alone, agrees on every decision-relevant number: leapfrog exponent 3.7e-10 vs the author's 2.98e-10 (both ≪ 0.2, noise), max|dE| 0.00134469 identical, bound_fraction 1; euler unbinds at the identical step 15547 (orbit 77.7), bound_fraction 0.007773, and fails B1. `verdict.py` on my `metrics-check2.json` (with the author's file as second argument) returns PASS with no DISPUTED outcomes. No engine code touched; adoption cost zero. This is calibration gold for the rung machinery, not a physics claim.

## Reproduction

- Author's command, in a scratch copy (the binary writes into its cwd): `gcc -O2 -Wall -Wextra -o kepler_rung kepler_rung.c -lm && ./kepler_rung`. Output and all four compared data files byte-identical to the author's. Numbers that differ from the dossier: none.
- Independent implementation (`/tmp/check2/indep.c`, from the spec, not the author's code): leapfrog exponent 3.736e-10 (author 2.984e-10 — different rounding in window-edge/mid-time arithmetic; both are "0" against the 0.2 threshold), bound_fraction 1, steps_per_orbit 200, max|dE| 0.00134469, first_unbound −1; euler exponent −1.079e-9, bound_fraction 0.0077730, first_unbound 15547. Independent Python least-squares over the author's `win_*.txt` reproduces the author's exponents exactly.
- Wall time ~0.1 s for both configs, matching the dossier's 0.11 s.

## Spec and oracle check

- KDK order correct (half kick, drift, half kick); my run confirms L conserved to 1.6e-13 over 2e6 steps, r ∈ [0.5, 1.506].
- euler is genuine forward Euler: the drift uses the **old** velocity (`kepler_rung.c` lines 79–81). Semi-implicit Euler would have been symplectic, stayed bound, and VOIDed the rung as a passing negative — the one implementation error that mattered here, and it is absent.
- Oracle values verified analytically: E0 = 3/2 − 2 = −0.5; L = √3/2 = 0.8660254037844386 (matches to the last digit); vis-viva v² = 2/0.5 − 1 = 3; T = 2π; apoapsis speed 1/√3 (the rung's constant …58 is the correctly rounded value; computing √0.75/1.5 gives …57 — 1 ulp of association, no action).
- Two benign reading notes: bound_fraction (j−1)/N vs j/N differ by 5e-7 for euler (immaterial to B1); "counting every substep" — KDK's two kicks count as one step, which the rung's own arithmetic fixes (2,000,000 steps = 10^4 orbits → 200; counting force evaluations would give 400 > 256 and contradict the rung header).

## Predictions

`predictions.md` mtime 18:35:44, run outputs 18:35:47.5 — written ~3 s before the decisive run, consistent with the log order (run.log is empty, so mtimes are the only witness). All predictions held: leapfrog max|dE| 1.34e-3 inside the predicted 1e-5…1e-3 band, slope ≈ 0, bound 1.0, 200 steps/orbit; euler unbound at orbit 77.7 (predicted within 500), bound_fraction 0.0078 inside the predicted 0.005–0.05 band, including the correctly foreseen vacuous E1 pass on the post-escape plateau.

## Attack (adversarial cases)

1. **10× longer** (2e7 steps, 10^5 orbits): leapfrog still bounded, same max|dE| 0.00134469, slope 7.5e-11 — no secular leak hiding past the frozen horizon. euler's first unbound step unchanged (15547).
2. **Compiler sensitivity**: author's binary at `-O0` reports bit-identical metrics — no FMA/optimization dependence.
3. **e = 0.9 at the frozen h**: leapfrog unbinds on step 1 (pericentre r = 0.1 under-resolved at h ≈ 0.0314) → bound_fraction 0. B1 bites when a real failure exists; the criterion is not decorative. **e = 0**: max|dE| 1.2e-7, slope ≈ 0 — correct h-scaling.

## Novelty and fit

Calibration canary, first execution under the lab's directed-rung machinery (H0200 froze canaries then r1–r3); no prior H-entry covers it. Consistent with board bottleneck 2 ("one fixed step passes the physics at about 350–700 steps per orbit" — that bar is for full physics quality; energy boundedness alone holds already at 200 steps/orbit for e = 0.5, no contradiction). PRINCIPLES fit: "A test that cannot fail is a control" — euler is the control and failed as it must, on B1.

## What the author missed

- The exponent metric measures only secular trend; it reads ≈ 0 both for escaped negatives (plateau, flagged by the author) and for genuinely fluctuating bound cases — max|dE|, reported in the dossier but not a criterion, is the amplitude discriminator. Worth remembering when reading future rungs with negatives that stay bound.
- The "counting every substep" wording in the rung is ambiguous (steps vs force evaluations); the header's own arithmetic resolves it, but a future rung could pin it explicitly. The frozen rung is not mine to edit.
