Working...
Check complete. `check.md` written to the run folder; grade **silver**.

**What I did (45 min):**

**Reproduction — all bit-identical.** `falsifier-v2.py` (0.2 s) regenerates `falsifier2-out.json` exactly; every dossier number verified, including cap=1 = the scout's published record (via `git show 96d62b5`), ν=8 at 3.131×10⁵/unit (8.15×10⁶× below pairwise), uncapped 1.4159×10¹² saturated. `consumer-gate.py 256 11,22` (73 s) reproduces the stored JSON identically. Pre-registration clean: predictions.md (20:27:43) precedes both decisive runs; patch.diff empty; tree clean. Two 4th-digit text slips noted (1.418 vs 1.416e12; "binds at ε≥1e-2" contradicted by the script's own sweep, 0.386 < 0.5 at 1e-3).

**Three adversarial findings:**
1. **Held-out seeds 77/88**: fg ladder stable, NN = far_share to 3 digits again, G1-vs-DR1 map advantage 3.4–3.9×.
2. **The author's own named next rung, executed by me** (5 seeds × 20 orbits, 344 s, aggregation fixed — needed a one-line edit since N_ORBIT is hard-coded to 10): **VOIDs again by the same pre-registered rule.** FLOOR fails strict at both radii; riders eject (per-seed deltas +47.6, −110.6); NN *passes* the strict gates at r=1.8 while G8 (the best scheme, fg 6.4×10⁻⁴) fails them. The gates separate chaos luck, not news quality — "one clean rung away" is an instrument problem, not a compute problem.
3. **N-scaling probe** (512 vs 256 stars, fixed total mass): every metric moves *against* the predicted N^−1/2 (ratios 0.92–2.49 vs 0.71), coherently at both radii — the background-only ghost map carries an N-independent coherent star-field error, so the 16×-engine-margin claim is unsupported by this harness.

**Verdict:** silver — fully reproduced, honest VOID, new seed-stable force-error measurements load-bearing for b-news-gravity; the behavioural cap validation remains one *redesigned* experiment away (wire the docstring's S/slope gates, ensemble statistics, aggregate field in the map). The one gold-making experiment and six specific misses are spelled out in `check.md`.
