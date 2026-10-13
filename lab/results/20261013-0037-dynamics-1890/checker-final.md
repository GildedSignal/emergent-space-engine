Working...
Verification complete. The tree is back as the runner left it (the author's examples were already restored out by the runner after regen; my probes are removed; only `lab/results/` is untracked).

## Check summary — `20261013-0037-dynamics-1890` (high-gamma-clock)

**Grade: silver** — written to `lab/results/20261013-0037-dynamics-1890/check.md`.

**Reproduced** (runner's regen + my re-runs from the patched tree):
- Sweep bit-identical on re-run: 403 ok / 81 `Range` / 6 `NoBoundOrbit`; E→1⁺ compiles at all 22 periapsis values; k·peri ∈ [1, 1.0001] at E ≥ 100.
- Flights: pump (γ 30.7→1.2082→186.7), turnburn (γ 1.1856, peri 2.1e10, **69,660 refusals survived**), fwd2_farstar silent leave death (k=0.526, E=1.000000, `fault=None` — leave path confirmed at step.rs:667).

**Attacks, all outside the author's domain:**
1. Refusal region pushed to periapsis 1.6e10 M (8× deeper): `from_state` refuses everywhere, `from_invariants` builds the same key cleanly — the "fit arithmetic, not the key" claim extends.
2. Pump reproduced at γ 5 (min 1.0177 → repump 21.9) and γ 300 (min 12.5 → repump 393.4) — noting the author's own window held **zero** post-switch checkpoints for γ 300.
3. **fwd15 flown to the 2^40 window end: alive at γ 2,056, k flat at 1.09e-8, zero refusals** — the old γ≈1,800 wall is gone on shipped code (the pre-merge page's open direction 4, measured in the lab for the first time).

**Why not gold:** `predictions.md` self-discloses as written after the runs — nothing was held out (r3-v3 precedent). Plus the dossier's brake_g300 "same shape" was extrapolation at publication, and the clock error band was quoted from point values (regen shows 1.96e-6; my γ-1,879 extension 1.3e-5).

**Page corrected in place** (5 overstatements: γ-300 attribution, error band, "and it compiles" → 5-of-8, non-regenerable E_key figure, domain bullet now carries the γ-2,056 extension). Gold path named: pre-register, then fly the prograde-nose pump threshold, the in-flight E→1 crossing, and re-derive L from the flight's own tube words.
