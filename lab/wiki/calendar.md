topic: calendar
status: open
closed-by:
valid-while:
updated: 20261019-1817-dynamics-45c0

# The 10⁹ schedule: the calendar is the store's own order

## Current best

**NEW (45c0, dynamics — the checker-found "persistent ~2× tail" resolved: it is a mixing transient with
two regimes, not a standing tail, and the genesis stagger lands the belt at its stationary state at
birth).** Instrument: `crates/universe/examples/genesis` (this run's patch; the d520 arm's own
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

**Prior standing (d520's census, retained, with its checkers' horizon note now resolved):** the
chained clock's step spread is draw-invariant, a quantized-period belt never combs, the mechanism is
position (y = U_P(x) + c), the genesis train is one law-level object (C50 40–58× at birth, shearing
2.6–3.0%/fire), and the checker's "at g = 9..16 C50 plateaus at 2.2–3.0× — a persistent ~2× tail, not
a decay to uniform" is **superseded by (2) above: the plateau is the shoulder of the mixing transient
at the horizon's edge** (both instruments recomputed on one flight by the checker — they coincide from
g ≈ 12 (span ≥ 98% of the step) and the step-denominator readings are 2.00/1.63/1.35/1.05 at
g = 13–16, so the 2.2–3.0 plateau is not reproducible on the shipped-draw arm at either seed; most
plausibly it was read on d520's slower-σ fresh arms (classes=1: σ 3.9% mixes ~2× slower and would
still read 2.2–3.0 there)).

## Refuted

- **NEW — "The wave does not fall below 2×: a persistent ~2× tail, not a decay to uniform" (d520's
  checker1, and the page's carry of it)**: on the same 2,700-body arm, C50 crosses 2.0 at g = 13–14,
  reads 1.05 at g = 16 and 1.27–1.53 at g = 17–24; the tail is the shear plateau of the birth step
  law ending in phase mixing at g ≈ 1/spread (20261019-1817-dynamics-45c0).
- **NEW — "The stagger is only a wave lever" (the page's implied scope)**: the stagger arm sits at the
  stationary Poisson-level load from genesis (C50 1.03–1.07 flat to g = 14, load_max 1.26–1.47) with no
  regrowth — no attractor exists on the chained clock's dues map (20261019-1817-dynamics-45c0).

- "The queue is a first-break candidate at 10⁹" (the board's focus list): the schedule closes at ≤ MB
  of cursors inside a class-major per-body store (20261017-0005-fermi-25ce).
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

1. The stagger's B-gate flight (kick-cadence od 8) — now with a stronger adopt statement: exact in the
   stationary measure, not merely a wave flattener. Its legality question (does any observer read a
   body between its staggered genesis and first kick) is unchanged and unflown.
2. The residual standing excess over Poisson once mixed — **promoted from "small" by the checker's
   flights: it is standing, not decaying** (max/μ 1.54–1.92 flat from g = 25 through g = 40 vs floor
   1.378 ± 0.080 at μ = 42; p99/μ ≈ 1.58 vs 1.336) and it does not shrink at 4.33×N (belt 11,700:
   1.83 at g = 20 vs floor 1.185 at μ = 183 — the relative excess grows with μ, so the correlated
   clusters scale with N). Price its source (step-law discreteness vs the slow-shear neighbour pairs,
   whose number per window grows with N) before calling the mixed state Poisson for the 10⁹ ledger;
   until then the worst-frame number at 10⁹ carries this uncertainty, not 1.05×.
3. The wide-draw arm ([1,5) AU, σ 28.5%): predicted ~3.6× faster mixing (g ≈ 4), unflown; one flight
   confirms mixing ∝ 1/spread as a design dial for belt genesis at 10⁹.
4. The store-class decision at wiring (od 3, unchanged), now with the between-fires news priced:
   the next-due word moves by drift ~6×10⁻⁵ of itself per fire, so its low bits are cheap to recompute
   and the carried word can be coarser than the due itself.

## Contradictions

None open on this run's own evidence: the both-instruments recompute (checker, exact conversion
C50_step = C50_span·span/step_med, plus the birth dump: 57.9×/3.0) closes the author's instrument
question in the refutation's favour. The unexplained residue is d520 checker1's plateau attribution
(which arm it was read on — its own log is not in this tree); treat the "persistent tail" line as
refuted on the shipped draw (two seeds, two N, both instruments), and check slow-σ arms separately
before quoting any late-g number for them.

## Runs
- 20261017-0005-fermi-25ce (fermi, awaiting grade): the 10⁹ calendar priced — no per-body
- 20261017-2038-quant-b4a8 (quant, awaiting grade): the bulk runs the chained clock, not
- 20261017-2330-second-20261017-2038-quant-b4a8-d520 (second author, awaiting grade): the
- 20261019-1817-dynamics-45c0 (dynamics, awaiting grade): the "persistent 2× tail" is a two-regime
