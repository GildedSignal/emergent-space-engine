# Dossier — 20261012-2257-scout-64e4 (lens: scout)

**Claim.** The per-frame deadline rekey is *proven schedule-only on shipped code* — three genuinely
divergent rekey policies (shipped every-advance, never, lazy-on-player-motion) end every probe with
a bit-identical canonical digest — so the fixed tier can be deleted outright, and the only channel
that ever made a lazy calendar "break digests" is the session's habit of logging the player's keys
at the frame's *presented* tick, whose pacing leak and its grid fix are both demonstrated here on
the shipped public API.

**Bottleneck.** `frame-cost` open direction 1 (board: "what deletes the per-frame rekey…"). The
expected gain is not new speed from me (the build is Sonnet's `wt/frame`) but the removal of the
one risk that can kill that build: gate F1 demands "every digest bit for bit", and a correct lazy
calendar will *look* to break it whenever decisions ride the presented tick. This run supplies the
missing determinism-safe construction: any deadline policy + decisions logged off the presented
tick.

**Evidence** (all from `bash lab/results/20261012-2257-scout-64e4/regen.sh`, ~3 s after a ~10 s
build, Linux i7-4790-class, single-threaded, under 200 MB):

- **E1 — schedule-only, proven by divergence + identity.** Scripted decisions at canonical ticks
  (`schedule`), a moving player, starved to one resolved item per frame (`Budget::events(1)`, so
  the deadline calendar alone chooses *which* entity resolves). Seeds 1 and 3, 48 and 400 members,
  8 and 60 game-seconds:
  - digests bit-identical across shipped/never/lazy in every triad (e.g. seed 1, 60 s:
    `e38b245b…` ×3; seed 3, 60 s: `35812c30…` ×3; 400 members: `2dbc92e4…` ×3);
  - the schedules really differed: the per-frame queue-front fingerprints differ in every triad
    (`b93fba44…`/`af34e9dd…`/`edbf9a46…`), and at 60 s even the frame counts and event streams
    differ (3637/3634/3636 frames; 3653/3650/3652 events), with kicks 15/15/15, encounters 8/8/8,
    contacts 3/3/3 (seed 1) and kicks 12/12/12, encounters 5/5/5 (seed 3);
  - with a 60 s flight that contains kicks and encounters, and unstarved runs agreeing with
    starved ones, the invariance is not an artifact of a quiet scene.
- **E2 — the leak and the fix, on the shipped API.** The same wall timeline of four key flips,
  three presentation rates, rtf 100, one cut:
  - `raw` (exactly what `xtask/src/universe/session.rs::step` does — `input(u.now, keys)` at the
    frame boundary): three *different* digests per seed across 30/60/144 Hz, and the canon itself
    moves (seed 1 encounters 39/37/38, contacts 17/14/14; seed 3 encounters 22/23/23);
  - `grid` (the fix shape, two lines: the decision tick derived from the wall timeline and snapped
    up to a canonical 2²⁰-tick grid via `schedule`): one digest per seed across all three rates
    (`7b8f956c…` ×3, `f5b97834…` ×3), encounters 30/30/30 and 19/19/19.
- **E0 — what the one-switch deletion buys (and what it does not).** Quiet frames (events = 0),
  `pop` synthetic populations of individual bodies: rekey on/off 188.6/152.7 µs at 1,001 bodies
  (−19%, ≈36 ns/body) and 2.30/2.07 ms at 10,001 (−10%, ≈23 ns/body); the plane itself (28 bodies)
  16.7/11.1 µs (−34%). Consistent with the page: the rekey walk is a minority of the tier — the
  drain/defer/requeue passes own the rest — so the *full* deletion (min-peek, lazy deadlines) is
  the build's job; this run's contribution is the licence to do it.

**Predictions** (`predictions.md`, written before any decisive run): P1 held (identity under
divergence, including the held-out seed-3, 400-member and 60 s cases); P2 held (three digests in
raw mode, independently of taleb-40c0's harness); P3 held after one harness correction — my first
grid arm quantized the *presented* tick and still leaked (a useful negative: quantizing `now` does
not fix it, because adjacent pacings can straddle a cell boundary); the fix that holds derives the
tick from the *wall* timeline. P4 partially held: the on/off delta is the rekey share only
(10–34%), drain dominates, as the page's refutations predicted.

**What would make it wrong.** A scene where an outcome secretly reads a deadline or the observer:
`pos` and `observer` are documented "for deadlines only; never an outcome" (`universe.rs`), and
E1 is direct evidence, but the probes cover plane scenes ≤ 400 members and 60 game-seconds with
one flip pattern; a fleet-scale or 10⁶-body scene with hand-outs in flight is the untested corner
(hand-outs are queue items too). The grid fix's cost is input latency ≤ one grid cell (2²⁰ ticks ≈
5.2 game-s at rtf 100 with this Q) and a canon change relative to today's raw-logged histories.

**Cost of adopting.** Near zero for the diagnosis; the switch itself (`rekey_on_advance`, default
shipped) is 8 lines in `universe.rs`; the real adoption is *sequencing*: land canonical decision
logging (E2's two lines, the held a342 shape) **before or with** `wt/frame`'s lazy calendar, or
gate F1's digest criterion will fail honest builds. Fit with PRINCIPLES: "no work for no reason,
so no ticks" (¶14) — a zero-event frame that still touches every body three times is exactly the
forbidden tick; and "the simulation decides" (¶22): scheduling is ours to change freely, which E1
now proves for the deadline tier.

**The lens (scout), and the cross-field map it owes.** Requirements: 10⁴–10⁶ entities, ≤ 16.7 ms
frame, digest = f(cut) only, zero-event frame ≈ free, deterministic. The structures that already
solved it: **timing wheels** (Varghese–Lauck 1987; the Linux kernel timer wheel; Kafka's
purgatory — millions of timers, O(1) touch, and *no* implementation re-evaluates timers because an
unrelated body moved; UNVERIFIED at source) and **calendar queues** (Brown 1988; two-level
variants, Ronngren–Ayani 1997, UNVERIFIED) — the lab already measured these in-house
(4955's monotone bucket wheel, 4211's dyadic wheel + skin, 7–20×). The determinism contract is
**parallel DES's committed state** (Chandy–Misra, Time Warp, Jefferson 1985 — schedule-independent
canon; UNVERIFIED), which the engine already implements (taleb-40c0); this run extends it from
budgets/threads/pace to the *deadline heuristic itself*. The session fix is game-engine canon
("fix your timestep", deterministic lockstep: log inputs on the simulation's grid, never at
presentation time; UNVERIFIED). Known failure modes carried over: wheel bucket overflow at one
horizon (pick the span by the deadline horizon), calendar resize storms, and grid latency in the
input path. What the lens may have missed: everything above is scheduling-side; if `wt/frame`
finds an outcome that *does* read a deadline (a horizon promise somewhere), E1's domain is the
record to re-run first.
