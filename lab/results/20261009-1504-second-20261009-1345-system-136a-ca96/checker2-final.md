Working...
Check complete. `check2.md` written: **Grade: gold**.

**What I did**

- **Reproduced everything from the dossier's commands** in a clean tree (empty `patch.diff`, no crate edits): `regen/exp.py` bit-for-bit (7.3 s); `exp2` — all 12 sweeps, both controls, wall-clock row identical (only p99/max last-digit timing jitter; med 2.21 µs matches); `exp2b` — **bit-for-bit identical** `metrics2b.json`. Peak 72 MB, well under budget.
- **Provenance held**: `predictions.md` (15:13:34) predates both run outputs (15:17:32, 15:21:28) and the dossier (15:23:32).
- **Four adversarial classes of my own** (`/tmp/check2-136a/exp3`, 17 full-population sweeps): fresh seeds 2/3 reproduce the zero-miss cliff at [1×10⁻⁵, 3×10⁻⁵) and the 9.3–10% fine-band miss; −δ symmetric; high-e belt σ_e=0.3 misses 34% at the fine band; and **common-mode ϖ rotation with Δϖ = 0 — the cache key unchanged — still misses 5.5% at 2.4×10⁻⁴**: the key is blind to absolute ϖ, which the original's own model drifts 22.6× faster than differential, so the kill is *stronger* than the dossier claims. `extra = 0` everywhere.
- **Novelty/goal fit**: no HISTORY entry measures section staleness; this is the checker-named gold experiment for today's silver, it deletes a pending adoption, and the comparison is a faithful model of in-band reuse (verified against the crate's `sections`/`run_section`/`check` and `SAFETY = 1.1`).

**Why gold despite P1/P3/P4 failing**: the failures are the measurement itself — the run existed to test the guess that 2.4×10⁻⁴ is safe, the interpretation was pre-committed on both branches (delivered ×1.8 = 32·δ*/1.77e-4 exactly), and every claim-bearing prediction (controls, miss ordering, extras, wall-clock) held.

**Disclosed in check2.md**: my exp2 rerun overwrote `exp2/metrics2.json` and `exp2_fragile.jsonl` in place (the dossier's own command does this); I verified all numbers identical, then restored byte/size-exact. Also noted: the stored 162 KB fragile file was an undisclosed post-run prefix of a 5.9 MB deterministic output, plus three minor prose-rate slips (90.9%/91.1% actual vs "90.3%/90.5%").
