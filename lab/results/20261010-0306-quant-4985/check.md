Grade: silver

**Abstract.** Claim: first H_live baseline on the shipped plane — the live ledger saturates (light-cone prune balances creation) at ~2.3 KB per orbiter ship and ~5.0 KB per battle member, so 8 GB holds ~10⁶ bodies; the whales are re-minted generators, retained segments and never-freed corpses. Reproduced byte-for-byte (4/5 logs identical, the 5th differs in wall time only; digests match). Extended adversarially: at 10⁵ game-seconds, 2,354 B/ship with +16,153 ship events adding 736 B; 4000 members give 4.7 KB/member steady, 729 MB peak; allocator/ledger 16.8–17.3×; universe suite green (54 tests). Cost to adopt: none (additive instrumentation). Two dossier rate figures are unit errors; the capacity order was already H0158's on the old engine.

## Reproduction

Clean tree, `git apply work/patch.diff`, build (9.8 s), all five commands rerun: `seed1-m48`, `seed1-m200`, `seed5-m48`, `long-30000` byte-identical to the author's logs; `seed1-m1000` differs only in wall time (8.2 s vs 8.3 s). All digests, `live=` and ledger values match. `cargo test --release -p emergent-universe`: 54 passed, 0 failed. The structural claims hold in code: `PlainBodies` has push/put/retire/prune and no removal (`recs` never shrinks — corpses stay); `bytes_of` counts `size_of::<Segment>()` per history entry while each `Segment` holds an `Arc<Entry>` whose trajectory heap is outside the ledger, so the 16.8× split is real by construction; prune is `2·light_distance + 2²⁶` ticks every 64 frames (`universe.rs:870-872,970`).

Checked against the logs: 2,322 B/ship and 5.9 segs/ship at t=3×10⁴ (53408/23; 136/23); +4,620 events → +8 segments, +1,152 B between 10⁴ and 3×10⁴; member steady 5,134/4,730/5,050/5,265 B at 48/200/1000 members and seed 5; allocator/ledger 16.74× (m1000 end); peak 97.3 MB vs 34.2 MB steady (2.85×); handout 480 members in ~30 s, live 0.56→11.7 MB; worst body 40,496 B vs 6,204 mean (6.5×); creation mint (6624+2848)/92 ≈ 103 B/event; ~49 B/s/member reproduces as 51.7.

## Predictions

`predictions.md` mtime 03:13:20; all five logs 03:23:11–24 — written before the decisive runs. Falsifiers were real and the author scored the misses honestly (magnitude 10× high on per-ship bytes; "three to four orders" corrected to 2.5–3). Saturation and the ≥2× undercount held.

## Adversarial cases (mine)

1. **10⁵ game-seconds** (3.3× the author's horizon): ship ledger 54,144 B (2,354 B/ship), 138 segments (6.0/ship); between 3×10⁴ and 10⁵, +16,153 ship events added +736 B and +2 segments. Allocator live flat at 2.06 MB, peak unchanged (7.1 MB). Saturation is durable, not a transient.
2. **4000 members** (4× the worst case): steady 4,713 B/member, worst body 38 KB in the fight, peak RSS 729 MB, live/ledger 17.3×. Consistent; the per-member verdict scales.
3. **Seed 9**: 2,229 B/ship, 5,093 B/member, star flat at 10⁴. Holds.
4. **members=0** (pure orbiters, to isolate per-ship allocator cost): panics — `a battle needs two fleets` (`scenes.rs:14`). The orbiter-only allocator truth is unreachable without editing the scenario; the 16.8× is measured only on battle-carrying scenes.

## Novelty

HANDOFF:70 lists H_live as "not measured yet"; this is the first measurement on the shipped plane, through the player's path, and the instrument is new (`cost.rs` times compiles, `tail.rs` times frames). But the headline order is not new: H0158 (25 September, the pre-pivot `crates/engine`) already derived capacity from ~2.7 KB per tracked ship (~1.4M ships on 4 GiB) — explicitly "a process-level measurement, not byte accounting". What is new here: the saturation mechanism (creation vs prune equilibrium), the whale anatomy (re-minted generator, retained `Arc<Entry>` segments, corpse leak), and the ledger/allocator split. The re-mint premise itself is the taste log's 5-October finding (99% of kicks recompile).

## Goal fit

Direct hit on the board focus "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and the B18 memory gate's missing baseline; couples memory to bottleneck 1 (kick cadence). PRINCIPLES #6 "Store the generator, not the generated" — measured, the generator store is the whale; #24 — 2.3 KB against the quoted ~0.1-bit floor is the headroom. Respected: additive instrumentation, no gate touched, integers/logs decide.

## Why silver, not gold

Real, reproduced exactly, honest, and needed — but a baseline, not a mover: nothing is deleted, no premise falls (it confirms the suspected whale), and the gain is quantified headroom, not a 10× step. The author names the adoptable experiment themselves. Also the capacity order was already known approximately (H0158).

**The one experiment for gold:** the deduping generator store (quantized class + lazy exact residual), judged against this baseline and B18 — per-body live bytes must fall ≥ 10× at unchanged behaviour (digests of the plane unchanged). A cheaper companion that would harden the baseline itself: isolate the allocator truth into corpses vs fleet lattice world vs fixed cost (the author's own lens note), and measure the orbiter-only scene by allowing a degenerate battle.

## What the author missed

- **"0.2 events/s/ship" is a unit error**: the logs show 0.23 events/s fleet-wide across 23 ships = 0.010/s/ship (20×). The conclusion survives (my 10⁵ run: 23k events, flat memory).
- **"~3.7 events/s/member … 20× the orbiters'" does not reproduce** from any slice: t=31.7→101.7 in m1000 gives 40.8/s fleet-wide, 0.061/s per member; the ratio is ~6× per body or ~177× fleet-wide, not 20×.
- **"star — 1,160 B flat, zero events, at every snapshot, all runs" is contradicted by the author's own log**: star_b=1320 at t=3×10⁴ (long-30000, last row), 1352 at 10⁵ (my run), and planet_b 3152→3312 by t=10⁴ in every run. The negative control holds only to ~10⁴.
- "Alive members fall 1000→393": peak alive was 862 (1000 requested).
- The 16.8× is never decomposed; if even part of it is per-body-proportional (it grows with battle size: 12–13× at 48 members, 17× at 1000–4000), the allocator-inclusive capacity of battle scenes is nearer 2×10⁵ than 10⁶. The "~10⁶" headline is the ledger-only, orbiter-only best case, and the orbiter-only allocator truth is unmeasured (members=0 panics).
