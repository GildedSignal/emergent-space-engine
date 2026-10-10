# Dossier — run 20261010-2141-system-eea5 (lens: the whole system)

## Claim

In the plane, **every kick pays exactly one full trajectory compile, and that one
rebind-per-kick is a single mechanism wearing three hats — the per-kick cost and
its p99 tail, the per-body memory ceiling, and the encounters re-pay trigger —
so the design's already-adopted jet (offset-from-entry + multiply-add updates,
re-anchored) is one lever against three board bottlenecks, but its measured
ceiling is ~1.6× on the median kick (up to ~10× on the tail), not the 5–10×
everywhere one might hope.**

## Bottleneck

Board focus #1 (kicks dominate engine cost) × focus #5 / the H_live risk
(distinctions per game-second decide whether 10⁹ fit in 8 GB) × the top scaling
risk (#6, candidate re-pay). Expected gain if the jet is wired: O(10×) on the
kick p99 tail and the collapse of the private-trajectory-per-body memory cost;
what it deletes: the fresh compile per kick (~37% of median kick time, 91% of
the p99 tail) and the 75× gap between the law's 16-byte tube and the measured
1203 bytes per live body.

## Evidence (Linux x86 cloud box, shared, 8 vCPU; orders of magnitude only)

Commands (each ≤ 60 s; the instrumentation patch is this run's `patch.diff`):
```
cargo build --release -p xtask                       # ~35 s
$CARGO_TARGET_DIR/release/xtask universe --kick-bench --seconds 55   # 0.12 s wall
$CARGO_TARGET_DIR/release/xtask universe --bench --seconds 10 --unpaced  # 0.39 s wall
```
Raw JSON: `kickbench-55s.json`, `kickbench-10s.json`, `bench-10s.json` in this
folder. The instrumentation: a `(ns, count)` accumulator around
`Rebinding::from_state` (`crates/universe/src/bind.rs`), read as a delta around
each distinct kick's resolver call in `xtask/src/universe/kick_bench.rs`.

1. **Compiles per distinct kick = 1.0** (37/37 samples, `compiles_per_kick`),
   and the memo **never** shares: `exact_hit_rate = 0.0` (31 distinct exact
   shapes; quantized 12+12-bit key shares only 16%, and reusing it is the
   killed law change). Code path: `step.rs` `kick → rebind → bind →
   Rebinding::from_state` (step.rs:28, 381; bind.rs:226) — there is no other
   kick path. P1 confirmed.
2. **Compile share of kick resolver time: median 0.37 (stable: 0.359, 0.372,
   0.365 across three runs), p99 0.91.** Kick cost itself: median 42–69 µs,
   p99 439 µs (the tail is compile-dominated: deep-encounter kicks compile
   `Passage` trajectories, flat 4096 B each in `bytes_of`). P2's ≥ 50% median
   **failed**; the readout (a Newton solve on the old entry), forces,
   sigma-delta and the new binding's remainder decode+turn are ~63% at the
   median. So the jet's honest ceiling: ~1.6× median, ~10× p99.
3. **Memory: bytes_per_body = 1203 against the law's 16-byte tube (75×)**;
   `catalogue_live = 28 = bodies`: one private compiled trajectory per body,
   zero sharing ever (item 1). The trajectory is the bulk of the 1203
   (`body.rs:170–176`: `BodyRec + plan + trajectory knots + history`). At 10⁹
   bodies this is ~1.2 TB: the 8 GB requirement is decided by this gap, not by
   the tube. Live memory stayed bounded during the run (slots recycle via the
   free list; `prune` trims history) — the churn is CPU, the loss is the
   compression ceiling. P4's bounded half held.
4. **The surprise (P3 badly missed, and it matters): in the flying plane today
   the view dominates and kicks are rare.** `--bench` over 10 game-seconds:
   `stats.kicks = 0` (ships' kick cadence is longer than the horizon), engine
   share 3.8% of frame time, view gather 73%, view JSON 17%. The kick lever is
   a *scale* lever (belts, fleets, B10/B18 scenes), not the current slice's
   bottleneck — the slice's bottleneck is the gather.

## Predictions (`predictions.md`, written before the run)

- P1 hit exactly (1.0 compiles/kick; 0.0 exact sharing).
- P2 missed at the median (0.37 vs ≥ 0.5), held in spirit at p99 (0.91 vs
  60–90% guessed).
- P3 badly missed: ship items are not ≥ 80% of resolved items — in 10
  game-seconds there were *zero* resolved kicks; the fleet slice (10 µs) and
  the view dominate the slice instead.
- P4 half-held: memory bounded (no growth), but the measured ceiling loss
  (1203 B/body, 0 sharing) is the concrete H_live face.

## The simplification (the lens's deliverable)

**What it unifies:** three bottlenecks are one number, the rebind-per-kick:
(i) kick cost/tail (compile = 37% median, 91% p99 of the resolver);
(ii) memory (the unshared ~1.2 KB private trajectory per body is why
bytes/body is 75× the tube — kicks mint a fresh distinguishing key per body
per cadence, so no population program can ever hit, and B18's scar layer
grows at one trajectory per kick); (iii) encounters (every rebind is an
element change that re-sets candidate pairs — the 92% window-setup share of
gold components-4643 is the same re-pay).

**What it deletes:** the fresh compile per kick. The jet already adopted in
law.md ("strong-field reuse is the jet, re-anchored… about 0.05 compiles per
kick") stores the *deviation from the shared generator* (the body's own
entry) and re-anchors when the offset reaches √(floor/C). That is the same
mechanism as shipmem's scars (program + sparse deviations) — two mechanisms
that are secretly one: **deviation-from-generator storage**; today the tube
side has no scar layer at all, so every deviation buys a whole new generator.

**Cheapest experiment that shows the behaviours stay:** wire the jet for one
doll's ships (integer offset + the memo's ∂/∂E, ∂/∂L multiply-add, re-anchor
at the red-team's floor), re-run `--kick-bench` (expect compile share
→ ~0.05 compiles/kick, kick p99 −~80%) and judge with B5's error-type gate
(exponent ≤ 0.2) plus B12's Jacobi on handoffs. Budget: one directed build.

**Blind spot (named, as the lens demands):** deep encounters. The jet's
C·drift² offset grows fastest exactly where the p99 tail lives (SyMBA shells,
`Passage` trajectories); if re-anchoring approaches one compile per kick
there, the win shrinks to zero precisely at the tail — the 730-kick figure
was measured in one regime, not in the shells. Handoffs and thrust flushes
must still rebind exactly (a frame change is not an offset), and every
between-kick reader must apply the offset or the digest drifts.

## What would make it wrong

A kick path that skips `Rebinding::from_state` (none exists in the code
today), or a wiring of the jet that fails B5/B12 — then the 37%/91% shares
stand as the ceiling of a dead lever and the kick cost moves to readout and
forces (themselves candidates for the same treatment: the readout's Newton
solve is a per-observation root-find that the shared cycle table could serve).

## Cost of adoption, and fit with PRINCIPLES

Cost: one build item (the jet in `crates/universe`'s bind/step, plus the
readout offset in `observe`), no gate changes; judged by existing B5/B12.
Fit: principle 3, "Compute only surprises… Nothing is evolved that can be
derived when looked at" — the post-kick trajectory is *derived* from the
pre-kick one plus an integer offset; principle 6, "Store the generator, not
the generated" — the offset is the compressed generator of the new orbit;
principle 1, less is more; principle 13, errors never compound (the
re-anchor bounds the jet's error below the floor instead of letting it walk).

## The lens (what this lens may have made me miss)

A system view couples everything and can over-rate any single lever: my P2
and P3 guesses were both wrong because I stared at the kick path and not at
the plane's actual frame budget — the gather is 73% of today's slice. The
coupling claim (three bottlenecks, one number) survives, but the *ranking*
of the jet belongs to the integrator's board, next to the already-queued
gather/readout work. I did not measure the encounters re-pay on the plane
itself (no `crates/encounters` wiring in the slice); that third hat is cited
from components-4643, not re-measured here.
