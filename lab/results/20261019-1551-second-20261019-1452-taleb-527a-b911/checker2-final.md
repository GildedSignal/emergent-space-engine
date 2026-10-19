Working...
Check complete. **Grade: gold** — written to `check2.md`, with two refinement notes added to the author's wiki page in place.

**What I did** (45-min budget, tree restored clean after):

- **Reproduced**: applied `work/patch.diff`, verified every headline number against the regen logs and my own parses — A guard at gs 328,274 (census 610,481±26 phasing), B/C flat (spans 88/181 bindings), D digit-identical to live's census (204,864), level law 1.35/1.43·K, onset 1.53→2.3 late, ×1.99 duplication, channel-1 saturation 443.9 MB by ~42k in all five arms, refusals 0 everywhere. Re-derived the RSS regression independently in numpy: c1=1.062, c2=1.360, rmse 15.7 MB (an initial disagreement was my own solver bug).
- **Four adversarial cases**: (1) post-onset freeze at 120k gs — outside the author's range; the ratchet still dies, with wave-like bulk drains (90–120k oscillation, RSS flat 750 vs live 878+), so the stock is reclaimable; (2) keep-arm idle-box re-flight reproduces the author's 116,479 *exactly* (regen's 106,615 was load phasing — this falsifies the dossier's "counts are not load-elastic" for dropping arms); (3) K=10⁵ freeze arm — census dead flat at baseline+1.4k while the scan channel alone guards at gs 37,063 (527a: 38,033), double-measuring the domain boundary; (4) patch audit confirms off = shipped bit for bit.
- **Novelty**: no prior run froze the retention term; 527a's channel-2 inference is now a measured mechanism, and 527a's "never visited again" letter is refuted by the term-split.

Misses recorded: the load-elasticity caveat, "±50" being B-only (C is ±90), D's 248 ms being a one-sample tail (p99 11.9–13.0 and over=840 vs 2 are the solid evidence), and P5's digit-identity now resting on one common probe row since regen overwrote the original logs.
