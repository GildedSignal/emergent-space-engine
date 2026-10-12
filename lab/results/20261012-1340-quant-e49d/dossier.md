# Run 20261012-1340-quant-e49d (quant lens): the wake of one kick in the encounter tier

## Claim

One kick's re-certification wake in the Binet-cone tier is O(candidate degree) = O(N) single-thread
work (6.8 ms at N=10⁴, slope 1.00–1.07; a full 16.7 ms frame at N≈2.4×10⁴), and the queued slack
skin cannot absorb player burns (skippable 94.6% at δa/a=1e-9 but 0.25% at 1e-3, where the slack
rule is also unsound: 5 skipped pairs changed outcome) — but 98% of the wake (the window setups)
has deadlines ≥ tens of orbits away (no candidate pair's first post-kick conjunction inside 10
orbits; 99.95% of setups find no encounter within 10 orbits), so deadline-ordered scheduling turns
the burst into a stream; only the cone re-scan (1.3–2.1% of the wake) must land in the kick's
frame.

## Bottleneck

The top scaling risk (board, 5 October): candidate work must track real encounters, and
`components-4643` left "the slack skin (12.6×)" as the lever, queued as build `b-encounter-skin`.
The unmeasured half was the player wildcard (principle 5): a burn is not a thermal kick. This run
sizes the wake in seconds, splits it by urgency, and finds the skin's regime boundary. It deletes
the premise that the skin alone is the lever for kick cost; what it does not delete is the skin
for thermal kicks. Fits PRINCIPLES: "The player is the only wildcard, and their influence travels
at c" (5) and "the algorithm that allocates the work to prevent those heavy tails, it's the most
important one" (12, OC#36).

## Evidence

Machine: shared GitHub Actions runner, 8 vCPU (Xeon E5-2676/x86-64 class per /proc), 15 GB, load
1-min 1.4–4.6 during the runs; Linux/x86, so orders of magnitude only (the integrator re-measures
on the M1). Belt: the crate's own `kick` spec (N bodies, σ_e=1e-2, ρ=1e-4, a∈[1,1.5], seed
20261050), kicks at t=10 orbits, horizon 1000 orbits, 24 kicked bodies (quant lens tails) for
`burn`, the crate's 100 for `kick`.

Commands (each ≤ 12 s, from this folder; code in `work/encounters`, a copy of `crates/encounters`
with one added experiment, binary `encounters-burn`):

```
cd work/encounters && CARGO_TARGET_DIR=./target cargo build --release
./target/release/encounters-burn kick  > ../../run-kick-baseline.txt   # the crate's own, N=1e4
./target/release/encounters-burn burn  > ../../run-burn.txt            # N sweep + eps sweep
```

Raw JSON: `run-burn.txt`, `run-kick-baseline.txt`. Numbers:

- **Wake ∝ N** (`burn`, p50 µs per kick, eps=1e-3): 570 @ 3e3, 6,556 @ 1e4, 19,632 @ 3e4;
  fitted slope 1.05 (pairs slope 0.98: 89 → 256 → 844 → 2,535 per kick). Per pair 8.4–9.6 µs.
  The crate's independent 100-kick mean agrees (7,470 µs, 813 pairs).
- **Capacity:** a 3.3 ms frame share is crossed at N≈5×10³, a full 16.7 ms frame at N≈2.4×10⁴ —
  five orders of magnitude below 10⁹. Burn magnitude barely matters (eps 1e-5→1e-2 all ≈8 ms per
  10⁴; a 10% orbit change costs *less*: 611 pairs, the body leaves part of the belt's U-range).
- **Tail across kicked bodies:** p99/p50 ≤ 2.9, max/p50 ≤ 1.9 at N≥3e3. No unlucky-body spike;
  every kick is uniformly frame-scale once N≈2×10⁴.
- **Skin regime boundary** (`kick`, N=1e4): slack-skippable 0.946 @ eps 1e-9, 0.575 @ 1e-7,
  0.030 @ 1e-5, 0.0025 @ 1e-3 — with **5 slack_skip_violations** at 1e-3 (skipped pairs whose hit
  set changed). A 0.35 g × 10 s burn is δa/a ≈ 2×10⁻³; the plane's throttle reaches 11,561 g
  (δa/a > 1). The slack budget models a pure window drift, so at burn eps it is both useless
  (0.25%) and unsound (violations > 0).
- **Urgency split** (`burn`): cone re-scan (phase A) = 1.3–2.1% of the wake (0.4–1.2 ms p99 at
  3e4). Phase B (setups, 98%+): hit within 10 orbits for 0.03–0.14% of pairs, within 100 orbits
  for ~0.5%; first post-kick conjunction (the sound, cheap deadline 1/|Δn|) inside 10 orbits for
  ~0% of pairs, inside 100 orbits for ~48%. A 3e4-body wake (20 ms) spread over its deadlines is
  ≈50 setups/orbit ≈ 0.5 ms/orbit of schedulable stream, not a frame spike.
- `changed_frac` ≈ 0.08 for all eps ≤ 1e-2 is tolerance-dominated (hit-time drift > 1e-3 over a
  1000-orbit horizon), not physics; at eps=1e-1 the metric degenerates (old hit-partners leave the
  candidate set) — reported as a metric caveat, not a result.

## Predictions

`predictions.md` was written before both runs. Held: wake exponent ~1 (0.98–1.07 vs predicted
0.95–1.1); capacity (3.3 ms between 10³ and 10⁴; full frame below 3×10⁴ — measured 5×10³ and
2.4×10⁴); tail p99/p50 ≤ 2 (max 2.9 at the smallest N, 1.4–1.9 elsewhere); urgency (scan < 5%,
≥80% no hit within 10 orbits — measured 99.95%); skin < 0.1 skippable at eps ≥ 1e-2 (measured
0.0025 already at 1e-3). Miss: "≥ 0.8 skippable at eps ≤ 1e-7" — at 1e-7 it is 0.575; the budget
distribution's p10 (4.7e-8) sits above 1.5×rel_dt only up to eps ≈ 3e-8. The kill criterion
("skippable < 0.2 at eps ≥ 1e-3 ⇒ the skin alone cannot absorb player burns") fired: 0.0025.

## What would make it wrong

The deadline-stream conclusion rests on the synodic bound being the true due time; if encounters
could occur before the first post-kick conjunction (they cannot in Kepler: coincidence requires a
conjunction), or if the engine must present encounter *possibilities* (not events) within a frame
of the burn, the stream becomes urgent again. Timings are one shared x86 box under load; the M1
re-measures. If `b-encounter-skin` builds an exact (margin-based, not drift-budget) skin, its
skippable fraction at burn eps could exceed my numbers — my claim is about the *rule as coded in
the crate* (1.5×rel_dt drift budget), which is what the queue would have copied.

## Cost of adoption, and fit

Nothing to build in the engine: two scheduling rules for the motion-law/events design. (1) The
skin is for thermal kicks only; player burns bypass it by construction (a burn is known to exceed
any thermal skin, so do not even test). (2) A kick's wake is charged to the allocator as: eager
cone re-scan (bounded, ~2% of the wake; at 10⁶ bodies even this is ~20–40 ms — the remaining
linear wall, to be killed by the envelope tier `b-coorbital-cert`, not by scheduling), plus
deadline-sorted setups keyed by first synodic conjunction (a float bound, one divide per pair).
Delete: any plan to re-certify eagerly on kick. PRINCIPLES: "Priority is slack, not proximity"
(5); "the simulation tells us what's next not us" (22) — the deadlines are the simulation's own
conjunction times.

## The lens (what it may have missed)

I measured one belt, one ρ, uniform a; a fleet or co-orbital clump (the 6 October gold) changes
the degree constant, not the mechanism, but the deadline distribution there (Δn ≈ 0 ⇒ T_syn → ∞)
deserves its own check. The two harnesses (crate `kick` and my `burn`) share the crate's sections
and events code, so agreement is not independence; the N-slope and per-pair µs are the robust
facts, absolute µs less so. A quant lens prices the burst but does not price exactness: the 5
violations matter more than any millisecond here.
