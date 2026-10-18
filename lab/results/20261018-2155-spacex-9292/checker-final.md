Working...
Check complete. **Grade: silver** — written to `lab/results/20261018-2155-spacex-9292/check.md`, with the author's `wiki/view.md` corrected in place where it overstated. Tree left clean (scratch probe variant built to `/tmp`, source deleted; only `lab/results/` untracked).

**Reproduction.** regen.sh exit 0; every dossier headline reconciles with the fresh logs (coast 786 cells FULL at 10⁴–10⁵, burn-L8 churn p99 4.86e-6 = |dβ|, crossed-cell K-flat 0.032/0.032/0.036 % per frame at 10³/10⁴/10⁵, L15 disp p99 2.30e-3 < θ_f/2, zero pairs past half-cell in all seven arms). Diffs found, none load-bearing: b1e4 pairs 2,001,908 vs 2,099,088 (52 s wall-cap pools 206 vs 216 intervals — 9,718×216 = the dossier figure exactly), L15 crossed 6.20 % vs 6.16 % (run-to-run count wobble, verified ~1e-4 relative with a byte-identical rerun).

**Attacks (4, two outside the flown grid).**
- **L15 × 4 flight length**: letter breaks — 2.92 % displayed / 0.357 % root-frame past θ_f/2 per frame, dβ/frame p99 4.7e-3 > θ_f/2, churn still growing at frame 1440 (the dossier's γ²-falls argument mispredicted the boundary).
- **L15 × 10× zoom, author's own 360 frames**: 46.5 % displayed / 0.68 % root past θ_f/2 — still 6.3× observer-side.
- **L8 × 10× zoom**: holds; crossed 0.335 % = 10.5× the stock floor — the dβ/θ_f law quantitatively confirmed.
- **Seed 7**: fully holds.

What survives everywhere: observer-side dominance, O(occupied cells) re-binning, ~350 near rows. What dies outside the flown window: "never emitter-side" and "0 past half a cell" — the record there needs an unpriced staleness-repair tier of ~4e-3·K far rows/frame. Also flagged: **P1's far-row clause failed** (9,718 < 1.2e4) yet the dossier reports P1 held; "p99 at θ_f/11" is actually the max; the wiki Refuted count (3.4e6) matched no log — corrected to the regen counts.

Gold experiment named: fly the record's own cost law through the broken window (long top-dial burns × zoom) and price the root-refresh tier and zoom re-window, converting "safe as flown" into "safe under the wildcard, with the boundary priced."
