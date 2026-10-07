Working...
Check complete. `check2.md` written; nothing else in the run folder touched (all reproduction ran in a `/tmp` copy — `cert2.py` overwrites `results2.json` in place, so running it in the run folder would have destroyed evidence).

**Verdict: silver** (second checker, blind to the first).

**What I did:**
- **Reproduced bit-for-bit**: `cert2.py`, `cert.py`, and the B2 heredoc in a clean copy. The regenerated `results2.json` matches the stored one on all physics (only the machine block differs); the B2 snippet reproduces `results3.json`'s seven realized encounters exactly; `cert.py` reproduces `run1.log` line-for-line including the documented crash. I re-derived by hand the Binet tangency algebra (Δϖ\* = 0.7268, travel 1.4268 rad → t_tang = 2854/1427/713.6) — correct.
- **Protocol**: `predictions.md` (15:56) precedes all scripts and results (16:07–16:16). Predictions 1 and 5 held; 3 failed as written and was honestly disclosed — but its pre-registered exponent (H ∝ Δϖ̇⁻¹) was never measured (ensemble misses at one rate only; run-1 slope 0.45 nonmonotone).
- **Three adversarial cases of my own**: e=0.7 and retrograde pairs both age under differential precession (controls exact — mechanism generalizes); the author's proposed co-precessing fix probed viable (0 misses vs 27/27 waste + 1 miss) though partly vacuous (the test pair un-crosses; deep-crossing untested, nothing in the crate).
- **Novelty**: confirmed — `crates/encounters/src/kepler.rs` fixes `pom` at construction; no history entry couples precession to certificate aging.

**Why not gold**: the horizon law was pre-registered but never fitted; the shadowing question (kick cadence vs the 40–400-orbit horizon — the dossier's "same order" sentence is off by 1.5–2.6 decades) is argued, not measured; the fix is unrung. One experiment away: implement co-precessing sections in `crates/encounters`, rung with ≥3 miss-showing rates and a kick-cadence case.
