# Dossier — run 20261010-0541-system-d51f (lens: the whole system)

## Claim

The plane's cost atom is the tube readout up the doll chain (~6.4–7.2 µs per level), paid
independently by every light-arrival mechanism; the view gather costs 13× the whole engine advance
at rtf 100, the scheduler burns ~46% of the engine's median frame re-deriving positions per event
for deadlines, and the two mechanisms already compute the same quantity (arrival time and its rate
1+n·β) twice — a naive news gravity would pay it a third time, per source per kick, at ~100–170 µs
per kick.

## Bottleneck

Board #1 (kicks dominate) seen whole-system: not the kicks' arithmetic but the *retarded readout*
they and everything else share. Expected gain of one shared arrival structure (per-doll readout
service + incremental deadlines via the arrival rate the view already computes): deletes the
scheduler's per-event walk today (26.7 µs of a 57 µs median engine frame) and caps news gravity's
per-kick read cost at one walk per (source, kick epoch) instead of one per source per kicked body.

## Evidence (Linux x86, shared runner, 8 vCPU, load 1.1, orders of magnitude only)

`cargo test --release -p emergent-universe --test lab_arrival -- --nocapture` (≤ 5 s; 3 repeats stable):

- plane(seed 7, rtf 100, 300 frames, 2827 events): **gather median 775 µs/frame, engine median
  57 µs/frame** — the gather is 13× the engine. 36 594 chain levels / 300 frames = 122/frame ⇒
  **~6.4 µs per level readout** (gather path).
- `Universe::apply`'s per-event `root_state_raw` for the deadline: 1 123 calls, **7.13–7.17 µs per
  call**, 3.74 calls/frame = **26.7 µs/frame ≈ 46% of the median engine frame** (two independent
  paths land on the same ~6.4–7.2 µs/readout: the measurement is internally consistent).
- Per-frame (body, tick) memo of `ramped` readouts: **bit-identical views every frame and identical
  universe digest** (asserted in the test), but hit share only **2.9%**, gather gain ~1% (noise).
  Reason: each emitter is read at its own retarded tick, so doll-centre readouts are *not* shared
  within a frame — my prediction of 25–60% sharing was wrong.
- Control (stream scene, 64 emitters, root doll, depth 1): **0 hits** — the memo measurement is not
  an artifact.

Derived (arithmetic from the measured readout cost, not run): news gravity as specified in law.md
("evaluated from the source's tube as the body's past light cone last saw it"), naive — 2–3 Newton
reads × depth-2 walk × ~4 sources = 16–24 levels = **~100–170 µs per kick**, i.e. 2–3× today's
entire engine frame added to every kick.

## Predictions

`predictions.md`, written before the run. Held: bit identity (3), control ≈ 0% (2), scheduler tax
exists (5 — but 46% of the engine frame, above my 1–15% of the kick path). Falsified and reported:
within-frame doll-chain redundancy 25–60% (measured 2.9% — retarded ticks differ per emitter), and
the 10–40% gather drop (measured ~1%). The news-gravity multiplier (6) is arithmetic, labelled so.

## What would make it wrong

If the readout cost is an artifact of this scene's depth or of `cartesian`'s Newton panel solve
being unwarmed, the absolute µs shrink at other scenes; the *structure* claim (three mechanisms,
one quantity, built twice, about to be built a third time) would still need the arrival-rate reuse
measured before adoption. If `apply`'s position update is already amortized away in the M1 numbers
(H0210's 29 µs kick), my 46% share of the *frame* overstates its share of *kicks*.

## Cost of adoption, fit with PRINCIPLES

One structure: the per-doll retarded readout service plus the arrival rate 1+n·β carried per pair
(the view's `ViewCache.inst` already computes and stores exactly this rate every frame; the
scheduler's deadline needs only `deadline' = deadline + Δt·(1+n·β)`). Cost: one owner unifies
`Universe::apply`'s walk, `view::crossing` and the news-gravity design before it is built —
cheapest now, while news gravity is still a branch. Fit: "Compute only surprises" (3 — a body whose
state has not changed is re-read at full cost today), "the best part is no part" (17), "a component
that exists only to repair another" is deleted (the lens): the deadline walk repairs the queue's
lack of the arrival rate.

## The lens (what it may have made me miss)

The whole-system lens hunted a shared *structure* and found a shared *quantity*; the hard special
case is a doll whose centre is relativistic (β→1): the arrival rate approaches 0 or 2, incremental
deadlines degrade, and the composition of arrival maps across dolls is no longer near-linear —
exactly the regime of the "root-clock event keys" open problem (HANDOFF risks). Also missed by
construction: whether the gather's 61 reads/frame itself should exist (the view caps at one sample
per pixel; 775 µs/frame for ~60 emitters is a per-emitter gather that pixel capping would delete
first — that may be the bigger deletion, and it is already in representation.md §2).

## Artifacts

- `crates/universe/src/observe.rs` (lab module: counters, opt-in memo; `state_rate` now reads
  through it), `crates/universe/src/universe.rs` (`apply` charges the scheduler tax),
  `crates/universe/tests/lab_arrival.rs` (the flight, the asserts, the control).
- Machine state: Linux 6.8.0, 8 vCPU, load 1.08/1.16/0.86, 13 GB available.
