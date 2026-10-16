Working...
Check complete. **Grade: silver** — written to `lab/results/20261016-2138-dynamics-217f/check.md`, with the author's wiki page corrected in place where it overstated. Tree restored to shipped-clean.

**What reproduced (regen exit 0 plus my own runs):**
- The mechanism is real in shipped code: `escalation *= 2.0` (alloc.rs:1410), initialized 1.0, consumed only by `speed_factor` = `margin·E·vmax + (E−1)` (line 544), never reduced anywhere. A genuine one-way global ratchet.
- Newtonian battery: conflicts at ignition only, then zero rollbacks forever; latch frozen through stage 17 **and my 40-stage run (80,000 chronons)**; digests bit-identical across shipped/decay/off arms at both horizons. The certificate moves scheduling, never results — every run.
- Novel: no wiki page or H entry measures rollback/AIMD dynamics; the fix is 10 lines, default-off, digest-safe.

**Why not gold — three adversarial findings:**
1. **Nondeterminism**: three identical shipped runs latched ×2, ×2, ×4 (fix phase saw ×16); late regions 33/33/9. The dossier headline "frozen at ×4 after two conflicts" is one sample — disclosed in fix-final.md, not in the dossier or page (both now corrected).
2. **The tax is overstated**: "77–90 vs 1–2 avoided/stage" is law-confounded — the decay arm at escalation 1.0 on the *same Newtonian scene* still pays ~54/stage, so the ratchet-attributable cost is ~×1.5, not ×50.
3. **The author's own named decisive experiment, flown by me** (frames harness, 60 Hz, rates 15k/30k, 3 reps/arm): no shipped-vs-decay deadline-miss separation at 44 bodies. Plus my sub-stride probe (200-unit relativistic cells, closer than any author scene): zero conflicts — no relativistic geometry has ever latched the ratchet.

**Gold path**: a tax that survives its surface — frames or ≥10⁴-body comparison, latched vs decayed, over enough reps to beat run-to-run noise (or the honest "hygiene-only" conclusion, also adoptable); paired with per-region escalation, since the global halving mirrors the global doubling's wrong locality.
