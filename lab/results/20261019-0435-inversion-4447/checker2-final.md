Working...
Check complete. **Grade: gold** — written to `lab/results/20261019-0435-inversion-4447/check2.md`.

**What I did:**
- **Reproduced**: applied `work/patch.diff` to a clean tree, rebuilt, and verified the runner's regen.log against the raw logs — every headline number traces (guard at 560,862/332,604 gs, mid-flight slopes 5.68/16.33, final-40% 3.02/4.56, coast 0.02 flat with held_max 1, held 741/589 with SCAN_BACKLOG=2048 never engaged, dashboard under-count 189 of 1,601 MB, doll 0 at frame 948, one-hour mark 988.8 MB at gs 360,195).
- **Predictions**: pre-registered with frozen kill criteria and a voiding control; P1/P3/P5 held, P2 honestly reported half-held (RSS/held compounds 1.35→2.16 MB).
- **Three adversarial arms of my own, all outside the author's grid**: seed 7 at 10⁴ (ratchet seed-stable, held trajectory identical, final slope 3.27); **K=10⁵ — the author's flagged-inference decade — guard-stopped at 37,123 gs with slope 42.75 MB/1k gs ⇒ 4 GiB at ~95k gs ≈ 16 wall-min** (the two-point "~70k ≈ 12 min" holds in order, ~25% optimistic); coast at 3×10⁴ flat to 613k gs (burn-specific at both rungs). Side note: at 10⁵ the frame channel stops being mild (0.46% over, max 322 ms) — the dossier's "mild at these K" scoping is load-bearing and correctly drawn.
- **Novelty**: the page's own record confirms the resolved contradiction — d839's checker's "then flat" (ended inside the 40–60k local plateau) and dcf1's "wall gone / 8 GB ~300k gs out" (ended at the SOI switch, the ratchet's phase boundary). Neither unboundedness past 12× the longest burn flight, nor the K-growing slope, nor interstellar persistence was known.
- **Page corrections**: folded my arms in as a second-checker note and added the missing Refuted line for dcf1's K-flat extrapolation.

Tree restored (patch reverted, my seed-7 example copy removed); nothing else in the run folder touched; no commits or pushes.
