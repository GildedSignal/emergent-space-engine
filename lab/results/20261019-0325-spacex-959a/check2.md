# check2 — 20261019-0325-spacex-959a

Grade: gold

**Abstract (for the integrator).** The sky record's serving path is O(cells), not O(K): each
cell's aggregate kept as running sums on the events the record already pays. Reproduced on the
runner's regen and my re-fly: serve_ms p50 1.09→0.18 ms (10⁴, 6.1×), 10.55→0.16 (10⁵, 66×),
33.18→0.14 (3×10⁵, 237×); audits zero, running-vs-recomputed Σlum drift ≤ 5.6×10⁻¹⁵, every END
digest bit-identical to e6c9's published anchors. My decade-up arm (10⁶, one rung beyond the
author): serve 0.12–0.13 ms against e6c9's measured 142/143 ms rebuild (~1100×), sums_ops steady
16–54/frame. Fine floor at 10⁵: 1.23 ms (cost follows cells); rebuild control 1.71 ms (parity).
Adoption: ~120 gated lines, no engine change — e6c9's checkers' named gold step (a), flown.

## Reasons

**Reproduction.** The tree had been reset after the runner's regen; I applied `work/patch.diff`
myself and rebuilt (clean except e6c9's known no-op `drop(&mut)` warning). The regen table
reproduces every dossier number within load noise (ctl 1.07/10.45 vs 1.09/10.55; sums
0.19/0.16/0.15 vs 0.18/0.16/0.14; fine floor 1.21 vs 1.20; long 300 frames p50 0.19, 118
cells_wrong summed over the last 74 frames; refly max 0.37). I verified the anchors against
e6c9's published branch (`claude/lab-...-e6c9`): END digests 5dc903e6/bd6f9840/82aa152c/c3943af5
match this run's arms bit for bit, and the "e6c9 1.03/10.66/33.18" column matches e6c9's own
serve-arm p50s (1.03/10.66/33.2). The "142–143 ms at 10⁶, required not optional" quotes are real
(e6c9 check.md l.51, check2.md l.40). Patch audit: the diff against e6c9's patch is 118 lines,
all additions gated behind `ES_SKY_SUMS` (report fields, CellSums, add/sub at five call sites,
the serve branch, the drift audit); the rebuild walk, driver, and serve=0 path are untouched —
one binary, both arms, as claimed.

**Predictions.** predictions.md (42 min mark) precedes the only surviving author log (the 10⁵
refly, 32 min) and the patch (27 min); the author's grid logs were overwritten by the runner's
regen, so mtime proof is partial — regen reproducibility covers it (same caveat e6c9's check2
recorded). All seven clauses held on re-fly: serve flat 0.07–1.23 ≤ 3.5 ms; sums_ops O(due)
(steady 0–2/frame at 10⁴; 16–54 at 10⁶ = 2×due+churn — the relabeling kill criterion does not
fire); audits zero ≤ 120 frames; drift ≤ 5.6e-15 ≤ 1e-12; digests identical across arms and to
e6c9's anchors; wire within 0.03% (10⁴/10⁵) and 0.002% at the fine floor (my control); fine
floor ≤ 6 ms (1.20). Both held-out clauses held (seed 7: audits 0, 0.16 ms; 3×10⁵ per-frame max
0.18–0.20, no spike).

**Attacks (mine; `$T universe --skyserv K frames seed floor serve margin`, logs preserved at
/tmp/959a-check2/).**
1. **One decade up, 10⁶×10, sums on** (outside the author's range): serve_ms 0.12–0.13 ms every
   frame against e6c9's measured 142/143 ms rebuild — the dossier's ~0.2 ms extrapolation is
   conservative; 786 cells FULL, 1,146 rows, 302 KB served of 269 MB; cold = k_far (999,689),
   frame 2 = 2×k_far (1,999,378), then 16–54 ops/frame; drift 7.9e-15; missing/extra/tier 0;
   digest probes clean. cells_wrong = 27 of 786 every frame — exactly e6c9's check2's probe-side
   fleet row-id aliasing (present in the rebuild arm too), not a sums regression.
2. **500 frames at 10⁴** (prediction announced 500; author flew 300): serve p50 0.17/max 0.33 ms
   flat, drift 1.1e-15, missing/extra/tier 0, digest probes clean. The standing wrong-cell class
   persists and grows: 1.18/frame (frames 200–299) → 5.29 (300–500), same class as the rebuild
   arm's published 2.62 (e6c9 check2, other box); it is membership-driven and mechanically
   independent of the sums (the census counts `self.cells`, which the sums never touch).
3. **Fine floor 1e-3 at 10⁵** (author flew fine floor only at 10⁴): serve 1.23 ms at 6,284 cells
   — the cost follows the cell count, not K (the rebuild at 10⁵ stock pays 10.45 ms for 786
   cells' worth of members); drift 1.9e-15; wrong-cell 0.001% class; END digest = the 10⁵ stock
   anchor.
4. **The missing control, flown**: fine floor 10⁴ rebuild arm (unset) = 1.71 ms p50 (2 wrong
   cells, same class) vs sums 1.20 — parity-class with a sums edge, corroborating the page's
   checker-flown 1.74; wire parity 0.002%. serve=0 at the fine floor digests bd6f9840 = both
   serve arms'.

**Novelty.** The deletion was the named next step — e6c9's residue note ("deletable to O(cells)
by running sums maintained on the same due events, no new mechanism"), both its checkers
("running sums now mandatory"; gold recipe step (a)), and the live view page's open direction
("e6c9's running sums" as the in-budget form at 10⁹). No run had built or measured it; 959a
flies it, and the page's NEW block correctly flips that direction to built-and-measured. The
page needs no correction: every number in it traces to a log I re-derived, including the
fine-floor control sentence and the aliasing boundary (inherited, line 194).

**Goal fit.** Board live question 1 (bodies 28 → 10⁹): the view-gather chain's serving path is
now flat in K end to end, measured to 10⁶. PRINCIPLES 17 ("the best part is no part" — the walk
is deleted, not tuned), 3 ("compute only surprises" — aggregates move only at crossings and tier
moves), 14 ("no work for no reason, so no ticks" — the per-frame rebuild was one). Cost: ~120
gated lines; adoptable with e6c9's record in one step.

## What the author missed

- The pre-registered grid announced a 500-frame long arm; the dossier flew 300 and never flags
  the change (my 500 covers it; the claim stands — but the lab has graded reporting gaps before).
- "The record's last objection at scale is gone" overreaches one sentence past its evidence:
  e6c9's checkers' gold steps (b) (widen the fleet row-id base so the census audits at 10⁶ —
  my flight confirms cells_wrong 27 still stands) and (c) (pin the steady wrong-cell population
  over ≥ 10⁴ frames) remain open on the record's adoption file. The page carries both honestly;
  the dossier sentence does not.
- The cancellation corner (a hot body entering/leaving a cell's sums) stays unflown — the author
  flags it; note the per-frame drift audit recomputes only Σlum, not the lum-weighted colour/
  light-seconds/shift sums, which share the arithmetic.
- The 10³ parity clause and the load-contaminated first 10⁵ pass are reported honestly; nothing
  to deduct there.
