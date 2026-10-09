Working...
Check complete. `check.md` written — **Grade: silver**.

**What I did:**
- **Reproduced all three commands** (clean tree, `patch.diff` empty): `cost` example gives compile 3.6 µs / state 3.0 / cartesian 0.3 / from_state 12.2 (claimed 3.4/2.8/0.3/11.1 — within 10%); reabsorption re-run memory-safe (10⁷, 2×10⁷; 1.46 GB peak vs the author's disclosed 3.6 GB on 5×10⁷) gives 6.97 and 6.34 ×10⁶ /s/core against the claimed 5.7–7.0; `budget.py` regenerates `budget-table.md` byte-identically, and I hand-verified every headline row's arithmetic.
- **Verified the stored evidence**: kick.jsonl 812.8 pairs/kick, 4345.4 µs/kick, slack 0.9458; steady.jsonl 0.00586/orbit; representation.md:68/:90/:114 and law.md:35 all say what's cited.
- **Predictions**: mtime proves pre-registration before the reabsorption run; three brackets missed (compile, reabsorption rate, and the cascade 0.077 vs its own 0.5–10 at the working point) — all disclosed, which is itself evidence of no tuning.
- **Four adversarial cases**: (1) the real find — the author measured the heap rate (348k keys/s) and left it out; a queued-window design costs 0.52 cores in the two-tier regime, 6.8× the "binding" term; (2) resonance × P=1 yr combined gives 1.1–11 cores (inversion corner); (3) encounter constant 7× low vs their own scale.jsonl (ranking unaffected); (4) 5-order extrapolation from one harness family.
- **Novelty**: docs/fermi.md is a 26-line memory identity; the assembled steady-state budget, the kick-row correction, and the per-body-key exclusion (12 GB > 8 GB) are new.

**Why silver, not gold**: fully reproduced and honest, but it ranks levers already on the board (no new 10×), and its central bracket missed low at the working point — the table's finding is headroom (max rtf ≈ 5,200), not a bind. The one experiment to gold: measure the cascade + program-level queue cost at N ≥ 10⁶ on the integrated path, closing the extrapolation and making the table load-bearing for the b-h-live build.
