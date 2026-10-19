Working...
Check complete. Verdict written to `lab/results/20261019-1817-system-c7a6/check2.md`: **Grade: gold**.

**What I did**

- **Reproduced**: regen exit 0; verified every headline number against the regenerated logs myself — reads 7,268,353 / hist 20,649 (0.28%) / deepest 5,276.5 vs the dossier's 7,266,323 / 20,413 / 5,272.9 (wall-cap jitter only); coast 5,271.3 exact; armD's ages (p50 4,623→4,934, max 6,079→7,292 vs keep_med 8,265–12,906), first wave 13.8–14.8k, 7.01/body at gs 174,231, RSS 1,043 MB — all exact.
- **Instrument audit**: `PlainBodies` is the only `BodyStore`; the deep `binding_at(i, born)` reader is `#[cfg(test)]`; `bindings_of` is the prune-side sweep — the census misses no reader.
- **Adversarial, both outside the author's range**: rtf 4000 burn to 230k game-s (past his 197k horizon) — demand constant holds (5,315.7), keep_med 139,731, ratio 26.3× rising, and keep_med at matched gs matches his digit (105,355 vs 105,316); N = 10⁵ coast+view (a decade up) — all 100,048 emitters delivered every gather, lawful leg 3,155.5 N-independent, zero loss at census keep_over_demand 0.3×.
- **Novelty**: `nladder.md`'s channel-2 entry explicitly left "the view/retention design" open; the five prior runs are all supply-side. New topic, real gap.
- **Predictions**: P3 exact, P4 held with margin; P1/P2 letter misses disclosed as misses (my rtf-4000 arm confirms the P1 letter genuinely fails — keep 139,731 < 3×10⁵ — so it wasn't tuned away).
- **Page corrections** (in place, marked `[checker2]`): the census counts attempts, not returns, so "no read *returns* beyond one leg" is inferred — I anchored it to the measured no-emitter-lost evidence; and "headless reads nothing at all" now notes the bench's own end-of-flight one-leg gather sits after the last census print.

Gold rationale: a premise kill on shipped code (the retained interval is not the view's supply — ≥ 92% of channel 2's stock unread), reproduced, held under both out-of-range attacks, adoptable in one keep-law change of the same class as b911's already-flown freeze. Residual risks (scene universality of the 5,273 s constant, the replay contract untested) are named in the check and already on the page's open directions.
