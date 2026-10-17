# Dossier — the boundary event priced in information: 99.88% of belt boundaries carry no news

Run id: 20261017-2038-components-3570 (lens: first principles, one component at a time).
Machine: the lab's Linux box, 8 vCPU, load shared with the window's other runs.

## Claim

On the shipped belt, **99.88% of boundary events reproduce the previous interval and step
exactly, fire no certificate, and carry zero bits of news** — the boundary comb is a
per-body no-op machine that costs p50 25.2 µs / mean 32.3 µs per event (28% of the
kick+boundary resolver CPU on this run), and its entire decision content is derivable once
at the kick from the binding the kick just compiled.

## Bottleneck

Board focus "the kick / belt CPU at 10⁹": kick-cadence's two-comb law made the boundary
comb an irreducible-looking term (+25–26% belt CPU, 2 events/body/interval). This run asks
the lens question instead: what is the boundary's information floor? The answer deletes
~28% of belt resolver events and CPU at 10⁹ (9.96 → ~7.2 M1 cores in kick-cadence's own
ledger arithmetic) and halves the belt's event stream (delivery, queue, scan pressure).

## The component, its requirement, its floor

- **Requirement** (PRINCIPLES #3: "Compute only surprises … Nothing is evolved that can be
  derived when looked at"; #1 less is more). The boundary (`What::Boundary`, step.rs:805)
  = readout + two point certificates (surface, doll edge / leave) + `plan_interval`
  (re-derive the step and insert the next kick+boundary).
- **Floor**: the certificates are a function of r over the interval, and r ∈ [periapsis,
  apoapsis] of the cycle the kick just bound (the binding's `OrbitKey`; the readout itself
  is `radius × unit scale`, binding.rs `cartesian`). The plan repeats on the aligned grid
  (`step.rs:107`); the anchor tick is known when planned. So a steady body's boundary has
  **0 bits of output**; the informative case is one exact key-range test at kick time —
  a handful of integer compares, ~ns, amortized over a 28,141-game-s interval.
- **Idiot index**: 25 µs measured against ~2–3 ns of decidable content ⇒ **~10⁴ per
  event**; in aggregate 0.12% of events carry all the news while costing 100% of the comb.

## Evidence (all numbers from `regen.sh`, ≤ 8 min)

Flight: shipped `nladder 10000 coast 150 1800` (kick-cadence's own scale and arm class;
10,028 bodies, ~270,000 game-s ≈ 9.6 belt intervals, 336,767 probed events; probe =
`BOUND_PROBE=1`, print-only, one stderr line per kick/boundary, state deltas + wall ns;
digests not applicable — the probe writes no game state).

| Quantity | Value |
|---|---|
| boundaries / kicks | 167,609 / 169,158 (parity 0.991 — the two combs) |
| **boundary no-op fraction** (iv==iv0 and st==st0, alive) | **0.9988** |
| news-carrying boundaries (plan or step changed, or died) | 196 / 167,609 = 0.117% (15 of the 196 also moved the step; 0 deaths) |
| boundary wall | p50 25.2 µs, p99 35.4 µs, mean 32.3 µs |
| kick wall (same run) | p50 50.4 µs, mean 83.1 µs (ratio 2.0×) |
| resolver CPU spent on no-op boundaries | **27.8%** of kick+boundary resolver time |
| trajectories at boundary | 99.66% Cycle, 0.34% Passage |
| doll edge margin me ≤ −4 (r under 1/16 of edge) | 96.9% |
| surface margin ms ≤ 1 (r under 2× surface, doll units) | **41.3%** — not margin-safe |

Cross-check: the 27.8% CPU share agrees with kick-cadence's independent "+25–26% belt CPU"
comb-mass estimate (their µs/event read 12.6–13.2 µs on their load; mine reads higher on a
shared box — same order, load-normalized conclusion identical).

## Predictions (predictions.md, written before the decisive run)

- **P1 (≥95% no-op): HELD, 99.88%.**
- **P2 margins: split** — edge half HELD (96.9% ≤ −4); surface half **FAILED**: 41.3% of
  boundaries sit at r < 2× surface in doll units, so a margin-based certificate would
  misfire; the design's key-range test must be exact, not margin-based. Reported as failed.
- **P3 (kick/boundary cost ratio 2–8×): HELD, 2.0×.**
- **P4 (event parity ±20%): HELD, 0.991.**
- **P5 (≥90% non-clock): HELD by doll** — 82% doll 2, 0.7% doll 3, 17% doll 0 (root locals,
  the clock path `boundary_clock`, which only re-anchors: an even weaker no-op class).

## The design within 10× of the floor (priced, not built)

At the kick, the resolver already holds the fresh binding: evaluate the interval's
certificates exactly from the key's [r_min, r_max] (Cycle: periapsis..apoapsis = periapsis/k;
Passage: the arc's radial extent) against (surface, edge) in the doll's units, plus the
hysteresis test `want ∈ (cur/2, 2·cur)` on the key's own step scale. Clean ⇒ do not schedule
the boundary; schedule the next kick directly (the anchor tick is already known). Inconclusive
or crossing ⇒ schedule it as today. Belt events fall 2 → 1 per body per interval; the 0.12%
news class is exactly the class that still fires. Cost at the kick: a few integer compares
(~ns), inside the 50 µs kick — < 10⁻⁴ of it. Legality: this deletes events, so it is a law
change — the digest changes, the B-gates and the comb freeze (kick-cadence's recurrence
gate) must re-freeze; the surface point-check vs range-check difference can only catch
*more* (a dip between ticks now provable), never fewer, certificate violations. The exact
key-range conversion (doll unit scale) is the one code-level fact to pin at adoption.

## What would make it wrong

- If the 0.12% news class is not predictable from the key (e.g. interval changes driven by
  `next_exit` caps that the key cannot see), those boundaries must still fire — the census
  does not decompose the 196; the design fires on any inconclusive test, so it stays safe,
  but its savings shrink if the inconclusive class is wide (the ms ≤ 1 population says the
  surface test will be inconclusive for ~40% of bodies — their boundaries still fire unless
  the range test is done exactly; the exact test is the design's load-bearing part).
- The clock path (root locals, 17% of boundaries here) only re-anchors and does not replan;
  deleting it touches the map's read tick — a separate, smaller question.
- Cloud timings, shared box: orders of magnitude only; the integrator re-measures on the M1.

## Fit with PRINCIPLES

- #3 "Compute only surprises … nothing is evolved that can be derived when looked at": the
  boundary is evolved (167,609 times) to derive what the kick already held — measured, not
  argued.
- #1 "The cheapest compute is compute not done": the deletion is the deliverable.
- #2 "It's a game … behaviours matter": judged by the plan/state stream (behaviour), not
  trajectories; the no-op test is bit-exact equality of the plan it re-derives.

## The lens's blind spot

A local optimum can move cost to a neighbour: deleting boundaries moves their certificate
work into kicks (priced, ~ns) and their anchor bookkeeping into the plan (free). Not
measured here: the delivery/scheduler side (what the allocator pays to carry half the
events) and the flight-level digest change. The census is one scene class (the phase-locked
belt at genesis; stirred/driven belts per the memory-h-live scenes may carry more news at
boundaries — the 0.12% class is where churn would show up first).

## Reproduce

`bash lab/results/20261017-2038-components-3570/regen.sh` (applies work/patch.diff, builds,
flies `10000 coast 150 1800` with `BOUND_PROBE=1`, prints the census JSON; author's census
in work/census.json, raw probed stream in work/run10k.err.gz).
