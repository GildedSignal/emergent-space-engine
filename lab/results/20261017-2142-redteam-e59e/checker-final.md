Working...
Check complete. **`Grade: gold`** — written to `lab/results/20261017-2142-redteam-e59e/check.md`, with two in-place corrections to the author's proposed wiki page.

**What was verified:**
- **Reproduction:** `python3 falsifier.py` → `evidence.json` byte-identical, 0.2 s. The suspicious shared digits in P5 (`…4073464…`) decompose as `n·0.002 − π` — real integration output at the author's step size, not fabrication.
- **Predictions:** mtime order confirms `predictions.md` (21:51:30) preceded the final script (21:52:50) and dossier (21:53:49); 7/7 held; the P5 sign fix was disclosed.
- **Citations, all in place:** §2 L53–59 has no opacity; `view.rs:15` "(no lensing yet)"; `kerr.rs:717` "captured rays return None"; r6's oracle is literally `rows_found ≥ 0.999` for every live emitter (branch `claude/lab-20261017-1018-redteam-13c6`) — its presence bar demands the rows occlusion must remove; all seven conversation lines verbatim; G6's "observatory provides … occlusion" verified; L28 spoke-count bug real (145, not 128).
- **Novelty:** view.md's 45 runs cover multiplicity/delay/deflection-keys/photon-ring — none measured opacity; HISTORY's occlusion entries are the pre-pivot inertial law, as the dossier's blind-spot note says.

**My three adversarial cases** (independent instruments, none of the author's code): a periapsis-method deflection at dphi=2×10⁻⁵ confirms every P5 value to 5×10⁻⁴ and extends the divergence to b/b_c=1.0001 (8.81049 vs the analytic 8.81011); an outside-domain probe (r_o < 3 M, never tested by the author) shows the Synge-formula reading inverts inside the photon sphere — true shadow 62.0% of the sky at 2.5 M where the formula reads 38.0% — every reported number sits at r_o ≥ 3.2 M and the omission claim only strengthens; and aberration widens a 2R planet's blocked arc 16.7% → 27.7% at closing β=0.5 (54.9% at 0.9), so static arcs are a lower bound.

**Page corrections:** the proposed §2 amendment now carries the r_o ≥ 3 M validity note (the formula would be wrong as adopted below the photon sphere), and direction 5 notes the eclipse-parity gate must cover moving observers. No other files in the run folder touched; no git commands run.
