Working...
Check complete. `check.md` written to `lab/results/20261006-1029-system-06a8/`; nothing else in the folder touched; no git commands run; scratch work isolated in `/tmp/check-06a8`.

**Grade: silver.** Summary of what grounded it:

**Reproduced** — `python3 probe.py` (23 s, deterministic, bit-identical raw.json matching the author's; patch.diff empty). Every table number matches; two prose-only discrepancies (A32 evals 32.1 not "32.3"; 14 of 15 apsidal failures, not 12). Both controls behaved; kill criterion fired in its strongest form; predictions.md predates the decisive run.

**Attacked three ways, all confirming the kill:**
1. **Kernel coefficient** — the author's `gsec = 0.75·n·μ·α·b⁽¹⁾` looks 3× the Laplace–Lagrange rate (n/4·μ·α·b⁽¹⁾). Rerun with ÷3: nonres 0.688 → 0.771 (still < 0.90), res pump 0.653 in-band 0.00. Verdict survives.
2. **Window width at 2:1** — pump recovers (0.667 → 0.94) only as the window widens to 180°, where the schedule degenerates into a uniform cadence at A-comparable eval counts, and A4 still beats it. Also proves the dossier's "coarser sub-steps" mechanism is wrong in direction: B8's sub-steps are 6× *finer* than A4's 1.48-yr cadence (the "0.078 yr" figure is bogus); the real failure is coverage of the delocalised tide.
3. **Held-out 3:2 band** (never tested by the author) — B8 pump 0.693, in-band 0.00; the resonance kill generalises.

**Why not gold:** the resonance half was already legislated (H0203, H0205 killed instantaneous conjunction kicks, representation.md:68 restricts them to resonance; uncited by the author), so the run kills a tempting *reading* rather than a held premise; the positive deliverable (fixed-cadence floor ≈ 8/orbit at probe tolerances) is float-replica-level; and the dossier's two mechanism narratives carry errors (the 0.078-yr arithmetic; "truncation, not cadence" mislabelled — the failing seeds sit at the resonance fringe where the lab's own rule says averaging breaks, and the proposed full-α kernel would not fix them). The named experiment for gold: fix the coefficient and re-measure the cadence floor on the design's own path (integer law / plane behave gates).
