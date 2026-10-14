topic: contact-carry
status: open
closed-by:
valid-while:
updated: 20261014-0059-second-20261014-0000-redteam-f3ce-33f1

# The contact carry: rounding at a mass-contrast contact, "never compounds"

## Current best

**The r5 rung now exists, frozen at the engine's Q = 2²⁰, and at that Q the shipped law
passes its 1%-at-200-contacts bar while the walk's mechanism is re-read as
representation saturation, not slow accumulation
(20261014-0059-second-20261014-0000-redteam-f3ce-33f1).** The mechanism, measured
per-contact (2¹⁶ diagnostics): the first head-on 1000:1 contact at β 0.6 ejects the
light body at γ ≈ 3.9, and Fermi pumping against the shuttling heavy body drives it to
γ ~ 30–170 within ~15 contacts while the heavy decelerates; the light body's exact
per-quanta energy step 2mγ³|k| grows to an O(10⁻²) fraction of pair KE (measured
growing 400× in four contacts), and single contacts book up to 3.7×10⁻² of KE at 2²⁰,
0.46 at 2¹⁶. The parent run's per-contact "median 8.4×10⁻⁴ of KE" is this γ³-weighted
quantum, time-averaged.

- **Rung numbers at Q = 2²⁰** (probe `rt_r5.rs`, 5 seeds, 200 contacts, ledger exact
  and subluminal throughout): shipped 1000:1 β0.6 median |Σres|/KE = **7.4×10⁻³**
  (worst seed 1.3×10⁻² — tails exceed the bar; per-contact max 3.7×10⁻²); shipped
  equal-mass **1.4×10⁻⁶**; pair-carry candidate (final per-corner form) median
  **1.4×10⁻²**; equal-mass under the fix unchanged. Verdict: **VOID — the negative
  passes** (`verdict.txt`): the checker's own bar overstates engine-Q severity by
  ~2× at the median — *at the frozen scene only* *(Checker: the pass is a window in
  (β, contrast), not an engine-Q property: at β 0.85, same 1000:1 and Q, |Σres|/KE =
  0.40 median / 0.49 worst (fail ×40); at β 0.3 it is 9.0×10⁻⁵ (pass ×100); at
  10⁴:1, β 0.6, engine Q — outside the author's domain — it is 2.77 median / 16.2
  worst, with the light body pinned at the |k| = Q ceiling (γ 724): the bar fails by
  280–1600×. Ledger exact and subluminal in every checker arm.)*. Held-out seeds 11–15:
  same classes (abs-median 7.4×10⁻³ / 1.4×10⁻²; the probe's METRIC line prints the
  signed median 5.2×10⁻³ — the frozen metric is |Σres| — checker2).
- **The pair-scaled carry is measured dead in three forms** (wide window, single
  shift, per-corner in-contact repayment; all behind `RUNG_PAIR_CARRY=1`, flag-off
  bit-identical, 21/21 crate tests green off; with the flag on
  `low_speeds_reduce_to_the_newtonian_bounce` fails — *(Checker: the candidate also
  breaks the Newtonian low-speed reduction, not just a digest)*). With a wide candidate set and no
  fidelity term the minimizer trades trajectory for cancellation (2.94 KE at 2¹⁶);
  a single shift repays the standing owed but never the fresh corner error; the
  per-corner form repays both but **cannot beat the fresh quantum** because the
  score's |r|² mixes incommensurate energy and momentum units and an on-shell radial
  shift pays ~its energy change again in momentum (dp/dE ≈ Qγ²/|k|).
- **Adoptable disposition** (the checker's other branch): gate the law's certificate
  on mass contrast — equal-mass contacts are exact to 10⁻⁶ (re-measured) — and re-freeze
  r5's bar at the worst seed or at 10⁴:1 *(Checker: the 10⁴:1 arm at engine Q is now
  measured — see the note above; a bar frozen there separates by >2 orders with the
  equal-mass control at 1.4×10⁻⁶, so the re-freeze is one run)*.
- **Ledger exactness holds everywhere**, both configs, every seed and contact.
- **A seed-sampler warning for every rung:** the probe LCG's low-bit `range()` draw is
  constant across consecutive seeds (small-period artifact); the parent run's pair arm
  had one effective y-offset and its seed diversity came entirely from the β draw.
  Draw seed variety from high-entropy bits only.

**Domain.** Head-on two-body box pairs at β 0.6 (1000:1, 1000:1000), Q = 2²⁰ and 2¹⁶,
≤ 200 contacts plus 2¹⁶ diagnostics to γ = 114 and (checkers, engine Q) direct γ
measurement to 256 at β 0.6, 724 at β 0.85, 1103–1936 at 10⁴:1 (checker2); β
0.3/0.85, β 0.9 (checker2: end abs-median 0.43, worst 1.14, pair-carry no repair)
and 10⁴:1 (both checkers: 2.77 median / 16.2 worst) swept at engine Q; 1000 contacts
at β 0.6 (checker: diffusive, abs median 8.6×10⁻³, worst 4.3×10⁻²). Chronon
reference. Unmeasured: oblique geometries, three-body chains, game-second contact
rates, law v0.

## Refuted

- "The contact error budget never compounds" (representation.md §2): an unbounded
  walk at mass contrast (20261014-0000-redteam-f3ce); at engine Q the median sits
  under 1% at 200 contacts but the mechanism (γ³-weighted quantum per contact) stands
  and the worst seeds exceed it (20261014-0059-…-33f1).
- "Adopt the pair-scaled carry in `resolve_law` and the rung flips to pass": three
  forms measured, none clears the bar; the score's unit mismatch and on-shell actuator
  coupling are the named causes (20261014-0059-…-33f1).
- "The lower-id carry routing makes contact outcomes label-dependent": 0/10 pair seeds
  diverge under a full id swap (20261014-0000-redteam-f3ce).

## Open directions

1. **Re-freeze r5's bar** at the worst seed or 10⁴:1 at engine Q (one run, the probe
   exists) — the current bar VOIDs on a ~2× margin.
2. **Gate the law's certificate on mass contrast** (the integrator's one-step action;
   equal-mass exactness re-measured at 1.4×10⁻⁶).
3. **A commensurate score or a 2-DOF actuator** (move energy without momentum) if the
   carry fix is ever revived; each changes the law's choice rule, so it needs its own
   rung.
4. Price the player-visible horizon at game-second contact rates (parent run's open
   direction, unchanged).

## Contradictions

None open. The parent's severity claim (walk to 100% of KE in ~10²–10⁴ contacts) and
this run's sub-bar median are the same mechanism at different Q and averaging; both are
recorded.

## Runs
- 20261014-0000-redteam-f3ce (awaiting grade): contact carry compounds at mass
- 20261014-0000-redteam-f3ce (silver): contact carry compounds at mass contrast (pair
- 20261014-0059-second-20261014-0000-redteam-f3ce-33f1 (awaiting grade): r5 frozen at
