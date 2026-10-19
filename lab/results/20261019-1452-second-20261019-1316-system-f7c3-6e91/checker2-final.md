Working...
Check complete. Summary:

**Grade: gold** — written to `check2.md`, with my bracket appended to the author's `wiki/cell-rebind.md`.

**Reproduction** (clean tree, `work/patch.diff` applied by me): the decisive pair is bit-identical across three independent sessions — B13 exact 60/64 (worst 2.12e-2), served 46/64 (worst 5.93e-1), +QWEAK 47/64; memo/qmemo controls green; clean-stash control pins the exact arm's red on this box's libm, so the −14-draw delta is the serve. Microbench 4.84 µs compile / 0.725 µs hit (author 4.95/0.641 — same order; live-stream constants wobble 15–20% under load, recorded).

**Four attacks, one outside the author's range:**
1. **Width probe 14+14** (8× finer cell, the run's named-but-unflown successor): 53/64, worst 9.31e-2 — 6.4× per 8× width ⇒ width-limited, near-linear; the dossier's 11→17 extrapolation holds. Reverted after.
2. **Belt seed 3**: recurrence 0.9516→0.9510, cells +1.2% — the belt stream is unmoved on a third seed.
3. **Microbench at 10⁴**: 4.84 µs / 0.728 µs — constants are scale-robust; the 104 µs rebuttal stands.
4. Determinism re-runs identical.

**Corrections found (in check2, none disqualifying):** the "29,097 identical belt rebinds" are structural (9,699 bodies × 3 fires), not bit-identity; per-draw errors don't correlate with kick count, so "accumulates along the approach" overstates linear accumulation — the amplification is encounter-phase alignment.

**Novelty:** no prior run flew the gates under `ES_QMEMO` (9eeb left them open; f7c3's checker named this the gold experiment); no HISTORY entry. The page is faithful; topic stays open (not three agreeing golds).

Tree restored to pristine exactly as found (only untracked `lab/results/`); no commits made.
