Grade: gold

**Abstract.** H_live, measured on shipped code: a kicked body costs ~50 bits once plus ~2 bits per further doubling (49.9→68.3 bits at K=1→1024; state, both shelf runs and `verify a` reproduce bit for bit), the shipped shelf stays ~1–7 bits above that floor with bit-exact round trips through repacks, and reabsorption costs 1.26 µs/kick ≈ 8% of one core at the board's 6×10⁴ kicks/game-second — so at 10⁹ bodies the first wall is memory (fully mixed ≈ 7.9 GB, hit after ~1–55 play-hours), not compute. The premise that H_live might compound (44 bits/kick draw account) is wrong: 173× below the floor at K=256. Adopt: ever-kicked fraction f as the memory dial, a repeated-kick scene in B18, and drop the kick-side "190 cores" framing. No code.

## Reproduction (clean tree, `git apply work/patch.diff`)

- `state 1048576`: all seven `state_bits` **bit-identical** (49.904 / 52.686 / 54.682 / 58.391 / 61.897 / 65.185 / 68.263). 19 s.
- `shelf 1048576 8 0.25` and `shelf 1048576 16 0.5`: bytes/bits per ship, `state_bits`, `floor_gap_bits` and `mismatches` **identical in every epoch**; only `compact_ms`/`hot_ns`/`kick_ns` move a few percent with load. `mismatches:0` in all 24 epochs, including the repack near K̄≈4.5 (66.6→62.5 bits as claimed).
- `verify a`: 4 belts, 0 missed, 0 false; encounter rates 1.75×10⁻⁴ / 6.8×10⁻⁴ / 1.89×10⁻³ / 4.96×10⁻³ per body per orbit — the dossier's 1.75×10⁻⁴–5×10⁻³ exactly; ln2/rate = 140–3960 orbits ✓.
- The "frozen ladder's 50.0" anchor: `example ladder 1 1048576 1 0` → `floor_bits: 50.0001`. Verified.
- Fermi arithmetic re-checked: 63.5 bits → 7.94 GB at 10⁹; 4–6 GB for bodies → f_wall 0.5–0.75; N_max 5–7×10⁸; 6×10⁴ × 1.26 µs = 76 ms/s ≈ 8% of a core. All correct.
- `predictions.md` mtime 08:09:23 precedes the first decisive artifact `state.jsonl` 08:12:43 (then shelf-a 08:14:14, shelf-b 08:14:49). Held out before the run.

## Predictions

P1 held (49.9→68.3; slope 1.5–2.8 bits/doubling; K=256 measured 65.2 against a band topping at 64 — the author quotes the numbers, honest overshoot). P2 held (draw 11 264 vs floor 65.2 = 173×). P3 held (gap ≤ 6.6 bits through K̄=2 in shelf-a, no compounding, bit-exact). P4 held (1.26 µs/kick, 8%). P5 held and sharpened (7.9 GB at K̄=8).

## My adversarial cases

1. **Fresh seeds** (convoy g=3 and g=41, new kick seeds, m=2¹⁹): 49.80 / 64.26 / 67.13 bits at K=1/256/1024 — same curve, no seed sensitivity.
2. **Saturation** (K=4096, 16384 at m=2¹⁸): 67.96 / 69.61 bits — the slope *decelerates* (≈0.8 bits/doubling at the top); the pre-registered kill criterion (140 bits at K=1024) is nowhere near. H_live is genuinely bounded.
3. **Correlated victims** (contiguous runs of 64, x=0.5, 8 epochs): bit-exact 8/8; gap drifts to 9.4 bits — slightly worse than iid's ~7, so the author's conjecture that correlation "helps compression" is not what the store shows, but the claim that matters (no compounding, lossless) holds.
4. **Full churn** (x=1.0, every ship every epoch, 8 epochs): bits saturate 54.2→61.8 with increments +3.1→+0.3; gap stable ≈6.3; bit-exact 8/8. Compaction 2.2–2.7 µs/kick at m=2¹⁸ — 2× the 2²⁰ figure, still inside P4's bound; confirms the author's caveat that per-kick compaction cost has untested scale sensitivity (in both directions).

## Novelty

HANDOFF (line 69) still reads "not measured yet" at HEAD. The prior H_live runs are complementary, not duplicative: `20261007-0528-fermi-aab3` (silver) measured bits *created per encounter* analytically and its check explicitly left H_live unmeasured on the store side; `20261007-0128-b-h-live-1599` is grade **missing** (never delivered; its brief is the dashboard definition in `xtask universe`). The shipmem freeze (78f87d7) measured single-pass ladder floors, not repeated-kick saturation or reabsorption cost. The 190-core figure is pre-existing board text. Repeated-kick floor, store gap and µs/kick reabsorption are new on the record.

## Goal fit

Board: "fitting 10⁹ in 8 GB (`crates/shipmem`…) decided by distinctions created per game-second" — this is that number, measured. It shows a premise is wrong twice over: H_live does not compound (the fear behind "not measured yet"), and the kick side of the 190-core framing is dead (0.3% hot + 8% compaction of one core). PRINCIPLES: "The memory floor is information" (24) — measured as a rate equation, not bytes×count; "Compute only surprises" (3) — first kick 44–50 bits, later doublings ~2; "Store the generator, not the generated" (6) — quantified against the draw account. Procedure clean: one example file, shipped as patch, tree restored, no crate/doc/gate edits.

## What the author missed

- "Store stays 0.8–7 bits above the floor" omits shelf-b epoch 8's transient **12.0-bit** gap just before the repack rescues it (the repack is disclosed; the range is not).
- The `model_bits` formula treats all four columns as 11 bits, but Δt draws 17 (`below(2<<16)−2¹⁶`); the "+6" constant absorbs it empirically, and the code's `model_bits` column (44 at K=1) is wrong by construction even though every measured number is right.
- Empirical-entropy bias: at K≥1024 the floor is underestimated by ~0.7 bits/column (~3 bits at K=1024) — conservative for the gap claim, but "68.3 bits" is really ≈71.
- Everything is one program shape (a single Rate(0.0) convoy, shared e/l/ω). The floor is kick-model-only and robust; the *store gap* is convoy-specific and unmeasured for streams, formations and multi-program shelves.
- p99 framing: the 1.2 µs tail recurs every epoch (the forward map regrows after each compact — visible in shelf-b through epoch 16), it is not only "first-touch blocks".
