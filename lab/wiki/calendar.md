topic: calendar
status: open
closed-by:
valid-while:
updated: 20261020-0036-components-6b9a

# The 10⁹ schedule: the calendar is the store's own order

## Current best

**NEW (6b9a, components — the apparatus itself is measured on shipped code, and the
record's single-queue framing undercounts it 5×: the live plane's scheduler is FIVE
per-body calendars plus the deadline position cache, 156 B/body at the shipped
`body_cap` sizing, two of the five holding the whole population at every census — and
the same next-tick fact sits in both).** Instrument A (counting allocator around the
shipped `Calendar::new`, no engine change): key `Scalar` 16 B, slot 24 B, **exactly
28.00 B/slot, N-flat 10⁴→10⁶**, capacity reserved once at `body_cap`
(universe.rs:481–490 for all five; `pos` 16 B/body at :479) — 156 B/body = **156 GB
≈ 19.5× the 8 GB machine at 10⁹**, while live-population sizing (L = λ·τ·N =
4×10⁻⁵ × 43.6 × 10⁹ ≈ 1.74×10⁶ slots, λ and τ from 0659) costs **0.272 GB ≈ 3.4% —
a ×573 flip on a sizing policy alone, same shipped code. [Checker, 20261020: the flip
is real at the orders measured, but not capacity policy alone — `Calendar` slots ARE
body ids (`pos` indexed by id, `set` errs on slot ≥ len, no growth path), so live
sizing needs dense live ids at promotion or 25ce's cursors.] Instrument B (census on
the nladder driver, print-only `sched_census` getter): at K = 10⁴ and 3×10⁴, through
steady kicking (≈3,000 kicks a census window), **`ship_ticks` = 1.000–1.002×N and
`waiting` = 1.000–1.002×N at every census, with identical counts (30,043/30,043) —
two whole-population tick-keyed containers over the same bodies; `child_ticks`
(311–333) and `prunable` (105–108) are the locals' absolute scale, N-independent;
`queue` = 5–6** (the always-queued few); live slot content ≈ 72 B/body. [Checker,
20261020: extended on three arms — N = 10⁵ (identical: 100,023/100,023, locals
311–333/105–108 absolute), horizon 2.5 belt steps at K = 10⁴ (no drain, prunable
103–107 absolute), and a wave arm at rtf 10⁵ (1667 gs/frame): there `waiting`
oscillates 0.04–0.98×N and `queue` swings 259→9,642 — "waiting ≈ N" is coast-regime;
the regime-invariant facts are `ship_ticks` = 1.001×N always and queue+waiting ≈ N
(100,046 = N+18 at every wave census), so the ≈72 B/body live content and the 156
B/body capacity are regime-independent; `prunable` peaks at 312 (0.03×N) in waves.]
The CPU
neighbour is a non-issue (heap ops 31/38/333–364 ns at n = 10⁶, ≥120× under the
fired item's 44.7–82.5 µs): the apparatus is a bytes component. **Composition
correction:** the 10⁹ ledger's wired memory row (1.7–2.4 B/live-body, 07b4) is a
store-only number and no row prices the scheduler (grep-checked; the record's only
queue-byte entries are 6a0e's single-calendar 16→8 B scan and 25ce's cursor design),
so "wired 0.2–2.0×" holds ONLY if the calendars are deleted or live-sized — unnamed
wiring work; unresized, the scheduler alone is 20× the machine. All of it is
schedule-only state (universe.rs's header: the queue's order never reaches an
outcome; 9c67/d65c's digest-indifference proof for `pos`). Coast-only census, one
scene family, rtf 1000, x86 → orders (20261020-0036-components-6b9a; `regen.sh` ~2 min
cold; predictions pre-registered: P1/P2/P3/P6/P7 held, P4/P5 failed — child_ticks and
prunable are locals-scale, which sharpens the two-container redundancy).

**Prior standing (45c0, dynamics — the checker-found "persistent ~2× tail" resolved: it is a mixing transient with
two regimes, not a standing tail, and the genesis stagger lands the belt at its stationary state at
birth).** Instrument: `crates/universe/examples/genesis` (that run's patch; the d520 arm's own
population — 2,700 belt, seed 1, shipped `plane_extra`, census at head + g·1.03·step_max; C50 over the
dues' own span, which coincides with the page's step denominator once the span saturates, g ≳ 14), plus
one added method (`Universe::stagger_genesis`: each root-doll ship's genesis plan delayed by hash(id)
mod one median step; a scene variant, drift exact until the first kick). The law, both seeds agreeing:
(1) **Shear regime (gens 1–7): C50(dues)/C50(steps) = 0.99–1.00 (min 0.987) at every census** — dues(g) = due(0) +
n·F is a monotone image of the step law, so the early "plateau" is the birth step distribution showing
through, computable at genesis with zero fires (step law at birth: median 5.714×10⁹ ticks, p1–p99
spread 7.84%, C50 3.05; the genesis train's first-dues span is 5.3% of one step = the 58× wave).
[Checker, 20261019: verified at birth on the rerun's own census dump — C50(due0) = 57.9 on the step
denominator (d520's 58.2 reproduced) and 3.0 on own-span, i.e. the train *is* the step law's own shape.]
(2) **Wrap + mixing (gens 8–24): the dues span saturates at one step and the concentration breaks away
from the still-3.2–3.4 C50_steps and decays toward uniform** — 2.02 at g=13, 1.64 at g=14, 1.05 at g=16
(a phase-lucky census; the shoulder 1.44–1.53 follows), 1.27–1.53 at g=17–24, ~1.2 from g=25;
battalion 1 in all 55 census rows on all arms; mixing at g ≈ 1/spread ≈ 13 fires (the birth draw
is the dial: checker2's σ-28.5% [1,5) AU arm would mix ~3.6× faster; the iid-uniform C50 floor at
n = 2,700 is 1.032 ± 0.014, so 1.05/1.03 stagger-side is floor-level). (3) **The stagger arm kills the
whole phenomenon at birth: C50 1.05 at g=0 and 1.03–1.07 flat through g=14, no regrowth** (the uniform
stagger is invariant under the shear — no attractor exists to re-grow the tail), with per-window load
Poisson-level from genesis (max/μ 1.26–1.47 against a Poisson floor 1.378 ± 0.080 at μ = 42; the ship
arm reads 18.9 at g=0 decaying to 1.85–2.11, p99/μ 17.4 → 1.56–1.80). (4) **News rate:** the
birth-data forecast (due ≡ d0 + k·s0) holds phase to 1% for ~16 fires (fc_p50 crosses 0.01 at g = 16,
reads 1.45% at g = 19; 2.2% at 25 fires, p90 4.8%); the per-fire step drift is p50 6.0–6.9×10⁻⁵, p90
1.2–1.9×10⁻⁴. Consequences: the belt's *genesis* load wave (the 19× birth spike) is a ~16–25-fire
≈ 5–8-game-day transient with no re-growth and no attractor; the stagger's adopt statement strengthens
from "flattens the train" to "exact in the stationary measure"; and the calendar key stays the carried
next-due word, but its between-fires news is priced at 6×10⁻⁵/fire — a birth-derived schedule with
drift corrections is valid to 1% for ~16 fires. **The post-mix load tail is NOT deleted:** max/μ stands
at 1.54–1.92 from g = 25 through g = 40 (checker flight) against the Poisson floor 1.378 ± 0.080, and
at belt 11,700 (μ = 183, floor 1.185) it reads 1.83 at g = 20 — the excess over iid does not shrink
with N, so "no standing-tail mitigation needed at 10⁹" is premature until od 2 prices it.
[Predictions: P2 (regrowth) and P5 (C50 stays > 2) killed as pre-registered; P3 held; P4 held to
g = 15, letter-failed from g = 16 (the dossier's "g ≈ 19" overstates the break).]
[Checker, 20261019: reproduced bit-identically (fresh `ship 3000 2 1`), and extended past the author's
range on both axes: horizon g = 40 at 2,700 (C50 → 1.19–1.23, load_max flat 1.54–1.92, fc_p50 0.057),
and N = 11,700 belt (C50 trajectory identical g-for-g: 1.02/1.48/1.55/1.50/1.45 at g = 16–20 — the
mixing time is N-independent, so the ~13–16-fire scale extrapolates toward 10⁹; the load excess is the
one number that does not.]

## Refuted

- **NEW — "the event queue's byte price is the single-calendar 16→8 B question" (the
  record's framing under 6a0e's silver and 25ce's refuted line, which priced ONE
  queue): the shipped apparatus is five calendars at `body_cap` + the 16 B `pos`
  cache = 156 B/body measured, two containers whole-population and mutually
  redundant; 6a0e's 8 B scan applied to all five still leaves 56 B/body = 56 GB at
  10⁹ — the lever is the sizing/deletion, not the container swap
  (20261020-0036-components-6b9a).**
- **NEW — "the wired 10⁹ memory row (0.2–2.0×) is a composition of the wired plane":
  it is a store-only number (07b4's 1.7–2.4 B/live-body); unresized scheduler state
  adds 156 B/body ≈ 19.5× the machine, so the closure sentence silently assumes the
  calendar deletion no row names (20261020-0036-components-6b9a).**
- **NEW — "the queue is a first-break candidate at 10⁹" (the board's focus list): the schedule closes at ≤ MB
  of cursors inside a class-major per-body store (20261017-0005-fermi-25ce).** [6b9a
  note: true of the DESIGN; the shipped code it would replace is the 156 B/body
  apparatus this run measures.]
- "The program classes are interchangeable on memory fit" (e7ef's composition reading): the calendar
  axis keeps any per-body who-enumeration ≥ the 3.6 GB permutation floor (20261017-0005-fermi-25ce;
  checker2 note retained).
- A continuous per-body hash stagger as the compact plane's cure (f82a's form): must be quantized to
  classes in a compact store (20261017-0005-fermi-25ce; f82a's arms stand for the live plane).
- "The belt's step spread is set by the orbit draw" (b4a8's record): artifact of 2^ilog2 labels; the
  spread is the angle-drawn U_P term (20261017-2330-…-d520).
- "The shipped law is `aligned`, so next-due is grid-derivable" (the page's premise): the belt runs
  the chained clock; carried next-due state moves every fire (20261017-2038-quant-b4a8).
- "The comb (K=1) is a belt-scale danger on the shipped law": no battalions on the chained clock
  (20261017-2038-quant-b4a8; scope notes retained).
- "Shared exact (anchor, full) ⇒ shared ticks" (od 4's premise): the step is position-derived; 32
  shared classes give 2,700 distinct steps (20261017-2330-…-d520).

## Open directions

1. **The sizing flip is the cheapest 10⁹ memory lever this page owns** (6b9a): live-
   population capacity (L = λ·τ·N) turns 156 GB into 0.27 GB with the shipped
   `Calendar` code — a policy-class change plus dense live ids at promotion (slots are
   body ids and the calendar never grows; checker, 20261020), not an algorithm. The
   full deletion stays 25ce's class-major cursors (the next-due word is already
   carried: od 4 below).
2. **`waiting` duplicates `ship_ticks` over the whole population** (6b9a census,
   identical counts at every instant sampled): one key-range read of `ship_ticks`
   (pop while min ≤ target) replaces the second container; requires re-deriving
   `rekey`'s wake walk and `pull_ships`' min under due-pop transiently absent. Named,
   not built.
3. The stagger's B-gate flight (kick-cadence od 8) — now with a stronger adopt statement: exact in the
   stationary measure, not merely a wave flattener. Its legality question (does any observer read a
   body between its staggered genesis and first kick) is unchanged and unflown.
4. The residual standing excess over Poisson once mixed — **promoted from "small" by the checker's
   flights: it is standing, not decaying** (max/μ 1.54–1.92 flat from g = 25 through g = 40 vs floor
   1.378 ± 0.080 at μ = 42; p99/μ ≈ 1.58 vs 1.336) and it does not shrink at 4.33×N (belt 11,700:
   1.83 at g = 20 vs floor 1.185 at μ = 183 — the relative excess grows with μ, so the correlated
   clusters scale with N). Price its source (step-law discreteness vs the slow-shear neighbour pairs,
   whose number per window grows with N) before calling the mixed state Poisson for the 10⁹ ledger;
   until then the worst-frame number at 10⁹ carries this uncertainty, not 1.05×.
5. The wide-draw arm ([1,5) AU, σ 28.5%): predicted ~3.6× faster mixing (g ≈ 4), unflown; one flight
   confirms mixing ∝ 1/spread as a design dial for belt genesis at 10⁹.
6. The store-class decision at wiring (od 3, unchanged), now with the between-fires news priced:
   the next-due word moves by drift ~6×10⁻⁵ of itself per fire, so its low bits are cheap to recompute
7. (6b9a) The census's unflown corners: a burn arm — its wave shape is proxy-flown by
   the checker at rtf 10⁵ (waiting drains to 0.04×N transiently, queue to 0.96×N;
   ship_ticks and the ≈N partition of queue+waiting invariant; capacity unaffected),
   a real burn arm stays unflown — a fleet-doll scene (does `child_ticks` become
   whole-population under a 10⁶-fleet doll?), and the M1 re-measure of the heap-op
   constants.

## Contradictions

None open on this run's own evidence: the both-instruments recompute (checker, exact conversion
C50_step = C50_span·span/step_med, plus the birth dump: 57.9×/3.0) closes the author's instrument
question in the refutation's favour. The unexplained residue is d520 checker1's plateau attribution
(which arm it was read on — its own log is not in this tree); treat the "persistent tail" line as
refuted on the shipped draw (two seeds, two N, both instruments), and check slow-σ arms separately
before quoting any late-g number for them. 6b9a's apparatus measurement composes with 25ce's cursor
design (the design is the deletion; the measurement is the shipped cost it deletes) — no conflict.

## Runs
- 20261017-0005-fermi-25ce (fermi, awaiting grade): the 10⁹ calendar priced — no per-body
- 20261017-2038-quant-b4a8 (quant, awaiting grade): the bulk runs the chained clock, not
- 20261017-2330-second-20261017-2038-quant-b4a8-d520 (second author, awaiting grade): the
- 20261019-1817-dynamics-45c0 (dynamics, awaiting grade): the "persistent 2× tail" is a two-regime
- 20261020-0036-components-6b9a (components, awaiting grade): the apparatus measured — five calendars + pos = 156 B/body at body_cap (19.5× the machine at 10⁹; ×573 flip to live sizing), ship_ticks and waiting both whole-population and redundant, the wired ledger row store-only.
