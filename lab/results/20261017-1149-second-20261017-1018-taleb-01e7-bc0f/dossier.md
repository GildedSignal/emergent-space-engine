# Dossier — 20261017-1149-second-…-taleb-01e7-bc0f (second author on 01e7)

**Claim.** The checker's named experiment is done at the page's own protocol (≥ 3 seeds ×
≥ 2 replicates) and the 01e7 claim holds, strengthened: the single-call batch channel —
5d87's strongest limb ("one call per process") — crashes **7/12 here (11/17 pooled with
the checker), identically on-grid (3/6) and off-grid (4/6), always at scene start
32→48**, with panic values stable per seed and reachability raced (one same-seed
replicate pair splits); and the "quiet classes never crash" reading is dead as a
window-independent statement — this window crashed the dispersed-gas and crossing arms
**late** (chronon 1120–2720: vmax-16 3/6, vmax-8 2/6, crossing 1/4 — the first crossing
crash on record, 1/16 pooled), so the only strictly clean classes are the zero-churn
wave (0/15 pooled) and `min_region 32` (rb exactly 0, 9/9 pooled): **no scene-design
dodge exists; the engine-side publish/rollback boundary fix is the only door.**

**Bottleneck.** The record defect the checker named (three falsified arms reported from
single draws against the page's direction-4 protocol; rows not regenerating). Gain: the
allocator-ratchet conflict resolution becomes adoptable — both limbs of the driver rule
are now killed at protocol strength, and the exposure is wider than 01e7 reported
(every overlap class reaches the assert, at scene start under churn, late under
dispersion). Nothing to build: it selects the engine-side fix (9b46 open direction 1).

**Evidence.** Shipped `main` + 01e7's example file verbatim (`work/patch.diff`, one new
file, no engine edit; panic site = shipped assert `alloc.rs:1451:17`, thread `alloc-N`,
exit 101). Every number below is `bash lab/results/20261017-1149-second-20261017-1018-taleb-01e7-bc0f/regen.sh`
(292 s this window; every process < 2 GB; frames draws 6 s). Box light: load ≈ 0.9 on
8 vCPU, frames survivors keep the rate exactly (present/s 595–599 at r600), so the
raised quiet-class incidence below is not a simple overload artifact (per-draw load
unrecorded — window effects cannot be fully excluded, and that is the point).

| arm (all selfchurn n 120→240 bodies unless stated) | draws | crashes | panic `s0→fin_hi` | rb (survivors) |
|---|---|---|---|---|
| **frames vmax 2, r600** | 9 | **3** | 32→48 ×2, 80→96 | 68–89 |
| **chunks on-grid 128** (8×window) | 3 | **2** | 32→48, 80→96 — same values per seed as frames | 70 |
| **batch single 1792** (on-grid, 112×16) | 6 (3 seeds × 2) | **3** | all 32→48 | 70–79 |
| **batch single 1800** (off-grid) | 6 (3 seeds × 2) | **4** | all 32→48 | 71–74 |
| batch single, per seed (both horizons) | 12 | s11 **4/4**, s15 **3/4**, s21 **0/4** | s11, s15 → 32→48 | s21 71–79 |
| frames vmax 8, r600 | 6 | **2** | 1360→1440, 1408→1472 (late) | 1–4 |
| frames vmax 16, fresh seeds 22–24 × 2 | 6 | **3** | 1120→1184, 1424→1440, 1616→1632 (late) | 1–8 |
| frames vmax 8, n 480 | 3 | **1** | 2064→2128 (late) | 1 |
| **frames vmax 2, n 480** (960 bodies) | 6 (3 seeds × 2) | **1** | 80→96 (scene start) | **123–180** |
| crossing (2 clusters, meet ~250) | 4 | **1** | 2576→2720 (late; first on record, 1/16 pooled) | 1–3 |
| wave (zero-spread planned merge) | 5 | 0 | — | 1–2 (0/15 pooled) |
| frames vmax 2, **min_region 32** | 3 | 0 | — | **exactly 0, E = 1** (9/9 pooled) |
| frames vmax 2, **window 32** | 3 | 0 | — | 83–109 (9/9 pooled) |
| frames vmax 8, r300 | 3 | 0 | — | 1–3 |

Structure the pooled record adds: (i) **E = 2^rb exactly on every survivor, 37/37
across all arms** — up to 2^180 on the n480 draw (the unbounded ratchet, far past u64);
(ii) batch survivors run the whole 1792–1800 horizon in **0.4 s** (present/s
3900–6700): the crash is decided in the first ~48 chronons, which is why horizon class
(on/off-grid, 1792 vs 1800) cannot matter and does not (3/6 vs 4/6, same values);
(iii) two crash phases exist — **scene start** (churn classes: 32–96) and **late,
quiet-phase reclash** (dispersed/crossed classes: 1120–2720, panic gaps 16–144 = 1–9
windows, matching the page's 1–10); (iv) a crashing draw never prints its rb (the row
prints at completion), so rb cannot be a draw-level predictor *by construction* — and
at arm level it is dead as a separator: n480-vmax-2 survivors sit at rb 123–180, far
above the n240 crash band's 57–95, and survive 5/6.

**Predictions** (`predictions.md`, written before the run). **A2 held** (panic values
stable per seed across replicates; the same-seed split happened: s15@1792 r1 crash,
r2 survive). **C1, C2 held** (n480: 1/6, crash at 80→96, survivors rb 123–180).
**A1 partial fail**: on-grid batch 3/6 against a ≥ 4/6 threshold (off-grid 4/6 held;
pooled 7/12 keeps the limb dead). **A3 failed**: held-out seed 21 is quiet in batch
(0/4) while s11 crashes 4/4 — batch propensity is seed-skewed inside the race.
**B1 failed, the run's one real discovery**: I predicted 0–1 vmax-16 crashes, got 3/6
(pooled 4/22) — "rare, not never" is window-dependent, not a class property; the same
window also broke my vmax-8 (2/6 vs 0–1 predicted) and crossing/sc8-n480 core cells
(1/4, 1/3 vs 0). Every miss points the same way: quiet-class incidence is
fat-tailed across windows. Core arms otherwise regenerated as standing: frames 3/9,
chunks 2/3 same-values-per-seed, mr32 0/3 at rb 0, w32 0/3, wave 0/5, r300 0/3.

**What would make it wrong.** One window, shared box; per-draw load unrecorded, so the
quiet-class incidence (3/6, 2/6, 1/4) is a window sample, not a rate — the pooled
denominators (4/22, 4/18, 1/16) carry the uncertainty. The frames and batch races are
wall-clock draws; per-seed batch propensity (s11 4/4 vs s21 0/4) is 4 draws deep per
seed. The churn scenes are synthetic Bounce gas, not the flown universe (page open
direction 5). Cost of adopting: none — a measurement; it confirms the engine-side
boundary fix already specified (refuse an advance whose rollback would cross a
published tick, or hold publication) and retires every driver/scene dodge at protocol
strength. PRINCIPLES §13 "basically we don't want errors that can compound" — the
certificate aborts instead of degrading; §25 "not making mistakes matters more than
doing things efficiently… don't multiply by zero" — the zero now reaches every overlap
class, late if not early.

**The lens.** The second-author lens prizes a record that regenerates; what it may
have missed is mechanism: the late quiet-phase crashes (gap 16–144, few conflicts,
publication far along) and the seed-skewed batch propensity both suggest the race is
between conflict *discovery latency* and *publication cadence* — a timing analysis
(when fin_hi passes s0 per reclash) could turn incidence from a sampled race into a
predicted one, but that is new work, not this run's.
