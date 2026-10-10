Working...
Check complete. `check2.md` is written; the tree is restored to exactly the state I found (only the untracked `lab/results/` remains), nothing else in the run folder touched, no commits.

**Grade: gold.**

What I did, and what held:

**Reproduction (bit-for-bit).** Clean tree + `work/patch.diff`, rebuilt, reran all three scenes. ctrl = 2093 encounters, 44,850 pairs, 15,948,922 steps — identical to the crate's frozen `verify.jsonl`; fleet2 (4623/171,049) and retro (71,923/169,431) body/encounter lines byte-identical to the author's stored outputs (only `wall_s` differs). `analyze.py` reproduces every table number: 43.7% cross-fleet, 56.28% ceiling, 519 certs/enc for 99% vs the quadratic tier's 37; retro 96.4% cross-sense, ceiling 3.60%. The author's sampler matches `make_belt`'s RNG draw order exactly, so ctrl is a true re-instantiation of the crate's belt.

**Instrument.** The one non-crate code path (retro's mirrored march) verified independently: Python port of `Body::state`, 40 random reported events checked analytically, brute-force fine-grid scans of the busiest intra- and cross-sense pairs find exactly the reported minima — no false positives, no misses.

**Adversarial cases.** Warm single fleet (22% at W=1 — layer 2 without the grouping confound), break-even σ_e=0.012 (42%), cold dense n=1500 control (99.5% — the certificate's valid domain positively confirmed, so this is scoping, not a hit piece), seed variation (stable), and the incremental-maintenance reading of re-ranking (same ~4×10² certs/enc cost class — kill robust to implementation).

**Predictions.** Pre-registered kill criterion held decisively; one numeric prediction (≥95% cross) missed at 43.7% and was disclosed as the discovery of layer 2 — handled per the house rule.

**Caveats kept in the check:** the headline slightly overreaches (the gold's own cold-formation scene still works, 100% at 2.9 certs/enc); the spec says "beside the existing tiers", so the load-bearing kill is economic (battles restore the 10¹²-pair tier the gold condemned); the 10⁶ rank-break is mechanism-plus-arithmetic, not directly measured. Novelty clean — the build is still queued on both lanes, so the spec edit lands before anything is built.
