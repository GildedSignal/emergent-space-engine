Working...
Check complete. **Verdict from `lab/verdict.py`: PASS** — leapfrog passes E1/B1/C1, euler fails B1 exactly as the dossier claims.

**What I did**

- **Reproduction** (clean scratch tree, empty `patch.diff`): every number bit-exact — `metrics.json` md5 equal, all six data files and `picture.svg` byte-identical, deterministic across reruns, 0.106 s wall vs the dossier's 0.11 s.
- **Independent implementation** written from the rung text alone (own window logic, vis-viva start): agrees — euler's first unbound step identical (15547, orbit 77.7350), max/final |dE| identical, exponents agree to 6 digits (residual ~10⁻¹⁰ is float-path noise). Slopes also recomputed from the author's `win_*.txt` with an independent least-squares: identical, window edges match the spec's log-spacing exactly.
- **Oracles:** E0 = −0.5, L = 0.8660254037844386 exact, T = 2π, r envelope 0.5–1.506 with no secular growth over 10⁴ orbits, leapfrog conserves L to 1.6e-13. `predictions.md` (18:35:44) predates the binary and all outputs (18:35:47.4x–.5x); every predicted band held.
- **Adversarial cases:** (1) slow euler inside the window span — E1 still blind (0.0087); (2) **new finding: a bound-but-drifting euler (h = T/2000, 10³-orbit horizon) passes both E1 (0.07) and B1 (1.0) with |dE| = 0.49** — near-saturation drift defeats both metrics, extending the author's escaped-negative caveat; (3) unsaturated drift fires E1 at 0.708, so the metric is alive; (4) leapfrog bounded at e ≤ 0.8, dies at e = 0.9 — the frozen e = 0.5 sits well inside the stable region, but C1 is eccentricity-blind; (5) verdict.py tamper paths (VOID on neutered negative, DISPUTED on mismatch, VOID on gaps) all fire correctly.
- **Novelty:** machinery lands in `6b22aee`; HISTORY.md's Kepler entries are law-lab orbit banks, not canaries. No redo.

**Files written** (nothing else touched in the run folder; no git commands run): `metrics-check.json` and `check.md`.
