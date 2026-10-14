updated: 20261014-2012-components-38bf

# The N ladder: 28 live bodies toward 10⁹

## Current best

**The input seam inside a wave is measured and bounded: with the pull capped, a player decision
mid-wave costs O(1) — 0.168 ms once, ≤ 0.229 ms at 60 Hz through the whole wave — and a no-op
decision moves no kick but can move the log (20261014-2012-components-38bf).** On shipped main plus
this run's re-derivation of bf21's cap (`ES_PULL_CAP`, default-unset; bench `wave_input`), the wave
scene (2×10⁵, seed 1, L8 burn, rtf 100, 12 ms, cut 16,000 game-s settled): uncapped worst frame
1,486.9 ms / 9 over; capped 12.487 ms with the digest bit-identical (`c2b834bb…`, kicks 225,949
equal — bf21's certificate reproduced independently); then one no-op decision at the wave's p50
costs 0.168 ms (≤ 2 events), and 657 of them (every frame of p01–p99, an adversarial bound: the
shipped page calls `input` on key change only, `session.rs:118`) cost ≤ 0.229 ms each — max frame
12.5 ms, 1 over, lag +0.21 game-s. The checker-2-bf21 exposure (`input` resolving the player's
items over an overdue backlog outside the queue) is **bounded, with or without the cap**: O(1), not
O(backlog); the input path needs no deferral machinery. Margin: kicks bit-equal
everywhere, but the 657 no-op decisions add encounters at the log's margin (+1 measured; +2 on the
checker's re-run — pace-dependent: the decision's requeue carries scans at ticks the scheduled items
never scan) — "same keys" is not "no
event". Unmeasured: a key-**changing** decision mid-wave (a turn re-plans the player), the player
inside the belt band, 4×10⁵, a busy box (4487's 1-event second seam is load-conditional; it did not
appear here — the worst frames are the budgeted drain itself, and P1 vs P2 digests equal under
settle-at-cut on one pair, which does not retire 4487's instability finding).
   *[Checker 38bf: every counter and the P1/P2 digest identity reproduce (8 further flights);
   the exposure never fired **even uncapped** — one mid-wave decision with the cap unset costs
   0.154 ms at rtf 100 and 0.158 ms at rtf 200 (the uncapped frame monsters 1.3–1.9 s are the
   scheduled pulls, not the input path; the lane is already tiled to the player's key), so "real
   as a mechanism" is structure, not a measured cost. The named untested arm is answered: a
   key-changing decision (`word(5,8)`) costs 0.20 ms at 2×10⁵, and 657 of them every frame at
   3×10⁵ hold max frame 11.97 ms (0.26 ms a call, RSS 1.38 GB; `one` at 3×10⁵: 0.161 ms, max
   12.1 ms — the window is N-independent, `belt_first`). The one-decision digest does not
   regenerate (three runs, three values at the same frame — decision-bearing digests at the 16 k
   cut are wall-unstable, 4487's direction 12; compare counters, not those digests). And
   `session.rs:118` does not exist in this tree — no shipped caller of `input` outside examples;
   the realism caveat rests on an unverifiable citation.]*

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
(stagger the birth grid over one step → ~24× flatter drain utilisation), unmeasured here. Domain: seed 1, the
ladder belt, Linux shared box, 2×10⁵ burn only; the view's gather during the deferred window unmeasured.
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
staggering is not optional. effb's kick-term composition, its checker's "0.5 AU belt 5.3 cores at
231 µs" line, and the cadence axis of 1738's cube all inherit the correction; ladder.txt's law was
right with the wrong period label. Domain: the ladder's belt (Rayleigh e 0.07, periapsis > 1.2 AU,
planar, prograde) at 2–3 AU, one Linux box; not measured: belts inside P_D's orbit, near
secondaries (f' shortens), under thrust, or a P_D that itself rebinds (the doll's clock is
dynamic); the locals' arm of the probe carried a doll-unit bug and made no claim.


**The deletion program gets its method, priced from Julien's library mined verbatim for the first
time (20261014-1631-library-7f99; 762 highlighted books, 4,580 highlights cached in the run).**
A grep-backed audit of the engine's own record: **26 kills, 5 revival-shaped events** — landed
same-job add-backs 2 (the rotating binary doll — the family H0210 killed; the chronon kept as test
judge) = **8%**, all five = 19%: the law level brackets Musk's 10% add-back quota ("if you do not
end up adding back at least 10% of them, then you didn't delete enough", Isaacson). The shipped
frame path holds **0 add-backs** (only the frame tier and the old view search were ever deleted
there) — below quota, and the unfired backlog is exactly the named terms: a2c1's two sensors, b29a's
sticky promotion, 0e37's `entry` field. Ordering: automation last (the allocator lands after the
deletions; the 6 anchored guard/fallback sites — the caps, the density rule + walk-all, the hull
widening — exist only to manage undeleted state). Promotion collapses to a **filter**: the refit's
refusal is the trigger (b29a's 9–26% at Δv/v ≈ 1), no hysteresis machinery, no sticky binding. The
direction-0 build gets its acceptance number: **427 (p95) – 877 (p50) recompiles/frame** at 33 ms
against measured demand 0/s (belt) and 1.4/s (cast) — ≥ 9×10³ headroom; the +24 B two-word
completion is the expected add-back (4.6% of the 520 B deleted). All numbers: the run's `audit.py`.
   *[Checker 7f99: the revival census misses one landed scoped restoration — r9 killed kick-avg,
   yet `docs/law.md` keeps kicks orbit-averaged on stable orbits (PRINCIPLES register) — a sixth
   revival-shaped event, putting the law level at 3/26 ≈ 12% landed; and the 26 kills are a sample
   (the Refuted sections of encounters/b12/kick-cadence/kick-jet hold more). The frame-path 0 and
   the ordering survive both corrections.]*
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
45 ms at 10⁵ vs 315 ms here: the exact monster is schedule-conditional (where the item lands in
the wave), the phenomenon is not. *[checker 6138: one reading of two — at 5×10⁴ burn on this box
the wave passes with zero frames over budget (the only failures are the second seam, 1 event,
17-19 ms), so the onset N moves with the drain rate: machine-conditional as much as
schedule-conditional; and the batch model misses its drain term: at rtf 200 (2×10⁵ burn, same
seed) the monsters carry 30,301 events against 24,535 at rtf 100, the extra ≈ the halved drain's
25 frames × ~245 events — batch = wave demand in the item horizon − what the budget-cut drain
removed, and the first doubling (6,393 → 24,535, 3.8× for 2× N) is superlinear, so "linear in N"
holds for the demand term only.]* Named fix, in the engine's own idiom: the scan is already holdable off
the critical path (`universe.rs:1164`); hold it when the backlog it would read is over a threshold
and let the budgeted drain resolve it — certificate: `frame_digest` unchanged. Gate consequence: an
N rung flown 20 s certifies a window that excludes every belt body's first event; the rung must fly
past the wave (≥ 150 s) before F1 can certify scale. Domain: Linux shared box, one box, burn arms at
10⁵–2×10⁵ only (3×10⁵ quoted from the M1 record: it exceeds this box's 2 GB cap); a second milder
burn-only seam at frames 11,094+ (13–55 ms, event-thin, every ~50 frames) is unnamed.

**Break #3's scan half is decomposed: the player's scan walks its certificate's poison, not the
doll — a write-once speed cap and a global-count density rule (20261014-1511-components-a2c1).**
An env-gated census on the shipped `PlayerNeighbourhood::capture`/`Radial::candidates` (counters
only, digest-neutral; the ladder's own arms, 20 s flights): the unpoisoned certificate keeps
**15 + 2 bodies at every N** (the first call's window: bins 479–486 around the player), but one
hot kicked tube (a local on a periapsis-heavy ellipse) raises the doll's `speed_cap` 84×
(1.16e-4 → 9.76e-3, monotone: `note` only maxes and `rebuild` only maxes, so it never falls for
the process's life), and `scap·h` (h = the player's plan step, 1.1e12) becomes 96% of the window:
±9× the player's radius, hit 2,402 bin-entries, **walked 194 a call (flight average; late calls
203) at 10⁴–3×10⁵, 12× the
certificate's own keep set, kept 177** *[checker a2c1: 10⁶ untested — 3×10⁵ reproduced
identically (194/177, 711 MB); the claim's domain ends where the measurement does]*; the
hull-of-history registration widens entries 905 → 2,885 (~14 bins/body) as kicks land. At
**N=10³ the density rule fires on 183/193 calls and the fallback walks every body of every doll
(1,017 of 1,028)** — the rule compares a doll-local hit against `bodies/4` counted over all
dolls, so the misfire is N-dependent and inverted (adding belt bodies to other dolls
un-poisons doll 2) *[checker a2c1: the misfire domain is wider than the author's "N ≲ 2×10³" —
it fires at 2,000/3,000/5,000/9,000 and passes at 9,500; the crossover is bodies ≈ 4×(2,425−64)
≈ 9,444, so the 10⁴ arm sits ~5% above it — a 9,000-body universe walks everything, a
10,000-body one does not]*; capture then costs **more at 10³ than at 10⁵ per
call on this box (author 178 vs 129 µs; checker regen 110.8 vs 105.7 µs — direction holds, the
gap is inside shared-box noise)**, and the held answers (idle-time) scale the same
(1,428 vs 824 µs author; checker regen 1,299 vs 777 µs; standing ~10 KB a held scan ≈ 57 B a
kept candidate, held max 270 at 10⁴ burn / 191 at 10⁵ in regen — schedule-dependent, the
author's 1,020 not reproduced). The ladder break-3 "one item 14.6 ms" near the belt
*[checker: inferred, not observed — 3×10⁵ × 48 ns ≈ 14.4 ms fits the walk-all arithmetic, but
no root-doll scan was recorded in any arm (40 s burn included: the player's binding stays in
doll 2 past frame 948)]* is this walk-all at the M1's ~48 ns/body.
Named fixes, in cost order: `rebuild` resets-then-maxes the caps over the retained bindings
(one line); the density rule counts the doll's own membership and the fallback iterates the
doll's registered ids, not `0..total` (a few lines); the window's representation — each body's
bins widened by its **own** speed bound, not the doll-wide cap (slow bodies stay in 1–2 bins,
hot ones correctly spread). Burn arms: finer `h`, 79 walked/call, density never fires (P4 held);
**unmeasured**: the belt's registration state (no belt events in 20 s flights — its first kicks
are at 13,051 game-s), the player inside the belt (the case the density rule was written for),
and the found set per scan. PRINCIPLES #5: the scan reads its neighbourhood, not the doll.

**Break #2's "representation's lever" is measured: the compiled orbit is write-only memory for
the engine, exactly its key, and the view's ramp completion is its one real reader
(20261014-1221-components-0e37).** On the wave scene (N=100,028, 80 wall s at rtf 200, past the
first-kick wave): held tables 2.0/body (100,076 current + 100,491 retired); standing 1,806 B/body
of which 74.3% is derived knots (current shape 672, retired 670; rec+plan 464); law-mandated
floor 673 B/body — idiot index 2.68× accounted, ~4.6× on footprint (459 MiB = 4.59 KB/body;
+2.33 KB/body across the wave, ladder's 2.6→5.1 reproduced). Flight table-reads are **O(1) in
N** (107–191 decodes/frame at N=10⁵, the same as N=2×10³; 2.2M reads ≈ the wave's own kicks ×
~10–15, ≈6.9×10⁻⁴/held-table/game-s) and **the belt's retired tables are read 0 times in
flight** — read only in the burst at their own next kick *[checker 0e37, all-path counter: true
of the belt (fetch rate flat across the wave), but the fixed cast's retired bindings are fetched
~1.4/game-s by the player's encounter scan (`encounter.rs:180` — all 56,454 in-flight retired
fetches over 40,000 game-s; state_of 0) — deletion costs ~0.1–1 % CPU in recompiles, not zero,
or one kept exception for the cast]*. 1,001/1,001 sampled current
Cycle tables regenerate **exactly** from `Orbit::compile(key)` (knots, crossings, all three
channel increments): the cache holds nothing beyond the key. The one mass reader is the view's
gather: cold 4,238.7 ms, 10.71 decodes/row, and **309,227 rows completed through a retired
binding in two gathers** (≥1/row post-wave — `observe::partial`'s ramp decodes the previous tube
2–3× per mid-window row), which the **two-word (a, ȧ) completion** replaces (a-word's open
direction 1; the one-word form is gate-refuted, the two-word is second order at the handover by
construction). Design, priced: `Segment` drops `entry`, gains key (+56 B) + word (~24 B) →
deletes ~520 B/body accounted (~800 B/body footprint) at ≈zero flight CPU *[checker: ~0.1–1 %
above]*; the current generation
follows the same route once the Carlson kernel lands (2.9 µs/channel family, kick-jet de99) →
~750 B/body ≈ 1.1× the floor, moving the 4-GiB-at-10⁶ wall to ~2×10⁶ (free half) / ~4×10⁶ (with
kernel). Instrument digest-neutral: `frame_digest` identical pristine vs patched on every
flight. Domain: belt band (e ~0, ~7 knots), planar, headless flight (no per-frame gather),
Linux footprint; passages/plunges unsampled, high-e members are the same lever at 5–20× the
bytes (thinner tables, closed-form-kernel 5a3b), the gather's retired-read share is a post-wave
snapshot — the mid-window phase peak (≥2/row cold); at 40,000 game-s it is 0.02/row (checker),
the synchronized cadence's phase setting the share.

**The smallest promotion is no promotion: one belt event is a stack-local function on the compact
row, and the live bind is a regime change, not an event (20261014-0450-scout-b29a).** Composed from
shipped pub APIs (`Population::body`/`scar`, `Key::darwin`, `Orbit::compile`, readout,
`binding::cartesian`, `Rebinding::from_state`) on the lab belt band: ~38 µs p50 / ~78 µs p95 per
event and 12–40 B of standing state, against the wired sticky `resolve_handout`'s 486–585 µs and
8,257 B with no demotion (367f) — ~13× on CPU, ≥ 200× on bytes, zero standing body. The refit term
(`from_state`) is 21 µs p50 at belt keys; the **key-space arm** (integer ΔE/ΔL on the key's own
Q48/Q32 quanta) is 0.11 µs and stays at the kicked state's birth quantization floor at every
scale Δv/v ≤ 1e-1 (E 3.0 Q48 / L 7.6 Q32 quanta from the f64 invariants), with shape agreement
with the refit ≤ 1e-9 typical (tail 7.7e-8 at 65,536 — checker), impulse-independent — the r2
finding ("kicks are integers native to the law") made the cheapest exact arm, pending the
encounters tier delivering ΔE/ΔL as exact integers. At 10⁹ quiet the stream is 1.4 Linux cores
(refit arm) / 0.004 (key arm): the kick stops being the quiet-belt wall; encounter discovery stays
the cold rail's large term. The 8-byte scar's i16 grade ends near Δv/v ~ 1e-5 (92% Wide at 1e-4);
w/t column anchoring is a wiring decision (naive wiring forces Wide at 53%/47%; anchored in-order
deltas measure 12.07 B/event, checker). Domain: planar,
prograde, one belt band, Linux shared-cloud; not 3-D, not the GR doll, not the real contact-impulse
distribution. Checker: the 13× is cold-belt (σ0.07); at σ0.3/e≤0.9 the composed cost is ~76 µs
(6.4× under sticky); Δv/v=1 refuses 9–26% (the regime trigger observed); `Key::darwin` caps the
composed path at p ≤ 8192 M — belt bands beyond it (the store's `Spec` allows to 65536 M) need a
different row→key path.

**The 10⁹ ledger is composed, and the scoreboard's gaps resolve into two rails: the kick
gap is the hot rail's alone, and the cold rail is encounter-bound by ~1.9×10³ skin-on
(20261014-0059-fermi-effb).** The cadence law is now code-verified: `step_for` is one
step per 2⁻⁷ of the radial period, power-of-two rounded (`ctx.rs:44` `step_log2: 7`;
`step.rs:75-97`), so **rate = 2⁷/P with κ ∈ [128, 256] — a pure birth constant**; it
reproduces 3071's roster endpoints (top 0.0462 vs 0.0484, ratio 0.96 — 4.7% *above*
the κ=256 ceiling, so band-edge-tight; floor 3×10⁻⁵, which the hauler band cannot
reach — its κ<256 top at 0.5 AU is 2.29×10⁻⁵ — while Cinder's band [1.7, 3.3]×10⁻⁵
contains it at κ≈231 — **no period-independent clock floor** on either reading;
checker: the floor body's identity is unverified), contains 7497's Orbiters
(202–223 ⊂ [128, 256]), and validates the SI unit reading (root unit 1.477 km, c = 1,
game-second = second). Composed at 10⁹ quiet (rtf 1, 4 cores): kicks 0.12–1.065 cores
at Carlson (code-derived 1–2 AU belt 0.043–0.243, a9d7 rate 1.065; checker: at the
shipped 231 µs the true 1–2 AU band is 0.33–1.87 — the ledger's 0.94 is the κ=128@1 AU
edge — and a 0.5 AU belt runs up to 5.3 cores at 231 µs; Carlson busts 4 cores only
inside ~0.16 AU)
— 8.2 only at the a9d7 rate × 231 µs (367f's 8.3 and ad26's 1.08 re-derived
independently; both stand, the spread is the period mix: the record's per-body rate
constants span ~100× by instrument — roster mean 3.3×10⁻³, a9d7 3.55×10⁻⁵, haulers
1.8×10⁻⁷–2.3×10⁻⁵); **encounters 7.7×10³ cores skin-on (1,925× over; 9.66×10⁴
no-skin), 7,051× the kick term at Carlson pricing**; memory 2.6–5 GB quiet (fits),
15.75 driven (the quanta); hot 90–186 MB; H_live ~0; frame tier deleted (gate open).
Rails: hot (battle density 0.041/member/s) measured ceiling 2.8×10⁴ at the stack
(790b), model-scaled to ~4–6×10⁸ at the 42–55 ns floor (the ledger's own 4.9×10⁸;
checker-corrected from ~10⁷–10⁸) — the kick gap (10^3.3) buys
this rail, 4+ of the bodies gap's 6.4 orders; cold (belt) never kick-bound, encounter-
and memory-bound. **Expected break order as the plane grows: promotion stream ~10³
(367f) → hot D-slope 2.8×10⁴ (790b) → the wired encounter tier at ~5.2×10⁵ bodies
skin-on (~4.1×10⁴ no-skin; held-out, falsifiable when H0216 wires it) → memory at 10⁹
(quiet: never; driven: the quanta).** The cold rail's entire CPU bill is chosen at
generation: when shipmem's belt is wired, pick its `step_log2` knowing rate =
2^step_log2/P is the whole bill.

**The rule-2 conflict is resolved by decomposition: the tail is manufactured, and the
promotion certificate is arithmetic on stored birth constants (20261014-0000-fermi-3071,
adjudicating 20261013-2252-dynamics-ea91 against
20261013-2252-second-20261013-2130-library-ae3d-7497).** ea91's ho1 scene reproduces
bit-identically (digest `aca905ad…`). The plane's 28 natives carry compiled rates
0.0484 → 3×10⁻⁵/s (1,613:1 by construction — now derived from the cadence law above):
same-rate bodies have identical census counts (133,133 / 67,67,67 / 17,17 at T = 5,500
game-s), counts are identical across seeds 3/7/11 and member counts 48/120/400, and
exactly 2× under a doubled window (kicks 266 = 2·133 exactly; 133 = 2·67−1, 33 =
2·17−1). Roster-predicted native Gini 0.759 vs measured 0.718–0.745 (ρ = 0.94–0.96);
the model "natives = rate×T, members = measured" reproduces G_all within 0.017 (worst
case, tune) and even the Zipf slope (−1.6…−2.0). Held-out: seed 11 m120 held 5/5; the
doubled window held the ladder exactly (2× per ladder body; the roster Gini is
T-invariant by construction) while the player proved schedule-bound (350 ≠ 2×417) and
G_all *rose* (0.753) as dead members' one-time bursts froze against ∝T ladder bodies —
both misses in the driver/member channels no rank reads. So: **rule 2 is dead as a
ladder rule** (7497's verdict, now decomposed); **every ea91 measurement stands** as a
correct description of a manufactured distribution; the live fraction is set at
generation (12 of 28 natives above 3×10⁻³/s here), and the promotion cost question
stays at frame-cost's `resolve_handout`.

**The surprise-rate distribution as measured (ea91, instrument = the env-gated
per-body census in `Universe::apply`, digest-neutral):** across bodies, resolved items
have Gini 0.72–0.74, top-decile 47–56 %, Zipf −1.6…−2.0, busiest ~100× median; ranks are
regime-frozen among the living (natives ρ = 0.98–1.0; promoted ρ = 0.85–0.93 at 55 s
windows, at the Poisson null, below it at 30 s) — the regime is now explained: it is
the compiled period ladder. The churn channel is **death**: 47–64 % of promotions crash
within one run window, each after a birth burst, then 1–3 items per half-run of
quiescence; the steady stream avalanches (Fano 8–28, top 1 % of frames carry 10–26 % of
items, zero-frames 0–86 % by scene, lag-1 |ρ| ≤ 0.17). Domain: the plane's battle
scenes, m48–m400, windows 30–55 s at rtf 100 (the bench clamps `--members` to [4, 400]
and `--seconds` to ≤ 55); not the quiet belt, not below half-run scale.

**The kick census as measured (7497, instrument = `Update.kick` + `kick_log`,
digest-neutral):** the tube bulk is flat per orbit by construction (CV 0.17–0.20,
max/median 1.4–1.5, Gini ≤ 0.12; Orbiters 202–223/orbit across scenes and seeds); the
per-second spread is three decades (4.8×10⁻² → 3×10⁻⁵) but it is structure — rank per
second = rank in 1/P_orbit plus the clock's regime, knowable from body constants at
birth. The head is driver-caused: a held L12 burn puts 70.6 % of kicks on the player;
the 4,000-member battle spreads over 3,769 promoted members (p50 5, mean 20.6, max 174,
top member 0.07 %) — dispersed, headless, discovered by due-ness.

**The store's update path is population-independent by construction (events touch one
shard, sharded at 2²⁰ members) and its spikes live in compaction steps, not the append —
measured on shipped code (20261013-2130-library-ae3d; checker-corrected; store rows
re-regenerated by the 7497 run: 12.347 bits/member at 7 ns, storm 48.38 with graceful
fallback, convoy hot max 10.9 µs vs a 1.29 ms compaction step).**

The four rules that survive, with rule 2 struck and adjudicated:
1. **Delete before you measure cheaper, and to the quota** (Musk's algorithm + his 10% rule,
   library-7f99): every ladder term gets a *deleted* rung before a *cheaper* rung, and ~10% of
   deleted terms must come back — else the deletion was too timid. Audit 7f99: law level 8–19%
   (at quota), frame path 0% (backlog unfired: the caps, the density rule, the hull, the sticky
   promotion, `entry`).
2. ~~**The live set is a rank, not a count**~~ — **dead by measurement and by
   decomposition** (7497, adjudicated 3071): the distribution's bulk is flat per orbit
   by construction, its native concentration is the compiled period ladder (a birth
   constant), its head is driver-caused, and its churn is death. The live-set bar is a
   period/clock-regime threshold knowable at generation; falsify further on belt scenes
   (conjunction clustering), not the plane.
3. **Promotion judges on event time, not frame time** (sampling noise): the judged form is a
   **filter, not machinery** (library-7f99): the refit's refusal is the promote-to-live trigger
   (b29a: 9–26% refusal at Δv/v ≈ 1) — no hysteresis windows, no rank state. *[At the half-run
   scale live ranks sit at the counting-noise null (ea91). Held-out: the 210-handoff chatter
   vanishes if those handoffs never refuse the refit.]*
4. **Buy the option, not the headroom** (optionality): no ahead-of-demand promotion;
   the promotion to make cheap is the *ephemeral* one (demote at commit, frame-cost),
   and the repack/compaction step (1.29–12.1 ms) is the scheduled spike.
5. **One mechanism at every scale** (Waitzkin): a rung that needs a special case for
   the head of the distribution fails the rung, whatever its numbers.
6. **Automation last** (Musk, via library-7f99): the allocator lands after the frame-path
   deletions; a guard or fallback that exists to manage undeleted shared state (the 6 anchored
   sites) is a deletion marker, not a scheduling input.
7. **Shared state pays sensor cost** (Karpathy, via library-7f99): a doll-wide or singleton cache
   is priced procure + maintain + incorporate (the monotone cap, the window widening) — delete it
   for one exact per-body instrument rather than repair it (a2c1's fix order inverts).

## Refuted

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
- "The scan's walk is O(N) at ladder scale" (the reading of the ladder's before-fix capture
  profile, 45–50 ns a body, carried into break 3's wording): at 10⁴–3×10⁵ the walk is
  doll-scoped, 194 bodies a call (79 on the burn arms) — the O(N) reading holds only where the
  density rule fires, which by measurement is N ≲ ~9.4×10³ on these arms (checker: fires at
  9,000, passes at 9,500; the author's first reading was 2×10³), and there it walks every
  body of every doll (1,017 of 1,028 at 10³; 8,604 of 9,028 at 9,000) (20261014-1511-components-a2c1).
- "The density rule protects the walk": it inverts — its threshold (`bodies/4`, counted over all
  dolls) grows with populations the window never touches, so the same poisoned window passes at
  10⁴⁺ and fails at 10³, where the fallback (`0..total`, a `binding_at` a body) costs more than
  the 10⁵ scan it was meant to save (author 178 vs 129 µs/call; checker regen 110.8 vs 105.7 —
  direction only, the gap is inside shared-box noise) (same run).

- "The retired compiled orbit is needed by the engine between kicks" (the assumption under
  ladder break #2's memory wall): flight reads of held tables are O(1) in N and the *belt's*
  retired tables are read exactly 0 times in a headless flight past the wave *[checker: the
  cast's are fetched ~1.4/game-s by the player's scan — 56,454 over 40,000 game-s, all at
  `encounter.rs:180`; ~0.1–1 % CPU to recompile]*; the knots are a pure cache of the
  `OrbitKey` (1,001/1,001 sampled regen; checker: every current and retired table, knot-for-knot,
  300,520/300,520) (20261014-1221-components-0e37).
- "Deleting the retired generation is free at today's view": post-wave, the gather completes
  ≥1 row in 1 through the previous binding (309,227 completions in two gathers of 100,048 rows,
  10.71 decodes/row) — the deletion needs the two-word completion (a, ȧ), not just a key
  (same run; the one-word form already gate-refuted by a-word's f2b7).

- "Cost follows events, not bodies" as a measured update-path scaling law: the timed
  path is one shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise
  (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst
  compaction step is 12.1 ms at 0 repacks (20261013-2130-library-ae3d, checker). The
  general rule is the compaction step, not the repack.
- **"The live set is a rank, not a count" (rule 2): dead by its own named falsifier and
  by decomposition** — the per-body distribution on shipped plane scenes is not an
  intrinsic surprise tail (bulk flat per orbit; native concentration = compiled period
  ladder, identical across seeds and exactly T-scaling; head driver-caused; churn is
  death) (20261013-2252-second-…-7497; adjudicated 20261014-0000-fermi-3071).
- "The live set chatters rank-to-rank and needs hysteresis at the half-run scale": ranks
  among live bodies are at the Poisson re-noise null; the churn is death
  (20261013-2252-dynamics-ea91).
- "Most promoted bodies go dormant (zero events in the second half)": true only of the
  dead; among live promotions 0–9 % are dormant in a half-run (20261013-2252-dynamics-ea91).
**The wave's freeze is deleted, and the fix is certified bit-exact where the cut is canonical
(20261014-1719-second-20261014-1631-taleb-6138-4487; the checker's named gold experiment, built and
flown).** The named fix in the engine's own idiom: the player's in-root item pulls at most `PULL_HOLD
= 64` ship items; over that the rest goes to a drain inside `advance` (the ships below the oldest held
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

**The wave's freeze is the player's doll, measured on shipped main (20261014-1631-taleb-6138).** Every
belt body is born at tick 0 with one Δs, so the first kicks arrive as one smooth wave at 13,037–14,542
game-s; the player in the root doll resolves the whole backlog inside one unbudgeted item
(`pull_ships` at `universe.rs:769`), worst 315/1,213/1,244 ms, while the coast control holds 12.0 ms
through the same wave. *[checker 6138: the onset N is drain-rate conditional (5×10⁴ passes clean
here); the batch has a drain term — batch = wave demand in the item horizon − what the budget-cut
drain removed.]*

**The deletion program gets its method, priced from Julien's library mined verbatim for the first
time (20261014-1631-library-7f99; 762 highlighted books, 4,580 highlights cached in the run).**
A grep-backed audit of the engine's own record: 26 kills, 5 revival-shaped events (8–19%): the law
level brackets Musk's 10% add-back quota, the shipped frame path holds 0 add-backs and its unfired
backlog is exactly the named terms (a2c1's two sensors, b29a's sticky promotion, 0e37's `entry`
field); promotion collapses to a filter; automation last. *[Checker 7f99: one landed scoped
restoration missed (r9 killed kick-avg, `docs/law.md` keeps kicks orbit-averaged) — a sixth
revival-shaped event; the frame-path 0 and the ordering survive.]*

**Break #3's scan half is decomposed (20261014-1511-components-a2c1): the player's scan walks its
certificate's poison, not the doll** — a monotone `speed_cap` (84×) and an inverted density rule
(`bodies/4` over all dolls, misfiring at N ≲ 9.4×10³) put 194 walked entries a call against the
certificate's keep 15+2; named fixes in cost order: reset-then-max the caps, doll-local density,
per-body window widths.

**Break #2's lever is measured (20261014-1221-components-0e37): the compiled orbit is write-only
memory for the engine, exactly its key** — flight reads O(1) in N, the belt's retired tables read 0
times in flight, 1,001/1,001 sampled tables regenerate exactly from `Orbit::compile(key)`; the
deletion is priced (~520 B/body) pending the two-word (a, ȧ) ramp completion.

**The smallest promotion is no promotion (20261014-0450-scout-b29a): one belt event is a stack-local
function on the compact row** (~38 µs p50, 12–40 B standing) against the wired sticky resolve's
486–585 µs and 8,257 B; the key-space arm (integer ΔE/ΔL on the key's own quanta) is 0.11 µs.

**The 10⁹ ledger is composed (20261014-0059-fermi-effb): the kick gap is the hot rail's alone, the
cold rail is encounter-bound by ~1.9×10³ skin-on**; the cadence law is code-verified (`step_for` is
one step per 2⁻⁷ of the radial period: rate = 2⁷/P, a birth constant).

**The rule-2 conflict is resolved by decomposition (20261014-0000-fermi-3071): the tail is
manufactured, the live fraction is set at generation**; the surprise-rate distribution's regime is
the compiled period ladder, its head is driver-caused, its churn is death.

(The longer standing blocks — the store's update path, the four surviving rules with rule 2 struck,
the kick census, the surprise-rate distribution — are unchanged below this point on the page.)


- "The wave is the drain's problem": the drain holds the coast at 12.0 ms through the same wave; the
  freeze is the player's item alone (20261014-1631-taleb-6138).
- "The unbudgeted pull is the price of the scan's bit-exactness": the held pull — a 64-item slice,
  a budgeted key-ordered drain, and a scan that captures once the lane clears — is bit-identical on
  every scripted flight and at every canonical cut past the drain; the freeze it deletes was not
  buying the bits (20261014-1719-second-20261014-1631-taleb-6138-4487).
- "A belt flight's digest at a cut is a canonical comparison": two pristine 2×10⁵ wall-budgeted
  flights of shipped main differ at both cuts tested (16,000 and 21,000 game-s); only a deterministic
  budget (events, no wall) makes the comparison exact — and under it the engines agree bit for bit
  past the drain (same run).
- "The scan's walk is O(N) at ladder scale" / "the density rule protects the walk": the walk is
  doll-scoped (194 a call) and the rule inverts (20261014-1511-components-a2c1).
- "The retired compiled orbit is needed by the engine between kicks" / "deleting it is free at
  today's view": read-0 in flight but the view's ramp completes through it — the two-word completion
  is the prerequisite (20261014-1221-components-0e37).

- "effb's cadence law `rate = 2⁷/P with κ ∈ [128, 256]` — a pure birth constant, the cold rail's whole bill" (and the checker's 0.5-AU/5.3-core composition): right only inside secondary dolls; the root-doll belt runs on the doll's clock — measured 3.553×10⁻⁵/s flat in a, 24× the own-period law at p50; the dial's anchor is P_D (77.24 d), not P_own (20261014-1719-fermi-cf45).
- "A player decision inside a same-doll wave is an unbudgeted backlog drain" (the checker-2-bf21
  exposure, read as a cost): the drain never manifests — ≤ 0.229 ms a call at 2×10⁵ mid-wave, every
  frame through the wave, max frame 12.5 ms, and (checker) 0.154–0.158 ms **with the cap unset** at
  rtf 100 and 200: the scheduled pulls keep the ship lane tiled to the player's key, so `input`
  finds ≤ 2 due items regardless; what a no-op decision can still move is the log, not the kicks
  (+1 to +2 encounters per 657 decisions, pace-dependent) (20261014-2012-components-38bf).
- ladder.txt's "period of Cinder … 88 days": the root doll's shortest secondary is 77.24 d (same run).

## Open directions

0. **The key-changing decision mid-wave** (38bf's untested arm): a turn under burn re-plans the
   player (the no-op arm never re-derived the plan); one flight with `word(5,8)` at the wave's p50
   against the no-op control, judged on the frame profile and the counters. With it, the wave seam's
   player-facing story is closed and the cap can be adopted without an input caveat.
   *[Checker 38bf: flown — 0.201 ms at 2×10⁵ (encounters −3, kicks equal, max frame 12.48 ms), and
   657 key-changing decisions every frame of the window at 3×10⁵ hold max frame 11.97 ms (0.26 ms a
   call): answered affirmatively on this scene; the player inside the belt band and a busy box stay
   open.]*
0. **The capped pull is measured and certified** (bf21, above): adopt the constant (the env gate comes out;
   any small bound works — the cap only bites when the queue is behind, which is the wave), then re-fly the N rung
   past a *whole wave train period* (≥ 27.5 k game-s, not just past the first wave) so F1's window contains a
   wave; at 10⁶ the frame holds but real time does not (~34 s of lag per pass on this box) — the generation-side
   stagger (birth grid over one step, ~24× flatter) is the measured-next lever, a `shipmem` wiring decision
   (effb's direction 9). The event-thin 13–55 ms seam at frames 11,094+ under burn stays unnamed and open.
1. **The break-#2 build (the lever is now measured):** `Segment` drops `entry`, gains the key
   (+56 B) and the two-word (a, ȧ) completion (~24 B; a-word's open direction 1 is its missing
   half — the write needs the field's derivative at the kick); `observe::partial`'s ramp reads

   the word instead of decoding the previous tube; `binding_at` recompiles on the rare
   non-window read. Deletes ~520 B/body accounted (~800 B/body footprint) at zero flight CPU;
   with the Carlson kernel (kick-jet de99) the current generation deletes too (~750 B/body,
   ~1.1× the floor). The gather's retired-read census then re-runs as the acceptance check.
1. **Wire the belt's events through the scar batch, not `resolve_handout`** (b29a): the composed
   path deletes the sticky promotion entirely; the contract to settle at wiring is the tier → law
   kick interface (exact integer ΔE/ΔL in the key's quanta vs state-space impulse at 21 µs) and
   the w/t column anchoring. The refit's *refusal* is the true promote-to-live trigger.
2. **The deleted rungs** (rule 1): per term, what does the frame loop look like with the
   term gone; count what the per-frame walk visits that the hot tier did not touch.
3. **Event-time hysteresis on the shipped chatter case** (rule 3): retrograde 0.49 R_H,
   boundary evaluated at the doll's events; expect handoffs per 20 periods to collapse.
4. **Compaction as the scheduled spike** (measured): fold the storm row's update stream
   into the shipped allocator and check the p99 frame. Primary direction for the
   promotion work (rule 2's death redirects it here and to ephemeral promotion).
5. **The wired encounter wall** (effb's held-out number): when H0216 wires the encounters
   tier into the plane, the first CPU wall lands at ~5.2×10⁵ belt bodies skin-on
   (~4.1×10⁴ no-skin) — measure it there; the further ~1.9×10³ cut (cells, setup, what
   never needs a pair test) is the cold rail's 10⁹ lever, ahead of any kick-cost work.
   *[0e37: once wired, re-run the read census — the tier is the one consumer that could
   read belt tables between kicks; today's flight has none.]*
6. **The belt revival path** (both runs and the adjudication point here): a dense belt
   where conjunctions cluster on bodies could still be heavy-tailed *without* a driver —
   unmeasured; it is the one scene class that could revive a measured rank.
7. **The death channel at belt scale** (ea91): the 47–64 % promotion death rate is the
   battle pocket; measure the quiet belt's promotion mix (death vs dormancy) before
   sizing retirement vs demotion. The avalanche stream (Fano 8–28) is the allocator's
   target for burst absorption (PRINCIPLES #12).
   *[7f99: automation last — this direction and any allocator build fire after directions 0–2's
   deletions land; the quota expects ~10% back, the cast exception the candidate.]*
8. The haulers' far-field clock cadence per orbit is extrapolated from ~1 kick
   (0.03–0.3 % of an orbit measured); a full-orbit measurement needs ~10⁷–10⁸ game-s
   (wall-days) — only worth it if the ladder reaches the root-doll bulk. *[effb: the
   cadence law rate = 2⁷/P now explains why the haulers sit at ~1 kick per *measured
   window* without any separate far-field clock: their κ/P is simply small; no extra
   law is needed.]*
9. **Pick the belt's `step_log2` as a budget decision** (effb): the cold rail's whole
   CPU bill is 2^step_log2/P summed over the period mix; the billion's event load is a
   content policy, not an engine property — set it when wiring shipmem, with the
   encounter term (not the kick) as the binding constraint it must leave room for.
10. **The second seam now binds F1** (the fix removed the wave's monsters): 1-event frames at
   37.7/90.3/123.8 ms for 10⁵/2×10⁵/3×10⁵ burn, every ~50 frames (the player's item cadence), burn
   only — and from 5×10⁴ up (19–22 ms there, both engines, the same frames: it predates the fix;
   checker 4487) — the player's own item cost under burn (a2c1's walk-all and cap candidates name
   the suspects); unnamed, cheaper to diagnose than the pull was.
11. **The mid-drain cut** (16,000 game-s): the fixed engine's digest differs there by exactly the
   drain's unfinished share (11,473 events at 2×10⁵) — a cut is canonical for the held pull only
   once no held key remains below it; the rung writer's cut choice must respect that (or the settle
   must drain before the digest, which it does — the residual is the *flight's* pace, not the
   settle's).
12. The wall-schedule instability of the belt digest on shipped main (two pristine runs differ):
   worth its own run — it breaks the "digest independent of schedule" contract at 2×10⁵ belt scale
   even without any fix; the deterministic-budget mode (`NLADDER_EBUDGET`) is the instrument until
   it is understood.
13. The standing directions from a2c1 (the caps, the density rule, the per-body window), 0e37 (the
   two-word completion), b29a (the filter promotion), and the ladder's 10⁶ arm.

## Contradictions

- None open on this topic. (The main/taleb-6138 page conflict was two concurrent current-bests; both
  blocks are kept above, the newer first.)

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261014-0000-fermi-3071 (silver): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor; checker: cold-belt 13×, 6.4× at σ0.3, darwin domain p ≤ 8192 M.
- 20261014-1221-components-0e37 (silver): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
- 20261014-1511-components-a2c1 (silver): the scan seam censused — unpoisoned keep 15+2 at every N, the write-once `speed_cap` poisons the window ±9×r (walked 203, 12×), the density rule walks all dolls at N=10³ (1,017, 60×); capture dearer at 10³ (178 µs) than at 10⁵ (129 µs); fixes named in cost order.
- 20261014-1631-library-7f99 (gold): the library mined verbatim (4,580 highlights cached); deletion audit 26 kills / 2 landed add-backs (8%; law level at quota, frame path 0%); automation debt 6 anchored sites; promotion = refusal filter; lookup budget 427–877 recompiles/frame vs demand ≤ 1.4/s.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315 ms/1,213 ms single frames at 10⁵/2×10⁵ burn (seed-stable), the batch = wave density × the player's item horizon at universe.rs:769, coast 12.0 ms through the same wave; fix named (hold the scan), rung must fly past the wave.
- 20261014-1719-dynamics-bf21 (this run, awaiting grade): the wave is a standing train; the look-ahead pull capped holds 2×10⁵ burn at 11.97 ms max (114×) with the digest bit-identical; holding the whole scan is digest-refuted.
- 20261014-1719-fermi-cf45 (awaiting grade): the belt's clock is the doll's (P_D 77.24 d, interval 2.814e4 s flat in a, 24x the own-period law); effb's rate law corrected 24x at the plane's belt (its 1-2 AU core numbers move little; the anchor does not); shipped step_log2 148x over at flying pace; dial anchor P_D.
- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the wave's freeze deleted — pull held at 64, a budgeted drain, Waiting scans; 315→37.7 ms at 10⁵, 1,213→90.3 at 2×10⁵, 1,280→123.8 at 3×10⁵; bit-exact at every canonical cut past the drain; the mid-drain cut and the belt digest's wall-schedule instability named.
- 20261014-2012-components-38bf (awaiting grade): the input seam bounded — 0.17–0.23 ms a decision mid-wave under the cap, monsters 1,487→12.5 ms, digest bit-identical, +1 to +2 encounters per 657 no-op decisions (checker: 0.15–0.16 ms even uncapped; silver).
