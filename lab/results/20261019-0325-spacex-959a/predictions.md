# Predictions (written before the deletion flights; build in flight)

The change: e6c9's sky-record serve tier rebuilds each multi-member cell's aggregate from its
members every frame — the record's one O(K)-shaped term (10.7 ms of 13.4 at 10⁵, ~142 ms at 10⁶,
"required, not optional" per both e6c9 checkers). This run keeps the same aggregates as running
sums updated on the events that already touch the record (due refresh: sub old + add new; tier
moves and deaths: sub; far entries: add), behind `ES_SKY_SUMS=1`; unset is e6c9's server verbatim
(same binary). The serve tier then reads one `CellSums` per occupied cell: O(cells), no member walk.

Grid: stock floor 8e-3, coast, seed 1, e6c9's own frame counts (120/90/40/20 at 10³/10⁴/10⁵/3×10⁵);
fine floor 1e-3 at 10⁴×90; long arm 10⁴×500; held-out seed 7 at 10⁵×40. Controls flown unset at
10⁴/10⁵/3×10⁵ + serve=0 at 10⁴.

1. **serve_ms flat in K on the deletion arm: ≤ 3.5 ms at every rung 10³–3×10⁵** (the member walk
   deleted; what remains is the BTreeMap walk over ≤ 786 cells + one HashMap lookup + one row
   build per cell). Control arms in e6c9's band (≈ 3.7 / 13.4 / 35.8 ms at 10⁴/10⁵/3×10⁵, load
   wobble). At 3×10⁵ that is a ≥ 10× cut of the serving path; against e6c9's measured 142 ms at
   10⁶ (checker's arm) the same law extrapolates ~50×.
2. **sums_ops = O(due + tier_moves), flat in K: ≤ 40/frame steady** at every rung (each due
   refresh is one sub + one add; the cold frame alone is k_far ops). If sums_ops grows with K,
   the deletion is a relabeling, not a deletion — that is the kill criterion for the mechanism.
3. **Audit unchanged where e6c9 audited zero:** wrong_cell = cells_wrong = missing = extra =
   tier_err = 0 at every rung ≤ 120 frames. The 500-frame arm may show e6c9's checker's standing
   wrong-cell class (mean ~0–3, self-healing at due events) — predicted NOT worse than the
   control's, because membership is untouched; only the aggregate arithmetic moves.
4. **sums_drift ≤ 1e-12** (running vs member-recomputed Σlum; pure float add/sub rounding at
   ~1e-16/op over ≤ 10⁴ ops/cell-run).
5. **Digests identical across arms** (deletion = control = serve=0 at each rung) and equal to
   e6c9's recorded END digests (10⁴/90: bd6f9840…, 10⁵/40: 82aa152c…, 3×10⁵/20: c3943af5…) —
   the server stays read-only, outside the outcome channel.
6. **Wire within ±0.1%** of the control's served_B (same rows; Σlum float tails may change the
   JSON's last digits).
7. **Fine floor (1e-3, 6,284 cells):** deletion arm ≤ 6 ms (O(cells) grows with the cell count,
   not K) against the control's member-proportional cost.

Held out until after the grid: seed 7 at 10⁵ (audit zero, serve_ms in the same band), and the
per-frame distribution of serve_ms at 3×10⁵ (no p99 spike: the walk's cost was flat per frame,
so its deletion is too).
