Working...
Check complete. `check.md` written; tree restored to as-found (patch reverted, only untracked `lab/results/` remains); nothing else in the run folder touched.

**Grade: silver.**

- **Reproduction (bit-for-bit).** Fresh build 41.6 s; both gate groundings exact (planted-bounded 0.353 / worst err 1.27e-5; planted-compound 0.416 / 9.8e-7 — the P2 ranking inversion indeed absent here); the ignored dump test regenerated all three streams md5-identical to the author's; analyze.py reprinted every number in the dossier's table, the all-16 check, and the VR columns.
- **Predictions.** Written 19:54, before the streams (19:58) and analysis (20:01). P1/P3/P6/P7 held; P2, P4 slope clauses and P5 failed narrowly and were disclosed — consistent with pre-registration.
- **My attacks.** Seed sweep: clean and floor+δ* leak 6/6 LEAK (0.40–0.63) — but one re-draw at exactly δ* read 0.208 (grey), so the "empty gap ≥ 0.251" is a draw, not a guarantee. Coupled e+a walks still caught (new robustness). OU bounded error: no false positive. Pure-a memory: invisible (the author's disclosed blind spot, confirmed). Detection band lower edge ~2× optimistic (floor+δ*/2 → grey).
- **For gold:** wire the curve into B12-v2 and run it on the plane law's streams with a seed-robust verdict rule.

Nothing blocked; 30-minute budget respected (all processes well under 2 GB).
