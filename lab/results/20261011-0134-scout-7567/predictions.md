# Predictions (written before the decisive run)

Target: B12's statistic (`fit::growth_exponent`: slope of window MAXIMA in log-log) cannot
separate bounded from compounding error on chaotic ships. Candidate replacements from other
fields: Allan-deviation slope classification (time metrology) and rank panel statistics
(Mann-Kendall / Mann-Whitney; distribution-free thresholds). Falsifier: faithful synthetic
port of the five planted laws of `xtask/src/behave/laws.rs` (echo, bounded, compound, drift,
kick) plus a const-offset control and a slow leak at the stated floor, 16 ships, 1601 samples
(200 P at P/8), chaotic semimajor-axis diffusion clipped by the C_J level set (zero-velocity
cap), ~40 encounters per ship.

## Pre-registered expectations (cases not tuned on)

1. `growth_exponent` on **planted-bounded**: 0.3–0.6 (false flag of the control; red-team
   measured 0.49 on the real scene). Verdict FAIL where the contract requires PASS.
2. `growth_exponent` on **slow leak** (walk steps ε ≤ 0.05 × bounded amplitude): reads like
   bounded (walk hidden under the bounded part's maxima) → MISS.
3. **Allan-deviation slope** classifies: echo → −1/2 (white); compound → +1/2; drift → +1;
   kick → +1/2 or larger with end level ≫ floor; slow leak → +1/2 even below 5% of the
   bounded amplitude (Allan is amplitude-unbiased: any walk component shows, unlike maxima).
4. Allan's own failure mode (pre-registered): the **bounded control during its diffusion
   transient** (before a saturates on the C_J level set) reads +1/2 — a false flag — but
   **saturates by 5–10× the gate horizon** (law-only run, no oracle needed), after which its
   slope returns to ≤ 0. So: bounded at 1× horizon FAILS Allan, bounded at 10× horizon PASSES.
5. **Rank panel** (MW halves, 16 ships, binomial k≥3 of 16 at one-sided 2.5%): detects a
   level shift ≥ ~5% of the pooled error scale; flags bounded pre-saturation (same reason as
   Allan), passes post-saturation; catches compound/drift/kick.
6. Detection floor (derived): with n = 1600 samples and pooled scale σ, MW efficacy
   z ≈ √(3n)·(δ/σ) ⇒ δ/σ ≈ 0.05 gives z ≈ 3.5; the smallest leak end-level detectable by the
   panel is ≈ 5% of the bounded amplitude. `growth_exponent` has no such floor: it misses
   leaks up to ~30% of the bounded amplitude (maxima dominated by the bounded part).
7. Replay/state-only probe (the repo's own `planted_bounded_answers_each_time_from_that_states_alone`
   property): rerun-from-mid-state reproduces echo and planted-bounded error traces exactly,
   and cannot reproduce compound's accumulated realization. [Checked in the dossier by
   construction of the models, not measured here — the planted laws' code makes it evident.]

If 3, 4 or 6 fail (Allan no cleaner than the exponent; or bounded does not saturate), the
claim degrades to "maxima are the wrong functional" only, and the horizon extension loses its
justification — that would be a lead, not a silver.
