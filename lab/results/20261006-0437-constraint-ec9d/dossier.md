# Dossier — 20261006-0437-constraint-ec9d (lens: the constraint)

## Claim

The plane's kick-cost tail is not the rebind in general: it is `Passage::compile`, which fires
on fleet handouts (leavers) at **318–567 µs per compile, ~70× a cycle compile (4.5–6.8 µs)**,
and is 91–96% of a leaver's kick; the fix shape is a bounded (lazy) passage compile, which
changes *when* the work happens, not *what* is computed — so it cannot change outcomes.

## Bottleneck

Board focus line 1 / HANDOFF bottleneck 3 ("a kick costs 29 µs, 15 in rebinding fit and
compile"; Sol's interrupted `wt/kick` job). Measured on this Linux runner (orders of magnitude
only; the M1 re-measures): made-body kick ≈ 44 µs, leaver kick ≈ 365 µs median, p99 441 µs.
Kicks are the engine's dominant recurring cost (board), and the smoothness goal is p99, not
the mean (PRINCIPLES #12). Expected gain: the kick p99 drops ~10× (441 → ~50 µs) with the
*same bits*; at scale, every handout (fleet dissolution, battle members leaving) stops paying
a full-tube compile it may never read. What it deletes: the eager far-tail of every passage
compiled at a handout (panels below the join x = 2⁻¹⁰ out to 2× the doll edge), most of which
are discarded unread at the next kick — the exact-memo hit rate on distinct kicks is 0
(re-measured here), so every rebind recompiles and every eagerly-compiled panel is a gamble.

## Evidence

All commands ≤ 60 s; machine state recorded in the JSONs (Linux x86 runner, load ≈ 1).

1. Baseline on clean main (before my edits): `cargo run --release -q -p xtask -- universe
   --kick-bench --seconds 20` → `kick_us` median 43.9 µs (23 samples), `kick_us_leavers`
   median 365.4 µs, p99 440.7 (9 samples), `exact_hit_rate` 0.0, digest
   `2fd6e1ce…` (`kickbench-main.json`).
2. Instrumented build (patch: `instrumentation.patch`, applied with `git apply`): per-phase
   timers inside `step::kick` (readout / secondaries / tide / acceleration / rebind) and
   inside `Rebinding::from_state` (fit_key bisect / compile / at_radius / decode).
   `universe --kick-bench --seconds 20` → digest **identical to main** (`2fd6e1ce…`):
   - made: rebind 25–36 µs of ~44 (75%); inside it: compile 4.5, fit_key 4.0, decode 3.5,
     at_radius 1.1 µs.
   - leavers: rebind 350–360 µs of ~365 (**96%**); inside it: **compile 318.4 µs (91%)**,
     decode 8.1, fit_key 5.0, at_radius 2.8 µs. Force gathering is *not* the tail:
     secondaries 3.7–3.9 + tide 3.6 + acceleration 1.2 µs — less than a made body's
     (13.9 + 0.15 + 2.2), because the child doll has fewer sources (`kickbench-phases.json`,
     `kickbench-fitphases.json`).
3. Held-out seed 7: the one leaver kick's compile is 566.7 µs; made compiles 6.8 µs
   (`kickbench-fitphases-seed7.json`).
4. Population check by arithmetic, not inference: the made population's compile **total**
   across 23 kicks is 123–195 µs, so not even one ≥300 µs passage compile can sit there;
   the 6 passage rebinds (32 kicks − 26 cycles, memo field) are all leaver kicks.
5. Whole-plane context (`bench-main.json`, 30 s paced): frame p50 2.5 ms / p99 4.1 ms; engine
   5.6% of the frame, view gather 61% + JSON 25% (the known Sonnet job); the engine's own
   cost centre per kind: fleet 1811 items at 46.6 µs, player 3 at 1373 µs.
   Gates on main: B12 FAIL (exponent 1.604 vs 0.2), B13 60/64 — the known motion-law-v2
   front, untouched here (`behave-plane.json`).

Where the money goes inside `Passage::compile` (reading the code, `crates/space/src/orbit.rs`
`impl Passage`): the tail loop shrinks x = R/r by 15/16 per panel down to
endpoint = periapsis/outer_radius, each panel a quadrature (`tail_quad`). A leaver handed
into the doll has a small periapsis against a 2×-doll-edge outer radius, so the panel count
grows logarithmically in edge/periapsis — geometry, not iteration pathology. `fit_key`'s
bisection is flat and cheap (4–7 µs) for both populations.

## Predictions

`predictions.md` was written before the instrumented runs. What happened:

- P1 (made: rebind > 50%): **held** (75%; compile is the largest sub-phase).
- P2 (leavers: rebind ≥ 60%, force gathering not the cause): **held** (96%; secondaries+tide+acc
  ≈ 8.6 µs). My stated *mechanism* (Newton iterations in the fit) was **wrong** at the level
  below: fit_key is 5 µs flat; the cost is the passage **compile** (91%). The phase-level
  prediction held, the sub-mechanism did not — reported as held-with-correction.
- P3 (unaccounted remainder < 10%): **held** (≈ 0).
- P4 (consequence: fit-geometry problem ⇒ bounded-iteration fit): **half wrong** — the right
  exploit is a bounded *compile*, not a bounded fit.
- Kill criterion (rebind < 30% of leaver kick → constraint elsewhere): not triggered.

## What would make it wrong

- If handouts were rare at scale, a 0.5–1 ms compile per leaver would be amortised away. The
  plane disagrees (9 of 32 distinct kicks in 20 s are leavers; every fleet dissolution hands
  out its whole membership), and the board's scaling plan (encounters, belts) multiplies
  handouts. A universe where handouts are ~0 would demote this to a non-constraint.
- If leaver passages usually *are* read out to the far tail before their next kick, lazy
  compile only defers the same work. Measurement to falsify: count tail panels read between
  a handout rebind and the body's next rebind (the readout radii vs the join).
- 9 samples at seed 1 and 1 at seed 7 is a small tail population; the mechanism (panel count
  ∝ log(edge/periapsis)) is structural, but the median could move with the fleet's radius.

## Cost of adopting, and fit with PRINCIPLES

Adoption is one change in `Passage::compile`'s caller path (universe `bind`): bound the
compile at the radius reachable before the body's next certified event, extend on rebind.
Because every kick rebinds from scratch anyway (exact hit rate 0), the extension points are
already there. It touches `crates/space` (a `Passage::compile_bounded`) and `crates/universe`
(pass the bound), and must show an identical digest on the plane bench and the kick bench to
prove "the budget changes *when* work is done, never *what*" (plane.md, foundation 7).
- "Compute only surprises… Nothing is evolved that can be derived when looked at" (#3): the
  far tail of a passage is derived look-at work paid before anyone looks.
- "No work for no reason" (#14): panels compiled for a tube the next kick discards.
- "minimize spike compute and average compute usage" (#12): the 318–567 µs spike is exactly
  the p99 the smoothness gate cares about.

## The lens

The constraint lens measured the whole and followed the one number that dominates the tail;
what it may have missed: (a) correctness fronts (B12/B13) outrank cost for the goal right
now — a cheaper wrong law is not progress (this run deliberately touched no law); (b) the
view gather (61% of the frame) is the player-facing constraint at the plane's current size,
already Sonnet's; my result only orders the *engine's* internal costs; (c) I did not build
the bounded compile — the 10× is measured on the cost side, the digest-identical proof is
the missing experiment (silver, one experiment from gold, next run picks it up).

## Files

`bench-main.json`, `kickbench-main.json` (clean main); `kickbench-phases.json`,
`kickbench-fitphases.json` (seed 1), `kickbench-fitphases-seed7.json` (held-out seed);
`behave-plane.json`; `instrumentation.patch` (the timers; apply on main to reproduce 2–4);
`predictions.md`.
