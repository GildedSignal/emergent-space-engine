# Dossier — 20261016-0213-dynamics-69f3

- **Claim:** the burn's scan backlog is not a load-sharing queue but a **one-way service latch**: `drain_scans` serves only while `room ≥ 2·scan_ns`, so once one answer costs more than half the frame budget (S > b/2, S ∝ N at ≈ 1.7–3.0 µs/body) the drain freezes permanently — below the latch the seam is free (B = 0, every scan answered in its own frame), above it the backlog is a pure linear birth process at λ = 14.4 holds/s (N- and seed-independent: the player's own binding changes) to memory ruin at 115 B/body per held scan.
- **Bottleneck:** bodies in the flyable engine (the player's seam at belt scale, taleb-51b7's ruin band). What it deletes: any budget-tuning reading of the ruin — the boundary is `S < b/2`, a threshold in N × budget, not a utilization contest; and below the latch the whole seam costs nothing, so the cure is the candidate set (S ∝ candidates), which **reopens** the drain rather than merely speeding it.

## Evidence (lab box, Linux/x86, orders of magnitude)

Scene: `ES_BELT_PLAYER` (player born 2.5 AU circular, root doll — taleb-51b7's scene), rtf 600,
one sustained prograde burn (frames 120–600, level 0), coast 6 s, engine budget b = 5.0 ms,
paced 60 Hz. Instrument: two print-only atomics in `encounter.rs` (`scan_counters`: mints,
answers, answer-ns) + `held_scans()`, per-frame JSONL; patch = the knob, the counters, the probe
(`crates/universe/examples/scanqueue.rs`).

| arm | S per answer | answers in 16 s | held during burn | end held | RSS slope |
|---|---|---|---|---|---|
| N=500, seed 1 | 0.68 ms | 58/58 (all) | **0 always** | 0 | ~0 |
| N=1000, seed 7 | 1.73 ms | 58/58 (all) | **0 always** | 0 | ~0 |
| N=1000, seed 1 (pilot) | 2.97 ms | **1** | 14.5/s, linear | 115 | 2.2 MB/s |
| N=2000, seed 1 | 10.0 ms | **1** | 14.5/s, linear | 115 | 3.3 MB/s |

- **Arrivals:** exactly 58 mints / 115 pushes in every arm's 8-s burn (7.25 new scans/s, one
  duplicate push per mint through the `same_inputs` reuse) — independent of N and seed: arrivals
  are the player's own thrust-kick rebinds. Quiet coast before burn: 0 mints (taleb-51b7's
  cadence-off finding, reproduced at rtf 600).
- **The latch:** in both frozen arms exactly **one** answer ever runs (the first drain
  attempt), then `scan_ns = S ≥ 3–10 ms > b/2 = 2.5 ms` breaks `drain_scans` on every later
  frame, burn and coast alike; `scan_ns` can only decay through cheap answers, which can never
  run again — a one-way latch. N=1000 straddles it across seeds (s = 1.7–3.0 µs/body ⇒
  N_freeze(b=5 ms) ∈ [830, 1470]).
- **Memory:** held scans pin 115 B/body each (26 MB for 115 scans at N=2000), matching taleb-51b7's
  113 B/body at 10⁵ — the per-scan pin is linear in N, so the birth process ruins memory at
  2048-held (SCAN_BACKLOG) or the box fence, whichever first: t_ruin ≈ 2048/14.4 ≈ 142 s at any
  N whose 2048-pin fits RAM (at 10⁴ both land ≈ 2.3 GB within seconds of each other).
- **Commands** (each ≤ 20 s; regen.sh runs all four arms in parallel):
  `cargo build --release -p emergent-universe --example scanqueue && target/release/examples/scanqueue --n 2000 --rtf 600 --burn-s 8 --coast-s 6 --warmup-s 2` (arms: n ∈ {500, 1000×2 seeds, 2000}).

## Predictions (predictions.md, written before these arms)

P1 held (N=500 drains; stronger: B never rises at all). P3 held (linear birth, λ = 14.5/s,
answers ≤ 2, ≈115 B/body; end RSS 53 MB, predicted band 55–75 — just under). P4's band
[830, 1470] confirmed by the seed straddle at N=1000. **P2 failed as stated:** it predicted the
latch at N=1000 on held-out seed 7; seed 7's candidate set is 1.7× cheaper (S = 1.73 ms < 2.5)
and the seam serves freely — the freeze boundary is seed-fuzzy because S is (per-seed candidate
counts), which P4's band already implied but P2 pinned wrongly. P5 held (no fence, no cap in 16 s).

## What would make it wrong

The latch reading rests on `scan_ns` never decaying while frozen (code: `universe.rs:1205`,
decay only via a served answer) and on arrivals being truly exogenous (no answer mints anything —
code-read, not measured). If some idle path answers scans outside `drain_scans` at belt N, the
"pure birth" claim weakens to "birth ≫ death". The M1 numbers (s, and so N_freeze at any budget)
re-measure there; the lab box gives orders only.

## Cost of adopting, fit with PRINCIPLES

Nothing to merge: the finding retargets two standing adoptions — (1) the candidate-set cure
(nladder's open direction 2) gains a precise success criterion: bring S under b/2 **at the
player's own N**, which reopens the drain and makes the seam free (P1's regime), and (2) any
byte/count fence remains a guard, never a cure ("the cap the fence" — confirmed from the queue
side). Fits "Compute only surprises" and "the simulation decides": the seam's cost is decided by
one dimensionless number, S/(b/2), and below it the answer work hides entirely in idle frames.
Fixes/tunes nothing in the law; the probe and counters are print-only, digest-neutral by
construction (atomics no law reads).

## The lens (dynamics and attractors)

The queue looked like Kingman near saturation; it is instead a relay (hysteresis) with two point
attractors — B = 0 (serving) and linear growth (frozen) — separated by a latch in S, with the
birth rate exogenous. The lens missed the memory side at first: P3's RSS band assumed B·115 B·N
only; the measured reuse (one duplicate push per mint) halves the arrival cost of *new* state
but doubles queue traffic — harmless here, but a reuse-heavy workload (stationary player) would
fill SCAN_BACKLOG with duplicate Arcs, changing which cap bites first. Unmeasured.
