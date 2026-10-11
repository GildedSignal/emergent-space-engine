Working...
Check complete. **Grade: silver** — written to `lab/results/20261011-0517-taleb-3ebf/check2.md`.

**What held (the core):**
- **Bit-identical reproduction** of all 8 scenes in 35.9 s: encounters, cross fractions (72/61/64%, 12/10/11%), plateaus (0.28–0.39, 0.88), union kmax 7/14/31, cone_cross = n² exactly, exponents 2.00 / 1.97–2.02 / 1.91–1.98, ~397 setup evals/pair, 286 evals/encounter window tier. Controls reproduce the gold regime; `outside_cone` = 0 everywhere; lib is a verbatim crate copy (empty patch).
- **Held out on three fresh geometries** (my own seeds/builders in /tmp): apogee-graze interception 0.886 at k=32, perihelion interception 0.898, wide 2.5 rad packets 0.930 — the different-period failure is structural, not geometry-specific. My t_meet-sort control also validates the author's merge-join fix hint (kmax 299→41, ≥0.991 at k=32).
- Predictions pre-registered (mtime order consistent), 8/11 held, misses honestly diagnosed — including the honest correction that work per encounter is flat, not ∝ n.

**Why not gold:**
- The headline "19× fewer pairs, zero misses" is contradicted by the log's own data: zero-miss k at n=600 is 32 → **9.4×**; 18.7× (k=16) silently drops 2.1% — the exact failure mode the run forbids. By the author's own canon, that costs the grade.
- The positive fix ("group by integer period") is unmeasured at its boundary: my sweep shows a-spread 1e-3 already needs k ≈ 0.4·n, and b1's own 1e-4 a-jitter gives distinct integer periods — the fix only holds if fleets are period-quantized, a requirement the dossier never states.

Named gold experiment: period-keyed grouping sweep (exact shared keys vs spread) plus the corrected 9.4×. Folder otherwise untouched; no commits.
