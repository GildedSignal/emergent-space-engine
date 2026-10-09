Working...
Check complete. Verdict written to `lab/results/20261009-2043-quant-3cfc/check.md`: **Grade: silver.**

**Reproduced** (clean tree + author's patch, release rebuild):
- **Digest bit-identical** at 400/10 s (`aadaa1c8…`, cut 203025447, overflow 106/600, gather share 0.54).
- **The indivisible slice is real**: at 3,200/6,400/25,600 the entire window runs as one fleet item (`slices: 1`) of 643/630/742 ms carrying 1,329–3,936 leavers; RSS 123.5/315.5/842.0 MB matches the author exactly.
- **My adversarial extensions all strengthen it**: seeds 2 and 7 break the same way; `--threads 4` doesn't dissolve the unit; a 5 s window grows the single item to 1,524 ms; the 100k probe hit 1.85 GB at 68 s and was still climbing.
- Novelty confirmed: H0158's ladder is the old `crates/engine`; the plane has never been load-tested above the shipped clamp of 400; the fleet-side slice was left atomic by 68c5872's handout fix.

**Why not gold**:
1. Three of five held-out predictions failed (P1 capacity, P2 shape, P5 memory) — honest and informative, but the rubric's "predictions held" is not met.
2. The memory attribution is wrong on its own arithmetic: 842 MB / 2,573 leavers = 327 KB per leaver, not 6.5 KB; my measurement at 25,600 is **3.87 GB** against the author's "~1 GB (est.)". Linear ~150 KB/member puts the 8 GB ceiling at ≈5×10⁴ members — the conclusion (10⁵ cannot fly in 8 GB) survives, stronger than claimed, but the record's memory column would mis-plan B15 by ~50× if adopted as written.

**The gold experiment**: attribute the ~150–330 KB/member (the `formation` flag already exists in `scenes::battle` to suppress the exodus), or prove the fleet-boundary slicing fix holds p99 ≤ 16.7 ms at 3,200.

Tree restored (patch reverted; only the untracked `lab/results/` remains). No commits, no pushes.
