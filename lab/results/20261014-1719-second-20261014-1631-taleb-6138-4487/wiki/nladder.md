topic: nladder
status: open
closed-by:
valid-while:
updated: 20261014-1719-second-20261014-1631-taleb-6138-4487

# The N ladder: 28 live bodies toward 10⁹

## Current best

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

## Refuted

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

## Open directions

0. **The second seam now binds F1** (the fix removed the wave's monsters): 1-event frames at
   37.7/90.3/123.8 ms for 10⁵/2×10⁵/3×10⁵ burn, every ~50 frames (the player's item cadence), burn
   only — and from 5×10⁴ up (19–22 ms there, both engines, the same frames: it predates the fix;
   checker 4487) — the player's own item cost under burn (a2c1's walk-all and cap candidates name
   the suspects); unnamed, cheaper to diagnose than the pull was.
1. **The mid-drain cut** (16,000 game-s): the fixed engine's digest differs there by exactly the
   drain's unfinished share (11,473 events at 2×10⁵) — a cut is canonical for the held pull only
   once no held key remains below it; the rung writer's cut choice must respect that (or the settle
   must drain before the digest, which it does — the residual is the *flight's* pace, not the
   settle's).
2. The wall-schedule instability of the belt digest on shipped main (two pristine runs differ):
   worth its own run — it breaks the "digest independent of schedule" contract at 2×10⁵ belt scale
   even without any fix; the deterministic-budget mode (`NLADDER_EBUDGET`) is the instrument until
   it is understood.
3. The standing directions from a2c1 (the caps, the density rule, the per-body window), 0e37 (the
   two-word completion), b29a (the filter promotion), and the ladder's 10⁶ arm.

## Contradictions

- None open on this topic. (The main/taleb-6138 page conflict was two concurrent current-bests; both
  blocks are kept above, the newer first.)

## Runs

- 20261014-1719-second-20261014-1631-taleb-6138-4487 (awaiting grade): the checker's named gold
  experiment done — the held pull bounds the wave (1,213→90.3 ms at 2×10⁵, 3×10⁵ landed at 123.8 ms)
  and is bit-exact at canonical cuts; the second seam and the main's own schedule instability found.
- 20261014-1631-taleb-6138 (silver): the wave's ruin basin measured — 315/1,213 ms single frames at
  10⁵/2×10⁵ burn, the batch = wave density × the player's item horizon at universe.rs:769; fix named.
- 20261014-1631-library-7f99 (gold): the deletion program's method — 26 kills, the 10% add-back
  quota, automation last, promotion a filter.
- 20261014-1511-components-a2c1 (silver): break 3's scan half decomposed — the cap's monotone walk
  and the inverted density rule.
- 20261014-1221-components-0e37 (silver): break 2's lever — the compiled orbit is write-only memory,
  its one reader the view's ramp.
- 20261014-0450-scout-b29a (silver): the smallest promotion is no promotion.
- 20261014-0059-fermi-effb (silver): the 10⁹ ledger composed; the cadence law code-verified.
- 20261014-0000-fermi-3071 (silver): rule 2 dead by decomposition; the tail manufactured.
