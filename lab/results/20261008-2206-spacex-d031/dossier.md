# Dossier — 20261008-2206-spacex-d031 (SpaceX lens)

**Claim.** On the plane as shipped, the creation rate of distinctions is tiny (0.059 resolved events per body per game-second in the mature scene; the only true input is the player's ~6 decisions/1000 gs), but the engine stores each distinction at roughly 3,000× its information content and never reabsorbs history: live state grows ≈4 bytes/body/game-second, so at 10⁹ bodies the 8 GB budget fills in about 2 game-seconds — the wall is storage-per-distinction and missing reabsorption, not the distinction rate.

**Bottleneck.** HANDOFF's risk #2: "Distinctions created per game-second (H_live) … decide whether 10⁹ fit in 8 GB; not measured yet." First measured number, aimed there. Expected gain: redirects the `shipmem`/scars design (what to store, what to reabsorb) before the belt build; deletes nothing today but stops the memory question from being answered by body count.

**Evidence** (Linux/x86 runner, 8 vCPU, orders of magnitude only; machine state in the JSONs).

Patch: read-only counters threaded through `Stats` (kicks_recompiled, cat_inserts/releases, segs_retired, emitted-quanta histogram) and printed by `--bench`. Digest-neutral, verified: identical digest `09e408…` with and without the probe, before and after the last addition (rtf 100, 10 s).

Commands (each ≤ 60 s wall after a 35 s build):
```
CARGO_TARGET_DIR=<dir> cargo build --release -p xtask
<dir>/release/xtask universe --bench --rtf 100 --seconds 10 --unpaced   # also --rtf 1, --rtf 10
```
Outputs: `bench-rtf{1,10,100}.json` here.

Scene at rtf 100 × 10 s = 1000 game-seconds, 71 bodies, 5,189 B/body:
- Distinct resolved events: kicks 736, opens 77, boundaries 667, handoffs 0, lattice slices 2,680, decisions 6 → 4,166 events / 1000 gs = **0.059 events/body/game-second**.
- **93.5% of distinct kicks recompile the binding** (688/736; 84% at 100 gs early scene). Confirms the board's ~99% as a distinct-event measurement.
- **Catalogue at churn equilibrium**: 691 inserts = 691 releases, net 0, at every duration. Reabsorption of compiled entries already works.
- **History never reabsorbs**: 688 retired segments in 1000 gs (one per recompile), `Segment` = 192 B stack + a heap `Entry`. Nothing releases them.
- **bytes/body grows with scene age**: 1,203 (10 gs, 28 bodies) → 2,374 (100 gs, 39) → 5,189 (1000 gs, 71): ≈ +4 B/body/game-second, of which ≈1.9 B/body/gs is segments alone (688 × 192 B / 71 / 1000).
- Kick residuals: every emitted sigma-delta quantum lands above 2⁸ units at the body's own exponent — each kick writes a ≥8-significant-bit integer; the exact distribution saturated my top bucket (instrument limit, not a result).
- The shipped dashboard's `events_per_second` divides by **wall** seconds (410/s at rtf 100), i.e. it is rtf-inflated for any per-game-second use; `b-h-live` must not build on it unchanged.

Idiot index (the lens): stored ≈ 4 B/body/gs ÷ created ≈ 10⁻² bits/body/gs (6 decisions ≈ tens of bits per 1000 gs over 71 bodies) → **~3×10³**. Extrapolated to 10⁹ bodies [INFERENCE]: 4 GB per game-second; budget gone in ~2 gs. The 71-body scene is battle-dominated (2,680 of 4,166 events are fleet lattice slices); belt-scale rates will differ, but the storage-per-distinction mechanism is scene-independent.

**Predictions** (`predictions.md`, written before the ladder): #1 digest-neutrality verified at rtf 100 only (no uninstrumented baseline at 1/10 in budget); #2 FALSIFIED AS A TEST — the rtf ladder changes scene age and the scripted input log, so it measures transients, not schedule effects (the logs differ: 2 vs 6 decisions; digests rightly differ); #3 recompile >90% holds in the mature scene, 84% in the early one; #4 unresolved (bucket saturation); #5 verified everywhere; #6 verified (≈3,000× > 100×).

**What would make it wrong.** If retired segments are not meant to be live (e.g. a history tier is planned that reabsorbs or streams them to SSD), the 4 B/body/gs growth is not the wall and the claim reduces to "count the catalogue, it's already at equilibrium." Also: single scene, single seed, 1000 game-seconds; a belt-dominated scene could raise the kick rate per body above 1/gs and change the constant, though not the 10³ storage ratio. The `behave --law plane` suite was not rerun here (digest equality is the interference check); a checker should run it on the patch.

**Cost of adopting.** The counters are 30 lines, digest-neutral, and belong in `--bench` as the seed of `b-h-live`'s H_live output. The definition to adopt: H_live = **irreversible storage events per game-second** (segments appended, net catalogue entries, carry growth) × bytes, minus reabsorption — not resolved-event counts, which are mostly recompute, and not wall-based rates.

**Fit with PRINCIPLES.** "The memory floor is information-theoretic" (#24): the measured floor input is ~tens of bits/1000 gs while we store megabytes — the ratio is the work. "Compute only surprises" (#3): kicks are not surprises here (93.5% recompile = the same orbit refit each time); storing each refit is paying twice. "Less is more" (#1): reabsorbing history is deletion, the cheapest compute there is.

**The lens.** SpaceX's delete-first eye may undervalue the history: retired segments are the replay/exactness substrate (PRINCIPLES: replays at canonical ticks), so the fix is a tier that reabsorbs or streams, not dropping the scar. A lens closer to the law might ask whether the 93.5% recompile rate itself is the bug (why refit what a kick barely moved?) — that is the cadence question, already on the board.
