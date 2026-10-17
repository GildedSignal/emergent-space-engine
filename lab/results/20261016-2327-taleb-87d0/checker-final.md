Working...
Check complete. **Grade: gold** — written to `lab/results/20261016-2327-taleb-87d0/check.md`.

**What I did**

- **Reproduced** from a clean tree: applied `work/patch.diff` at HEAD myself, re-ran `work/sims.py` — output byte-identical to the author's `regen.log`; all sandbox content identical (only throwaway `.git` stat caches differ). Patch is +92/−9 on `lab/wiki.py` only, as claimed.
- **Predictions**: mtime 23:31 precedes every instrument (23:33–23:38); P1–P6 held; the one miss (27 index rows vs predicted 30) is disclosed.
- **Six adversarial cases** (own harness, sandboxes only), two outside the author's range: two concurrent next-runs from today's *damaged* nladder (the real 1637 shape — author flew only one), and a 50-run single-window replay — all zero markers, zero content loss, re-apply an exact no-op. Plus depth-4 crafted interleave (worse than the real page), setext `=======` page, index-flag semantics, and encounters/scan-queue flown post-heal (author flew only nladder). All pass.
- **Novelty**: git-wide, no fix exists on main; the only prior art is the silver's flat defuse, whose mis-pairing I verified by reading its patch off its branch — this run's stack pairing materially supersedes it, and S2 (19→46 on real inputs) is the first live compounding measurement.
- **Page**: faithful; one overstatement corrected in place — nladder heals to **7 blocks / 14 labeled versions** (2 truncated), not "8 labeled versions". Topic stays open (one gold run; three agreeing golds close it).

**Found beyond the dossier**: the patch also fixes an index false positive nobody claimed — shipped flags `wiki-memory` as conflicted off the inline `` `<<<<<<<` `` mention in its own prose; patched flags exactly the 3 damaged pages.

Tracked tree left pristine; only `check.md` and the one-line page correction were written. Gold per the README: reproduced, held-out predictions held, deletes a measured compounding failure mode from the lab's mandated memory (PRINCIPLES 13), adoptable in one merge + one `heal` — pending the second blind checker.
