Working...
Check complete. `lab/results/20261006-0220-redteam-fermi2-v2-b7a4/check.md` written — first line `Grade: gold`, abstract at the 120-word budget (123 naive tokens, two dense formulas included), nothing else in the run folder touched.

**What the check did:**

- **Reproduction (clean tree):** `sanity.py` (0.7 s), `kernel.py` (49.4 s), `leakage.py` (3.6 s) — `decisive.log`, `kernel-table.json`, and `leakage.log` all **byte-identical** to the stored copies. `patch.diff` empty. Timeline verified: predictions 02:34, decisive run 02:47. One anomaly: the JSON's mtime reveals a second, unlogged `kernel.py` run at 02:48 — benign since output is deterministic and identical, but undisclosed.
- **Provenance:** `probe-orig.py`/`eeff-orig.py` byte-identical to the prior run's files on its branch.
- **Adversarial cases (4):**
  1. Reproduced the prior run's artifact epoch columns from **their own code and stored JSON**: 3214.2/4017.2/4037.7 (landing on 2.0–2.5 turns of 1608.5, exactly as the author predicted), naive 16080.9 at 3.1M, and their fixed-sign tensor counts 2877/2395 exactly; the author's doubled-angle fix gives 1608.5 = 256·2π at every radius, which I re-derived algebraically (ω = √(M/r³) ⇒ sweep = 2π over their window). The half-angle unwrap bug is confirmed at their line 118.
  2. Held-out radii r=8, r=30: epoch formula vs einsum quadrature agree to 1e-5; axis = 512π√g exactly.
  3. Held-out kernel scenes r=3.5, r=5: geodesic Richardson −3.99996/−1.74997 vs closed −4/−1.75.
  4. E-independence bit-exact in closed form at the original P4 scene; the prior run's "eccentric" re-label checks out (ra = 7.5 exactly, e = 0.071).
- **Novelty:** nothing in HISTORY (newest H0214) or docs; this is the prior checker's specified gold-making experiment and HANDOFF's queued second author. It also corrects the prior **checker's** own "4017", which was itself an artifact.
- **Why gold, not silver:** every adopted number regenerates and survived my attacks; the one failed sub-prediction (P6 unbound: 6898/5320 vs <1500) is secondary to all adopted claims, was reported as failed (not claimed as held), and is diagnosed.
- **Recorded misses:** three log-contradicted side claims (transverse ≤2e-4 fails at 2.3e-3 on rosette peri; "true = naive" axis is 308 vs 289 at 3.1M; `leakage6.log` doesn't exist), P4's silent scene change, two cosmetic `sanity.py` bugs, the unlogged re-run, and the admitted gaps (out-of-plane eigenvalue unmeasured, τ₁₀×epoch not re-measured, unbound epochs closed-form-only).
