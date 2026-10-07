Working...
Check complete. `check.md` written to the run folder; nothing else in `lab/results/20261007-1843-second-20261007-1801-fermi-bb60-152f/` touched, tree otherwise clean, scratch removed.

**Grade: silver.**

**What I did:**
- **Reproduced** everything from the dossier in a clean tree (`work/patch.diff` is empty — no tree edits): all six kick-bench runs (3 seeds × RTF {100,1}) byte-identical on digests, memo blocks and sample counts; determinism rerun identical; refused 0 everywhere. Compile grid, decomposition bench and `budget2.py` rerun — output byte-identical, timings within noise (grid median 38.0 vs saved 37.3 vs quoted 34.7 µs). Frontier arithmetic re-derived by hand (N* 4.79×10⁶, S1c 1.83× over, swing 2,300×) — all check.
- **Held-out predictions:** seeds 2–3, RTF 1, decomposition, cadence, memory cap held; P5/P7/P3-leaver-p99 failed and were disclosed honestly (P7 against the author); P4 failed on made ships (11%, not >50%) but was never scored as a failure — noted.
- **Attacked:** unseen seeds 7/17/99 (exact hit 0.0 over 1,186–1,485 rebinds each) and members=200 concentrated fleet (0.0 over 5,924 rebinds, quantized up to 97.6% — the concentration direction, no claim breaks); the realistic-fleet conclusion is cadence-robust (2.09× over even at K1).
- **Novelty:** the headline kill was already test-pinned in main by `dbd4add` (5 October, "an exact memo never hits on distinct kicks", quantized 94%); the run confirms and extends it, and its genuinely new content is the compile-share decomposition, the (p, e) compile grid, the plane's measured cadence above the K1 LEO rate, and the frontier ∩ 2.5×10⁸ tube-memory wall.
- **Gold experiment named:** measure the jet re-anchor path's actual compiles-per-kick and fold cost on the plane's own rebinds, replacing the cited 0.05 constant with a shipped measurement.

Processes stayed far under the 2 GB budget; each command ran in seconds.
