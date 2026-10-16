# Dossier — 20261016-0504-system-e070 (lens: the whole system)

## Claim

On shipped main the pre-wave frame storm is the **belt's** first-kick wave, not the locals'
storm 917c attributed it to: the 300 ladder locals contribute 3% of the worst frame (50 of
922 events at 1e4; 50 of 8,482 at 1e5 — N-flat), while carrying **72% of the whole event
stream** (55,985 → 15,785 kicks when deleted; 4.5e-3 kicks/s per local = 82× the belt's
5.4e-5) — so the frame lever is the (unmerged) belt stagger, and the locals' lever is the
cadence law, not a spread: a locals' first-plan stagger is flown here digest-changing and
moves the frame peak by exactly 0.

## Bottleneck

`nladder`, the furthest-gap row (bodies 10⁶→10⁹): the frame's binding N-term and the event
stream's hot population are two different populations, and the page's next-lever reading
(917c: "the locals class is the next frame term... one law, one lever") conflates them.
This run separates them with the isolation control 917c never flew. No 10× is claimed; a
wrong next rung is deleted, which is the cheaper half.

## Evidence (all numbers from this box, Linux/x86, shared, orders of magnitude only)

Instrument (env-gated, off = bit-identical, verified): per-frame engine event counts
(`frame_events`), a tick-level trace of every resolved item (`ES_TRACE`), a queue/waiting
census (`ES_CENSUS_EVERY`), an engine-only frame arm (`ES_ENGINE_ONLY`), a no-locals scene
arm (`ES_NO_LOCALS`), and a locals' first-plan stagger (`ES_STAGGER_LOCALS=<bits>`,
per-id offset over 2^bits root ticks; the same law shape as ed3a's belt stagger, applied
to ships of secondary dolls). Flights: `xtask universe --bench --unpaced --engine-ms
100000 --rtf 1000 --seconds 30 --extra N` (30,000 game-s, coast, budget-free).

| arm | worst-frame events (bucket) | of which doll 0 / doll 2 | `frame_events` max / p99 | kicks total |
|---|---|---|---|---|
| 1e4 storm, seed 1 | 922 @ f849 | 872 / 50 | 479 / 332 | 55,985 |
| 1e4 no-locals, seed 1 | 894 @ f849 | 890 / 4 | 447 / 242 | 15,785 |
| 1e4 stagger-locals, seed 1 | — | — | 479 / 327 | 55,969 |
| 1e4 storm, seed 7 | — | — | 671 / 459 | 53,833 |
| 1e4 stagger-locals, seed 7 | — | — | 671 / 459 | 53,820 |
| 1e5 storm, seed 1 | 8,482 @ f849 | 8,432 / 50 | 4,241 / 2,404 | 145,985 |
| 1e5 stagger-locals, seed 1 | — | — | 4,241 / 2,404 | 145,969 |

- The storm's clock: the worst bucket's heaviest single tick is 2,873,098,240 = 14,177
  game-s = **exactly half of cf45's 2.814e4 s belt interval** — the belt bodies' clocks
  fire their first kicks together at Δs/2. Linear in N: 922 → 8,482 bucket events,
  479 → 4,241 max (8.9–9.2× for 10×). Fine structure: 437 distinct ticks inside one
  16.7-game-s bucket (the sub-grid beat 7da3 saw at 660-s spacing lives inside it).
- The locals' worst-bucket contribution is 50 events at 1e4 AND 50 at 1e5 (N-flat, as
  their count is fixed at `min(extra/2, 300)`), 3–6% of the storm. Their p99 contribution
  is larger (332 → 242, −27%) because their steady cadence (short orbits) fills ordinary
  frames, not the peak.
- The locals' event rate: (55,985 − 15,785)/300 locals = 134 kicks/local per 30,000 game-s
  = 4.5e-3/local/game-s, against the belt's 15,785/9,712 = 5.4e-5/body/game-s (matches
  a9d7's 3.55e-5 and cf45's doll-clock law). **82× per body.**
- The stagger arm: identical max/p99 at both N and both seeds (479, 671, 4,241), kicks
  55,969 vs 55,985 — the offset re-times ~16 locals' kicks near the cut and nothing else.
  Digests differ from the storm arm (a schedule change, as designed); re-runs reproduce.
- Off-arm identity: pristine main vs this patch with every env unset, `--rtf 100
  --seconds 20 --seed 1`: **digest 5b2d998b… both, byte-equal** (`pristine_digest.txt`,
  `patched_off_digest.txt`). An earlier build of this patch dropped `resolved += 1` and
  the queue's construction in `start()`; the off-arm digest check caught it (zero events,
  empty queue — the anomaly that first looked like an engine finding was my bug), both
  lines restored, control re-flown.

Commands: `regen.sh` (≤ 6 min on 8 vCPU; every number above regenerates).

## Predictions

`predictions.md` was written before the fixed binary flew. Outcome: **1, 2, 3 all failed
in the same direction** — I predicted the storm was the locals' birth synchrony (≥80% of
the peak); it is the belt's wave (94–97%), the no-locals peak stayed at 447 (predicted
≤ 80), and the stagger moved the peak by 0 (predicted ≤ 120). Held: the off-arm identity
(5), and the locals' N-flatness (4) — 50 events at both N. The falsifier did its job: the
page's uncontrolled attribution (917c's "the locals are the storm") fails its isolation
control on main; what stands is their direction-1 *class* claim, relocated from the frame
term to the event-rate term.

## What would make it wrong

- My no-locals arm changes the belt too (it moves all 300 locals' bodies into the belt):
  the belt grows 300/9,700 ≈ 3%. The storm's composition is read directly from the trace
  (doll 0 vs 2), so the attribution does not rest on that arm alone.
- On 917c's branch (ed3a's belt stagger in force) the residue they measured at 334 may
  genuinely be the locals; my claim is about **main**, where the wave dominates. The two
  readings compose: wave (main's term, belt, linear in N) > locals' residue (post-stagger
  term, N-flat at ~50 per worst frame here).
- A served session (view + a live player whose reads pull ships) resolves reads the bench
  loop does not; event totals there can only grow, and the locals' share of the stream
  with them.

## Cost of adopting, fit with PRINCIPLES

Adoption is negative-space: do not build a locals stagger (this run flew it; it buys 0 at
the frame); the frame lever stays ed3a's belt stagger, and the locals enter the ledger as
the hot event-rate population (cadence/cf45's dial). PRINCIPLES: "Measure before claiming,
and never strawman" — the control was missing; "a failed expectation is not automatically
a failed method: diagnose which one broke" — the method (isolation control) is what
worked. Cost: none beyond this instrument (default-off, digest-verified).

## The lens

The whole-system lens hunted "one law, one lever" and found the opposite worth keeping:
the frame's peak and the CPU's event stream are two different populations wearing one
name ("the locals class"); a lever aimed at the wrong one costs a rung. Missed by this
lens: I spent the first half of the window building the stagger before flying the
control that would have aimed it — the falsifier should have flown first.
