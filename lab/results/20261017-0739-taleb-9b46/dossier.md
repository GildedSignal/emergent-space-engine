# Dossier — 20261017-0739-taleb-9b46 (Taleb lens)

## Claim

The allocator's wave response is Extremistan and it can crash: at one frozen scene and one
N, the seed alone picks the end state (1 region vs 4,715), the latch level (E = 128 / 256 /
512), and the wall (17.9 / 20.4 / 160.5 s — 9× — with the *most fragmented* draw the
slowest), no quantity follows the knob the page attributed it to (N, the latch cap, the
one-region state), and a reachable assert (`alloc.rs:1456`, "rollback … would revise its
published tick") crashes any driver that publishes between advances — which is what calling
the shipped public `run_to` twice does.

## Bottleneck

Board item 4 (smoothness and the allocator, principle 12) via the allocator-ratchet page's
open contradiction ("shipped's own ruin tail … frequency and basin uncharacterised") and its
open direction 6. Expected gain: not throughput — it deletes the page's standing causal
readings (E grows with scene size; the one-region collapse is the cost; the cap buys
nothing but costs 2.3–3.6×), which are single-draw walls on a draw-dominated system, and it
adds one crash path (the assert) that no wall distribution subsumes.

## Evidence

Instrument: `crates/allocator/examples/ruin.rs` (new, public APIs only; prints a per-chunk
trace and the outcome digest). Scene family: 24-cell wave row (spacing 48, cell 0 hot at
vmax 128 quanta = 0.5c, the rest at 1 quantum) + a quiet archipelago grid (spacing 200,
gap 2,600 north — no body can reach it inside the horizon) of 12-body loose-gas cells,
`Law::Relativistic`, `min_region: 1`, margin 0.5, horizon 1,500, one `run_to` per arm.
Patch to shipped code: one line — the latch cap env (`ES_CAP`) on `escalation *= 2`
(`alloc.rs:1410`), default unbounded = shipped. Knobs were tuned **only at N = 864**;
everything below is held-out size or held-out seed. Commands: `regen.sh` (each arm ≤ 60 s
except G at 160 s and the quiet control; walls on the shared box are orders of magnitude).

| Arm (N = 27,936 unless said) | regions end | E | rollbacks | wall | promises exceeded | wasted ops |
|---|---|---|---|---|---|---|
| 14,112 shipped s1 | **1** | 128 | 7 | 11.4 s | 5,770 | 19,270 |
| 14,112 ES_CAP=64 s1 | **1** | 64 | 6 | **6.0 s** | 12,098 | 40,926 |
| 28k shipped s1 | 2,394 | 128 | 7 | 17.9 s | 29,528 | 123,146 |
| 28k shipped s1 (replicate) | 2,421 | 128 | 7 | 29.6 s | 28,946 | 124,934 |
| 28k shipped s7 | **1** | 256 | 8 | 20.4 s | 16,418 | 35,496 |
| 28k shipped s2 | 4,715 | **512** | 9 | **160.5 s** | 47,369 | 206,730 |

1. **The seed is the biggest knob.** Same scene, same N, same law: end regions 1 / 2,394 /
   4,715; E 256 / 128 / 512; wall 20.4 / 17.9 / 160.5 s. The worst draw is 9.0× the best,
   and it is the *most-fragmented* draw (4,715 regions) that is slowest — the cost is the
   conflict churn (47k broken promises, 207k wasted ops, 6,060 merges requested then found
   unnecessary), **not** the one-region collapse, which here finishes in 20.4 s.
2. **E is not a function of N.** 14k s1 → E = 128; 28k s1 → E = 128; 28k s7 → 256; 28k s2
   → 512. The page's "latch level grows with the conflict wave and the scene size"
   (measured 4→32→64–256 at 44→…→14,080) does not survive seed controls: within one scene
   family the level is a draw (its 2⁶–2⁸ "band" is where my draws land too, for none of the
   reasons the page gives). Identical-config replicates spread 1.65× in wall (17.9 vs
   29.6 s) — single-draw walls on this battery, the page's included, are noise.
3. **The latch cap is result-neutral and wall-neutral-in-draw.** At 14k, ES_CAP=64 reaches
   the same one-region end state with the **same digest** (`e538163e…`) and a 1.9×
   *faster* wall (6.0 vs 11.4 s) while paying 2.1× the wasted ops — the exact inversion of
   the page's cap64 verdict (2.3–3.6× wasted ops, DNF-tailed wall). Both verdicts are true
   of their draws, neither is true of the controller: wasted ops do not predict the wall.
4. **A reachable crash.** Chunked `run_to` (publish between advances — exactly the shipped
   `Regions::advance` pattern in `xtask/src/regions.rs:35`, and any replay/checkpoint
   driver) on the 864-body conflict scene panics 2/2 runs at `alloc.rs:1456`
   ("rollback of region … from … would revise its published tick …"), with a second worker
   cascading at `alloc.rs:1776`. At chunk 500 the 14k and 28k scenes survive 1/1 each (the
   collapse finishes inside chunk 1, so no conflict straddles the publication): the crash
   needs a conflict discovered after a publication — reachable, phase-dependent, not
   universal. Digests of the surviving chunked runs equal the single-call digests, so the
   panic guard is the only difference between "advance twice" and "advance once".
5. **The quiet control inverts the page's collapse story.** With the cannon cold (no wave,
   E = 1, 0 rollbacks at every size tried), the 28k scene is the *slowest* configuration
   measured: it did not reach tick 150 in 260 s (< 0.6 chronons/s; trace file
   `out/F-28k-quiet-traced.txt`), against 17.9–160.5 s for the whole wave matrix. The
   many-region regime (2,296 cold cells at `min_region: 1`) is the expensive one — the
   page measured 248–287 chronons/s for it at 1,408 bodies and called the one-region state
   "the faster one"; at 28k it is not a slowdown but a stall. Mechanism unopened (merge/avoid
   churn vs per-unit floor); the conflict wave, the latch and the collapse were never the
   scene's cost floor.


## Predictions

`predictions.md` was written before the matrix. Scorecard, honestly: P1 half-held (E ≥ 8
yes; E growing with N no — refuted by the seed controls), P2's threshold mechanism and
end-state prediction failed (coupling happened at 14k and not at 28k at the same E = 128;
the quiet half failed too: E stayed 1 but the 28k quiet scene stalls, fastest-wall
prediction wrong by >30×), P3 failed (cap64 collapses too, and is *faster* at 14k; the digest
half held), P4 failed at chunk 500 (the assert is phase-dependent, firing at chunk 100 on
the small scene), P5 failed (walls grow ~linearly in N within a seed). The failures are
the result: every quantity I attributed to a knob turned out to be a draw.

## What would make it wrong

- The walls are one box, load ~2, orders of magnitude only; the *ratios* (9× across seeds,
  1.65× across identical replicates, 1.9× cap-vs-shipped) are the claim, not the seconds.
- The crash is a debug-style `assert!` — active in this release profile (it fired). If the
  integrator runs release-with-`debug-assertions`-off only, `assert!` still fires (it is
  not `debug_assert!`); what would make the finding moot is a driver-level rule "one
  `run_to` per process", which nothing documents today.
- My scene family is colder and sparser than the battery's (walls are ~100× faster at
  equal N); the page's DNF-at-300 s draw stays unexplained by this run — I bound the
  *variance* structure, not that specific draw.

## Cost of adoption, and fit

Adoption is mostly deletion of beliefs, plus one guard: (a) retire "E grows with scene
size" and "the cap costs 2.3–3.6×" from the page (both single-draw); (b) any allocator
verdict needs ≥ 3 seeds and identical-config replicates before it is a verdict; (c) the
publish/rollback boundary needs a decision (refuse the advance, or hold publication until
the conflict wave quenchs) before any driver calls `run_to` twice on a conflict scene.
PRINCIPLES: "In Extremistan, inequalities are such that one single observation can
disproportionately impact the aggregate" (Taleb) — the allocator's cost is exactly that;
"Measure before claiming, and never strawman" — the page's controller verdicts were
single-draw; "Errors never compound" — the assert is the certificate policing exactly
that, and it can crash the engine rather than degrade.

## The lens

Taleb-prizing-robustness missed two things: I did not open the 28k-quiet trace's slowness
(>190 s single-chunk for a no-conflict scene — possibly the same churn channel as G, possibly
an unrelated unit-cost floor; one `wc` of attention away), and I did not test frames mode,
where publication is continuous — if the assert can fire there, the crash is in play, not
just in batch drivers. Both are the next run's first experiments.
