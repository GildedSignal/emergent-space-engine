topic: nladder
status: open
closed-by:
valid-while:
updated: 20261014-1859-spacex-cb7b

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The wave's height is a generation accident, deleted by staggering the birth grid (20261014-1859-spacex-cb7b).**
Spreading each clock ship's first kick over one step (a uniform draw at birth, ships only, `ES_STAGGER`,
~10 lines in `plan_clock`, no engine term) flattens the wave's arrival width **20.2×** (1,491 → 30,109
game-s = one step, bf21's unmeasured "~24×" lever now measured) and on clean main at 10⁵ burn deletes
the monster frames outright: events/frame max 6,712 → **338 (19.9×, the census ratio)**, wave-region
over-budget frames 5 → **0**, worst frame 338.1 → 34.4 ms, with refusals 0, dead 0 and every non-belt
counter identical (boundaries 32,368=32,368, handoffs 1=1, lost 25=25, opens 433=433, catalogue
100,076=100,076); the 300 locals identical to the tick. The over-budget frames that remain (31) are all
the second seam (1-9 events, frames 11,094+), the same residual 4487's engine-side fix leaves — the two
halves (engine-side pull-hold, generation-side stagger) are complements: the cap holds the frame, the
stagger keeps the drain's load shape current (bf21's ~34 s/pass at 10⁶). One-shot physics cost: a first
interval up to ~2 steps with the kick's weight still Δs — jacobi worst |ΔJ|·r 2.7e-5 at step 7 and
2.3e-4 at step 5, inside the cadence's own class (ad35's 0.5·n^-2.1) but up to 45× the control's
per-ship worst on encounter-diverged ships; if the ratio binds, scale the first Δs with the delay
(named, unbuilt). Domain: 10⁵ burn, seed 1, one Linux box, 21 k game-s of the 30 k spread flown (the
second wave unflown; the census plus the clock's per-body next-half planning — no shared grid — is the
evidence arrivals stay spread); a player inside the belt band during a wave still untested; B13/B14 not
run on a staggered build.

**The wave's fix is measured and certified, and the wave is a standing train (20261014-1719-dynamics-bf21).**
Capping the player's look-ahead pull (`pull_ships_capped`, 9 lines, `ES_PULL_CAP`-gated; the pull resolves every
ship below the player's *next* item inside its current one, outside the budget — the burst 6138 named) holds the
same 2×10⁵ burn flight at **max 11.97 ms, 0 frames over 12 ms** against the baseline's **1,364.9 ms / 12 over**
(114×; monsters 25,547 events, spaced exactly 50 frames, reproduced from 6138's basin), with the digest
**bit-identical**, encounters 4,060 = 4,060 and kicks 225,975 = 225,975; the wave's cost becomes the drain's
1.45 s lag, unchanged from the coast control. The certificate *kills the literal fix*: deferring the capture to
answer time (the "hold the scan" reading) breaks it — 4,029 encounters, digest differs (the late capture meets
pruned history: the drain's ~1.45 s game lag against the prune's 2×light-distance retention) — so the capture
stays at the player's item (every item before its tick is resolved by key order; the pull-ahead was eagerness),
and only the answer is held, which `Held` already did. The wave itself is **not a one-shot shock**: every belt
body's step is ≈ 26.1–29.1 k game-s (a continuum, not one power of two), and the cohort recurs with its shape
(second items 26,101–29,084, width 1.1 k → 3.0 k game-s: no phase mixing), so a rung must fly past *every* wave
(~27.5 k game-s apart, ≈ 4.6 min at rtf 100), not just the first; the arrival width is a generation choice
(stagger the birth grid over one step → ~24× flatter drain utilisation), unmeasured here *[measured now: cb7b
above]*. Domain: seed 1, the ladder belt, Linux shared box, 2×10⁵ burn only; the view's gather during the
deferred window unmeasured.
   *[Checker bf21: reproduced three ways — clean tree, patched-unset and capped are one digest
(`ba1a66b4…`), so the patch is default-neutral and the cap changes no bit; held out on seed 7
(1416 → 12.1 ms, digest equal) and at 4×10⁵ (3276 → 12.0 ms, 61,701-event items, 1.88 GB RSS —
this box's ceiling). The digest is cap-value-invariant (ES_PULL_CAP 0 and 1 also give `ba1a66b4…`,
equal counts): on these scenes the scan's candidates never overlap the wave backlog, so "the
pull-ahead was eagerness" is scene-structural, not a law — a player inside the belt band during a
wave is the untested exposure. And the frame profile is not cap-monotone: cap 0 leaves 734 ms
monsters, cap 1 leaves 94 ms (other unbudgeted terms near the player's item re-emerge), so
"any small bound" is wrong — 64 is a measured operating point. The patch's comments describe a
capture-deferral that is not in the code (`backlog` is dead; the capture is immediate): rewrite
them at adoption. The wrong-variant numbers are the author's killed build, not rebuilt by the
checker.]*
   *[Checker 2 bf21: every certificate reproduced independently — pristine main (universe.rs
   reverted, same example) gives the same digest `ba1a66b4…`, so default-neutrality is proven, not
   argued; held out on seed 3 (1,257 → 11.96 ms, digest `618d9d23…` equal, counts equal), at 4×10⁵
   (3,901 ms / 65,556-event items → 11.97 ms, 0 over, digest `1d13ab6a…` equal, RSS 1.84-1.86 GB
   — this box's ceiling) and coast (`c55dcf84…` equal). Two corrections to the notes above: (a) the
   non-monotone caps are NOT reproduced on a quiet box — cap 0 and cap 1 both hold 11.98/11.97 ms
   with the same 333-events/frame profile and the same digest, and 333 events ≈ 16 ms of engine
   work leaves nothing to bill a 734 ms frame to: those spikes were box contention (wall time,
   descheduling), not engine terms, so "64 is a measured operating point" rests on schedule noise;
   (b) the neutrality is law on the queue path — the scan reads `binding_at(j, t)` (encounter.rs
   capture, same-doll candidates only), and key order makes every binding at t final before the
   player's item pops — the one hole is `input` (universe.rs:1182), which resolves the player's
   item over an overdue backlog outside the queue: a player issuing input inside a same-doll wave
   is the real untested exposure. Settle at 4×10⁵ grows to 11 s (the deferred backlog answered
   after the flight): the drain, not the frame, scales with N.]*

**The wave's freeze is deleted, and the fix is certified bit-exact where the cut is canonical
(20261014-1719-second-20261014-1631-taleb-6138-4487; the checker's named gold experiment, built and
flown).** The named fix in the engine's own idiom: the player's in-root item pulls at most `PULL_HOLD
:= 64` ship items; over that the rest goes to a drain inside `advance` (the ships below the oldest held
key, in the pull's own key order, one item a pass behind the same `spent_before` gate as any other
item), and the scan that needed the pull is held as a `Waiting` entry that captures only once the ship
lane is clear of its key (answered FIFO, folded into the digest like any held scan; the children-only
pull is untouched). Measured, 200 s flights at rtf 100, budget 12 ms, this Linux box: worst frame
**315→37.7 ms at 10⁵, 1,213→90.3 ms at 2×10⁵ (seed 1; seed 2 1,244→81.4), 1,280 (M1 record)→123.8 ms
at 3×10⁵** (peak 1,705 MB, inside the box's 2 GB cap); events/frame max 24,467→**333**; the wave region
itself now runs at **11.94 ms worst** (the budgeted drain saturated, exactly the coast control's shape),
the overload appearing as 1.67 s of recovered lag instead of 1.2 s freezes. Certificates:
`frame_digest` (8 scripted flights × 4 schedules) identical pristine vs fixed vs every-pull-forced
(`set_pull_hold(0)`, a doc-hidden control); belt flights bit-identical at the post-wave canonical cut
(21,000 game-s, deterministic 25-events budget: digest `ae06c773…`, kicks/events/encounters equal to
the digit), at all three cuts at N=2,000, and both cuts on the coast control. *[checker 4487: seed 3
and every-pull-held (`NLADDER_HOLD=0`) reproduce the post-drain identity (hold 0 matches at both
cuts); the 3×10⁵ arm is a quiet-box number — under a loaded box its worst frame inflates ~4× on
0-event frames while evmax stays 333.]* *[checker2 4487, from the patch on a clean tree: 3×10⁵ under
the deterministic budget joins the identity — pristine 2,615 ms worst / 52,846 events in a frame vs
fixed 12.0 ms / 218, digest `d4f4441e…` equal to the digit; seed 7 and `NLADDER_HOLD=1` (minimum
slice) also match at 21,000 game-s — and at seed 7 the resolved-events counter sits 6,116 apart at the
identical digest, so the counter is pace-dependent and the digest is the certificate.]* Two findings bound the
claim: (a) a **mid-drain cut is not canonical** — at 16,000 game-s the fixed engine holds 11,473 fewer
resolved events (the drain's unfinished share) and the digest differs; (b) the instrument itself — a
wall-budgeted 2×10⁵ belt flight — **is not schedule-stable on shipped main** (two pristine runs differ
at both cuts: `f6869cbb…`/`02570fef…`), so belt digests compare only under a deterministic budget.
Residual: the worst frames are now the unnamed **second seam** (1 event each, every ~50 frames, burn
only: 37.7/90.3/123.8 ms at 1/2/3×10⁵ — it grows with N and now binds F1; the fix does not touch it).

**The belt's cadence is the doll's clock, and the 10⁹ rate law is corrected 24× (20261014-1719-fermi-cf45).**
Measured on shipped main (`examples/cadence.rs`, read-only, seed 1 + held-out 11, N 1000/4000):
every root-doll ship steps at 2^step_log2 per period of the doll's **shortest secondary**
(P_D = 77.24 d — the record's "Cinder 88 d" is off 14%), Δs rounded one octave down and refined
+7.9% by f'(U_P+c): interval **2.814×10⁴ s p50, flat in a** across 2–3 AU (quartile means
2.818→2.805×10⁴ s; the own-period law demands ×1.84), rate **3.553×10⁻⁵ /game-s/body** seed- and
N-stable, kicks/own-orbit 2,674–5,484 (5–11× the old 512/orbit bar); three instruments agree
(plan interval; per-body counter exactly 2 kicks in 60,333 game-s; first kicks at 1.41×10⁴ s inside
taleb-6138's measured wave window), and `step_for` on the same bodies gives 6.77×10⁵ s — **24.1×
slower**: effb's "rate = 2⁷/P_own, a pure birth constant — the whole bill" is the *secondary-doll*
law read onto the root doll (`step.rs:554` reaches `step_for` only when `!on_clock()`; the roster
reproductions 3071/7497, 202–223 kicks/orbit, live in secondary dolls — a code-path reading, not
re-measured). Recomposed at 10⁹
(`compose.py`): 3.55×10⁴ kicks/game-s = 8.2 cores at 231 µs, 1.07 at the M1's 30 µs, 0.10 Carlson,
0.0039 key arm (rtf 1); **at flying pace the shipped step_log2 7 is 148× over even at 30 µs** —
the dial fits only at its coarse end (step_log2 0: 1.16×; Carlson ≤ 2–3: 0.45–0.90×; key arm
already 5: 0.14×; as shipped only the key arm fits, 0.54×), and its anchor is **P_D × the
f'(U_P+c) refinement, never P_own**. The birth wave at 10⁹ (all bodies at tick 0, first kicks
1.34–1.45×10⁴ game-s) is 26× the steady stream — 10 s/s at rtf 100 even at the key arm: birth-phase
staggering is not optional *[measured at 10⁵ by cb7b: 20× flatter, monsters gone]*. effb's kick-term
composition, its checker's "0.5 AU belt 5.3 cores at 231 µs" line, and the cadence axis of 1738's
cube all inherit the correction; ladder.txt's law was right with the wrong period label. Domain: the
ladder's belt (Rayleigh e 0.07, periapsis > 1.2 AU, planar, prograde) at 2–3 AU, one Linux box; not
measured: belts inside P_D's orbit, near secondaries (f' shortens), under thrust, or a P_D that
itself rebinds (the doll's clock is dynamic); the locals' arm of the probe carried a doll-unit bug
and made no claim.

**The wave's freeze is the player's doll, measured on shipped main: the shock a 20 s rung never
sees (F1's window ends 11,000 game-s before it) is absorbed as 1.45 s of lag when the player is out of
the root doll and as unbudgeted 0.3–1.2 s single frames when it is in it (20261014-1631-taleb-6138).**
Every belt body is born at tick 0 with one Δs, so the first kicks arrive as one smooth wave at
13,037–14,542 game-s (belt_first, 199,700 bodies: p01 13,377, p50 14,072, p99 14,473; ~221 bodies a
frame mean, no intrinsic spike — the monsters are accumulation). On this Linux box, 200 s flights at
rtf 100, budget 12 ms, L8 burn: worst frame **315 ms at 10⁵, 1,213 ms at 2×10⁵ (seed 1), 1,244 ms
(seed 2: structural, 1.03×)** against 12 ms; the monster frames sit in the wave, spaced 49–50 frames
(the player's item cadence), each carrying up to 24,467 events at ~49 µs inside one item; between
them the budgeted drain saturates at 11.9 ms / ~235 events and cannot catch up — it only reaches the
frame's 1.67 game-s tick, while `pull_ships(key, !in_root)` (`universe.rs:769`) resolves every ship
below the player's next item (~83 game-s of horizon under burn): **batch = wave density × the
player's item horizon, linear in N** (6,443 → 24,467 → the M1 record's 37,938 at 3×10⁵ ≈ 5 s a pull
at 10⁶). Control: same seed, same wave, coast — max 12.0 ms, zero frames over, 1.45 s of lag
recovered after the wave (the overload is real in both flights; the seam decides its shape). The
freeze does not ratchet (past the wave ≤ 1.2 ms sampled; bits held: refusals 0, dead 0). The M1's
45 ms at 10⁵ vs 315 ms here: the exact monster is schedule-conditional (where the item lands in the
wave), the phenomenon is not. *[checker 6138: one reading of two — at 5×10⁴ burn on this box the wave
passes with zero frames over budget (the only failures are the second seam, 1 event, 17-19 ms), so
the onset N moves with the drain rate: machine-conditional as much as schedule-conditional; and
the batch model misses its drain term: at rtf 200 (2×10⁵ burn, same seed) the monsters carry
30,301 events against 24,535 at rtf 100, the extra ≈ the halved drain's 25 frames × ~245 events —
batch = wave demand in the item horizon − what the budget-cut drain removed, and the first doubling
(6,393 → 24,535, 3.8× for 2× N) is superlinear, so "linear in N" holds for the demand term only.]*

**The deletion program gets its method, priced from Julien's library mined verbatim for the first
time (20261014-1631-library-7f99; 762 highlighted books, 4,580 highlights cached in the run).**
A grep-backed audit of the engine's own record: **26 kills, 5 revival-shaped events** — landed
same-job add-backs 2 (the rotating binary doll — the family H0210 killed; the chronon kept as test
judge) = **8%**, all five = 19%: the law level brackets Musk's 10% add-back quota. The shipped
frame path holds **0 add-backs** — below quota, and the unfired backlog is exactly the named terms:
a2c1's two sensors, b29a's sticky promotion, 0e37's `entry` field. Ordering: automation last.
Promotion collapses to a **filter**: the refit's refusal is the trigger, no hysteresis machinery.
Direction-0 build acceptance: 427 (p95) – 877 (p50) recompiles/frame against measured demand 0/s
(belt) and 1.4/s (cast) — ≥ 9×10³ headroom. *[Checker 7f99: the revival census misses one landed
scoped restoration — r9 killed kick-avg, yet `docs/law.md` keeps kicks orbit-averaged — a sixth
revival-shaped event, putting the law level at 3/26 ≈ 12%; the frame-path 0 and the ordering
survive both corrections.]*

**Break #3's scan half is decomposed: the player's scan walks its certificate's poison, not the
doll — a write-once speed cap and a global-count density rule (20261014-1511-components-a2c1).**
The unpoisoned certificate keeps **15 + 2 bodies at every N**, but one hot kicked tube raises the
doll's `speed_cap` 84× (monotone: never falls for the process's life), and `scap·h` becomes 96% of
the window: **walked 194 a call at 10⁴–3×10⁵, 12× the certificate's own keep set**; at N=10³ the
density rule fires and the fallback walks every body of every doll (1,017 of 1,028) — the rule
compares a doll-local hit against `bodies/4` over all dolls, misfiring below ~9.4×10³. Named fixes,
in cost order: `rebuild` resets-then-maxes the caps; the density rule counts the doll's own
membership; per-body window widths. *[checker a2c1: the misfire domain is wider than the author's
"N ≲ 2×10³" — the crossover is bodies ≈ 4×(2,425−64) ≈ 9,444, so a 9,000-body universe walks
everything, a 10,000-body one does not.]*

**Break #2's "representation's lever" is measured: the compiled orbit is write-only memory for
the engine, exactly its key, and the view's ramp completion is its one real reader
(20261014-1221-components-0e37).** On the wave scene (N=100,028, past the first-kick wave): standing
1,806 B/body of which 74.3% is derived knots; law-mandated floor 673 B/body — idiot index 2.68×
accounted. Flight table-reads are **O(1) in N** and the belt's retired tables are **read 0 times in
flight** — read only in the burst at their own next kick *[checker: the fixed cast's retired
bindings are fetched ~1.4/game-s by the player's encounter scan; deletion costs ~0.1–1 % CPU, or
one kept exception for the cast]*. 1,001/1,001 sampled current Cycle tables regenerate **exactly**
from `Orbit::compile(key)`. Design, priced: `Segment` drops `entry`, gains key + two-word completion
→ deletes ~520 B/body at ≈zero flight CPU; with the Carlson kernel → ~750 B/body ≈ 1.1× the floor.

**The smallest promotion is no promotion: one belt event is a stack-local function on the compact
row, and the live bind is a regime change, not an event (20261014-0450-scout-b29a).** ~38 µs p50 per
event and 12–40 B of standing state, against the wired sticky `resolve_handout`'s 486–585 µs and
8,257 B — ~13× on CPU, ≥ 200× on bytes. The key-space arm (integer ΔE/ΔL on the key's own quanta)
is 0.11 µs and stays at the birth quantization floor at every Δv/v ≤ 1e-1.

**The 10⁹ ledger is composed, and the scoreboard's gaps resolve into two rails: the kick gap is
the hot rail's alone, and the cold rail is encounter-bound by ~1.9×10³ skin-on
(20261014-0059-fermi-effb).** Cadence code-verified; composed at 10⁹ quiet: kicks 0.12–1.065 cores
at Carlson, **encounters 7.7×10³ cores skin-on (1,925× over)**; memory 2.6–5 GB quiet (fits), 15.75
driven; expected break order as the plane grows: promotion stream ~10³ → hot D-slope 2.8×10⁴ → the
wired encounter tier at ~5.2×10⁵ → memory at 10⁹. *[cf45 corrects the cadence law's anchor for the
root doll: rate = 2^step_log2/P_D, 24× the own-period law at the plane's belt.]*

**The rule-2 conflict is resolved by decomposition: the tail is manufactured, and the promotion
certificate is arithmetic on stored birth constants (20261014-0000-fermi-3071).** Rule 2 is dead as
a ladder rule; every ea91 measurement stands as a correct description of a manufactured
distribution; the live fraction is set at generation.

(The kick census, the surprise-rate distribution, the store's update path and the surviving rules
blocks are unchanged from the runs' own entries — see Runs for 7497, ea91, ae3d.)

## Refuted

- "The wave's height is an engine property" (the premise under the drain/scheduling readings): a
  birth-grid stagger alone (no engine change) deletes the wave's over-budget frames at 10⁵ and cuts
  evmax 19.9×, matching the arrival-width ratio — the synchronized birth grid was the manufacturer
  (20261014-1859-spacex-cb7b).
- "Hold the scan" read as holding the whole scan (capture at answer time): digest-refuted — the late capture
  reads pruned history (4,029 ≠ 4,060 encounters, digest differs); only the answer is holdable, and the capture
  must stay at the player's item, where the bindings at its tick are final (20261014-1719-dynamics-bf21).
- "The first kicks arrive as one smooth wave" (the one-shock reading of 6138's measurement): the arrivals are a
  standing train — the cohort recurs one step (~27.5 k game-s) later with its shape, width growing only 1.1 k →
  3.0 k game-s per pass; and the steps are a continuum, not the single power of two the pow2-rounding reading
  predicted (same run).
- "The wave is the drain's problem": the drain holds the coast at 12.0 ms through the same wave
  (0 frames over, 1.45 s lag); the freeze is the player's item alone (`pull_ships` at the root doll)
  (20261014-1631-taleb-6138).
- "The unbudgeted pull is the price of the scan's bit-exactness": the held pull — a 64-item slice,
  a budgeted key-ordered drain, and a scan that captures once the lane clears — is bit-identical on
  every scripted flight and at every canonical cut past the drain (20261014-1719-second-20261014-1631-taleb-6138-4487).
- "A belt flight's digest at a cut is a canonical comparison": two pristine 2×10⁵ wall-budgeted
  flights of shipped main differ at both cuts tested (16,000 and 21,000 game-s); only a deterministic
  budget makes the comparison exact (same run).
- "The scan's walk is O(N) at ladder scale" / "the density rule protects the walk": the walk is
  doll-scoped, 194 bodies a call at 10⁴–3×10⁵, and the rule inverts below ~9.4×10³ (1,017 of 1,028
  walked at 10³) (20261014-1511-components-a2c1).
- "The retired compiled orbit is needed by the engine between kicks" / "deleting it is free at
  today's view": read-0 in flight but the view's ramp completes through it — the two-word completion
  is the prerequisite (20261014-1221-components-0e37).
- "effb's cadence law `rate = 2⁷/P with κ ∈ [128, 256]` — a pure birth constant, the cold rail's whole bill": right only inside secondary dolls; the root-doll belt runs on the doll's clock — measured 3.553×10⁻⁵/s flat in a, 24× the own-period law at p50; the dial's anchor is P_D (77.24 d), not P_own (20261014-1719-fermi-cf45).
- ladder.txt's "period of Cinder … 88 days": the root doll's shortest secondary is 77.24 d (same run).
- "Cost follows events, not bodies" as a measured update-path scaling law: the timed path is one
  shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst compaction step is
  12.1 ms at 0 repacks (same run, checker). The general rule is the compaction step, not the repack.
- **"The live set is a rank, not a count" (rule 2): dead by its own named falsifier and by
  decomposition** (20261013-2252-second-…-7497; adjudicated 20261014-0000-fermi-3071).
- "The live set chatters rank-to-rank and needs hysteresis at the half-run scale": ranks among live
  bodies are at the Poisson re-noise null; the churn is death (20261013-2252-dynamics-ea91).
- "Most promoted bodies go dormant (zero events in the second half)": true only of the dead; among
  live promotions 0–9 % are dormant in a half-run (same run).

## Open directions

0. **Adopt the pair (engine-side pull-hold + generation-side stagger), then re-fly the rung past a
   whole wave-train period (≥ 27.5 k game-s).** The stagger is now measured (cb7b: 20× flatter,
   monsters gone at 10⁵; a ~10-line birth-only change or a birth-phase column when `shipmem` wires
   the belt — cf45's "not optional" at 10⁹), and it is what keeps the drain current where the cap
   only holds the frame (bf21's ~34 s of lag per pass at 10⁶). The stagger's open halves: scale the
   first Δs with the delay if the behaviour gates reject the one-shot class (cb7b's named unbuilt
   fix); fly a staggered wave with the player inside the belt band (both bf21's and cb7b's untested
   exposure).
1. **The second seam now binds F1** (both fixes leave it): 1-9 event frames at 33-38 ms at 10⁵,
   37.7/90.3/123.8 ms at 1/2/3×10⁵ burn, every ~50 frames (the player's item cadence), burn only,
   from 5×10⁴ up (it predates both fixes; 4487, cb7b) — the player's own item cost under burn
   (a2c1's walk-all and cap are the named suspects); unnamed, cheaper to diagnose than the pull was.
2. **The mid-drain cut** (16,000 game-s): a cut is canonical for the held pull only once no held
   key remains below it (4487); the wall-schedule instability of the belt digest on shipped main is
   worth its own run (the deterministic-budget mode is the instrument until then).
3. **The break-#2 build** (0e37): `Segment` drops `entry`, gains the key and the two-word (a, ȧ)
   completion; deletes ~520 B/body at zero flight CPU; with the Carlson kernel ~750 B/body.
4. **Wire the belt's events through the scar batch, not `resolve_handout`** (b29a): the composed
   path deletes the sticky promotion; the refit's refusal is the promote-to-live trigger.
5. **The deleted rungs** (rule 1): per term, what does the frame loop look like with the term gone.
6. **The wired encounter wall** (effb): ~5.2×10⁵ belt bodies skin-on when the tier is wired; the
   further ~1.9×10³ cut is the cold rail's 10⁹ lever.
7. **Pick the belt's `step_log2` as a budget decision** (effb, cf45): the cold rail's whole CPU bill
   is 2^step_log2/P_D summed over the period mix — a content policy, set when wiring shipmem.
8. **Event-time hysteresis on the shipped chatter case** (rule 3); **compaction as the scheduled
   spike** (rule 4); **the belt revival path** (rule 6, the one scene class that could revive a
   measured rank); **the death channel at belt scale** (ea91).

## Contradictions

- None open on this topic. (The page's earlier main/taleb-6138 conflict was two concurrent
  current-bests; both blocks are kept above, the newer first. cb7b's page unions the two sides.)

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261014-0000-fermi-3071 (silver): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law code-verified; encounters 1,925× over skin-on; two rails.
- 20261014-0450-scout-b29a (silver): the smallest promotion is no promotion (~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs).
- 20261014-1221-components-0e37 (silver): break #2's lever measured — compiled orbits are write-only in flight, exactly the key; floor 673 vs standing 1,806 B/body; the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (silver): break 3's scan half decomposed — the cap's monotone walk (194 a call, 12× the keep set) and the inverted density rule (walks all dolls below ~9.4×10³).
- 20261014-1631-library-7f99 (silver): the deletion program's method — 26 kills, the 10% add-back quota bracketed at the law level, frame path 0%; promotion = refusal filter; automation last.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon; coast 12.0 ms through the same wave.
- 20261014-1719-dynamics-bf21 (awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24× the own-period law); shipped step_log2 148× over at flying pace; dial anchor P_D; birth staggering "not optional" at 10⁹.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted by the pull-hold drain + held scan — 315→37.7 ms at 10⁵, evmax 24,467→333, bit-exact at canonical cuts; the second seam is the residual.
- 20261014-1859-spacex-cb7b (this run): the birth-grid stagger measured — arrival width 20.2× flatter (one step), evmax 6,712→338, wave over-budget frames 5→0, max 338→34.4 ms at 10⁵ burn on clean main; non-belt counters identical; one-shot Jacobi cost inside the cadence class (ratio unheld at step 5).
