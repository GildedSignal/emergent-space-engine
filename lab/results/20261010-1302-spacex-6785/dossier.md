# Dossier — 20261010-1302-spacex-6785 (SpaceX lens)

**Claim.** The per-event position-cache refresh (`root_state_raw` in `Universe::apply`) is
20% of a ship's item cost and pure scheduling state — deleting it (refresh once per
`advance` per *resolved* body, a dirty set) keeps every digest bit-identical and cuts the
ship class's measured cost 31–37% (31.9 → 20.2–22.0 µs per item); the naive once-per-advance
placement is KILLED (it wrecks the frame tail), and the worst remaining idiot index in a
kick is the rebind (`Rebinding::from_state`, 12.3 µs of ~35), not the kick count.

## Bottleneck

Board focus #1 ("kicks dominate the engine's cost") and #4 (smoothness). Six runs already
killed kick-count reducers (correctors, splits, averaging). This run attacked the other
lever the board names — *cheaper events* — with the lens's idiot index: measured cost ÷
physical floor, per piece of one kick. Gain: ~1.5× on the ship path at zero behaviour
change; deletes a per-event cost the engine has no reason to pay (PRINCIPLES #14, "no work
for no reason"; the cache's own doc: "for deadlines only; never an outcome").

## Evidence (Linux/x86 runner, shared, orders of magnitude only)

The kick, decomposed (`cost_split`, `cost`, unpatched): pure resolve 35 µs =
rebind `from_state` 12.3 + `root_state` cache 6.9 + own readout 3.4 + secondaries 3.3 +
tide 3.3 + `compile` 3.4 + glue. So ~20% of every kick was bookkeeping for a cache that
never affects outcomes, and ~35% is a cartesian→elements round trip whose floor is an
integer Δ(E,L) patch (idiot index ≥ 100×).

The patch (universe.rs: apply marks resolved bodies; rekey refreshes only those, once per
`advance`; ~14 lines changed in one file, plus bench `crates/universe/examples/idiot.rs`):

|---|---|---|
| digest B (seed 7, Sparse, 200, held out) | 2138e8c5… | **identical** |
| digest C (600 frames, rtf 100) | 169e1aa3… | **identical** |
| digest `tail` (rtf 100, budget-of-one ordering) | e8d0d065… | **identical** |
| ship class, µs/item (`cost_ns[2]/items[2]`, in-process) | 31.9 | **20.2–20.4** |
| settle A / B, µs/item (wall) | 78.5 / 140.7 | 71.5–79.2 / 128–148 (noisy box) |
| `cost_split` whole-universe, µs/item | 49.7 | 43.0–43.2 |
| `tail` worst items (>1 ms) / frames >5 ms | 4 / 2 | 2–3 / 2 |
| frame p99 / max, 200 members rtf 100 | 6.5 / 17.7 ms | 6.0–6.9 / 17.0–19.0 ms (noise) |
| `cargo test --release -p emergent-universe` | green | **green (54 passed, incl. budget granularity)** |
Reproduce (each ≤ 60 s where possible; final run in `final.txt`):
```
cargo build --release -p emergent-universe --example cost_split --example tail --example cost --example idiot
/home/glmlab/lab-target-1/release/examples/idiot        # digests A/B/C, ~16 s
/home/glmlab/lab-target-1/release/examples/tail 10 100 1 48
```
Baselines in `baseline.txt`; patched runs in `patched.txt`, `patched-dirty.txt`.
(`git stash` the universe.rs patch to rebuild the baseline binary.)

## Predictions (`predictions.md`)

P1 digest invariance: **held**, all four digests, both placements — the falsifier never
fired. P2 saving 10–15%: **held on the ship class** (31–37%), whole-universe unresolvable
for noise. P3 frame tail unchanged: **held within noise**; the worst item is the fleet open
(31 opens in one frame, 12.9 ms) — present before and after, the next tail target. P4
`from_state` stays the worst ratio: **held** (12.3 µs vs a floor of an integer element
patch). Miss: I predicted the naive placement would pass P3; it did not — that is the
killed configuration above.

## What would make it wrong

A scenario where deadline ordering genuinely changes outcomes (schedule dependence) would
flip a digest; four cuts across two orderings and three scenarios say otherwise, but the
player's own light cone at extreme rtf is untested here. Also: this box is shared — the M1
re-measure may move the absolute µs (the integrator re-measures; the digest claims are
exact and portable).

## Cost of adoption, fit

~14 lines in one file, one field, no API change; the full `emergent-universe` suite is
green on the patched tree (54 passed, including budget granularity and
digest-across-orderings). Fits PRINCIPLES #1 ("the cheapest compute is compute not
done"), #14 ("no work for no reason"), #28 (the cache is an instrument, not an outcome).
Process note: an intermediate edit accidentally dropped `apply`'s `resolved += 1`; every
digest stayed identical while the budget-granularity test caught it in 2 s — outcomes are
schedule-independent, but bounded-work-per-frame is a contract digests cannot see.
Next lever this run names: the rebind (`from_state`, 12.3 µs, ~35% of a kick) — a Δ(E,L)
integer patch instead of the cartesian round trip; that is motion-law territory (higher
tier), so this run only measures it.

## The lens (what it may have missed)

The idiot index treats "floor = what physics needs" as obvious; for the rebind the floor is
a *law* question (what the canonical tube update may skip), not a benchmark. A systems
lens might also ask who *consumes* deadlines at all if the allocator changes shape — if the
slack skin (queued build) reworks scheduling, this cache could be deletable outright, which
would be the better delete.
