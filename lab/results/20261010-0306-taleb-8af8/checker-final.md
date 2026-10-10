Working...
Check complete. **Grade: gold.**

**What I did:**
- **Reproduced** every dossier command from `work/patch.diff` on the clean tree (`a838a28`): `seam cost`, `ring`, `mixed-arc0.1`, the five-arc graded sweep, belt control — all counters, ranks and fractions **bit-identical** to `work/seam-raw.jsonl`; every command ≤ 14 s.
- **Predictions audit:** `predictions.md` predates the raw results by ~6 min (runs sum to ~80 s — order is physical); P1 held, P3 held (0.18–0.67·ρ·n/arc), P2's completeness half failed and the author reports it as failed.
- **Four adversarial cases** via env-var overrides (reverted after; tree restored clean):
  1. **Random periapses:** rank@enc med 13, frac≤4 = 22% — alignment didn't flatter the law; it's worse without it.
  2. **ρ-ladder (5e-3→1e-3→5e-4):** cross candidates ~constant (25,985→22,437) while encounters ∝ ρ; setups per cross-encounter 17.5→74→139 — the author's argued ∝1/ρ extrapolation is now **measured** (~10⁴ at game ρ).
  3. **Tight convoy (da 5e-4):** the author's escape hatch breaks — encounters multiply (267,866 vs 94,852) and rank@enc med 22, so the gold's evidence sits further inside the failure region than claimed.
  4. **Eccentric fleet (σ_e 2e-2):** rank@enc med 53, frac≤4 = 8.5% at the same ρ·n/arc — the sizing law needs a third dimensionless number (eccentricity); this is the one substantive gap, folded into the verdict as a required amendment to contract (a).
- **Novelty:** HISTORY ends at H0215; the gold's rank-4 is recorded only as a constant in the board's taste log; the seam measurement also tensions the adopted q-candidate-degree silver at the fleet⊕belt boundary.

`check.md` written to the run folder; nothing else in it changed, no commits, no pushes, tree left clean.
