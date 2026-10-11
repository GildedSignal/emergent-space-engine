# Dossier — the plane's overload cliff and its stall floor

**Claim.** The plane's overflow design holds where it was claimed to hold — past capacity the
real-time factor dips with no hitch and bit-identical digests — but it fails silently below a
**per-frame budget floor that scales with the universe**: at a 0.2 ms engine budget a 32-body
universe still delivers 1,240× real time while a 428-body one delivers **0.00** (a silent stall:
frames stay cheap, no error, digest still exact), and the smoothness tail that moves first is not
frame time at all but **presented-time stalls** (delivered-RTF lowest 1% = 7.3 paced, 0.7 with an
11,500 g held burn) while worst frame stays 12–16 ms.

**Bottleneck.** Board #4 (smoothness and the allocator) and foundation 7 of docs/plane.md
("bounded work per presented frame"; "overflow … the real-time factor dips for a frame, smoothly,
and nothing hitches or degrades"). The measured gain is a design guard, not a speedup: the fixed
per-frame cost (deadline rekeying, queue and horizon bookkeeping, `Universe::advance`'s per-frame
prologue before any event is bought) is the allocator's ruin bar, and it must be O(1) in N or the
stall floor rises with every doll. What it deletes: any belief that "budget bites → dip" holds at
all budgets, and any smoothness gate that watches only `frame_ms`.

**Evidence** (Linux x86, 8 vCPU shared, load 1.1–1.6, 15 GB, no thermal data — orders of
magnitude only; the integrator re-measures on the M1). All runs: `xtask universe --bench`, seed 1,
threads 1, `--series` per-frame CSV; scripts and raw JSON/CSV in this folder.

| run | delivered RTF med | low 1% | overflow | worst frame ms | engine ms/game-s |
|---|---|---|---|---|---|
| rtf 300 unpaced | 300 | 300 | 3/600 | 6.4 | 8.9e-1 |
| rtf 3,000 unpaced | 3,000 | 1,240 | 23/600 | 6.8 | 1.6e-1 |
| rtf 30,000 unpaced | 30,000 | 1,013 | 269/600 | 9.7 | 2.1e-2 |
| rtf 300,000 (3 s) | 6,818 | 620 | 180/180 | 7.3 | 1.2e-1 |
| rtf 3,000 paced | 2,479 | **7.3** | 344/600 | **12.1** | 1.1e-1 |

1. **Dip, then cliff.** Budget 5 → 1 → 0.2 ms at rtf 3,000 (coast): delivered median 3,000 →
   1,243 → **1.6**; at 0.05 ms, 0.0. Between 1 and 0.2 ms the plane stops making progress per
   frame: the per-frame prologue costs ~0.2–1 ms before any event is bought.
2. **The floor scales with N.** At the same 0.2 ms budget: members 4 (32 bodies) delivers
   **1,239.5×**; members 400 (428 bodies) delivers **0.00**, 186 events/s, frames cheap. One fleet
   of 400 is enough to cross the floor on this box.
3. **Bits never drift (ruin closed).** Coast rtf 3,000, 10 s: engine budgets 5 / 1 / 0.2 / 0.05 ms
   and paced vs unpaced — one digest `fbb0c7d5…adc72` in all five runs, including the fully
   stalled ones. Determinism under overload is real at this scene.
4. **No unbudgeted synchronous claim found.** Worst frame over every run: 16.0 ms (level-15 burn),
   12.1 ms paced at saturation — never above one 60 Hz frame; the engine budget plus a ~1–3 ms
   gather bounds the frame even 100× beyond capacity.
5. **The tail is in presented time, not frame time.** Paced and saturated, `frame_ms` p99.9 is
   clean while delivered-RTF lowest 1% = 7.3 (a 400× dip): frames where the presented tick barely
   moves while a big item (compile, handoff) resolves under budget. With the player's held burn at
   11,500 g (`--level 15`) the low tail reaches **0.7** at unchanged cost per game-second
   (0.20 vs 0.16 ms) — the wildcard is the deepest stall, for free.
6. **Fat cell benign; throughput plateau.** Members 4→400 (32→428 bodies): frame cost ×6 for
   ×13 bodies (sublinear; contacts stay local). Unpaced capacity ≈ 3×10⁴ delivered median on this
   box; degradation past it is a plateau with a mild U in cost per game-second (0.021 ms at 30k →
   0.12 at 300k, ×5, bounded — no compounding spiral over the run).
7. Side findings: the scripted player dies at rtf ≥ 3,000 (a 20-nominal-frame burn is a
   1,000 s burn; the harness reports "the player is lost" cleanly, no crash) — the bench script is
   tuned for ~100×, so `--coast` (added here, patch saves it) isolates engine capacity; at
   rtf 3×10⁵ with the script the run errors out as a game-over before any stall.

Reproduce (each ≤ 60 s): `cargo build --release -p xtask` then
`target/release/xtask universe --bench --rtf 3000 --seconds 10 --unpaced --coast --engine-ms {5,1,0.2,0.05}`
(digests, row 3); `… --coast --members {4,400} --engine-ms 0.2` (row 2);
`… --rtf 3000 --seconds 10 --coast` (paced row); `… --rtf {300,3000,30000} --seconds 10 --unpaced --coast`
and `--rtf 300000 --seconds 3` (row 1); `… --level {0,15} --rtf 3000 --seconds 10 --unpaced` (row 5).

**Predictions.** `predictions.md` was written before the sweep. Held: P1 (capacity 10²–10⁴, plateau
not collapse), P3 (worst paced frame ≤ 50 ms; measured 12.1), P4 (identical bits, exactly),
P5 (≤10× for 100× members; measured 6×), P6 (level-15 cost within 2×; measured 1.25×), P7 (RTF
oscillates with the battle, no ratchet: per-sixth medians 941, 3000, 3000, 3000, 2290, 2479).
Failed in the letter, held in spirit: P2 — cost per game-second at 100× beyond capacity rose ×4.5
against at-capacity (predicted ≤1.5×), a bounded U, not compounding. Not predicted (missed by this
author until the budget sweep): the stall *floor* itself and its scaling with N — the cliff, rows
1–2, is the run's real finding; the predictions treated the budget axis as continuous.

**What would make it wrong.** The floor could be a bench artifact if the 0.2–1 ms prologue is
HTTP/step-loop overhead rather than `Universe::advance` internals (the series separates engine
from view: engine p50 alone is 2.9→8.8 ms at members 400, so the prologue is inside the engine,
but a profiler should confirm rekey as the term). Linux/shared-box timings shift the capacity
numbers, not the shape. Cost of adopting: cheap — gate the allocator on *fixed per-frame cost
measured against N* (an O(1)-in-N prologue, or amortized rekeying) and add *ticks presented per
frame, lowest 1%* to the plane's smoothness dashboard next to `frame_ms`; both are guards, no
representation change. A fix that shrinks the prologue is worth ~5× in worst-case overload headroom
on this box (floor 0.2–1 ms → below 0.05 ms), i.e. the difference between a fleet of 400 and a
fleet of 4,000 stalling silently. Fit with PRINCIPLES: "the algorithm that allocates the work to
prevent those heavy tails, it's the most important one" (P12) — a stall floor that grows with N is
a heavy tail the allocator itself creates; "Errors never compound" (P13) — bits did not compound,
and that held under every overload; "its risk of breaking makes anything you do to improve it
inconsequential unless you first reduce that risk of breaking" (Antifragile) — the silent stall is
the breaking risk; "don't multiply by zero" (P25) — delivered RTF 0.00 at 428 bodies is exactly the
zero.

**The lens.** Taleb made me attack the budget axis (the shock) rather than the rtf axis everyone
tunes, and that is where the cliff was; but it also biased me toward the dramatic stall and away
from equally useful measurements I skipped: no per-item profiling of the prologue (rekey vs queue
vs horizon), no threads>1 (the M1 has 8 cores; the floor may parallelize away), no seed spread
(one seed per row), and no paced members-400 run (the worst realistic cell, saturated at 60 Hz —
the stall would be player-visible and should be measured before any gate is frozen from this).
