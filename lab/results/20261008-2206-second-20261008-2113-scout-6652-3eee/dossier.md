# dossier.md — run 20261008-2206-second-20261008-2113-scout-6652-3eee (lens: second author)

**Claim.** The checker's named experiment is done and the original claim survives it
— but only after closing a second, deeper hole the checker's attack exposed the edge
of: with (1) admissibility re-derived as sweep-extended pooled radius ranges (the
original's common-longitude 2ρ filter is unsound at high e — the two bodies meet at
*different* longitudes, and dr/dλ = r²e·sin f/p is large there; the checker's false
"never-fires" routes and my first dissection's 84 missed fires are one and the same
hole), and (2) **alias completion** over the passage lattice {k·T_i + m·T_j} (the
replica's D(s) is exactly lattice-periodic, D(s+k·T_i+m·T_j)=D(s); cert A's window is
alias-complete by construction, the original's single-branch window only when the cap
domain fits one lattice cell — true on F1/F2/F4, false on F3x; **the two holes
cancelled on the original's measured families: the family that would have exposed
the alias hole was routed out by the radial hole**), the travel-time-difference
window misses **zero** of 1,857 certified fires across all five families — including
the checker's kill family F3x (618 fires, e up to 0.71) and the never-measured
wide-crossing half of Kind::Wide (F5, 398 fires) — at 68–82 closed-form evaluations
versus the numeric window's 294–2,559 (count ratio 5.5–19.9×), measured wall ratio
**11.2–126× (family medians 15–66×)** with the per-call ratio measured (3.76×:
mean_at_longitude 0.62 µs vs state_at_mean 2.35 µs) — and the price is width: the
sound window is 4.3–31× the numeric window's (family medians; p90 up to 93×), so the
original's "2.6× width" does **not** survive soundness, and the adoption trade (state
evals deleted vs firing measure armed) is now explicit and unmeasured.

**Bottleneck.** Board focus item 3 / the top scaling risk, continuing
q-candidate-degree and 20261008-2113-scout-6652: the Wide sections' numeric windows,
0.67–0.7% of sections but 91% of all state evaluations at 10⁶. This run answers the
checker's three named gaps: the margined routing (re-derived, not just margined), the
wide-crossing family, and the wall-clock ratio.

## What was actually wrong with the original (the run's main finding)

- **Hole 1 (the checker's, dug out).** The checker showed the 17-sample radial test
  routes out real high-e encounters and proposed adding a Lipschitz margin. Adding
  the margin was not enough: the filter's *criterion* — |Δr(λ)| < 2ρ at a common
  longitude — is the wrong shape. A meeting has both bodies within ρ of a common
  point at *their own* longitudes λ_i, λ_j (each within a ρ-sweep of λ*); at high e
  the sweep moves r by more than ρ, so real meeting longitudes sit where the
  common-longitude Δr exceeds any fixed 2ρ band. Direct dissection: fire at
  s = −10.203, meeting longitude λ* = 2.5536 *inside the arc but outside the slice*,
  s + h(λ*) = −12.79 against a window covering h ∈ [−1.67, 3.67]. The sound filter
  (cert B3): per apse-split segment, each body's achievable radius range over the
  segment extended by its sweep sw_k = ρ/rmin_orbit,k, Lipschitz-inflated
  (fixed point from below); admissible iff the pooled ranges overlap within ρ.
- **Hole 2 (new).** With hole 1 fixed the section still "missed" 27 fires — all at
  s + k·T_i of covered fires (T_i = 12.77, s + T_i = 2.57 inside the window). The
  crate's first-hit queries every passage pair within the cap domain; those pairs
  include i completing extra revolutions between θ_c-passage and meeting, i.e. the
  window must cover **all lattice aliases** of W₀ that intersect the domain, returned
  as their hull (the Section is one interval). On F1/F2/F4 domains (5–11) fit inside
  one cell of the lattice (periods 12–17); on F3x (domains 20+) they do not. Cert A
  is alias-complete by construction (it crawls the whole domain) — which is why A
  never missed. The two holes cancelled on the original's families: F3x, the only
  family whose domains span cells, was exactly the family hole 1 routed out.
- **Also closed, disclosed:** cert B's margin doubled to H·step (was H·step/2,
  unsound by 2×); the h margin now bounds |h′| per atomic apse-split segment by the
  endpoint-range rectangle (the original's g-monotonicity fails across
  apse-straddling sample gaps and at interior sign changes of g — constructible,
  unexposed); the sweep tolerance c uses orbit-wide extrema because the sweep can
  leave the arc (the original's slice-local c is unsound at arc edges).

## Evidence (this folder; `python3 second.py` regenerates `second-out.json`, 119 s, single core, <200 MB)

- **Families** (fresh draws, seeds fixed; F1/F2/F3x/F4 from the original generator,
  F5 new): 40 Wide sections, 1,857 certified fires. **missB3 = missB = missA = 0 and
  bad_route = 0 on every family.** F3x: 8/8 windowed (original: 6/6 routed, 3
  falsely), evals 624–2,559 vs 70–82, width med 4.3× (p90 63×). F5 (cross=True,
  max(dm,dp) ≥ 0.2): 10/10 windowed, zero misses, width med 10.7×. F1: 640 fires,
  width med 13.4×. F2: 7/8 sections fire zero (one-sided arcs) — none route out
  (below). F4: zero misses, width med 16.6×.
- **Wall clock, measured, not asserted** (the checker's gap c): per call,
  mean_at_longitude 0.62 µs vs state_at_mean 2.35 µs = **3.76×**; end-to-end per
  section (cert A vs cert B3, min of 2 repeats): median 66× (F3x), 20× (F5), 21×
  (F1), 15× (F2), 28× (F4); **minimum over all 40 sections 11.2×**. evalsB (first
  cut, 5 samples) = 10 and evalsB3 = 68–82 counted separately, as the checker asked.
- **Census** (500 engineered tangencies, du uniform in (−1.2, 1.2)·R — a design
  choice, disclosed): of 457 sections, wide-crossing is **36%**, wide-merged 64%,
  narrow-crossing 0%; median max-e 0.15 on both halves. Wide-crossing is not a
  corner case: the original's "zero misses on tangency families" silently meant
  "on merged arcs", which are ~2/3 of the population under this law.
- **Truth, certified** (replaces the original's asserted-clean outside scan): whole-
  domain hierarchical scan, Lipschitz confirm threshold ρ + Σ(h/2 + τstep/2) in both
  s and τ, refinement of fire-free violations to depth 3. Certification statement:
  every fire deeper than ρ − Σ·τ_cap/2 ≈ 0.955ρ is detected; outside detected bands
  and 135 unresolved edge-strips (≤ 3.4 per firing section), D ≥ ρ is certified.
  Fires are s-grid points with D < ρ (the original's counting convention; nested
  detections may double-count within a band).
- The record regenerates from shipped code: `python3 second.py` (fixed seeds,
  deterministic, 119 s) reproduces `second-out.json` bit-identically in every field
  except the timing fields (tA/tB3, wall ratios, the microbench per-call ratio
  3.69–3.79×), verified across three reruns; `run-log.txt` holds the decisive run's
  per-section lines. The F3x dissection that found both holes is re-runnable from
  `second.py`'s imports (`tangency.make_pair('F3x')`, first draw, as used in the run).

## Predictions (predictions.md, written before the decisive run; smoke disclosed there)

- **Held:** P1 (zero misses, zero bad routes — the load-bearing claim, on all five
  families); P2 (F3x all-windowed, width med 4.3 ≤ 5×); P3's soundness half and the
  census P4 (36% vs 40–50% predicted); P5 decisively (wall ≥ 10× everywhere: min
  11.2×; per-call 3.76 in the 2.5–4.5 band).
- **Failed, and reported as failed:** P3's width letter (F5 med 10.7×, better than
  the predicted 20–100×, still fat) and **P6's letter outright**: F1 width 13.4× and
  F2 30.6× against predicted 2.5–3.5×/5–8×. The original's 2.57× was bought with the
  unsound narrow admissible band and the single-branch window; soundness costs
  roughly 3–5× in width on the belt bulk. This is the honest adoption cost, not a
  tuning failure: the width decomposes as (h-range over the sound admissible band)
  + 2c(orbit-wide) + margins, each individually necessary for the zero-miss proof.

## What would make it wrong

- A certified fire outside B3's hull on any family kills the re-derived certificate
  (the proof would have a third hole). The unresolved strips bound what could have
  been missed: fires shallower than 4.5% inside ρ, within ~h₃ of a band edge.
- The width is the adoption cost, and it is unmeasured in engine terms: an armed
  passage costs one exact per-pair check (one `d_of_s`-style evaluation, ~33 state
  evals), so a 10× wider window arms ~10× more passages per orbit — against a 5–20×
  cut in *setup* evaluations paid once per element change. Whether the trade wins
  depends on passages-per-element-change, i.e. on the belt's kick rate, which this
  run does not measure. Named next experiments, in order: (a) the per-λ* sweep
  tolerance with reference body (ε_j = 0 exactly, ε_i ≤ 1.001·(ρ + Δ(λ*))·r_i⁺/L_i,
  take the intersection of the two role-swapped windows — derivation above, ~2×
  tighter than the orbit-wide c on the belt bulk, pure arithmetic); (b) measure
  armed-passages per element change on a belt rung and decide the trade; (c) F5's
  residual width is structural (along-track tolerance at transversal crossings) —
  the crate's linear cross_window, margined for its second-order term, is the tight
  instrument there; the design consequence is a hybrid (merged → h-window,
  crossing → margined cross_window), not one certificate.
- The never-fires routing never fired: routed_noradial = 0 on all 40 sections — the
  sound margins admit the meeting zones even on F2's one-sided arcs (7/8 fire zero).
  The original's "4/10 provable never-fires" bonus does not survive soundness as
  built; a sound routing needs the pooled ranges to separate by more than ρ +
  inflations, which wants the adaptive split deepened at band edges (cheap, +2 evals
  per split). Until then B3 behaves like A: it arms windows that cannot fire.
- The record regenerates from shipped code: `python3 second.py` (fixed seeds,
  deterministic, 119 s) reproduces `second-out.json` and `run-log.txt` verbatim; the
  F3x dissection that found both holes is re-runnable from `second.py`'s imports
  (`tangency.make_pair('F3x')`, first draw, as used during the run).

## Cost of adoption, fit with PRINCIPLES

- One file of float Python against the crate's Rust: the algorithmic facts (count
  ratios, zero misses, the two holes) transfer; the integer re-derivation (h in
  ticks, windows as tick ceilings, the lattice aliases as exact integer periods —
  which the crate already has: `Body.period` is an integer) remains mechanical but
  undone. The wall ratios are Python-vs-Python, symmetric, order-of-magnitude only
  (cloud timing rule); the M1 re-measures.
- P18 "the right question, then the representation": the alias lattice is the
  representation that makes the window an exact union, not a search. P13 "errors
  never compound": both closed holes were silent-drop errors, the worst kind; the
  certificate now drops nothing. P19 "a fix signals the wrong representation": the
  2ρ common-longitude filter was the fix-shaped wrong shape; the pooled ranges are
  the meeting's own geometry. P26: conjunction screening's time filter survives
  contact with the adversarial families only after these two repairs. P1 "the best
  part is no part": not achieved here — the never-fires tier went silent; reported
  rather than hidden.

## The lens (second author)

What this lens may have missed: I validated the certificate against my own truth
instrument — a second checker should re-derive the pooled-range inequality and the
alias argument independently (both are short) and attack the unresolved strips with
a targeted dense scan at their recorded locations. The census's du-law is a choice;
a belt-run-derived law (from the actual Binet-offset distribution of candidate
pairs) would set the wide-crossing share properly. The 90-minute budget cut the
planned tightening (a) — the width numbers are therefore the *loose* end of the
frontier, not its floor.
