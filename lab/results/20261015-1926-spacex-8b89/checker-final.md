Working...
Check complete. **Grade: gold**, written to `lab/results/20261015-1926-spacex-8b89/check.md`.

**What I did:**
- **Reproduced**: applied `work/patch.diff` to base `9626abf8` myself, rebuilt, and verified the runner's regen (ALL IDENTITY, 7 scenes). Every dossier number matches the regenerated logs exactly — census, bytes/body, catalogue_live, promotions, rss, wall — except trivial timing jitter (burn wall 31.74 s vs 31.0; ratio grazes the registered ≤6× at 6.05×). Anchors confirmed: ctl burn digest `5caeb1b6…64c451` + seam counters 40,187/624,994 = e0f9's published; variant mixed `61c3a24a…` = 3dc8's.
- **Predictions**: written 19:38, before dossier (19:52) and patch save (19:54). P1/P2/P3/P5 held; P4's death-rate half failed and is honestly reported with a correct diagnosis (fall time outlasts the cut).
- **Attacked with 10 flights, all digest-identical**, including three outside the author's domain: a 10⁵ belt (10× their max N: 1,332→658 B/body, rss 257→105 MB, catalogue 100,076→3), the never-flown stargraze class (rss 1,078→20 MB, passage p50 596 µs), and burn seed 7 through the spawn path. Crate suite: 0 failures with the seam off.
- **Novelty**: 3dc8 named exactly this open edge (births/no-kick rebinds never settle); no prior run demotes them. Page fold-in verified faithful — no correction needed (it already flags the 3.5× as extrapolation).
- Tree restored to base; only `check.md` added.

**Named soft spots** (in check.md): the composed ALL+`ES_RETAIN_HOT` arm is unwon and is the one-flight adoption question; the "~3.5× census" headline is optimistic (measured 2.0× at birth state — the exact claim is the arcs term → 0); deep-window compile p50 is ~2× the mixed-scene figure the cache arithmetic should use. Not a page-closing third gold — the topic stays open.
