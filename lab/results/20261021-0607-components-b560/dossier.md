# Dossier — the calendar's family intern key: the engine owns it, the belt's clock lost it

**Run:** 20261021-0607-components-b560 (components lens). **Topic:** formation-family (od 2, the
engine-side key census); the board's families row ("how long a member's certificate lasts
against its separation") and the calendar's per-body slots.

## Claim (one sentence)

The shipped engine already has the calendar's family intern key — two same-orbit planets
δx = 10⁶ root apart co-fire at ONE key through 383 fires (25,525/25,525 censuses, identical
steps) on the doll split's aligned grid — but the belt's ships cannot use it: the chained
fictitious clock derives every interval from the body's own continuous state, so 16 same-orbit
members hold 16 distinct keys from the very first due at every separation δx = 10²–10⁶ root
(1.5 km to 1.5 Mm), a pre-word barrier a877's w11 does not touch.

## Bottleneck

The board's families row (~10² in memory, ~10 in kicks): a same-(E,L) family's F members
currently cost F calendar slots (`ship_ticks`, part of the 156 B/body apparatus, calendar page)
and F fires. The floor is one slot and one fire per family per epoch (PRINCIPLES 33: "a body
resolves only the influences that are significant at its own scale" — at the parent's scale the
family is one body). Idiot index while unshared: F× on slots and F× on fires. This run measures
which representation decision of the shipped engine blocks the sharing, and shows the engine's
own existing mechanism (the aligned grid, step.rs:19 "every interval starts on a multiple of
its own length") already delivers the floor's key half for doll-split bodies.

## Evidence (all numbers from `census-r{1,2}au.txt`, regen: `regen.sh`, each run < 20 s wall)

Harness: restricted problem — star, one source planet of 1/1000 at r, families of F = 16 ships
on one circular orbit at r (same r, e = 0; members at phase offsets = δx root along-track,
phase = "fraction of the radial period since periapsis, Q32"), plus a clone control (all 16
identical spec) and an aligned-grid pair (2 `Kind::Planet` bodies, same r/e, δx = 10⁶). Census:
jump `advance` to the earliest pending due; read every body's `next_time` (the calendar's own
key) once per generation. r = 1 AU (`census-r1au.txt`, 25,525 censuses) and r = 2 AU
(`census-r2au.txt`, 25,526 censuses).

- **Clone control: 100% co-fire, one distinct key, 350 fires, zero spread** (anchor/step/dues
  identical) — the instrument and the engine's determinism on identical bodies hold.
- **Ship families (chained clock): fork at index 0 — 16 distinct dues at EVERY census, from the
  first recorded due, at δx = 100, 10³, 10⁴, 10⁵, 10⁶ root.** `mean_distinct_dues = 16.00`,
  `anchors_eq = steps_eq = false`. This is not the 61-bit word: the first dues differ before
  any kick has landed (birth anchor = own event tick; interval = `ext.ticks(ext.time(y, ds))`
  of the body's own state, plan_clock step.rs:626-654 — a continuous per-body quantity, no
  grid). First-due spread at birth: 18,415 ticks (δx=100) to 5.4×10⁸ (δx=10⁶), i.e. 12–36× the
  members' light-time separation; last-due spread after ~300 fires grows to 5.3×10⁶ –
  1.9×10¹⁰ ticks. Same verdict at r = 2 AU.
- **Aligned pair (doll split): co-fire at every one of 25,525 censuses, stream never forks
  through 383 fires, identical steps 2³⁵** (r = 1 AU; at r = 2 AU: 25,526/25,526, 192 fires,
  steps 2³⁷). Two bodies at δx = 10⁶ root — a million km — share ONE calendar key despite
  different kick differentials at their different phases: the aligned grid absorbs the
  differential (the grid moves only when the step changes by a factor of 2, which the tide's
  differential never triggered in 383 fires).

## Predictions (`predictions.md`, written before the decisive run)

- Held: (1) the clone control co-fires bit-identically forever (instrument valid).
- **Wrong, informatively:** (2) I predicted the word split would not reach the calendar at
  kick 0 and g_fork ≫ 1 — in fact g_fork = 0 at every δx, for a stronger reason than the word:
  the chained clock's interval and anchor are per-body continuous quantities, so members'
  dues differ from birth by more than their light-time offsets. (3, 5) moot (no sharing ever
  begins, so no δx-trend and no re-joining; distinct dues stay 16 at every census). (4) the
  compression exists, but only on the aligned grid (the planet pair), not on the ships' clock.
  The failure of (2) is the result: the sharing barrier is the clock's representation, upstream
  of a877's word barrier.

## What would make it wrong

The harness is the restricted problem with circular families (e = 0), one source planet,
co-orbital with it; eccentric members, belt radii with synodic drift (planet at 1 AU, ships at
2.2–3.5 AU), and real fleet dolls (`fleet.rs`, whose members are doll bodies — and may already
sit on aligned grids; unflown) could change the fork structure. The pair arm is two bodies
only; a 16-planet aligned family at large F could hit the step-size factor-2 fork (the one
mechanism that breaks key sharing on the grid) at longer horizons than 383 fires. The mechanism
reading (plan_clock as the barrier) is from the code path, not from a patched flight — a ship
family flown on an aligned grid (the law change this run points to) is the named next
experiment.

## Cost of adopting, and fit with PRINCIPLES

Adoption is not a drop-in: giving root-doll ships a family-anchored grid (the member reads the
family reference's aligned step; its own chained clock refines only when its certificate Ξ
crosses) is a law change on the belt's clock, gated exactly like the w11 plane (B13/B12/B17/B18,
the page's od 1). The payoff this run prices: F→1 calendar slots and F→1 fires per family epoch
on the families row, with the engine's own aligned mechanism as precedent — no new part
(PRINCIPLES 17: "the best part is no part"; 19: "a fix signals the wrong representation" —
here the fix already exists in the same engine). Numbers are Linux/x86 cloud timings; orders of
magnitude only.

## The lens

The components lens priced one component (the calendar's per-body slots for formations) against
its floor (one key per family) and measured the shipped gap (F×, from census 0). What it may
have missed — the neighbours: the fires themselves (kick compute) still fork at any word until
a877's w11 lands, so the memory half can be adopted alone but the kick half cannot; and the
census reads `next_time`, not the queue's deadline keys (`key_of`, deadline + moved), which
could merge keys the dues separate — a coarser intern than the dues allow, unmeasured.
