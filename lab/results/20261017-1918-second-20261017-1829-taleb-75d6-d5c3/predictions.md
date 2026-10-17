# Predictions — 20261017-1918-second-...-d5c3 (second author on 20261017-1829-taleb-75d6)

**Written before the decisive runs.** The checker named the gold path: fix the readout (one common
absolute tick for all arms — v1 read each arm at its own `t_wave_end + m·P_min`, a tick the stagger moves
by design), rerun off/on against the finest ladder (ref9, step_log2 9), and run the SYMMETRIC clock-start
arm under K1–K4 unchanged. Gold if the corrected K2 still fires ≥ 3× against the finest ladder (any
per-body-grid-shifting stagger is illegal), or if the symmetric arm passes where ed3a's fails (the
successor is validated).

## The question, restated

ed3a's stagger shifts each body's whole kick grid by an id-derived `off` (first kick `half + off`, anchor
kept at 0: the first half-drift is `half + off` long against a `2·half` step — one asymmetry). The
symmetric arm (new, `ES_STAGGER_SYM`) starts the whole clock at `t + off`: same kick grid (first kick
`half + off` within 10⁻⁴ of a step), first interval `[off, off+2·half)` split exactly at its midpoint,
register re-projected there, the tube drifting free until `off`. So the two arms share the grid shift and
differ exactly in the first step's split and the register's anchor. Measured together they decompose the
term the checker left unresolved (its monotone-asymmetry fit failed: ρ = 0.23).

## Instrument v2

`stagger_legality.rs`: arms off | on (`ES_STAGGER`) | sym (`ES_STAGGER_SYM`) | ref8 | ref9; every arm
reads at the SAME absolute ticks `at:T1,T2`, with T from the OFF arm's base (`base` arm prints
`t_wave_end` and `p_min`; floor convention). Seed 1 (quiet): T1 = 15385526345828, T2 = 30768114771015
(≈1 and 2 orbits of the shortest belt body past the wave). Seed 2 (resonant, v1's held-out):
T1 = 15474922198888 (`base 2` = 2937639321 + 1.54719845595674434e13). New `lead` column (the current
binding's `lead`). Scene, draw (k ∈ [128,256), extra = 256), key readouts, C1–C3 verbatim from v1.

**New control C4 (the construction is what it claims, measured on the shipped record):** just past the
wave end, `off` and `sym` bodies sit at their first rebind with `lead = half` (off: lead == first_kick,
128/128 measured; sym: |lead − first_kick(off arm)| ≤ 5.1×10⁵ ticks = 9×10⁻⁵ of a step, the step
re-derived at `t+off`), while `on` bodies sit with `lead = half + off` (lead == first_kick, 128/128,
anchor 0). The wave spread survives in sym (width 5.56×10⁹ ticks ≈ on's, vs off's 2.10×10⁸).

## Kill criteria (pre-registered; X ∈ {on, sym}; ε = X − ref9 per body at the common tick)

- **K1 (bias):** |mean(ε_X − ε_off)| > 5·(std/√n) on ln a or e at any horizon, either seed.
- **K2 (class, the corrected headline):** median|ε_X| > 3·median|ε_off| at h=1, seed 1, against ref9.
- **K3 (compounding):** median per-body growth exponent of |ε| (h1→h2, vs orbits completed) exceeds
  off's by more than 0.3.
- **K4 (tail):** any body with |ε_X| > 10·p99|ε_off| (seed 1, h=2).
- **K5 (mechanism, new — the decomposition):** Spearman ρ between the per-body differentials
  (ε_on − ε_off) and (ε_sym − ε_off) on ln a, h=1, seed 1. ρ ≥ 0.7: the two arms pay the same per-body
  term (the shifted grid); ρ ≤ 0.3: different terms (ed3a's asymmetry dominates its arm).

**Decision rule (the checker's, verbatim):** ILLEGAL-IN-ANY-SHAPE if K2 fires for both on and sym;
SUCCESSOR-VALIDATED if K2 fires for on but not sym (then K5 should read low).

## My Fermi expectations (falsifiable, before running)

- **P1 (ed3a's arm, corrected):** K2_on(ln a) ∈ [3, 7] — the checker's 4.8× (4.2×10⁻⁷ vs 8.7×10⁻⁸)
  was measured one arm's-tick off; the common tick moves it by ≲30%, not below the 3× bar.
- **P2 (the run's real bet — the symmetric arm):** K2_sym(ln a) ≥ 3 — it FIRES. Reason: the sym arm
  shares the shifted kick grid, and the checker already showed bodies whose offset is < 5% of a step
  (a nearly symmetric first step in ed3a's own arm) pay the full 2–6×10⁻⁷ differential — the term rides
  the grid shift (the tide-sampling phase each body's kicks land at), not the first step's split.
  Confidence 0.7. If it passes instead (< 3×), the successor is validated and the mechanism is the
  first interval.
- **P3 (mechanism):** ρ((on−off),(sym−off)) on ln a at h=1 ≥ 0.7 (shared grid ⇒ shared per-body term).
- **P4 (ladder, continuity):** off-vs-ref8 median |Δln a| ≈ 1.7×10⁻⁸, off-vs-ref9 ≈ 8.7×10⁻⁸,
  ref8-vs-ref9 ≈ 6.8×10⁻⁹ (the checker's numbers, now at common ticks; ±30% tolerance).
- **P5 (ref-free differential):** median per-body |ε_on − ε_off| (ln a, h=1, no reference involved)
  ≈ 2×10⁻⁷ (the checker's same-tick 2.1×10⁻⁷), and |ε_sym − ε_off| within 2× of that.
- **P6:** K1 passes for both arms everywhere (|z| ≤ 5); K3 passes (Δ slope < 0.3); K4 passes on ln a
  and e, the apsidal angle may show one marginal body (v1 saw a single body at 2.2× a 10·p99 line).
- **P7 (seed 2, resonant):** drowned — all arms within a factor 2 of each other against ref9
  (v1: both arms ~2×10⁻⁴, equal to three digits).
- **P8 (grid identity):** first_kick(on) − first_kick(off) ∈ [0, step) per body; max |first_kick(sym) −
  first_kick(on)| ≤ 10⁶ ticks (1.8×10⁻⁴ of a step).
- **P9:** alive 128/128, refusals 0, in every arm including refs; C1 (birth keys identical across
  off/on/sym), C2 (planets bit-identical), C3 (both gates unset: frame_digest identical to pristine)
  all hold.

**VOID if:** any control fails; a refusal; a dead body; fewer than 120/128 bodies readable at every
horizon in any arm; ref9's horizons missing.

**What would change my reading:** if K2_sym fires but ρ < 0.7, the two arms pay different per-body terms
on the same grid — then neither "grid shift" nor "first step" alone explains the class, and the dossier
must say the mechanism is still unresolved (the kill of both shapes stands; the successor must avoid
per-body grid shifts entirely, e.g. stagger the births' own clocks as doll-level phases, or accept the
wave). If both arms pass K2, v1's kill was an artifact of the instrument alone and ed3a's shape is
rehabilitated at the common tick — I would report that against my own run's premise.
