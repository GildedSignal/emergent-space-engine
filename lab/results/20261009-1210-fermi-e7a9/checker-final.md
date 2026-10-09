Working...
Check complete. **Grade: silver** — written to `lab/results/20261009-1210-fermi-e7a9/check.md`; tree restored to clean, no commits.

**What I did:**
- **Reproduced bit-exact.** Applied `work/patch.diff` to clean `main` (a838a28). Built clean-main *first* and took my own digest baseline (`a7d089f9…1ca8df7`) — identical to the patched run, so read-only-ness is confirmed independently, not just against the author's baseline. All three decisive runs match digests, stocks, flows, and kick counts exactly; crate suite green; both new tests pass; `/frame` serves `dash.h_live` on a live server.
- **Predictions verified held-out** (12:14:46 vs 12:22 runs). P4 held; P1/P2/P3 failed and are honestly diagnosed.
- **Four adversarial runs:** seeds 3/7 (74.7/75.4 bits/body), window 20 s (72.2), dense 400-member scene at rtf 1000 (74.8, 82% reabsorption). The 70–90 bit width and decaying net slope survive every attack.
- **Novelty:** first measurement of the board's named quantity (`docs/plane.md:36`, "not measured yet"); components-98bc covered the program side, this covers the exception side.

**Why not gold:** the dossier's "Neither kill criterion triggered" is false on its own letter — predictions.md's criterion is "live bits per body ≥ 64", and every long run exceeds it (author's 66.2–85.4, mine 72–75). The reframing (all-exceptions worst case, kicked fraction is the real denominator) is defensible and disclosed in estimate.md, but a fired pre-registered kill criterion must be reported as fired. Plus the unmeasured denominator at 10⁹.

**One experiment to gold:** H_live on the wired belt (b-belt-wire) — measures the kicked fraction under generator coverage and tests whether sustained encounters hold creation flat.

**Author's misses recorded:** kill-criterion contradiction; "members 5000" is actually 400 (CLI clamp); m5000 bits/kick 6.32 printed as 6.1; flow metrics carry undisclosed budget-slicing noise; dead-but-stored bodies skipped.
