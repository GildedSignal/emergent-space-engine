Grade: gold

**Abstract (for the integrator).** Second check, blind to the first. Everything reproduces: with the staleness fix, the corner probe passes (tick 4194304) and all 40 heap/wheel pairs in `steady.jsonl` are digest-identical; the three stored 97bf rows regenerate byte-identically, heap and wheel. I rebuilt the pre-fix wheel from the parent's git commit plus only the E/F/S and corner grafts: the recorded failures reproduce byte-for-byte (corner FAIL 3145728; F diverges at steps 4/6/39780). Steady ratios hold on seeds the author never ran: mixed 2.2–2.4× at 2²⁰–2²⁴, spread 2.8–3.0×, storm 2.0–2.2×, and the heap still wins all-far quiet regions (up to ~2×). The gain is 2–3×, not 10×; gold rests on the premise corrections: the parent's "identical stream everywhere" was false pre-fix, and its 4.5× headline was one-shot. Adoption: the ~30-line fix plus the regime rule (heap fallback or a second wheel level beyond W).

## Reproduction (clean rebuild of `work/calendar-bench`, release)

- **Correctness, post-fix:** `corner` → OK, tick 4194304, ids 0–7. F diff at N=2/4/16/64, seed 7, 100k → all OK. Full battery A–F/S × {4096, 16384} × seeds {1,3,7} × 50k (42 runs) → all OK. `S 1048576 1 300000 diff` → OK.
- **P3 (record regenerates):** `A 262144 2 500000` → digest 17500833722892154388, sets 499385; `C 4194304 1 500000` → 9112003053027925743 / 498543; `A 16777216 2 500000` → 14321985119129707386 / sets 1 — all identical to the stored rows, heap and wheel.
- **Pre-fix is real:** I extracted the parent's pristine `main.rs` from git (commit 59f154f), grafted only the E/F/S cases and the corner mode, and rebuilt. Output is byte-identical to `results/prefix-failures.txt`: corner FAIL (wheel 3145728 vs heap 4194304); DIVERGE steps 4, 6, 39780 with the same `now`/`over_min` fields; F 64 OK. The bug is exactly `over.first()` read without a liveness check in `cascade`/`next_tick`/`deliver`; the diff against the parent confirms the fix touches nothing else on any path A–D (RNG, heap, cases, driver unchanged apart from added instrumentation).
- **Steady-state digests, exact:** E 2²⁴ seed 2 → 17210357980770661858 (both structs); S 2²⁴ corrected (12M/11M warmup) → 3034658216857615761; A 2²⁰ seed 1 → 5114642149038888776; F 2¹⁶ seed 1 → 6841659395089832192; S 2²⁰ (warmup 1M, reconstructed) → 18082141526428749561 and steps 27062.
- **Ratios on this pass:** E 2²⁴ 2.3×; A 2²⁰ 2.15×; S 2²⁴ 3.0×; F 2¹⁶ heap wins 1.9×. Absolute ns vary with box load (heap 466 vs recorded 325 on E 2²⁴); ratios do not. All 40 heap/wheel pairs in `steady.jsonl` digest-equal (verified programmatically), and the table's medians match the file exactly.

## Adversarial cases (mine, not the author's)

- Nine fresh-seed diff runs at N=2²⁰/2¹⁸, seeds 5–17, up to 500k deliveries, including case D (half-beyond-horizon) at 2²⁰ and F at 500k: zero divergences.
- Fresh-seed steady: E 2²⁰ seed 5 → heap 203 / wheel 83 (2.4×, digests match each other) — the gold-condition gain is not seed-cherry-picked. F 2²⁰ seed 7 → heap 229 / wheel 282: the heap-favoured carve-out also reproduces on a fresh seed.
- Floors on this pass: seq 1.25 ns, chain 1.88 ns (author recorded 2.12/2.70 under load; same tsc 3.592 GHz) — same orders.

## Predictions

`predictions.md` covers exactly the checker-named experiment; P1–P4, P6 (the gold condition), P9 held; P5/P7/P8 partial in the disclosed directions (wheel better than predicted on spread, heap's all-far win larger than predicted at 2¹⁶) — honestly reported as partial, with the two mid-run measurement defects (short warmup, dropped `last_k`) disclosed in the dossier rather than hidden.

## Novelty and fit

No timing-wheel entry in `docs/HISTORY.md`; the direct ancestor is the parent run 97bf (silver, in git, unmerged) and this run performs precisely its checker-named experiment — not a redo. Wheels are classic prior art (Varghese–Lauck; kernel timer wheels), stolen per #26. Fit: #14 (the calendar is the queue that replaces ticks), #12 (gain now stated per regime with the losing regime named), #2 ("exact means deterministic and reproducible" — byte-identical regeneration, cross-process), #9 (the corner killed the parent's configuration, not the method). Gold rests on "shows that a premise is wrong": the parent's correctness claim was false in exactly the regime its lens looked away from, and its 4.5× headline was one-shot; both are now closed with measured bounds. The 10× arm of the gold rule is not met; the premise arm is.

## What the author missed

- The S 2²⁰ steady row's generating command is absent from the dossier's command list; I reconstructed it (`... 2000000 clean <st> 1000000`) and it regenerates the row exactly — a doc gap, not a data gap.
- No tail data at all this run: every steady row has `tail_mode: false` (p50/p99/p999 = 0.0). PRINCIPLES #12 is explicitly p95/99; the claim is mean-op-cost. The recorded `burst_max` (~5×10⁵ deliveries in one step at E 2²⁴) shows the calendar can still hand the engine 500k-event frames — whether that burst shape is smoothable is unmeasured and interacts with the wheel's win more than the heap's.
- Stale text: the `over` field comment still says "store (-t, id)" and diff mode prints `-nt`, but the code now stores (t, id); the next diff-mode reader will be misled by the sign.
- The E mix (1/16 storm) is the author's choice, not the engine's measured re-time distribution; what decides wheel vs heap for the engine is the plane's actual kick-horizon distribution vs W, which belongs to the engine, not this bench. The named next experiment (second wheel level for the all-far regime) is correctly scoped but untried.
