# Dossier — run 20261020-1621-system-7fd3 (lens: the whole system)

## Claim

The plane's two worst scoreboard gaps are indeed one object — every kick's `rebind` mints a
compiled trajectory — but the census kills both proposed deletions and moves the lever: the
minted knot table is a **~20-reader cache with a 100%-hit history (1.05 retired reads per
mint)**, so the store earns its bytes, while the kick's real core is **the fit around the
compile (74% of the rebind; the compile itself is 26%)**, which no run had named.

## Bottleneck

Board: "the kick: 75-160 µs against a ~50 ns floor" and "memory at 10⁹ (~2,460-5,100 B
against ~6 B)". HANDOFF joins them by object ("most of it the body's own compiled orbit"),
and the wiki's deletion candidates target the store (225d consequence 3: "the kick mint is
the memory ratchet's outright deletion target"). This run measures the store's consumers
directly. Expected gain if the store were deletable: ~10² in memory; measured instead: the
deletion is dead, and the unnamed 74% (the fit: `fit_key`, the witness inversions,
`at_radius`, residual, word choice) is the next 10× on the kick.

## Evidence (print-only census, `ES_MINT_CENSUS=1`; counters are relaxed atomics beside the
same paths; shipped digest path untouched; both arms ≤ 28 s wall)

Scenes: the standing belt flights `nladder 10000 coast 60 1800` and
`nladder 30000 coast 60 1800` (60 s wall, rtf 1800, ≈ 108k game-s ≈ 3.7 doll intervals;
9edc/3570's scene family at a shorter wall).

| quantity | N = 10⁴ | N = 3×10⁴ |
|---|---|---|
| mints (compiles, whole run incl. births) | 203,485 | 247,760 |
| fired kicks (ucensus) | 164,677 | 150,974 |
| rebinds (all mints incl. boundary/exit) | 203,276 | 247,551 |
| kick µs per fired kick | 41.2 | 44.0 |
| rebind share of kick time | 0.859 | 1.116* |
| **compile share of rebind time** | **0.265** | **0.259** |
| compile µs per mint | 7.6 | 7.8 |
| **external reads per mint** (`state` walks + `at_radius`) | **19.96** | **19.53** |
| mint's own reads per mint | 1.01 | 1.01 |
| **history reads per mint (retired segment answered)** | **1.051** | **0.664** |
| history hit rate | 213,940/213,940 | 164,410/164,410 |
| dashboard bytes/body (end) | 1,436 | 1,399 |
| end footprint MB | 61 | 159 |

\* rebind/kick > 1 at 3×10⁴ because 38%/23% of rebinds live outside kick items
(boundary-exit and hand-off rebinds, births), whose walls sit in other items; the per-rebind
cost agrees across N (28.7 vs 30.0 µs).

Reproduce: `bash lab/results/20261020-1621-system-7fd3/regen.sh` (~4 min: build + 2 flights
+ `compose.py`, which reprints the table). Raw logs: `out/arm-*.log`.

## Predictions (predictions.md, written before the runs)

- P1 (compile ≥ 50% of rebind): **KILLED** — 26%. The second half (rebind ≥ 50% of kick)
  held (86% at 10⁴).
- P2 (reads per mint ∈ [1, 4]): **KILLED at the kill criterion** — 19.96 and 19.53, ≥ 10:
  the store is a genuine shared cache, not a one-reader cache.
- P3 (history hits < 0.05 per mint): **KILLED at the kill criterion** — 1.05 and 0.66 per
  mint, hit rate 100%: retained history is load-bearing on the coasting belt's flyable path.
- P4 (mint's own reads 2-5): measured 1.01 — the instrument counts only the residual decode
  (the fit's `at_radius` inversion on cycles is below the counted dispatch; noted, not a
  physics claim).
- P5 (mints ≈ kicks + births within 20%): held with the excess named — 203,485 vs
  164,677 + 10,028 births = +16.4%, the boundary-exit and hand-off rebinds.

## What would make it wrong

The census counts dispatch-level calls (`Trajectory::state`, `Passage::at_radius`,
`binding_at` below `event_time`); a reader that walks a knot table by another entry point
would be missed (none found: universe reads route through `decode`/`orbit_state`; `Plunge`
state reads are uncounted but plunges are absent on this scene). The wall split has
`Instant` overhead (~50 ns on 28-44 µs paths, < 0.2%). The scenes are coasting; a burn arm
adds readouts (ff42's crash search) and would raise reads/mint further — against the
deletion, not for it. Cloud timings are Linux/x86: orders of magnitude only.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in code: the instrument is print-only and the two deletions it tested are
dead. What the integrator should take is the redirection: principle 3 ("compute only
surprises") does not license deleting the mint — the mint is read ~20× and its history
1× — and principle 18 ("the right question, then the representation") now points at the
fit: a cheaper exact fit (or a fit that reuses the previous binding's key when the state is
within its basin, an exactness question like the jet's) attacks 74% of the rebind where the
compile attacks 26%. The jet's retirement (law.md) already killed the cheap-update path for
the cycle; the fit is the un-tried half of the same bill.

## The lens (what it may have made me miss)

A unification lens wants one object to delete; the census says the object is load-bearing,
and the honest deliverable is the negative with the redirect. The blind spot I name: the
20 readers are counted, not attributed — the next run should split them by call site
(boundary predicates, view gather, `state_of` secondaries, planning) before any reader is
itself deleted; and the history reads' owner (likely `secondaries(d, t)` reading a body
bound later than t) is an inference, not measured. Extreme scenes (a fleet in one doll,
where efd4 measured 99.6% key sharing at birth) could change reads/mint by orders of
magnitude.
