Working...
Check complete. **Grade: silver** — written to `lab/results/20261008-1337-second-20261008-1252-taleb-2570-9420/check.md` (the only file I changed in that folder; all my runs went to `/tmp/check2570`).

**What reproduced** (shipped binary `cff18e98…`, tree `a838a28`):
- Canonical m192/s1 row regenerates **bit-for-bit** (digest `77d106d9…`, cut 609076340, bodies 212); `low1` differs (0.160 vs 0.029) exactly as documented — wall-sampled, non-canonical, both ≪ 1.
- `analyse.py` → byte-identical `metrics.json`; `verdict.py` → **KILL; killed: plane-4x**, positive passes, negative fails.
- Clamp real: `--members 1536 --describe` → 400 members; instrument exact in code (`dash.rs:104`).
- Predictions (13:40:04) predate every result file (13:40:50+); P1–P5 held on the declared seeds.

**My adversarial cases:** digest twins at the untested bracket point m96/s3 → SAME; m384 seed 3 → 0.000 (negative robust held-out). But **m96 seed 3 → `low1` = 9.70**: the "stall starts at 2×" calibration is a seed lottery — median-of-4 at 2× flips above 1.0. The 4× gate itself is robust (m192: 0.021–0.303 across four samples; m384: exactly 0.000 ×4).

**Why silver, not gold** — two record defects, neither touching the 4× verdict:
1. "Every reported JSON is from a complete rerun" is contradicted by mtimes: 9 of 14 files are first-pass (kept after the 300 s cut; each complete and regenerable — verified).
2. The 2× calibration fails as a median statement on one held-out seed; their own seed 13 (9.63) was the warning.

Gold-making step: a 7-seed m96 ensemble (~3.5 min) or retract the 2× claim, plus the corrected provenance line; the 4× rung can be frozen as-is. Also noted: the digest twins are near-tautological (`digest_at_cut` settles past any stall); the real budget-leak evidence — decisions taken exactly at canonical ticks in all 12 paced runs — does hold and is what the rung's `exact` criterion should cite.
