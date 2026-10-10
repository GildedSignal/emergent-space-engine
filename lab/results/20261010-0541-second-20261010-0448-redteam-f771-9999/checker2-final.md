Working...
Check complete. `check2.md` written with **Grade: gold**; nothing else in the run folder touched, `check.md` never read.

**What I did and found:**

1. **Reproduction — exact.** All three dossier commands in an isolated temp tree (2.7 s / 4.1 s / 40.4 s, each < 60 s): `r1w-output.txt` regenerates modulo the host line, `metrics.json` bit-identical across two runs (sha `ad519e7b…`), and every number in the curated `controls.txt` regenerates. Verified `binet_probe.py` is byte-identical to the parent branch's shipped script and regenerates that branch's `probe-output.txt` — the shipped tie-out is genuine, including the (7, 0.99) row (4.45e-4 / 1.93e-2 / 246).

2. **Predictions** — mtime order clean (06:04:30 → decisive run 06:27:25); 7/10 held, misses disclosed, all load-bearing ones (kill, m32 pass, low-e hole, m⁻², e*) held.

3. **Adversarials (5):** fresh-seed sweeps show the m16 kill in 5/5 draws and m32's worst draw at 0.9961 ≥ 0.99 (matching the Fermi argument); direct m=70 run confirms the budget extrapolation (9.79e-4 at 1070 crossings); invariant 1 confirmed necessary (on-grid absorb edge crashes capture); e=0.9999 m16 misclassification reproduces as the dossier frames it; **new finding:** below the e=0.01 floor the m32 period bias grows to 2.6e-2 at r_p=7 — up to 5× the top-corner bias, on the near-circular orbits players actually fly, and the re-freeze narrows the original envelope there without pricing it. Flips no frozen criterion, but the domain statement is asymmetric.

4. **Novelty** — this run is exactly the experiment the parent's silver named as the path to gold, plus the precession kill axis, a working hyperbolic branch, the e* table, the invariants, and the repeat-reading resolution.

Gold stands on: bit-for-bit reproduction, robust two-criterion kill, m32 qualified at e ≤ 0.99 with a measured banding decision, and a one-step-adoptable re-freeze whose criteria block is byte-identical to r1's frozen one — with the sub-floor pricing, the m64 median-vs-per-seed cost reading, and the Python-port caveat named for the integrator.
