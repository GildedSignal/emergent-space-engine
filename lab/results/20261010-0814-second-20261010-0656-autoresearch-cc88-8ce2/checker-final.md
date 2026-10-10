Working...
Check complete. `check.md` written to the run folder; nothing else touched; tree restored to clean HEAD.

**Grade: silver.**

**Reproduced, exactly:** E1 (baseline 87.7 → 74.0 µs with cc88's keep.patch, digests `59ea9969…`/`13cfe88b…` identical, refused 0, memo negative confirmed); E2 digit-identical (618 kicks, 45 anchors, 0.0728 compiles/kick, dk max 1.305×10⁻⁷ — and the churn-limited arithmetic is airtight: even all kicks on one body accumulate 8.1×10⁻⁵ < θ); E3 errors/anchors identical (timings only shift on the shared box); both suites green; `predictions.md` (08:23) precedes both evidence files.

**Adversarial findings (mine):**
1. **The plane's kicked bodies sit at median e = 0.94** (max 0.999) — the one variable joining E3 to E2, never measured by the author. At the plane's own kick size (1.3×10⁻⁷, one 45-kick churn window) the readout errs **4.36 relative at e=0.99, 1.97×10⁻⁴ at e=0.9, zero refusals**. So "the deletion stands for the plane's real workload" holds only for the advance increment; under df81's criterion (Δφ *and* Δt) the jet fails at the plane's actual e-mix.
2. **The refusal story is false:** refusals = 1–2 per 10,000 kicks at e ≥ 0.9 (their own anchors=15/16 were drift anchors alone) — the high-e failure is *silent* misalignment, worse than the clean refusal the dossier discloses.
3. The E3 table's e≥0.9 row mixes θ_r-campaign period/radius into the df81-θ table (actual: 7.1×10⁻³–1.3×10⁻¹ and 1.5–156).
4. Random-sign kicks (df81's second mode, untested) still break the readout 15× above floor at e=0.9.

**Why silver:** everything measured reproduces exactly, the work is novel (the second check df81 never got, first on the shipped integer compiler), and the falsification of df81's θ for Δt/readout is a real, adoptable premise correction to law.md's jet clause. But the load-bearing adoption claim (0.073 compiles/kick on the plane) is decomposed, unwired, and decided by the unmeasured e-mix my probe undercuts. The named gold experiment: re-run the cadence at the per-e budget θ(e)=√(floor/C_r(e)) on the plane's real population and wire the jet into `bind` for the end-to-end median.
