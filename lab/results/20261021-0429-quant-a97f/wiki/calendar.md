topic: calendar
status: open
closed-by:
valid-while:
updated: 20261021-0429-quant-a97f

# The 10⁹ schedule: the calendar is the store's own order

## Current best

**NEW (a97f, quant — od 4 executed: the standing worst-window excess is priced, attributed and bounded; neither of the page's two candidates).** 45c0's genesis census + a per-generation dump (id, due, step, a), shipped `plane_extra` seed 1, belts 2,700 (g≤40) and 11,700 (g≤20); counterfactual arms on a constant-step model valid one-fire-ahead to 6.4×10⁻⁵ periods (pred max/μ 1.801 vs meas 1.790), uniform-phase control on the floor. **Split (2,700 seed 1, g≥25, excess 0.33 over floor 1.375 [p10 1.280, p90 1.470]): ~57% the dues' own marginal non-uniformity** (i.i.d. resample keeps 1.564 — the genesis train's window-scale remnant; C50(dues) ≈ 1.06–1.25 over g≥25), **plus a seed-1 pairwise part of +0.14 from phase-aligned near-locked pairs** (co-firing pairs |Δs|/s ≈ 3.5×10⁻⁴ vs 1.4×10⁻² random ≈ 40×, 75%/88% < 10⁻³ vs 4.2% (18–20×), |Δa| −8% — **not a-neighbours**; exact step collisions 0; jitter 10⁻⁵/10⁻³ null at a 5-fire horizon). At 11,700 the pairwise part reads the same +0.13 (pre-saturation anchors, C50 1.45–1.55); the checker-of-45c0's "excess grows with μ" is the floor shrinking (1.375→1.176) under a clumped marginal, not a growing correlation. [Checker, 20261021: seed 2 (2,700, g≤33): mechanism holds — excess 0.166, calibration 1.612 vs 1.610, A4 on floor, |Δa| −8%, 0 collisions, 18× near-lock enrichment — but A6 = A0 = 1.541, i.e. **the pairwise part is +0.00 there: the split is seed-dependent (0–0.14), only the marginal-dominance, no-shear, no-lattice verdicts are seed-robust**, and the plateau's magnitude halves (1.54 vs 1.72).] **Both halves are a transient: frozen steps (conservative — measured drift 5×10⁻⁴→2.5×10⁻³/fire, growing, only accelerates mixing) reach the floor by fire ~100–120** (evolve.py; window-scale mixing ~10² fires ≈ 6–8× the C50 time). [Checker, 20261021: engine flight, seed 1, to g=49 — the decay is real in the engine, not only the model: plateau 1.59–2.11 flat through g≈37, then falling to ≈1.44 (median g=44–49) with p99 1.33–1.35 ≈ floor p99, inside evolve's fire-matched band; **the floor endpoint past g=49 stays model-extrapolated**.] The 10⁹ worst frame therefore carries ×1.2–1.8 of mean only inside the ~10²-fire epoch after a coherent clumping — or never, with the hash stagger (floor at genesis, 45c0). No engine change; the ledger line may quote Poisson windows outside the epoch (20261021-0429-quant-a97f).

**Prior standing (6b9a, components — the apparatus): five calendars + `pos` = 156 B/body at `body_cap` ≈ 19.5× the 8 GB machine at 10⁹** (key 16 B + slot 24 B, N-flat 10⁴→10⁶; capacity reserved once); live-population sizing (L = λ·τ·N ≈ 1.74×10⁶ slots) flips it **×573 to 0.27 GB** with shipped code but needs dense live ids at promotion (slots are body ids; checker 20261020) or 25ce's cursors. `ship_ticks` and `waiting` both whole-population with identical counts at every census — mutually redundant (regime-invariant: ship_ticks = 1.001×N always, queue+waiting ≈ N; wave arm: waiting 0.04–0.98×N, queue 259→9,642); heap ops 31–364 ns ≥120× under the fired item's 44.7–82.5 µs — a bytes component. The wired 10⁹ memory row (07b4, 1.7–2.4 B/live-body) is store-only: "wired 0.2–2.0×" silently assumes the calendar deletion/live-sizing no row names (20261020-0036-components-6b9a).

**Prior standing (45c0, dynamics — the genesis tail is a two-regime mixing transient): shear regime (gens 1–7) C50(dues)/C50(steps) = 0.99–1.00** — the birth step law showing through, computable at genesis with zero fires (step law: median 5.714×10⁹ ticks, p1–p99 7.84%, C50 3.05; first-dues span 5.3% of one step); **wrap+mixing to C50 ≈ 1.2 by g≈25, mixing ≈ 13 fires** (N-independent to 11,700); **the hash stagger (`Universe::stagger_genesis`, hash(id) mod one median step) lands the belt at the stationary state at birth** — C50 1.03–1.07 flat, per-window load Poisson from genesis, no regrowth (exact in the stationary measure); the birth-data forecast holds phase to 1% for ~16 fires (drift p50 6×10⁻⁵/fire on its pilot; a97f's deeper census reads 5×10⁻⁴→2.5×10⁻³ growing — a mixing accelerator either way) (20261019-1817-dynamics-45c0).

## Refuted

- **NEW — "the residual standing excess over Poisson is the slow-shear neighbour pairs whose number
  per window grows with N" (od 4's leading candidate, from the checker's μ-growth reading): refuted —
  persistent co-firing pairs are spatially unlocalised (|Δa| −8% vs random pairs, both seeds), the pairwise excess
  reads +0.13–0.14 at seed 1 and +0.00 at seed 2 (never N-growing), and the μ-growth is the iid floor
  shrinking under a clumped marginal; the source is the dues' own occupancy pattern plus (seed-dependent)
  phase-aligned near-locking, both birth-frozen and self-decaying (20261021-0429-quant-a97f).**
- **NEW — "step-law discreteness" as exact lattice collisions: refuted — zero exact step collisions in
  both belts; jitter at 10⁻⁵ and 10⁻³ removes nothing at a 5-fire horizon (20261021-0429-quant-a97f).**
- **NEW — "the mixed state is Poisson at window scale once C50 ≈ 1" (the ledger's implicit assumption
  at g ≳ 16): refuted through g = 40 — max/μ 1.59–1.92 against floor 1.375 while C50(dues) sits at
  ≈1.1–1.25; window-scale mixing completes only at ~10² fires (20261021-0429-quant-a97f).**
- **"the event queue's byte price is the single-calendar 16→8 B question" (the
  record's framing under 6a0e's silver and 25ce's refuted line, which priced ONE
  queue): the shipped apparatus is five calendars at `body_cap` + the 16 B `pos`
  cache = 156 B/body measured, two containers whole-population and mutually
  redundant; 6a0e's 8 B scan applied to all five still leaves 56 B/body = 56 GB at
  10⁹ — the lever is the sizing/deletion, not the container swap
  (20261020-0036-components-6b9a).**
- **"the wired 10⁹ memory row (0.2–2.0×) is a composition of the wired plane":
  it is a store-only number (07b4's 1.7–2.4 B/live-body); unresized scheduler state
  adds 156 B/body ≈ 19.5× the machine, so the closure sentence silently assumes the
  calendar deletion no row names (20261020-0036-components-6b9a).**
- **"the queue is a first-break candidate at 10⁹" (the board's focus list): the schedule closes at ≤ MB
  of cursors inside a class-major per-body store (20261017-0005-fermi-25ce).** [6b9a
  note: true of the DESIGN; the shipped code it would replace is the 156 B/body
  apparatus this run measures.]
- "The program classes are interchangeable on memory fit" (e7ef's composition reading): the calendar
  axis keeps any per-body who-enumeration ≥ the 3.6 GB permutation floor (20261017-0000-fermi-25ce;
  checker2 note retained).
- A continuous per-body hash stagger as the compact plane's cure (f82a's form): must be quantized to
  classes in a compact store (20261017-0000-fermi-25ce; f82a's arms stand for the live plane).
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
   carried).
2. **`waiting` duplicates `ship_ticks` over the whole population** (6b9a census,
   identical counts at every instant sampled): one key-range read of `ship_ticks`
   (pop while min ≤ target) replaces the second container; requires re-deriving
   `rekey`'s wake walk and `pull_ships`' min under due-pop transiently absent. Named,
   not built.
3. The stagger's B-gate flight (kick-cadence od 8) — adopt statement: exact in the
   stationary measure. Its legality question (does any observer read a body between its
   staggered genesis and first kick) is unchanged and unflown.
4. ~~The residual standing excess once mixed — price its source before calling the mixed state Poisson for the 10⁹ ledger.~~
   **Executed (a97f): neither shear nor lattice — marginal-dominant (57–100% by seed) plus a seed-dependent
   locked-pairs part (0–0.14); a ~10²-fire transient, bounded by frozen-step evolution to the floor by fire
   ~100–120, with the engine decay onset confirmed to g=49 by the checker. What remains: the engine-level
   confirmation flight to g ≈ 120–145 at two seeds (the floor endpoint past g=49 is model-extrapolated, and it
   simultaneously re-splits marginal/pairwise at matched mixing depth — the seed-2 split reads 100/0). Until
   then the 10⁹ worst-frame line may quote Poisson windows outside the epoch, or the stagger from birth.**
5. The wide-draw arm ([1,5) AU, σ 28.5%): predicted ~3.6× faster mixing (g ≈ 4), unflown; one flight
   confirms mixing ∝ 1/spread as a design dial for belt genesis at 10⁹.
6. The store-class decision at wiring (od 3, unchanged), now with the between-fires news priced:
   the next-due word moves by drift ~6×10⁻⁵ of itself per fire (growing with depth: to 2.5×10⁻³ by g=40),
   so its low bits are cheap to recompute.
7. (6b9a) The census's unflown corners: a burn arm (proxy-flown by the checker at rtf 10⁵;
   a real burn/fleet-doll arm — does `child_ticks` become whole-population under a 10⁶-fleet doll? —
   stays unflown), and the M1 re-measure of the heap-op constants.

## Contradictions

None open on this run's own evidence: the both-instruments recompute (checker, exact conversion
C50_step = C50_span·span/step_med, plus the birth dump: 57.9×/3.0) closes the author's instrument
question in the refutation's favour. The unexplained residue is d520 checker1's plateau attribution
(which arm it was read on — its own log is not in this tree); treat the "persistent tail" line as
refuted on the shipped draw (two seeds, two N, both instruments), and check slow-σ arms separately
before quoting any late-g number for them. 6b9a's apparatus measurement composes with 25ce's cursor
design (the design is the deletion; the measurement is the shipped cost it deletes) — no conflict.
[a97f note: 45c0's flight measured per-fire step drift p50 6×10⁻⁵ on its pilot; a97f's census reads
5×10⁻⁴ → 2.5×10⁻³ per fire growing with g — same instrument, different depth; the drift is a mixing
accelerator either way and does not change any verdict above.]

## Runs
- 20261017-0005-fermi-25ce (fermi, awaiting grade): the 10⁹ calendar priced — no per-body
- 20261017-2038-quant-b4a8 (quant, awaiting grade): the bulk runs the chained clock, not
- 20261017-2330-second-20261017-2038-quant-b4a8-d520 (second author, awaiting grade): the
- 20261019-1817-dynamics-45c0 (dynamics, awaiting grade): the "persistent 2× tail" is a two-regime
- 20261020-0036-components-6b9a (components, awaiting grade): the apparatus measured — five calendars + pos = 156 B/body at body_cap (19.5× the machine at 10⁹; ×573 flip to live sizing), ship_ticks and waiting both whole-population and redundant, the wired ledger row store-only.
- 20261021-0429-quant-a97f (quant, awaiting grade): od 4 executed — the excess is marginal-dominant (57–100% by seed) plus a seed-dependent locked-pairs part (0–0.14), not shear or lattice; a ~10²-fire transient to the Poisson floor (frozen-step bound; engine decay onset confirmed to g=49 by the checker), so 10⁹ quotes Poisson windows outside the epoch or the stagger from birth.
