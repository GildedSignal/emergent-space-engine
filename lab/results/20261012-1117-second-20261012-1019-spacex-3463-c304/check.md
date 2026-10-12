Grade: gold

**Abstract.** Claim: the plane's 845 MB at 4,000 members is unpruned rebind history (~10.2 kB per kick; the settle crosses ~95% of ticks past the last prune) plus ~19 kB per handed-out body; churn and body count are irrelevant. Reproduced bit-for-bit from `work/patch.diff` (fresh m4000: hist 572,188 KB, kicks 55,839, digest 632b4b53…; gap arm within 8%). Adversarial: the paced player path is identical (846 MB); seed 3 gives 10.10 kB/kick; m40000 at my own S=4 constructs flat at 19.4 kB/handout to #37,500 (696 MB), then kick onset hits the guard — the first author's "cannot construct 4×10⁴" (tick 136, kicks 0) was a wall artifact. Stock digest equals patched. Adoption: one small patch; budget 19 kB + 10 kB·kicks/horizon.

## Reasons

**Reproduction (clean tree, `git apply work/patch.diff`, release).**
- A m4000 S=8: peak rss 845,832 KB (author 845,828), live 903,411 (identical), hist 572,188 (identical), post-prune 82,708 (identical), kicks 55,839 (identical), trim 0.14%, digest `632b4b53…` identical; m4 digest `6af71966…` identical.
- B `--gap 2000`: rss 780,628 vs 779,724 (0.1%), hist 524,996 and post-prune 81,168 identical, kicks 53,477 identical. B ≈ A within 8%: churn irrelevant, confirmed.
- Per-kick retention: A 10.24, B 9.82, DA 10.90, DB 10.79 kB/kick from the author's files; my seed-3 run: 607,025 KB / 60,095 kicks = 10.10. The 10.2 kB/kick law holds across arms and seeds.
- Instrument lie: honest unpruned 159.0 kB/body vs dashboard 8,022 B = 19.8×; post-prune 32.9 kB = 4.1×; passages 14.2 kB average over 1,773 bodies, 2,046 tail panels — all match the dossier. Account explains 68.3% of live (≥60% predicted); trim ≤0.3%.

**My adversarial cases (beyond the author's).**
1. **Paced, the player path** (`--rtf 100 --seconds 8`, no `--unpaced`): peak 846,032 KB, hist 572,188 — identical to unpaced. Frames presented only 8.9M of the 162.4M-tick cut (budget-limited), so the settle's unpruned catch-up is the same for the player; in-frame prunes were no-ops anyway (now < 2^26 horizon until the settle). The blowup is not a bench artifact.
2. **Seed 3**: all orders hold (10.10 kB/kick, 82% post-prune drop, ~21× dashboard lie).
3. **m40000 at S=4** (my wall budget, not the author's S=8): construction flat at ~19.4 kB/handout through #37,500 (696 MB, tick frozen at 136), then kick onset at #38,000 — d_rss jumps to 288 MB/25 handouts, hist 888 MB, guard 1.879 GB, kicks 75,567. Same signature as the author's C, independently. The first author's own `orig-bench-m40000.json` (presented tick 136, kicks 0, 12,392 leavers, 47.7 s wall) is exactly the wall-speed truncation the dossier names; "cannot be constructed at 4×10⁴" is refuted.
4. **Observation-only**: with the patch stashed, the stock build's m48 digest `29f440d6…` equals the patched build's. Digests unchanged, end to end.

**Predictions.** `predictions.md` (11:38:23) precedes every decisive arm (A 11:39:04 … DB 11:47:54); only the disclosed m4/m48 digests and the S=1 smoke precede it. Held: 1 (retained, trim <30%, account ≥60%), 3 (d_rss 0.6→129+ MB/25, tracks kicks), 5 (19.8× ≥ 15×), 6. Falsified exactly as the pre-registered falsifiers demanded: 2 (B converged to A — churn killed by the author's own control) and 4 (C's guard fired at kick onset, construction stayed flat). The falsifications are the result, and are reported as such. Honest.

**Novelty.** No HISTORY entry measures the plane's store retention or the dashboard's `bytes_per_body`. H0209's shipmem (488 B per 10⁶ ships) is a design target — this run measures the gap (~2,100× steady, ~10⁴× worst window over the 16-byte tube). H0158's ~2.7 kB/ship was the old `engine` crate, a different store. The corrected claim (spacex-3463) is only in this folder's `orig-*` files (lab branches are not in this checkout); they match the dossier's quotes.

**Goal fit.** Board focus item 5 (10⁹ in 8 GB): a premise is shown wrong — growth is kicks × retention horizon, not body count; construction is flat 19 kB/handout at 10× N; the "cannot construct 4×10⁴" wall claim is dead. Per "The cheapest compute is compute not done" (1) and "deeply aware of von-neumann bottleneck and memory" (17): the lever for B18b/shipmem is bounding kick-history retention, not the tube representation. Adoption is one step: charge retired segments in `bytes_of`, prune inside `settle` (or at digest), budget ~19 kB/handout + ~10 kB/kick inside the prune horizon. Nothing touches gates, crates or `main`; digests proven unchanged.

## What the author missed

- `account_after_prune` models the light-distance term only; the shipped prune's `(oldest − 2^26)` min-term is omitted, so "33 kB/body steady" is a lower bound of the real rule's retention, and the measured 33–116 kB range is horizon- and population-age-dependent (the dossier discloses this, but the model/rule gap is not named).
- The mechanism sentence "prune runs only in `frame_to`" is right in effect but incomplete: the in-frame prunes are no-ops at this depth (now < 2^26 until the settle); the load-bearing fact is the settle's single unpruned 153M-tick catch-up. A longer real session (sim time past the horizon inside frames) would prune in-frame — the paced confirmation of that regime is still open.
- ~30% of live bytes (view cache, queue, JSON DOM) is attributed by class only, no allocation-site profile.
- Trivial: "history 869 MB at guard" — the probe's own last line reads 888 MB (2%); the 33 GB-at-10⁹ extrapolation assumes this workload's kicks per horizon.
