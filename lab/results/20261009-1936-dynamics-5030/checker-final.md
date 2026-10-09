Working...
Check complete. **Grade: silver.**

**What I did:** reproduced the full pipeline in a clean tree (`/tmp/check5030`, run folder untouched except `check.md`), verified pre-registration by mtime order (predictions 19:42:23 → tlib 19:50:18 → results 19:50:44), ran four adversarial probes, and scanned HISTORY/law.md for novelty.

**Findings:**
- **Physics reproduces bit-identical.** All 440 map runs, tlib.json, results.json, and every dossier number (boundaries per case, Euler 30–100× tighter, drift exponents, C2 Emax 4.1e-5 vs 1.0e-1, plateau 127/12/30, h* scatter 0.25→8) regenerate exactly. Monotonicity check: zero pass-then-fail runs — the boundary is a true floor, not first-touch.
- **Record defect:** the shipped `kick_cadence.py` was edited *after* the stored results and its `analyze` crashes (`TypeError`, line 324) before writing rows.json; the stored rows.json is stale (lacks `ok_strict`). One-line fix regenerates everything — the raw evidence survives, the derived dump doesn't.
- **Adversarial crack:** at 3× the window (60 secular periods), the held-out C6 flips class at N_lib = 30 — above its measured boundary of 19.2. The near-separatrix boundary is horizon-dependent. C2/C3 (the certificate's target families) hold class and e_max at N_lib = 5 over the same window.
- **Model-domain edges:** jz = 0 and e₀ = 0.99 break the DA quadrupole *truth* itself (E-drift 4.4 and 16) — outside scope, not a cadence failure.
- **Novelty:** first measurement of the board's #1 question (q-cadence was queued, unmeasured); distinct from r9's and r4's axes.

**The one experiment to gold:** fix the crash, regenerate rows.json, and run the horizon ladder (20→200→10³ secular periods) on C1/C5/C6 at the certificate cadences — showing mid-amplitude boundaries are horizon-stable and near-separatrix families get a margin or a detectable exclusion (libration frequency → 0).
