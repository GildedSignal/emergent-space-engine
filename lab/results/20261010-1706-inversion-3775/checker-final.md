Working...
Check complete. `check.md` written to the run folder — grade: **gold**.

**What I did:**

1. **Reproduced**: ran `breakup.py` in a clean `/tmp` copy — 11.4 s, exit 0, results.json **bit-identical** to the stored one (only `load`/`runtime_s` differ). All 17 dossier table rows match results.json exactly.

2. **Prediction record**: predictions.md (17:18) predates the final script (17:29) and results.json (17:32); patch.diff empty. Core predictions held (null plane exact at 3.3e-16, epoch stream flat ~3 checks/encounter with zero misses, formation control 0 misses); four magnitude misses honestly self-reported — which argues against tuning, not for it. No kill criterion triggered.

3. **Adversarial cases** (my own, all under budget):
   - σ=0.05 (50× dispersion): retention exactly 100%, plane residual 4.4e-16, rank-4 misses **92%** — failure worsens.
   - Bound eccentric parents (fragment e≈0.5 and 0.67): retention exactly 100%, epoch stream 2.9–3.0 checks/encounter, rank-4 misses 75–84%. The author's caveat (ii) resolves *in favour* of the claim.
   - Tighter belt: 55.0% — the dossier's non-regenerable parenthetical is real.
   - 3D argued: pairs share only P, so both the kill and the fix strengthen.

4. **Novelty**: the Binet-cone-equals-crossing-condition is documented (docs/law.md); the null-plane corollary, the churn kill, the cone-probe trigger, and the focus epoch-stream certificate are new — no prior mention of breakup clouds anywhere. The attack targets the real queued spec (`b-coorbital-cert.md`), whose test scenes contain exactly the gap this run exposes.

**Why gold, not silver**: it shows a gold's premise is wrong for the scene the game mass-produces on every death (exact mechanism, controls on both sides), deletes quadratic pair state for plane populations (5×10¹¹ pairs → O(N log N) sorts), and is adoptable in one step (re-route the queued build). Defects recorded: the 55% number not regenerable from shipped code, the structural nature of the epoch stream's "0 misses", the "46% of real encounters" wording (it's of at-P encounters), and the unexploited θ_Q clustering that could close the 14–39% at-Q residue.

Nothing else in the run folder was touched; no git commands run.
