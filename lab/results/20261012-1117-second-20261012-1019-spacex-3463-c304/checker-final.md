Working...
Check complete. **Grade: gold** — written to `lab/results/20261012-1117-second-20261012-1019-spacex-3463-c304/check.md`, nothing else touched; tree restored clean (only untracked `lab/results/` remains).

**What I did:**

1. **Reproduced from the patch** (clean tree, `git apply work/patch.diff`, release): fresh A (m4000) gives hist 572,188 KB, kicks 55,839, live 903,411 KB, post-prune 82,708 KB, digest `632b4b53…` — identical to the author's A2; B (gap) within 0.1% RSS with hist/post-prune/kicks identical; m4 digest `6af71966…` identical. Per-kick retention 10.24/9.82/10.90/10.79/10.10 kB across A/B/DA/DB/my-seed-3. The ~20×/4× dashboard lie and its decomposition match from the raw JSONs.

2. **Four adversarial cases of my own, all confirming:** (a) *paced* player-path run — 846 MB peak, identical hist, so the blowup is not a bench artifact (frames present only 8.9M of the 162.4M-tick cut; the settle's 153M-tick catch-up is unpruned in both modes); (b) seed 3 — all orders hold; (c) m40000 at my own S=4 — construction flat at 19.4 kB/handout to #37,500 (696 MB), then kick onset drives it to the 1.7 GB guard, killing the first author's "cannot construct 4×10⁴" (their own file: presented tick 136, kicks 0, 47.7 s wall); (d) stock build's m48 digest equals the patched build's — instrumentation proven observation-only.

3. **Predictions:** `predictions.md` (11:38:23) precedes every decisive arm (11:39:04 onward). Predictions 1/3/5/6 held; 2 and 4 fired as pre-registered falsifiers and are reported as the result — honest.

4. **Novelty/goal fit:** no HISTORY entry measures the plane's store retention or `bytes_per_body`; H0209's 488 B/10⁶ ships is a design target, H0158's 2.7 kB/ship a different crate. Premise correction on board item 5, adoptable in one step.

Noted misses (in check.md): the post-prune account omits the real prune's `oldest − 2^26` term (33 kB/body is a modeled lower bound; 33–116 kB range is horizon-dependent), no allocation-site profile of the ~30% unattributed live, and the trivial 869-vs-888 MB guard-history discrepancy.
