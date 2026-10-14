Working...
Check complete. **`Grade: silver`** — written to `lab/results/20261014-0000-inversion-30da/check.md`.

**What I did:**

- **Reproduced from scratch** on `f687ec25` + the patch (tree was clean; I applied it myself): mechanism confirmed line-by-line in `replay.rs` (55 s budget, `min(remaining, 27.5)` per-flight cap, `Stop::Deadline` → skipped, exit `(bad > 0)`); committed corpus 2.1 s / 0 skipped; per-flight 1.4/0.2/0.5 s exactly; growth table at noise level; my rerun of the decisive 13-flight corpus: **9 same, 4 skipped, "0 regression(s)", exit 0**.
- **Verified all derived arithmetic**, including the 41.5 coord-s per played second, which re-derives from the committed corpus's own session-start deltas (1205.1/29 s).
- **Three adversarial cases:** (A1) stripped-loss reached flight → `REGRESSION`, exit 1 — the gate *can* fail; (A2) one 35.1-s-solo flight alone in the corpus → skipped, exit 0 (and a 27.4-s near-miss that nails P2's predicted cliff); (A3) outside the author's range — 23-flight corpus → 15 of 23 dark, exit 0.
- **Novelty:** no prior page/HISTORY entry on coverage decay; but the skip→exit-0 path is *designed, tested* shipped behavior (`flight_tests.rs:173`) — the novelty is the quantified arrival (~19 min of real play) and the end-to-end demonstration.

**Why silver, not gold:** P2 wrong in magnitude, P1 partially wrong (both honestly reported — the lab's 1-October precedent bars gold on a failed held-out prediction); no board bottleneck moved; the fix is proposed, not built. One experiment to gold: land the contract patch (`skipped > 0` → non-zero + parallel replays) and show both sides.

**Author's misses (recorded + page corrected in place):** the `left < 0.5` skip prints *no line at all* — all three committed flights vanished silently in both reproductions, quieter than the dossier claims; the cap is `min(remaining, 27.5)`, so the decay is faster than the dossier's model; corpus counts are timing-dependent (author 10/1/2 vs reproductions 9/0/4); missing cross-link to yesterday's decision-log run (same gate, other blind side) — added.

Tree restored to its pre-check state; nothing committed or pushed.
