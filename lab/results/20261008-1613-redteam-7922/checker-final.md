Working...
Check complete — `lab/results/20261008-1613-redteam-7922/check.md` written, **Grade: gold**. Nothing else in the run folder touched (the script ran from a /tmp copy; `patch.diff` was empty, no tree edits to apply).

**What I did and found:**

| Check | Result |
|---|---|
| Reproduce | Bit-identical, 3.04 s, 207 MB peak |
| Predictions ordering | `predictions.md` 16:22 → decisive output 16:28:25 → dossier 16:29 ✓ |
| P1/P2/P5/P4 | Held (P4 after the author's disclosed sign fix); P3 half-missed, honestly re-scoped |
| Independent physics | My own derivation n* = (8·floor/5)^{1/3}·(\|E\|/δ)^{2/3} matches all 9 horizons ≤0.8%; δ-scaling confirmed (0.040–0.047 vs 0.0464) |
| Adversarial: beyond grid | e=0.999 → 0.20 compiles/kick (4× the 0.05 budget); e=0.9999 → jet dead — steeper than the dossier claimed |
| Adversarial: belt arithmetic | Exact-cost recompute (no power-law fit): p99 = 10×, p99.9 = 44–51×, share(e>0.9) = 13–18% — the author's numbers sit inside; concentration robust |
| Adversarial: A2 optics | Independent Schwarzschild null integration: n=1 aligned image deflects 6.2870 vs 2π (0.06%); Darwin's C0 = −0.40023 confirmed; weak-field limits validate the integrator |
| Premise audit in-tree | r1 seeds stop at e=0.7, light b∈[10,1000] vs b_c=5.196M; B9 gates creation cost only; H0178 "non-separatrix"; `lab/rungs/` has no r5/r6; representation.md:32 Binet headline is stale vs law.md:85 darwin16 |
| The open branch | No jet re-anchor trigger exists in the crates (frame "anchor" is a different mechanism) — the ambiguity is live in law.md:35 text about to be implemented; cost numbers hold either way |

**Gold because:** it shows a design premise wrong by 29× at e=0.99 (25 vs df81's 730-kick constant), reproduced, independently confirmed two ways, on board focus items 1 and 4, adoptable in one sentence plus two rung criteria.

**Recorded misses:** A3 overstates r5 (B8's engine tests already judge dense/sparse identity — right for r6 only); the compiler's own e-sweep stopping at 0.9 is a stronger in-tree citation the author missed; df81's folder and B18b's σ aren't on this branch (taken from law.md's word); the belt headline rides the correlated-kick worst case with no mixed-secular sample.
