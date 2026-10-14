# Dossier — 20261014-1719-dynamics-bf21

**Claim.** The belt's first-kick wave is a **standing train**, and the named hold-the-scan fix is
real but must be read precisely: capping the player's look-ahead pull (`ES_PULL_CAP`, 9 lines,
env-gated) turns the 1.36 s monster frames into 11.97 ms budget-saturated frames — **114× on the
worst frame, zero frames over budget, digest bit-identical, encounters and kicks exactly equal** —
while holding the *whole* scan (capture at answer time, the literal reading) breaks the certificate
(4,060 → 4,029 encounters, digest differs): the capture must stay at the player's item, where the
bindings at its tick are already final; only the answer is holdable, which the `Held` design already does.

**Bottleneck.** The board's first gap (bodies: 28 → 10⁶): the wave is what breaks the flyable frame
between ~3×10⁵ (the M1 record) and 10⁶. This deletes the unbudgeted burst itself (taleb-6138's
direction 0, priced), not its symptoms.

## Evidence (all from `regen.sh`, shipped code + `work/patch.diff`, Linux shared box)

1. **The wave is a train, not a shock** (`wave_train`, belt of 99,700 at N=10⁵, seed 1):
   first items all `Kick(0)`, min 13,051 / p50 14,072 / max 14,542 game-s (taleb's profile, exactly);
   after a settle past it, next items min 26,101 / p50 28,145 / max 29,084 — **the cohort recurs one
   step later with the same shape** (the per-body step ≈ 26,100–29,100 game-s ≈ P/2⁷; the spread is
   the step census, a continuum, not one power of two). Width grows only 1.1 k → 3.0 k game-s per
   pass: no phase mixing to uniform. A 20 s rung at rtf ≤ 100 sees **no** belt item at all; every
   wave needs ~27.5 k game-s (≈ 4.6 min at rtf 100) — the rung window question generalises to *every*
   wave, not just the first.
2. **Baseline reproduced** (`wave_flight` 2×10⁵ burn, 160 s, rtf 100, 12 ms budget, env unset):
   max frame **1,364.9 ms**, 12 frames over budget, worst item 25,547 events, monsters spaced exactly
   50 frames (the player's item cadence), worst lag 1.45 s — taleb-6138's basin (1,213/1,244 ms) on
   the same scene, schedule noise aside.
3. **The fix, measured** (same flight, `ES_PULL_CAP=64`): max frame **11.97 ms**, **0** frames over,
   events/frame max 333 (the budgeted drain), worst lag 1.45 s (unchanged: the drain's coast-shaped
   lag), scans held max 212, `digest=ba1a66b4c5e78fb5d…` — **bit-identical to the baseline's**;
   encounters 4,060 = 4,060, kicks 225,975 = 225,975.
4. **The wrong variant, measured** (first build: `Req` entries captured at answer time): max frame
   11.98 ms but encounters 4,029 ≠ 4,060 and digest `5a17ba1d…` ≠ baseline — the late capture reads
   pruned history (the drain's ~1.45 s game lag meets the prune's 2×light-distance retention).
   Pre-registered as the kill mode in `predictions.md`.

**The change** (`work/patch.diff`, `crates/universe/src/universe.rs`): `pull_ships_capped` — the
player's look-ahead pull (resolve every ship below the player's *next* item, inside its current item,
outside the budget) stops after `pull_cap()` ships; the rest is left to the queue the frame already
budgets for. Default `usize::MAX` = shipped behaviour bit for bit; `ES_PULL_CAP` is the lab's dial.
Nothing else changes: the scan still captures at the player's item (every item before its tick is
resolved by key order — the pull-ahead was eagerness, not correctness), and its answer was already
idle-time work (`Held`, `drain_scans`).

## Predictions (`predictions.md`, written before the flights)

- Held: (2) the train recurs at the step with the cohort's shape — second items 26.1–29.1 k game-s,
  no dispersion to uniform; (4) baseline monsters ~10²–10³ ms spaced ~50 frames carrying ~10⁴ events;
  (5) capped worst frame ≤ ~20 ms with the wave absorbed as lag (11.97 ms, lag 1.45 s unchanged);
  (7) settle cheap (0.2 s).
- Failed, and the failures are the result: (1) the steps are **not** one power of two — the census
  is a continuum (the pow2 reading of `step_for`'s rounding was wrong at this precision); (6) the
  first deferral variant was **not** digest-neutral (see 4 above) — the honest certificate needed the
  capture kept in place, which is the dossier's correction to taleb-6138's wording ("hold the scan":
  hold the *answer*, never the capture).

## What would make it wrong

- The capped pull leaves the scan's candidates stale wherever a ship's state at the scan's tick can
  change *without* an item before that tick (a handout, a capture): none exists in the motion law v2
  (a root ship never leaves the root), but a future wiring that changes bindings without an item
  below the player's key would need the gate variant — which is exactly what the digest says is
  unsafe today (pruning).
- The lag, not the frame, becomes the binding constraint at 10⁶: the wave's mean arrival
  (N/width ≈ 182/game-s per 2×10⁵) against the drain (~141/game-s per 12 ms frame at 60 fps) — at 10⁶
  the wave would cost ~34 s of lag per pass on this box. The frame holds; real time does not. The
  generation-side lever (stagger the belt's birth grid over one step: flattens 1.1 k → 27.5 k game-s
  of arrival width, ~24× on the drain'sutilisation) is measured here only as the step census — the
  stagger itself is unmeasured (a wiring decision in `shipmem`, effb's direction 9).
- One seed, one box, one scene class (the ladder belt, planar, prograde); the locals' dolls and the
  cast arm are untouched. The M1's absolute frame times will differ (taleb's 45 vs 315 ms at 10⁵);
  the certificate (digest equality, over-budget count) is schedule-free.

## Cost of adopting, fit

Nine lines in `universe.rs` behind a constant (the env gate comes out; `64` → any small bound — the
pull's steady-state load at 2×10⁵ is ~600 ships per item *when the queue is caught up*, and those
still resolve inside the item: the cap only bites when the queue is behind, which is the wave). Fit:
PRINCIPLES #12 ("the algorithm that allocates the work … the most important one") — the burst was
work placed outside the allocator; #14 no work for no reason (the pull-ahead bought nothing the queue
does not buy); #13 errors never compound (digest-identical, so the fix adds no drift); #34 the
oracle guards (the digest was the guard here, and it killed the first variant).

**The lens.** Dynamics saw a queueing system (arrival wave train vs drain, Kingman-shaped lag at
ρ→1) and nearly stopped at "hold the scan"; the lens's blind spot — transients vs attractors — is
what the train measurement adds: the wave is neither a one-shot transient nor an attractor, but a
standing train born of the synchronized birth cohort, and its width is a generation choice. What the
lens may have missed: the view's gather during the deferred-answer window (unmeasured), and whether
the player *sees* the 1.45 s lag (playability, not measured here).
