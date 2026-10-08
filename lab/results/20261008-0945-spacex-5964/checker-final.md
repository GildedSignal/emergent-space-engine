Working...
Check complete. `check.md` written to `lab/results/20261008-0945-spacex-5964/`; nothing else in the folder touched; no git operations.

**Grade: silver.**

Summary of the check:

**Reproduced** — `validate` (1.25e-3, exact) and `main` (`h_live_results.json` bit-for-bit identical, seeded, 152 s), `summarize` matches the dossier's table. Pre-registration is genuine: predictions (09:52) predate the run (10:06→10:09), and the pyc's recorded source mtime/size match the shipped script. But `main` peaks at **11.5 GB RSS** against the window's 2 GB rule.

**Central finding of my check** — a time-unit defect runs through every absolute number. The probe advances `M = M₀ + n·t` with `n = a⁻¹·⁵` rad per time unit, so one orbit = 2π/n̄ = 8.56 time units (the repo's own `encounters` crate states this convention; its truths are real orbits). Torb=100 is **11.7 real orbits**, not 100. Cross-anchored against the repo's frozen truth at the author's *exact* scene (`scale.jsonl`: n=10⁴, σ_e=0.01, ρ=1e-4 → 3.96e-2 encounters/body/orbit): the author's MC converts to 4.49e-2 — **1.13× of truth. The MC was accurate all along**; the printed rate is 8.56× low and the ÷4.2 "correction" (which calibrated the good instrument to the author's biased direct stepper, 0.27× of truth) makes the table rates ~36× low. Plus: `summarize.py`'s creation rates are 11.7× high and internally inconsistent with the dossier's own GB column by ×100; the Elias-delta coder undercounts every value ≥ 2; P6 actually holds but was reported as missed.

**What survives** — the representation decision is robust to all of it: my true-100-orbit probe gives cert ≈ 5–10 bits/body at full density (~7–10× slack, not 40–600×), doll 16–20⁺ bits (25–31%⁺ of the entire budget, growing), ship-mass fleets exactly 0 bits (zero-control reproduced; pure scale physics). Premises are grounded verbatim in law.md's 32-bit (E,L) memo key and per-band fixed point; novel against HISTORY (first dynamic-scar measurement; HANDOFF said "not measured yet").

**One experiment from gold**: re-derive the table in true orbital time anchored on the crate's frozen rows, drop ÷4.2, fix the game-hour arithmetic and Elias length, and measure the steady state past saturation at 100 and 1000 orbits.
