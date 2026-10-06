Working...
Check complete — `check.md` written to the run folder, grade **gold**. Nothing else in `lab/results/20261006-0220-q-fermi2-tide-v2-26a7/` touched.

**What I did and found:**

1. **Reproduction (clean tree, no patch to apply):**
   - `python3 verify.py` (15m14s, 56 MB RSS): regenerated `vectors.json` **bit-identical** to the author's — all 18 vectors, 163 checks, the refinement dict, and the same 4 disclosed failures at full float precision (159/163 pass).
   - `crosscheck_redteam.py` (11 s): kernel agreement 1e-13…1e-15 formula-level; the Riemann-free geodesic-pair measurement converges to the closed form (1.4984→1.5000 at r=6, 16.0077→16.0000 at r=3.1).
   - `work/derive5.py` (2.3 s): `omega_expr2.txt` byte-identical; `schwarztide.py` byte-identical to 0dee's — the v2 diff touches only instrumentation, exactly as claimed.

2. **Predictions:** mtime order supports pre-registration (predictions 02:38:41 → decisive vectors 02:54:41). Genuinely held-out items (3, 4, 5) held; the two misses (omega 1.2e-9 vs ≤1e-10; B.frame on long windows) were disclosed, and my independent n-refinement (8.04e-8→5.45e-9, ratio 14.7) and h-refinement (mixed round-off floor ~1e-9) confirm they're tolerance placement, not physics.

3. **My attacks:** plunge families the author never ran (E=1.2, L=2, down to r≈2.05) pass at the instrument floor (errA ≤ 2.4e-9, errW ≤ 4e-12); 40-digit near-circ residuals (−2.5e-16) justify the near-ISO admission; 0dee's stored B values (~1) proven non-regenerable — the defect this run fixes was real.

4. **Recorded against the author:** the X table's 1.2e-12 (actual 2.61e-13), the wrong "−1e-40" mechanism story, "18 families" = 18 windows/9 families, exit code 0 regardless of gates, and the still-untested whirl/turning-point/Φ-unwrap cases.
