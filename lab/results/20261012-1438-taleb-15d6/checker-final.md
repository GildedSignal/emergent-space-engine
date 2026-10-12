Working...
Check complete. `check.md` written to the run folder; nothing else there touched, no git operations.

**Grade: silver** — real, reproduced, one aimed-at-the-wrong-target experiment away from gold.

**What I did**
- **Reproduced** everything from the dossier in a clean tree with `work/patch.diff` applied: `control|pileup|espread|snap|scale` all match `run-log.txt` bit-identically on counted quantities (peak 415 MB; nc51200 hangs exactly as documented). Census sampled ranks wobble ~±1 pp across processes — the "±0.1%" note understates the author's own two runs; immaterial to any conclusion.
- **Predictions**: `predictions.md` (14:51) precedes `run-log.txt` (15:05); held-out claims held, misses honestly self-reported.
- **Adversarial**: seed robustness (13.7–15.1% on 3 fresh seeds); fixed-occupation scaling (miss flat across nc 200→3200 — occupation, not n); true-λ key sound at e=3e-2 where mean-λ hits max 171.
- **The decisive probe**: the red-team's target already exists — `wt/cx-b-coorbital-cert` (adce00d6, 10 Oct, named in the author's own dossier, one `git log --all` away). I compiled its `phase.rs` verbatim and ran it against the author's break scenes: **0 misses on all six**, and at 10⁶ — it measures window occupancy instead of assuming k=4 and bounds the equation of centre exactly. Both recommended guards were already built, stronger.

**What the author missed** — and what the check recovers for the integrator: the built cert's live gap is **cost, not soundness**. At the gold's own e-generator and 10⁶ ships its window k is ~3400 (3.4×10⁹ visits, ~1400 per contact) because reach is equation-of-centre-dominated — a number the author's ρ-occupation census (p50 3) cannot see and the builder's sparse scale gate (max_k=1) never measured. The missing dimensionless number for the built certificate is EoC-reach × density. Also flagged: `b-coorbital-cert.md` and the taste log still carry the rank-4 premise, so the queue spec remains dangerous as written.
