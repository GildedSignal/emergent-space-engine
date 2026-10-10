# Dossier — 20261010-1920-autoresearch-ccc6

## Claim

Four one-line-ish changes to `crates/encounters` cut candidate-pair setup cost
1.4–2.1× (every behaviour gate still zero-miss, including held-out e = 0.1–0.2
belts), and a sound dual-guard slack skin cuts a kick's re-certification 5.0×
at ε = 1e-9 and 1.9× at ε = 1e-7 with zero skip violations — cumulative 7.9×
on the board's open item (re-certification per candidate pair per element
change: 8.84 → ~1.1 µs/pair-equivalent at small kicks).

## Bottleneck

Board focus, encounters line: "the setup (2.5–24 µs per candidate pair per
element change)" and the top scaling risk (candidate work must track real
encounters). The 6 October gold left the slack skin (12.6×) as "the lever;
nothing to build". Setup is 92% of per-kick evals; Wide sections (tangencies,
merged arcs) carry ~all of it (600–2900 exact state evals each; Cross ~0).

## Evidence (Linux x86 cloud box, 8 vCPU, shared — orders of magnitude only)

Baseline → final, medians, same seeds (`crates/encounters`, `scale`/`kick`):

| spec | setup ns/pair | evals/pair |
|---|---|---|
| σ_e 1e-3, n 10⁴ | 35592.9 → 16701 (**2.13×**) | 120.7 → 59.3 |
| σ_e 0.01, n 10⁴ | 9165.8 → 4987 (**1.84×**) | 20.3 → 9.6 |
| σ_e 3e-3 (held out) | 13779.0 → 7719.5 (**1.79×**) | 39.6 → 19.2 |
| n 3·10⁴ (held out) | 6102.9 → 4363.2 (**1.40×**) | 9.7 → 4.6 |

Kick re-certification (812.8 candidate pairs/kick, horizon 1000 orbits),
same-binary A/B, skin on/off:

| ε (kick in a) | no skin µs/kick | skin µs/kick | gain | skipped | violations |
|---|---|---|---|---|---|
| 1e-9 | 4583.8 | 914.8 | **5.01×** | 94.5% | 0 |
| 1e-7 | 4644.8 | 2416.9 | 1.92× | 48.8% | 0 |
| 1e-5 | 4597.0 | 4357.6 | 1.06× | 2.8% | 0 |
| 1e-3 | 4527.2 | 4500.4 | 1.01× | 0% | 0 |

vs this morning's baseline binary (7188.6 µs at every ε): **7.86×** at ε1e-9.

Behaviour gates: verify a (4 belts), b (3), c (3 incl. narrow-adversarial,
coorbital, equal-period-keys), long, and held-out d (hot e0.1, mixed e0.2
a0.5–3, dense n3000) — all `missed:0 false:0 dup:0` before and after.
`changed_fraction`/`flipped_fraction` identical to baseline at every ε.

Reproduce (each ≤ 60 s):
```
cargo build --release -p emergent-encounters --bin encounters
/home/glmlab/lab-target-1/release/encounters scale sigma 0.001   # setup ns/pair
/home/glmlab/lab-target-1/release/encounters kick                # skin A/B + violations
for s in a b c d long; do .../encounters verify $s; done         # zero-miss gates
```
Patch: `work/patch.diff` (also saved by run.sh).

## The changes (one per round, keep/revert logged in log.md)

1. **R1** r³ = r²·√r instead of `powf(1.5)` in `rel_of`, `cross_window`, `rel`
   (−14%): identical math, cheaper libm path.
2. **R2** Kepler Newton tolerance 1e-15 → 1e-12 (−8%): one iteration spent
   polishing 3 ulps below every window margin.
3. **R3** `d_of_s` inner arc scan k = 32 → 12: the pair-distance along j's arc
   has ~2 extrema per orbit; 12 samples still bracket every Δr·Δv sign change
   — verified by the 14 belts (incl. e 0.2) staying zero-miss. Evals halve.
4. **R5** the slack skin in `kick()`: skip re-certification of a silent pair
   (no proposals over the horizon) iff its stored phase budget > 2× the kick's
   relative period drift AND the kicked body's Binet shift < ½ the pair's cone
   margin (`eps_u − cone_gap`); the skip set is built only when some budget
   covers the drift (no loss at ε ≥ 1e-5). The dual guard is what makes it
   sound where the pure phase rule (1.5×) showed 5 violations at ε = 1e-3: a
   large kick moves the sections' geometry, not just the phase.

## Predictions (predictions.md, written before the decisive runs)

Held: R1 10–30% (got 14%); R2 5–15% (got 8%, only visible in interleaved A/B —
the shared box drifted from load 1.5 to 4.8 mid-run); R3 1.5–2.2× on Wide-heavy
specs (got 1.8–2.1×); R5 ~10–15× at 1e-9 (got 5.0× vs the same binary, 7.9× vs
baseline), ~2× at 1e-7 (got 1.9×), ~1× at ≥1e-5 (got 1.01–1.06×), and exactly
as predicted the 1.5-factor phase-only rule is unsound at ε1e-3 (5 violations
reproduced) while the shipped dual guard has 0 on the whole ladder. R4
(arc-local Lipschitz) was predicted ~1× on tuned specs and skipped for the
window — it remains the next probe for e ≥ 0.1 belts, where vmax/v_apo ≈ 1.2–1.5
is pure waste in the conservative advancement.

## What would make it wrong

- **k = 12 is an empirical constant, not a proof.** A belt whose Δr·Δv wiggles
  more than ~6 half-cycles per arc could hide a dip between samples. The 14
  verify belts (e ≤ 0.2) all pass, but the sound form is an adaptive k from the
  arc's width against the relative-motion frequency, or a curvature bound.
- **The skin's guards are measured, not derived.** The budget bisection covers
  phase drift; the ½-cone-margin covers geometry; 0 violations on 81275 pairs ×
  4 ε. A derivation (drift model of the integer circle rotation under ε, plus
  section-shift vs margin) is required before it is law. The skin also stores
  one budget + margin per pair (~16 B on top of today's 12 B/section) — the
  per_pair_bytes_per_body metric should be re-run.
- R1/R2 change float rounding paths: hit times move at the 1e-12 level between
  versions. Gates are behaviour-level (missed/false/dup, changed fractions), so
  this is inside the research crate's contract; the canonical integer law is
  untouched.
- Cloud timings, shared box, medians of 3 with interleaved A/B; the integrator
  re-measures on the M1 (orders of magnitude only).

## Cost of adopting

One patch to `crates/encounters` (research crate, GLM-owned, r8 v3-verified):
three hot-path constants/arithmetic forms plus the skin in the kick
experiment. No API change, no new files, no gate change. The engine's
encounters design (law.md "Finding encounters") gains a cheaper setup per
element change at every measured spec; the harness's count-based
`crossover_orbits` proxy is unchanged (43.7 at σ0.01, n 10⁴ — it counts cone
pairs vs element-sort swaps, not seconds; timing element-sort's per-swap cost
against the new setup is the missing half of that comparison).

## Fit with PRINCIPLES

- "The cheapest compute is compute not done" (1): the skin deletes whole
  re-certifications; R3 deletes oversampled quadrature.
- "Compute only surprises" (3): a kick that cannot wake a proposal is not a
  surprise — the budget is its certificate.
- "we just need to have the right representation so that math is trivial" (18):
  Binet-space cone margin + phase budget is the pair's own slack language.
- "Run the simplest falsifying test first" (10): every round gated on the
  zero-miss verify sets before being kept.

## The lens (what it may have made me miss)

A local search tunes constants on two belts; it cannot find the structural
change. Two structural candidates sit one level up: (a) the Wide window itself
as a closed form — the tangency's D(s) is a low-order polynomial in s near the
tangent longitude, so the hull could be written down instead of walked
(predicted another ~3–5× on Wide-heavy specs, replacing R3's k entirely);
(b) budgets stored at first setup so re-certification after *any* event (not
just kicks) reuses them — the skin then generalizes from kicks to handoffs.
Also unmeasured: the skin's behaviour under a *sequence* of small kicks
(budgets decay; when do they get repaid?), and thread-level contention (all
timings here are the single-threaded setup path).
