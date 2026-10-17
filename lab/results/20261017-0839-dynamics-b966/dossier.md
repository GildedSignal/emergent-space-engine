# Dossier — 20261017-0839-dynamics-b966 (dynamics lens)

**Claim.** The shipped publish/rollback finality crash (`alloc.rs:1451`, "rollback … would
revise its published tick") is reachable in the **frame harness** — the live engine path —
racing frontier publication against conflict discovery: it fires on a large fraction of
draws at the keeping-up rate (11/19 at rate 600, n = 120, across two windows; chunked
batch 3/3), never with slack (rate 300: 0/6), and only occasionally when the engine falls
behind present (n = 240 and rate 1200: 2/12) — a reachable live-path panic whose
incidence, not whose possibility, is load-dependent.

**Bottleneck.** Board item 4 (smoothness and the allocator) via the page's open direction
2 ("Frames mode: … if the same assert can fire, the crash is in play, not only in batch
drivers. One `run_frames` run on the wave scene decides it"). Answer: it can, so the
crash is player-reachable, and open direction 1 (decide the publish/rollback boundary)
moves ahead of every performance question on this page: a reachable panic in the live
path is ruin, and "never risk ruin for an average gain".

**Evidence.** All runs on shipped `main` code plus this run's single-file patch
(`crates/allocator/examples/finframe.rs`, the instrument; no engine edit). Scene `drift`:
two loose gas clusters (n = 120 each) closing at Q/8, two quiet islands at ±2000 units;
default scheduler, `min_region: 1`, `speed_margin: 0.5`, 3 P + 4 E workers. Reproduce:
`bash lab/results/20261017-0839-dynamics-b966/regen.sh` (~4 min; every case ≤ 6 s).

| arm | draws | crashes | panic shape (s0 → fin_hi) |
|---|---|---|---|
| `drift chunks` (75/150/450 to H=1800) | 3 | **3** | 256→300, 300→375, 400→450 |
| `drift batch` single call H=1800 | 1 | 0 | (4 rollbacks, no crash) |
| `drift frames` rate 600, n=120 | 14 | **10** | 576→608, 624→672, 656→672, … gap always 16–64 |
| `drift frames` rate 300 | 3 | 0 | surviving frontier > 2100 |
| `drift frames` rate 1200 | 3 | 1 | 512→528 |
| `drift frames` n=240, rate 600 | 3 | 0 | but 35–84 acceleration drops (engine behind present) |
| `quiet frames` (n=40, 120) | 4 | 0 | rollbacks ≤ 1, no mid-horizon conflict |
| **regen window** (same arms, fresh draws) | 5+3+3+3+3 | 1+1+0+0+0 | rate-600 n=120: 1/5; n=240: 1/3 (768→784); rate 300: 0/3; rate 1200: 0/3 |

Raw outputs: `out/*.out`, `out/*.err` (panic messages in the `.err`). The one fully
keeping-up surviving draw printed `present/s 599.2` (target 600), 0 deadline misses,
frontier 3760, 1 rollback — survival with the engine keeping up is possible but is the
minority draw. Mechanism, read off the panic values and `alloc.rs`: `certify`'s clash
start is the **stride start** of the second-completing lineage's truth, which lies below
the stride's end; frontier-published finality (`fin_hi` = all-verified tick) only needs to
lead that start by one stride to make the shipped assert fire. Chunked advance forces the
race at every boundary (frontier jumps to the chunk target for all regions at once). In
frames mode the same race runs continuously against `present`. Across both windows the
incidence reads: rate 600 n=120 → 11/19 crashes (10/14 author window, 1/5 regen window —
per-window counts swing, Extremistan as on the rest of this page); n=240 at 600 → 1/6
(the "behind present" protection is a tendency, not a law); rate 300 → 0/6, the only arm
that never crashed; every observed gap `fin_hi − s0` = 16–64, i.e. 1–4 strides.

The conflicts that fire are split-sibling conflicts around chronon
576–692 (the cluster approach itself is *planned*: 76 merges, 0 conflicts of that pair),
which matches 9b46's trigger class "any conflict found after a publication".

**Predictions** (`predictions.md`, written before any `drift` run): P1 chunked crashes —
held (3/3). P2 frames crashes — held on 11/19 draws at rate 600 across two windows; my
alternative (the `ahead` cap structurally protects frames mode) is refuted: the observed
gaps (16–64) are smaller than the 150-chronon ahead lead, and survival tracks load, not
the cap. P3 single-call batch
survives — held (1/1). P4 quiet survives — held (4/4). P5 the crash is the conservative
stride-start rollback crossing published frontier finality — held in shape (fin_hi − s0 =
1–4 strides); my guess that the firing conflict would be the cluster approach (values
≥ 900) was wrong: split-sibling conflicts near 600 fire first.

**What would make it wrong.** All frames draws are on one scene family, one machine, one
config; incidence counts are small-bin draws from a race — the *rate-600* 11/19 is not a
parameter, only "a large fraction of draws, window-dependent" is. If the flown universe's real conflict rate (open
direction 5) is far lower than this battery's, wall-clock exposure shrinks — but one
reachable draw is enough for a live-path panic, so the adoption question does not depend
on incidence. Cost of adopting the finding: none (it is a measurement); the fix it
demands (open direction 1: refuse an advance whose rollback would cross a published tick,
or hold publication until the wave quenches) is localized to `rollback`/`publish` and was
already specified by 9b46 — this run upgrades its priority from "batch drivers" to "the
engine".

**Fit with PRINCIPLES.** "Errors never compound" (§13) — here the certificate does not
compound, it *aborts*: the finality police crashes the engine rather than degrade, which
is the wrong side of "the oracles are guards, not shepherds" (§34); and "not making
mistakes matters more than doing things efficiently" (§25) — a reachable panic in the
live path is the mistake that zeroes everything. The measurement also obeys §10: controls
on both sides, kill criterion pre-registered (if chunked had not crashed, VOID).

**The lens.** A dynamics lens saw a race and swept its load dimension (rate, n) instead
of more seeds per point — the incidence *band* (edge of keeping up) is the deliverable,
but per-arm draw counts are 3–14, so a checker could legitimately find rate-1200 more or
less exposed than 1/3. What I did not open: which lineages clash (split siblings vs
approach — inferred from the 76 planned merges and the ~600 chronon values, not traced),
and whether `fast_finality`'s light-cone path can also publish past a clash start (the
observed crashes are frontier-finality; both paths set `fin_hi`).
