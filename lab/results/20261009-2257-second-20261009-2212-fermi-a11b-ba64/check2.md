Grade: gold

**Abstract.** Second-author record repair on the 10⁹-in-8 GB budget, now regenerating. Reproduced on a clean tree at `a838a28` (patch empty): all five bench digests bit-exact, and m48/m400 match the original silver run's stored evidence (`09e40859…`, `aadaa1c8…`); `budget.py` reads only `evidence/*.json` plus named repo anchors (all verified in-tree). Live compiled state ~6.9 KB/body (my independent slope: 7.02 KB) = 428× the 16 B tube — the board's biggest memory lever, re-ranking item 3; N_hot ≈ 1.2–2.9×10⁴ at rtf 100 today (steady state); cold populations free by the horizon bound. Predictions pre-registered before first evidence and held, one cold outlier honestly reported. Adoption: zero code. My adversarial wobbles are second-order to the orders-of-magnitude claim.

## Reproduction

Clean tree at `a838a28` (`git status`: only untracked `lab/results/`), `work/patch.diff` empty, binary from the shipped tree. Ran the dossier's commands verbatim into `/tmp/check2`, then `budget.py` on my own evidence:

- **Digests, all five bench runs bit-exact** (m48 `09e40859`, m148 `d2e9a47a`, m248 `0fde55d8`, m448 `aadaa1c8`, rtf1 `d96acc05`), and m48/m448 equal the original run's committed evidence (`077df02`) — canonical state regenerates across sessions, boxes and checkers. This is the "regenerates" claim, proven at the hardest level.
- **Slope:** my ladder gives bpb 5192/5697/5976/6700 at 71/166/263/406 bodies → two-endpoint 7.02 KB, 4-pt OLS 7.02 KB (author: 6.85/6.86; 2.5% apart). Monotone, as predicted. 439× vs 428× the 16 B tube; ceiling 1.14×10⁶ vs 1.17×10⁶.
- **Event rates:** full-total 6.12/4.99/4.61/4.72×10⁻² (author: 6.13/5.01/4.87/5.07) — same shape, mildly declining, flat at the top. The original's 3.9×10⁻² reading as a kicks+slices+leavers subtotal artifact is confirmed on both sessions (my subtotal at 406: 3.45×10⁻²).
- **Transient:** rtf 1 identical digest and bodies/bpb (39/2293); rate 1.63/body/game-s = 35× steady (author 32×).
- **Kick cost:** my six medians 41.9–69.2 µs — bimodal in-session by load (65–69 early, 42–44 later), widening the disclosed 42–66 family; `exact_hit_rate` 0.0, 23 samples, everywhere. The M1 29 µs anchor governs capacity; box quotes stay orders-of-magnitude.
- **Derivations:** 175 cores, 0.0299 cores at belt cadence, 15.8 MB for 10⁹ programs, 1.143 orbits → 1.1×10⁻³ e-foldings, H_live ≈ 40 bits/game-s — all recompute exactly from anchors I verified in-tree (H0190 K1/K2, H0210's 29 µs, law.md's 16 B tube, the register's 0.126 bits).
- **Ordering:** predictions.md mtime 22:59:21 vs first evidence 22:59:37 (16 s), budget.py 23:02:02, dossier 23:03:14 — pre-registration now verifiable, which the original's empty run.log could not do.
- **Clamp:** `mod.rs:32` `clamp(4, 400)` read in source, and `--members 400` reproduces the m448 digest identically — "448 ran 400" proven, stated in the dossier.

## Predictions

All six held on my independent evidence too: medians in family (the author's run 1 at 60.0 was out of the 40–50 band and reported under the prediction's own pre-registered rule); slope monotone with two-endpoint in 6.5–7.7 KB (6.85; mine 7.02) and OLS within 15% (0.2%); full-total at the top in 4.5–5.5×10⁻² (5.07; mine 4.72); transient ≥10× (32×/35×); every derivation exact; budget.py provably reads only `evidence/` (constants are the four named anchors plus physical times and the M1 goal).

## Attack (my cases)

1. **Run-length dependence of bytes/body** (undisclosed magnitude): m248 at 5/10/20 s → bpb 6906/5960/5757, total live bytes 1.78→1.56 MB. The 10 s snapshot overstates the settled store by ~3–6%; "~0.1% cross-session" holds only at fixed run length. Direction favors the claim (settled store smaller, ceiling higher), lever still ~420×.
2. **Seed 7 at m448:** digest changes (`41aa0313…`), bpb 6960, rate 5.7×10⁻² — the ladder is not a one-seed artifact.
3. **Counter softness:** my event counters differ from stored (kicks 4663 vs 5069, ~8%) at a bit-identical digest — counters are scheduling-dependent work accounting; the committed state is canonical. The dossier's "digest-exact counters (stats, bytes) are hard" overstates: only the digest is hard; stats/bytes wobble at the few-% level.
4. **Transient generality:** m148 rtf 1 gives 14.6× (vs 35× at m48). "≥10×" generalizes; "~30×" is m48-specific.

None of these moves any conclusion by even a factor of 1.1 in the direction that matters.

## Novelty

The physics is the original run's (silver, `077df02`); HISTORY.md has no prior live-store figure for the plane path (representation.md's 88 B is the old `Body`; H0158's 2.7 KB/ship and the ~310 B/body of the lattice runs are a different engine). This run performed exactly the experiment the first checker named for gold: stated commands re-run, `budget.py` from evidence/, the missing slope points, the steady-state regime, the clamp, pre-registration ordering. That is the lab's designed silver→gold path, not a duplicate.

## Goal fit

Board item 3 + bottleneck 5 + the H_live risk: the 428× memory lever (~35× the slack skin's 12.6×) re-ranks the board; the hot/cold split is principle 33 as a budget. Zero code to adopt. PRINCIPLES: "Compute only surprises. Cost follows change and entropy" (3); "The memory floor is information" (24); "Measure before claiming" (10).

## Why gold

The claim moves a board bottleneck's ranking by ≫10× (the measured lever), is adoptable within one step (zero code), was reproduced by me digest-exactly with every soft number within a few percent, and its held-out predictions were pre-registered (verified by file times) and held. The record — the exact thing that held the original at silver — now regenerates from stated commands on a clean tree, including against the original run's own stored evidence.

## What the author missed

- The "digest-exact counters (stats, bytes) are hard" line: only the digest is; stats and bytes wobble a few % with scheduling and report timing (my kicks 4663 vs 5069, bpb 6564 vs 6700, bodies 410 vs 406 — at identical digests).
- The magnitude of run-length dependence in bytes/body (6906→5757 over 5→20 s); the "~0.1% cross-session" claim needs "at fixed run length" to be true.
- "~30× transient" is m48-specific (14.6× at m148); the regime caveat is robust, the number is not.
- The kick-cost family on this box extends to at least 42–69 µs within one session pair — even wider than disclosed, further reason the M1 anchor must govern any capacity quote.
