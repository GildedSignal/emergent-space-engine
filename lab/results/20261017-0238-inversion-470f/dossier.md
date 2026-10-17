# Dossier — 20261017-0238-inversion-470f (inversion lens)

## Claim

The plane's **peak memory is decided by the wall path, not the game**: the same flight (same
seed, args, binary, quiet machine) at 400 fleet members either peaks at ~44 MB or grows **~11
kB of live Rust allocations per game-second to 220.9 MB / 83,768 live allocations by 20,000
game-s, frees 78k allocations in one bulk drop, and leaves peak RSS at 206 MB forever** — with
`n_bodies`, `catalogue_live`, `bytes_per_body` (constant 5.9 kB/body) and the whole stats ledger
flat throughout; 5 of 15 seed-1 coast flights took the growing path (~33%), every other arm
(both burn arms, seed-2 coast, the shipped 48-member plane at 40,000 game-s, the 3,000-body
belt) was flat in every run. Memory is thus **not a canonical outcome** of an engine whose law
is — a 4.7× path-dependent swing in the very channel that sets the 10⁹ memory wall.

## Bottleneck

Failure mode "memory that grows with play" (the lens's list) on the board's top topic. Two wiki
pages held the open case: memory-h-live's "a reachable ruin state remains: peak RSS grows ~0.2
kB per surviving member per game-second through any battle that stays live" (d3fe, silver) and
nladder's "the long-lived-battle case where the one-time slice excess becomes a rate (4fa8's,
unflown)". This run re-measures that case on main at 4–7× every prior horizon: d3fe's clean
per-member rate is dead (fleets dissolve by ~3,000 game-s at every size flown; the slice bill
is one-time; the shipped plane and the belt never grow), but a stochastic, counter-invisible
growth of the same kind survives at 400 members — on the exact axis (fleet size) the N ladder
is about to climb. What it deletes: confidence in any single-run memory measurement; what it
asks: the counting-allocator census on the ladder's CI arm, and one run to isolate the cached
structure (the bulk drop at ~20,000 game-s is its signature).

## Evidence

Instrument: `crates/universe/examples/ruin_probe.rs` (work/patch.diff), print-only on shipped
code — the player's own loop (`frame_to` with `Budget::wall(5 ms)` + `gather_cached`, the
session's shape), unpaced, rtf 100, plus per-chunk `/proc/self/statm`/`VmHWM`, `/proc/self/maps`
(mapping count, total, `[heap]`), a **counting `GlobalAlloc`** (live bytes, live allocations,
cumulative allocs/frees) and the shipped counters. Every number:
`bash lab/results/20261017-0238-inversion-470f/regen.sh` (~8 min, quiet machine, each process
< 250 MB). The regenerable bimodality: `out-400-coast-40k.txt` (growing instance, preserved
also as `out-400-coast-40k-LEAKED-INSTANCE.txt`) beside `out-400-coast-r1..r4.txt` (flat).

1. **The growing path** (`out-400-coast-40k.txt`, seed 1, coast, 400 members): live allocations
   rise ~4.2/game-s to **83,768 / 220.9 MB live at gs 20,000** (avg blob 2.6 kB), `[heap]`
   tracking exactly, mapping count constant 34 (the main arena itself); between gs 20,000 and
   25,000 **live falls to 16.1 MB / 5,893 allocs — one bulk drop of ~78k allocations**; peak RSS
   207 MB (hwm) and RSS stays 206 MB to 40,000 gs and through the settle (+0 kB): the allocator
   never returns it. Held scans 0, pending handouts 0 — resolved state, not backlog. Flat the
   whole way: bodies 428, catalogue_live 428, store_bytes ~2.55 MB, slices frozen at 14,080
   (dissolved by 3,000 gs), `bytes_per_body` 5,961 B constant.
2. **The flat path** (`out-400-coast-r1..r4.txt`, same args): RSS ~44.4 MB flat; live bytes
   **decline** 24.4 → 14.7 MB and allocs 9.5k → 5.7k after the battle (frees outpace allocs).
   The ~30 MB RSS−live gap is glibc retention — even flat runs never return the battle's mint.
3. **The trigger is the wall path, not the game.** Identical invocations on a quiet machine
   split ~33/67 (5 growing of 15 seed-1 coast flights today); the run-varying quantities are
   the 5-ms budget's bite (presented ticks at nominal gs 1,000 vary 129.6M–143.2M across runs)
   and address-space layout. One binary produced both shapes (self-controlled). Cause not
   isolated [the frame-boundary slicing of fleet work inside `frame_to` is the prime suspect —
   inference]; the bulk drop at 20,000 game-s (one free sweep) is the signature the next run
   should backtrace.
4. **The controls.** Burn arms (seeds 1, 2): flat, 44.4 MB at 8,000/20,000 gs. Seed-2 coast:
   plateaus (44–54 MB across two runs, `out-400-coast-seed2.txt`). Shipped plane (48 members): flat 9.2 MB, five flights, 40,000 game-s.
   Belt plane (3,000 extra, seed 3): flat 17.3 MB over 6,000 gs (fleet alive throughout).
5. **Scale.** The growing path's peak (~221 MB at 428 bodies ≈ 516 B/body transient) is not an
   8 GB ruin at this scene — it is the **multiplier risk**: a 4.7× path-dependent swing in peak
   RSS that no shipped counter explains, so any per-body memory wall measured once (the
   1.2–1.65×10⁶ letter) carries an unknown 1–5× schedule factor until this is pinned or fenced.
   In d3fe's own units, the growing runs' live window ran ~0.3–1.3 kB/member/gs — its band.

## Predictions (predictions.md, written before the decisive flights)

- **P1 (d3fe's rate on main): BIMODAL — both pre-registered sides observed.** The band
  (0.05–0.5 kB/member/gs) holds inside the growing runs' live window (0.3–1.3); the kill side
  (< 0.01) holds in every flat run and at the shipped size. A coin-flip claim was not
  predicted; that omission is this run's lesson, and the frequency (~33%) is now part of the
  claim.
- **P2 (4fa8's unflown arm): REFUTED, clean.** The fleet-slice excess is one-time: events/game-s
  drop 17.6 → ~2 at dissolution and stay flat to 40,000 gs; `slices` freezes (4,110 / 14,080 /
  10,706 across arms). The long-lived-battle case is unreachable by growing the fleet (400
  members dissolve by ~3,000 gs; the belt plane holds one alive to 6,000 with no growth).
- **P3 (saturation): FAILED in the growing runs — the pre-registered "worse class".** The
  verdict rule said: if the slope does not fall after dissolution, "the grower is the session,
  not the battle — reported as such". It did not fall (the slope runs through dissolution at
  the same rate, until the bulk drop at 20,000 gs).
- **P4 (linearity): held to gs 20,000, broken by the drop.** The first-2,000-gs slope predicted
  the 20,000-gs live level within ±20%; the bulk free at 20–25k breaks any linear extrapolation
  — and the pre-registration did not anticipate a drop.
- **P5 (instrument honesty): held.** The leak moves nothing any shipped counter reads; only the
  counting allocator sees it (the census is this run's instrument deliverable).

## What would make it wrong

If the growing path is a debt artefact (the runs that fall behind early are the ones that
grow): against it, the growing 40k run presented full chunks (~200M ticks/1,000 gs) from chunk
2 onward while still growing linearly to 20,000, and flat runs also fell behind early — but the
correlation between early debt and growth was not measured run-pair by run-pair, so a
debt-triggered cache remains possible; if so the claim shrinks to "the debt cache is
counter-invisible and 5× the live store", which still breaks single-run memory measurement. If
a checker's fresh seed-1 coast runs never grow, the frequency (~33%) is the fragile number,
not the phenomenon (the preserved instance stands: 206 MB, one bulk drop, all counters flat).
Cost of adopting: zero code change asked. Fit with PRINCIPLES: "Canonical outcomes are exact
and independent of cache, partition, observation, schedule and hardware" — memory currently
violates the schedule clause; "Errors never compound" — an 11 kB/game-s accumulation held for
20,000 game-s is the compounding class, even though it later frees; the memory floor is
information-theoretic only if what grows is information — 2.6 kB blobs at 4/s are not.

## The lens

Inversion asked how the engine is guaranteed to fail; the answer is not the clean ruin of the
silver (dead at shipped size) but a worse shape: peak memory that flips between 44 and 206 MB
on wall-path luck, invisible to every shipped dial, on the axis the board is about to climb.
What the lens may have missed: the allocation site (time; the next run's job, the bulk drop is
the hook), the frequency estimate rests on 15 flights, and the 48/belt arms' flatness could in
principle be luck — five flat flights each at 6–40k game-s make that unlikely but not
impossible.
