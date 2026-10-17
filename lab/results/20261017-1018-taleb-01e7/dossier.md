# Dossier — 20261017-1018-taleb-01e7 (Taleb lens)

**Claim.** The wiki conflict on `allocator-ratchet` is resolved: the shipped finality assert
(`alloc.rs:1451`) is an **engine-side publish/rollback boundary defect exposed by sustained
spatial overlap** (dense slow gas: split-then-reclash churn at `min_region 1`), reachable in
the frame harness **at scene start** (panics at chronon 32–96, i.e. the first ~0.2 s of a
loaded scene at the keeping-up rate) and **through on-grid chunked batch targets** — so the
driver rule proposed as the complete fix (grid-aligned `run_to` targets) does not close it;
the no-crash 18/18 record was earned on the sparse/no-churn scene class (rb 0–8), and the
separator between the two disputed records is **rollback pressure**, not driver, grid or
bulk geometry.

**Bottleneck.** The page's open direction 1 (decide the publish/rollback boundary), the top
of the `allocator-ratchet` page and the dispute the index flags as "conflict to resolve".
Gain: a decision, not a speedup — one of the two proposed fixes is dead (the driver rule),
the engine-side fix (refuse an advance whose rollback would cross a published tick, or hold
publication) is confirmed necessary, and the exposure is named (`min_region 1` splits under
sustained overlap; rb ≥ ~50 is the crashing regime). It also deletes the remaining doubt
about b966 (three windows had reproduced frames panics; 5d87's grid theory said
structurally impossible — both records are real, of two classes).

**Evidence.** Shipped `main` + one new example file (`crates/allocator/examples/finpol.rs`;
no engine edit; verified the panic site is the shipped assert at `alloc.rs:1451:17`,
thread `alloc-N`). Scenes decouple the disputed variables: `selfchurn` = ONE loose gas
cluster (n = 240, no approach, internal spread `vmax` units/chronon), `wave` = zero-spread
Pass slabs (planned merge, no churn — 5d87's class), `crossing` = two churn clusters
meeting mid-run. Frames at rate 600 (keeping-up: present/s 599.2 on survivors), 3 P + 4 E
workers, margin 0.5, `Law::Relativistic`, window 16 unless stated. Reproduce:
`bash lab/results/20261017-1018-taleb-01e7/regen.sh` (~7 min; every process < 2 GB, draws ≤ 6 s).

| arm | draws | crashes | panic `s0→fin_hi` | rb (survivors) |
|---|---|---|---|---|
| **frames** selfchurn vmax 2, r600 | 9 | **3** | 32→48, 80→96, 32→48 | 57–95, E to 2⁵⁷ |
| **chunks on-grid** (128 = 8×window) vmax 2 | 3 | **2** | 32→48, 80→96 (batch: same values as frames, same seed) | 73 |
| frames selfchurn vmax 8, r600 | 6 | **1** | 1408→1472 (b966's shape) | 0–4 |
| frames selfchurn vmax 16, r600 | 5 | 0 | — | 1 (dispersed) |
| frames selfchurn vmax 8, n 480 | 3 | 0 | — | 1 |
| frames selfchurn vmax 8, r300 | 3 | 0 | — | 1–3 |
| frames crossing (2 clusters, meet ~250) | 4 | 0 | — | 0–8 |
| frames wave (no churn) r600 + r1200 | 6 | 0 | — | 1–2 |
| frames selfchurn vmax 2, **min_region 32** | 3 | 0 | — | **0**, E 1 |
| frames selfchurn vmax 2, **window 32** | 3 | 0 | — | **79–109** |
| batch single call, vmax 2/8 | 2 | 0 | — | 0 |

Raw: `out/*.{out,err}` (panics in `.err`). All panic gaps are 1–4 windows, on the grid, in
both drivers. The crashing regime correlates with rollback pressure, not with anything
else measured: every crashing arm sits at rb ≈ 57–95 (or deterministic batch equivalents);
every no-churn arm (wave, crossing, dispersed vmax 16) sits at rb ≤ 8 and never crashes;
`min_region 32` takes rb to exactly 0 (the dense slow gas never splits: one region, zero
conflicts) and never crashes; window 32 keeps rb 79–109 yet survived 3/3 — the coarser
stride/grid widens the race margin (`fin_hi − s0` must cross a 32-tick gap, not 16), a
lead, not a verdict. Escalation on crashing-arm survivors is 2^rb (2⁵⁷ observed) — the
page's unbounded ratchet in the same regime.

**Predictions** (`predictions.md`, written before any churn-scene run): P1 held — selfchurn
crashes in frames (3/9 at vmax 2, 1/6 at vmax 8); crossing 0/4, disclosed: the second fresh
family stayed quiet (its overlap is transient, rb ≤ 8 — consistent with the separator).
P2 held — wave 0/6 at every load. P3 held — **on-grid chunks crash** (2/3): the driver rule
is dead as a complete fix. P4 vacuous at vmax 8; at vmax 2 it became the window-32 lead.
P5 held — min_region 32 → 0 crashes, with the mechanism exposed: it deletes the conflicts
(rb 0), it does not fix the boundary. P6 **refuted, sign inverted**: vmax 2 crashes more
than vmax 8/16 — the dose axis is dispersion timescale (sustained overlap), not spread
magnitude; slow dense gas churns forever, fast gas disperses and goes quiet. P7
inconclusive here (r300 run only at vmax 8, which rarely crashes; b966/checker2's load
gradient stands). P8 held — single-call batch survives.

**What would make it wrong.** One machine, shared load; 3–9 draw bins (the page's own
Extremistan lesson: windows swing). The frames race is wall-clock-timing-dependent (same
seed crashes or survives across draws); the batch chunk panics repeat the same values per
seed, so the batch half is deterministic. The window-32 margin lead needs ≥ 6 draws to be
more than a lead. The churn class is synthetic Bounce-contact gas, not the flown universe
(open direction 5) — but a belt under synodic stirring or any battle is precisely a
sustained-overlap regime, so the exposure class is game-realistic even if the scene is
synthetic. Cost of adopting: none (a measurement); it selects the engine-side fix already
specified by 9b46 open direction 1 and retires the driver rule as the complete answer.

**Fit with PRINCIPLES.** §25 "not making mistakes matters more than doing things
efficiently… don't multiply by zero" — a panic in the player's first second is the zero;
§13 "errors never compound" — here the certificate aborts instead of degrading, the wrong
side of §34 "the oracles are guards, not shepherds"; §1 via negativa — `min_region 32`
shows the whole risk class deletes with the conflicts, but at the price of deleting splits
(a capability), which is why the boundary fix, not the knob, is the adoption.

**The lens.** Taleb asks what breaks: the answer inverted my own pre-registered dose
model — the ruin regime is not the spectacular two-cluster collision but the boring,
perpetually-overlapping cloud; concavity lives in conflict discovery lag, and the crash
comes at scene start, when the player has no slack to absorb it. What the lens may have
missed: it prizes the survival question over the cost question, so the window-32 margin
(possibly a cheap partial mitigation) was noticed only incidentally.
