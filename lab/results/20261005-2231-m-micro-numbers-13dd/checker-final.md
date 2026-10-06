Working...
Check complete. `check.md` written to the run folder; nothing else touched (all adversarial builds ran in `/tmp/check13dd`; no git commands).

**Grade: silver.**

**Reproduced:** every physics number in the dossier matches its recorded outputs exactly — probe A's full table (exponents, fin_med, identities, min_d, one-step fails), probe B's digest counts, probe C's digits. Only ns/op moved with load (ratios unchanged at 0.34–0.35). Pre-registration is genuine: `predictions.md` (22:37:45) predates the probe sources (22:55/22:57) and outputs (22:59).

**What survived my attack:**
- Floor-at-the-shear walks, robustly and accelerating with window length (0.108 @ 50 orbits → 0.393 @ 200; 0.169 conjunction-free).
- The fixed-grid carry constraint is mathematically sound — I verified the m=30 worked example by hand and the `unkick` inverse construction algebraically.
- A5 (the adaptive rescale) is uniformly worst-or-near-worst and non-invertible in every scene — the case for retiring the re-expression is solid.
- Bit identity of A1–A4 held everywhere; probe C holds to 2.2×10⁻³ even at 6 factors over 4 octaves and 10^±300.

**What did not survive:** the headline "nearest/carried bounded at 0.001" is 50-orbit-window luck on one fixed seed table. Fresh seeds: 0.053. 200 orbits: 0.057–0.075. In the conjunction-free two-body scene nearest-shear (0.057) is float64-class (0.082) — it walks too, ~3–7× slower than floor, under B12's 0.2 but not bounded. "B12-class guarantee from structure" is overstated.

**Other findings:** the shear-as-bijection is prior art inside the repo the same evening (`lorentz.rs`, commit 7f81a9c, 17 min before predictions — uncited in the dossier's novelty framing); probe B's float arm has i64 wraparound on 34% of sources (6510/19200) plus a +2¹⁰ rounding-offset slip on the exact arm and a precompute asymmetry in the timing; the dossier's quoted timings don't match its own `.out` files.

**The gold experiment:** wire the rounding rule into the engine's own quantize site (force.rs/kicks.rs) and pass B12 on the plane — measured on the design's cheap path, not a standalone probe.
