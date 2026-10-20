Working...
**Grade: silver** — `check.md` written; the author's page corrected in place where it overstated.

**What I did:**

1. **Reproduced exactly.** Applied `work/patch.diff` to the clean tree (base `2a2afff2`), ran `regen.sh`: `instrument-out.txt`, `shipped-defl.txt` byte-identical, `max |residual − tail| = 1.00e−9`, ~12 s. The shipped-law half is sound — capture thresholds sit exactly at Bardeen's b_c±, and I independently expanded the oracle's quadrature tail (next correction ~1e−10), confirming the author's reading that `kerr::deflection` is exact and only the oracle carries its own 2b/r_max cutoff bias.

2. **Main attack (the instrument, not the physics): the shadow-edge map is wrong at a ≠ 0.** The author's α = asin(b√(1−2M/r_o)/r_o) is Schwarzschild's static-observer formula with Kerr b_c substituted — in Kerr, g_tφ ≠ 0 changes the static tetrad's φ-leg. Exact map: sin α = √(g_φφ − g_tφ²/g_tt)·Q/r_o²·√(1−2M/r_o), validated two independent ways (tetrad projection vs radial-only null identity: 6e−15). It moves edges up to 16°, **kills the "retrograde edge wraps past tangential at r_o ≤ 3.2M" claim entirely** (tangential exactly at r_o = r_ph⁻ = 3.3–4.0M, never past — the wrap rows are map artifacts), cuts the centre headline from 33° to 20°, and flips the retrograde error's sign at 3.2M. The χ-blind kill itself survives and strengthens (prograde at 3.2M errs up to −43.9°, worse than reported); the freeze-ready r15 embeds the wrong reference table, so it is not adoptable in one step.

3. **Adversarial cases outside the range:** χ = 0.3 (edge error only −1.5° — below the proposed ≥2.7° negative bar, which needs scoping to the χ grid) and χ = 0.9999 (continuous). Novelty holds (no Kerr-view entry in the record; B19 item 2 gates photon b± capture but no sky map; 039d was Schwarzschild). Predictions: P1/P5 held, P2/P3 failed on sign, P4 half — honestly reported, bars gold by house precedent.

4. **Silver → gold:** one line — re-derive the table and r15 on the exact static tetrad, replace the wrap clause with tangential-at-r_ph⁻, rerun predictions. Oracle, shipped comparison and rim wall need no change.

Tree restored; only `check.md` and the corrected `wiki/representation-premises.md` changed in the run folder.
