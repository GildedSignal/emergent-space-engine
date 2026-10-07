Working...
Check complete. `check.md` written; nothing else in the run folder touched (my experiments ran from `/tmp`).

**Grade: silver.**

**Reproduced** (clean tree, empty patch.diff): the decisive gatherbench within ~1% at all three scales (0.747/2.97/27.45 ms; 7.19 µs/entry; surprise 4.7/8.2/7.4%); the unbudgeted engine demand exactly (0.047/1.30 ms); the paced shares (gather 0.669 vs 0.694) with an **identical canonical digest** — absolute paced medians differ ~4× purely from machine load, which the author had disclosed. Kickbench exact. Code claims verified in source: `session.rs` budgets the engine only, `gather_cached` unbudgeted; plane.md foundation 7 forbids exactly that. Predictions were pre-registered before the decisive run (mtime order) and all four held.

**Why not gold:** the 10× gain is projected from the surprise rate — the gate is unbuilt, and the author says so; and the headline was already in H0210 ("the view gather is 83% of a light frame", cache built in H0211/H0213), uncited. What is genuinely new: the post-cache decomposition (readouts ≈ 1/entry, ~100% of the gather), the linear 7.2 µs/entry scaling, the measured view surprise rate, and the verified unimplemented gather budget.

**My adversarial findings:** surprise triples to 23.3% at rtf 400 (the deletion claim is rtf-scoped — missed by the author), 10.1% at an untuned 1200-member scale, and a cold-gather control (112 vs 70 readouts) confirming the memo lever is already spent, so deletion is the only remaining lever. One phrasing correction: the 16.7 ms breakpoint is ≈2,300 entries by the author's own slope, not 3,770.
