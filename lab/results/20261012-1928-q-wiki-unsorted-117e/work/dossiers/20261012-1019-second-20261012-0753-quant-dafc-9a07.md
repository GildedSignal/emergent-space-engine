# Dossier — 20261012-1019-second-20261012-0753-quant-dafc-9a07 (second author, quant lens)

**Claim.** The checker's falsification of run 20261012-0753-quant-dafc's claim 5 (the canonical
digest flips run-to-run, `6ce6…` ↔ `56f4…`, "engine-side") does not reproduce: across 70+ runs
that deterministically sweep **every** mechanism by which the schedule can reach the engine —
per-frame game-time target (`--dt-ms` 16.7→100 ms), budget bite (`--engine-events` 1→64,
wall 5/10/15 ms), pacing on/off, box load 0.8→7.5, one contended core, threads 1→8, and
history pruning disabled — the digest at the fixed cut (406050894) is **one value per seed**
(3 seeds × 3 schedules each), the per-body canonical state is bit-identical across schedules
(field-group dump), and the checker's named suspect, `frame_to`'s wall-derived `want`, is
exonerated by construction; `56f4…` is not the digest of any neighbouring cell either
(level 1–3, members 47/49/50), so it remains unreproduced and without a mechanism in the
shipped code — while the checker's *other* finding (the smoothness frontier is
machine-state-dependent) is confirmed and now holds on 3 seeds.

## Bottleneck

The integrator's named prerequisite (check.md: "after the integrator bisects the digest flip
… capacity claims on a plane whose canonical digest is unstable at a fixed cut are built on
sand"). Gain: removes an alleged PRINCIPLES-#1 engine bug from the record or localises it;
either way the plane's digest control is either restored or precisely wounded.

## Evidence

Machine: this GitHub Actions runner (Linux/x86, 8 vCPU), load recorded per run (uptime in
every JSON; 0.8→7.5 during the hunts). Tree a838a284 = the run branch's parent = the checker's
clean tree: same shipped semantics for every cell. All data in `data/`, summary via the prior
run's `summ.py`.

**The probe patch (disclosed; env/flag-gated, digest bytes unchanged).** `ES_DIGEST_PARTS=1`
prints per-body physics/bookkeeping/global sub-hashes at the cut; `--dt-ms F` fixes the
unpaced frame's `wall_dt`; `--engine-events N` replaces the wall budget with an item-count
budget (deterministic deferral); `ES_NO_PRUNE=1` disables history pruning. With the flags
off, the digest path is byte-identical to shipped (all flip-hunt cells ran flags-off; the
`dt=16.6667` control reproduces the shipped unpaced digest `6ce6…`).

1. **The flip does not reproduce.** Author: 4 runs `6ce6…`. Me: 11 paced (load 0.8–7.5),
   8 paced under 6 CPU spinners, 4 paced pinned to one core shared with a spinner, 3 unpaced,
   9 dt-swept, 14 event-budget-swept, 3 threads-swept (2/4/8), 1 pruned-off, 1 prune control —
   **all `6ce6…`**. The checker's `56f4…` (3 of their 9 runs, including one unpaced) never
   appears. Neighbouring cells have distinct digests (level 1/2/3 → `5079…`/`67c7…`/`663a…`;
   members 47/49/50 → `83fa…`/`0af6…`/`a93d…`), so `56f4…` is not a mislabelled cell.
2. **Every schedule mechanism is exonerated deterministically.** The wall enters the engine
   in exactly two places (`want = rtf·wall_dt/TICK_SECONDS` in `frame_to`; `Budget::wall`'s
   `Instant`): sweeping `--dt-ms` over 16.7→100 ms (per-frame target 338k→2.03M ticks) and
   `--engine-events` over 1→64 (deferral from "1 item per frame" to unlimited) leaves the
   digest at `6ce6…` in every combination. Threads 1→8 (the `resolve_wave` path) and pruning
   entirely off: same digest. Equal-deadline requeue order, the one mechanism deferral could
   perturb, is exercised by the event-budget sweep and moves nothing.
3. **The canonical state is bit-identical across schedules, per body.** `ES_DIGEST_PARTS=1`
   on paced/unpaced/loaded runs: all 77 lines identical except the un-hashed `resolved`
   work-counter (6746 vs 6756 — same state, 10 items moved from the frames into the final
   settle). The digest hashes no schedule-dependent field: per-body `events` counters sit in
   the unchanged bookkeeping group.
4. **Schedule invariance holds on 3 seeds** (the checker's "≥3 seeds"): seeds 1/2/3 ×
   {paced at load ~4, unpaced, unpaced + ev4 + dt33} → one digest per seed
   (`6ce6…`/`c979…`/`1e05…`), cut and inputs identical within seed.
5. **The frontier is machine-state-dependent — the checker's smoothness reruns confirmed,
   on 3 seeds.** Paced b5 rtf100 at load ~4: 0 hitches >16.7 ms (seeds 1/2/3, worst
   6.5/6.8/7.0 ms), low1 = 100, 3–4 overflow frames, gather share 0.63–0.65 — matching the
   checker's load-1.4–3.0 reruns, not the author's load-0.3 dips (low1 9.9, 38 overflow,
   gather 3.62 ms). The prior dossier's "5 ms is 2× too small" and "dip floor ~10×" are
   machine-state artefacts, as the checker held; the readout-ownership (gather 0.61–0.69 of
   frame time) and the budget's soft edge reproduce on every seed and load state.

Reproduce (each ≤ 45 s, from this folder):
`/home/glmlab/lab-target-0/release/xtask universe --bench --rtf 100 --seconds 20 [--unpaced
--dt-ms F | --engine-events N | --seed S | --threads T]` then `python3 summ.py <json>`;
`ES_DIGEST_PARTS=1 … 2> parts.txt` for the field-group dump; `ES_NO_PRUNE=1` for the prune
probe. (The binary is the probe patch; flags-off cells match shipped digests.)

## Predictions (predictions.md, written before any of my runs)

- **P1 wrong-side:** unpaced was predicted one-digest — true, but so is everything else; the
  interesting prediction space (jitter-driven flips) turned out empty, which P2 caught:
  **P2 wrong** — 11+12 paced runs incl. load 7.5 and a contended core, all one digest.
- **P3 wrong:** the flip does not localise to a field group because it never occurs; the
  field-group dump instead proves bit-identity across schedules (the H-bookkeeping/H-physics
  dichotomy was built for a flip that is not there to classify).
- **P4 vacuous-true:** with nothing to exclude, one digest per seed across all schedules.
- **P5 untested as stated** (needed a physics flip; none exists).
- **P6 right in substance, wrong in mechanism:** seed changes the digest value, never its
  schedule-invariance.
- **Kill criterion averted:** P1 held, so no widening to threads/maps was forced — though I
  swept threads and prune anyway (both innocent).

## What would make it wrong

`56f4…` was real in the checker's session (3 of 9 runs, one unpaced — I take their report as
ground truth and cannot explain it). If it ever reproduces, run that session with
`ES_DIGEST_PARTS=1`: one line will move, naming the field group and body, and the bisect
finishes in one step. What my sweep cannot exclude: a cause outside the shipped code's
schedule paths (their runner's build state, a stale binary, or a cell misread) — the lab's
own 5 October lesson cuts both ways: 3 agreeing runs from one checker session share that
harness. My box is not theirs; the M1 remeasure remains the integrator's.

## Cost of adoption, and fit

Nothing to adopt in the engine: the digest control stands as shipped, and
`digest_note`/H0213's claim survives its strongest attack *on every axis measurable here*.
Adopt the caveat both checkers now agree on: the smoothness frontier (knee, dips, hitches)
is a function of machine state, not of (rtf, members, budget) alone — the M1 remeasure is
the real frontier. The probe patch is not for merging; `ES_DIGEST_PARTS` is worth keeping
in mind as a one-step bisect tool if the flip ever shows again. Fits PRINCIPLES #2 ("exact
means deterministic and reproducible") and #10 ("measure before claiming"); the falsified
falsification is itself a result ("a failed expectation is not automatically a failed
method", H0183).

## The lens

The second-author lens inherits the quant lens's hunger for a mechanism and nearly
manufactured one: with 70+ runs and no flip, the honest output is an exoneration table, not
a bisect. The trap I had pre-registered (H-bookkeeping at 0.65) shows the prediction
market can be confidently pointed at a phenomenon that is not there — the cheap falsifying
test (the dt sweep, 50 s) should have come before the loaded flip-hunt (3 min). What the
quant lens did right: refusing to accept "two attractors" without a mechanism, and pricing
each axis (dt, deferral, threads, prune) as a separate, deterministically falsifiable bet.
