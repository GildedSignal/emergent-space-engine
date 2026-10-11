Grade: gold

**Abstract.** Claim: the plane's silent freeze is real and members-worsening, but its mechanism is neither a per-frame prologue (directly measured: 15 µs/frame at 428 bodies, 99% rekey) nor "delivers 0.00×" (28.8× unpaced, 5.2× paced as a 39-frame clock stutter) — delivered = throughput ÷ event density, and the m4→m400 cliff factors as 11.3× throughput × 70× opening density. Reproduced bit-exact on a fresh build: every digest (grid, paced, and all four row-1 originals against `orig/`), e(B) = 1.18/3.09/20.3/75.7 with no knee, prologue 15.4 µs, paced worst cell 5.16×/92% frozen/40 jumps of 1.3 game-s. My extensions: no knee at 0.1 ms; seed 2 satisfies T/D; prologue stays linear to 2,190 bodies (90 µs). It kills the silver's wrong prologue-audit gate; adopt the density×target vs sustainable-events/s shed instead.

**Reproduction** (base tree + `orig/patch.diff`'s `--coast` arm + `work/patch.diff`, fresh `cargo build --release -p xtask`, shared box, load 0.5–2.1):

| claim | author | mine |
|---|---|---|
| prologue @428 bodies | 15.0 µs (rekey 14.7) | 15.4 µs (rekey 15.0) |
| prologue @32 bodies | 6.7 µs | 7.1 µs |
| e(B) m400, 0.05/0.2/1/5 ms | 1.18/3.09/20.3/75.7 | 3.05 @0.2, 73.1 @5 (rest from their JSONs, recomputed) |
| delivered m4→m400 @0.2 ms | 22,836× → 28.8× (792×) | 21,631× → 28.3×; T/D exact in every cell |
| T×D factorization | 11.3× (e 2.1, fps 5.3) × 70× | 11.0× (7402→668 ev/s; fps 5.3) × 69× (0.34→23.6) |
| paced worst cell (60 Hz, m400, 0.2 ms) | 5.16×, med 0, 93% frozen, 39×1.3 gs, worst 15.95 ms, digest equal | 5.16×, med 0, 92% frozen, 40×1.29 gs, worst 15.05 ms, digest f5c0c9f7 equal |
| row-1 digests vs `orig/` | 029f9c92/e68f7fcf/95750d31/475f4db2 all exact | all four equal (I re-ran 300000: 475f4db2 exact, med 7,435 vs orig 6,818) |
| density profile m400 | 17/32/31/3.5 ev/gs | 17.2/31.8/30.7/3.5 from their JSONs (nested ranges; one digest per scene across budgets legitimizes it) |
| record corrections | 371 bodies stalled, engine p50 0.28→5.23, view 3.35 of frame 4.77 | confirmed in their JSONs and mine |

`tables.py` regenerates every table from `data/`. Determinism held again: one digest per members count across budgets, pacing, processes and days (P13).

**Predictions.** `predictions.md` (19:27:16) precedes the first grid artifact (19:27:28). P1 held (e(0.05,400)=1.18 ≥ 1; 1.6% of events at 1% of budget); P2 held inside the pre-registered bands (11.3× ≤ 30×, 70× ≥ 10×); P3 held (17.5–28.8× with ~90% frozen); P4 held (5.2× in 2–50, worst 15.95 ≤ 17, digest equal); P5 held (15 µs in 5–100; 0.3%/5% of engine); P6 held with the 30,000-row median −25% disclosed in advance as load scatter. The P2/P3 derivation from the original JSONs was disclosed before the run — honest.

**Adversarial** (mine): (1) budget 0.1 ms at m400, unmeasured by the author: e = 1.49/frame, 14.9 per budget-ms, digest unchanged — no knee between their grid points; the prologue story stays dead. (2) Seed 2 at m400/0.2 ms: delivered 53.3×, median 0, T/D exact (851 ev/s ÷ 15.97 ev/gs) — the factorization is not a seed-1 artifact. (3) Prologue scaling: I raised the harness's `--members` clamp (400) locally and measured 41.4 µs at 931 bodies and 90.3 µs at 2,190 — linear-ish, no super-linear growth; rekey alone would need ~5,000 bodies to eat a 0.2 ms budget. (4) rtf 300,000 coast fresh: digest bit-exact.

**Novelty.** H0210 already recorded "one digest across budgets and threads" (re-verified here, not new). No HISTORY entry measures the per-frame prologue, decomposes the delivered rate, or proposes a density/throughput shed. The predecessor is today's original run (silver, mechanism mis-attributed); this run converts the checker's counter-reading from arithmetic on old JSONs into direct measurement, quantifies the factorization, and fixes the record's provenance (scripted vs coast row 1, 371 vs 428 bodies, the engine-p50 column mix-up).

**Goal fit.** Board #4, foundation 7. The run shows a premise wrong twice over: the silver's mechanism (no 0.2–1 ms prologue exists at game-relevant sizes) and the reading of "0.00×" (a run-average of 28.8× hiding in a median). It also shows foundation 7's "overflow … becomes a brief, smooth dip … never a visible degradation" fails in form under sustained overload: the rate is preserved on average but as a stutter (93% of frames frozen, 1.3 game-s jumps). "The simulation tells us what's next not us" (P22) — the front's own density is the shed signal, not a per-frame cost audit. Cost to adopt: small, arithmetic on quantities the dashboard already has; the prologue audit is deleted before it was built.

**What the author missed.**
- `work/patch.diff` does not reproduce the dossier's commands as saved: it drops the `--coast` flag arm (present only in `orig/patch.diff`) and will not stack on it (both re-declare `coast`/`series`). I reconstructed the union (work patch + one line from orig). Everything then regenerates bit-exact, but a checker following "apply work/patch.diff" hits `unknown universe argument --coast` on every grid command. The next author should save one cumulative diff.
- The demand arithmetic "5.85 s of engine per wall second — 293× the 5 ms/60 Hz budget" is wrong as stated: 5 ms/60 Hz is 0.30 s/s, so the ratio is 19.5×. The conclusion (no frame budget holds 3,000× at 400 members; the allocator must dip deliberately) survives, but the number overstates ~15×.
- "~29 ns/body" is 34.5 ns/body as measured (14.75 µs ÷ 428) and 35–50 ns/body marginal above ~900 bodies; "~7,000 bodies to reach 0.2 ms" is nearer 5,000. The `--members` clamp at 400 silently forbids the direct probe.
- The evidence header's "load 0.18–0.25" is contradicted by the JSONs' own uptime lines (0.53–2.1).
- Their own disclosed gaps stand: one seed for the factorization (my seed-2 cell now covers it), 0.05/1 ms paced cells unmeasured, the view gather (70% of the frame at m400) untested as a shed target, and no per-frame events column to ground D(t) inside one run.
