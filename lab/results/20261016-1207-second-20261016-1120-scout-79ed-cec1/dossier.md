# Dossier — 20261016-1207-second-20261016-1120-scout-79ed-cec1 (second author, topic: binet-cells)

## Claim

The named experiment is done — r1 re-frozen with the band-constant rule in the freeze
(`r1v2-rings-band-constant.md`, sha256 below, written and hashed before the run) and
executed on the **full frozen case set** for the first time — and the scout run's claim
**holds and sharpens**: on every channel where the two rules differ, the one-law refit
wins — worst-offset e=0 circles **exact to 1.6e-14 vs centre's 1.61e-1 worst error**
(pass 1.00 vs 0.20 at m16, 1.00 vs 0.49 at m32), and it lifts the m16 sampler to
256/256 precession **and** period (centre 255/256 both; medians 1.509e-4 vs 1.856e-4)
at **unchanged crossings** (38/77) with no regression anywhere (light 64/64 both arms,
ISCO 2/2, shape 1.0, the letter's never-before-run 10⁴-cycle 1e-12 repeat bar passes
with worst drift 1.0e-14). But the full certificate **cannot be granted to either
rule**: two defects of the letter's law itself, shared by both arms at every m, fail
frozen criteria — **the photon capture rows (γ1.03, γ1.1 misclassified at every m:
the piecewise law cannot turn a photon inside a hyperbolic band — the model's photon
barrier is b̂ = 7.26 (m16) → 7.38 (m32), converging to √54 = 7.35, against GR's
3√3 = 5.20)**, plus the matter E=1 threshold shifted to L̂ ≈ 4.23 (GR 4; x=1.03
misclassified), and the near-separatrix strong rows miss the letter's bars at
m16 (4/6) and m32 (5/6) — m64 passes both. So: **the band-constant rule question is
settled (refit); adoption of either rule waits on a law fix for hyperbolic-band
turning, priced by b̂→√54 and L̂≈4.23.**

## Bottleneck

Bottleneck 0 (the representation). The checker's one-experiment-to-gold was exactly
this execution; it decides the rule (refit, unconditionally, on the differing
channels) and exposes what no prior run could: the certificate's own capture and
near-separatrix bars are unreachable by any constant rule at m ≤ 32. Value: the
integrator can adopt the refit rule into `docs/representation.md`'s Binet cells the
moment the light law's turning is fixed, and knows the fix's acceptance test (b̂ →
3√3, L̂ → 4; `barriers.py`, 0.5 s).

## Evidence

Everything regenerates: `regen.sh` (~8 min) → `report.json`, `detail.json`,
`barriers.json`, `r1v2-picture.png`, and the console table. Sampler draw pinned to the
letter (one `random()` for p, one for e, redraw both on reject; light b's continue the
stream — the dead-line draw of 79ed is not used).

```
config            prec    period  prog  defl  cap  isco  shape  repeat  cr   nearcirc  strongf
m8-centre   (neg) 0.9844  0.9570  1.0   1.0   3    1     1.0    1.0     18   0.20      0.000
m8-refit          1.0000  0.9766  1.0   1.0   3    1     1.0    1.0     18   1.00      0.000
m16-centre        0.9961  0.9961  1.0   1.0   3    1     1.0    1.0     38   0.20      0.667
m16-refit         1.0000  1.0000  1.0   1.0   3    1     1.0    1.0     38   1.00      0.667
m32-centre        1.0000  1.0000  1.0   1.0   3    1     1.0    1.0     77   0.49      0.833
m32-refit         1.0000  1.0000  1.0   1.0   3    1     1.0    1.0     77   1.00      0.833
```

- **Instrument (rebuilt from 79ed's script, four fixes, each named in the code):**
  F1 `band_of` assigned exact dyadic band edges two bands off (the "circle defect");
  F2 the hyperbolic branch's bisection exit replaced by the exact quadratic in
  y = e^{λφ} plus the closed-form turn ln(B/A)/2λ, with time integrated over
  hyperbolic segments; F3 escape detection (was max_events → misread as plunge) and an
  exact stop at the escape radius (the deflection overshoot, first order in width);
  F4 the horizon as an unambiguous capture (band-edge ties let orbits cross into
  unphysical u > 1/2 bands). Calibration: the frozen arm reproduces 79ed's instrument
  on 79ed's own draw to 1.3e-13 (median advance error, all m; crossings and period
  errors likewise). RK45 integration of the piecewise band ODE matches the walk
  (v agrees to 2e-4 at u = 0.15 along an E=1 dive) — the capture findings are the
  law's, not the walker's.
- **The case-set corrections this exposes in 79ed's harness** (disclosed, all fixed):
  the E=1 capture rows were launched with the bound-orbit first integral
  (1/L² − u² + 2u³) instead of the E=1 one (**2u/L²** − u² + 2u³) — ~8× too fast
  inward, which is why every arm "misclassified 5/10": the truth rows above threshold
  plowed through the barrier. The oracle ports (periapsis_elliptic,
  bound_period_quad, deflection_quadrature — the latter newly ported and verified
  against direct quadrature to 1e-8..1e-12) are unchanged and faithful.
- **Predictions (predictions.md, written before the run):** P1, P4, P5, P6, P7, P8
  held (circles exact; ISCO 2/2; light 64/64 with refit ≈ centre; repeat at 10⁴
  cycles inside 1e-14; sampler medians and pass counts inside every pre-registered
  band; crossings identical across arms). **P2 and P3 were refuted** — the
  pre-registered both-arms branch fired: strong rows fail at m16 (4/6) and m32 (5/6)
  for both rules, and capture fails 3/10 at every m for both rules. The kill bar did
  not fire against the refit (no arm-attributable failure): by its own clause, both-
  arms-every-m failures are certificate findings, and they are reported as such.
- **The barriers, bisected (both arms identical at 1e-3 resolution):** photon
  b̂ = 7.2632 (m16), 7.3823 (m32) — the m→∞ limit is √54 = 7.3485, and the mechanism
  is structural: the per-band light equilibrium up(c) = 3c²/(6c−1) > c for all
  c < 1/3, so an in-band turn always lands above the band and is deferred past the
  photon sphere. Matter L̂ = 4.2261 (m16), 4.2495 (m32) against GR's 4 (turning
  becomes possible only where 3c² − c + 1/L² > 0).

## Predictions

`predictions.md` (mtime before the run; the freeze file hashed first — see below).
Six of eight held, two refuted in the direction the freeze needed them tested; the
refutations are the run's new knowledge.

## What would make it wrong

- The two law-level defects are measured on a float64 instrument whose own faithfulness
  is cross-checked two ways (79ed-calibration and RK45); a shipped-code harness could
  still disagree on the m64 claim (measured here only on the two failing rows).
- The long runs at m32 use 16 seeds, not 32 (the pre-registered cut, `predictions.md`);
  m16 and m8 are full.
- The circle rows are my placement grid (12 bands × 5 offsets), not fe85's; the
  worst-offset values are insensitive to the grid (the centre error is the first-order
  family law), but a freeze should pin the grid.
- The refit's integer form and compile cost remain unpriced (unchanged from 79ed).

## Cost of adopting, fit with PRINCIPLES

Adopting the refit rule: canon reset (256/256 turning-band constants move — 79ed's
measured price), no new state, no per-crossing cost; **but the certificate needs the
law fix first** (hyperbolic-band turning for light, and either local refinement or a
relaxed near-separatrix bar). Fit: "A fix signals the wrong representation" (19) — the
photon barrier at √54 is the band-Taylor representation showing its edge, and the
refit's win is exactly a representative-point choice with no regime branch (4). "We
need to build towards GR" (30): the capture channel is the one place the current law
is not yet GR at any m.

## The lens (what the second-author lens may have missed)

I inherited the scout's float64 instrument and rebuilt rather than re-run; a
shipped-code (Rust) harness would be the independent check the lab's rule prefers. The
CONT (contained-only) arm was dropped from this record on 79ed + its checker's
evidence; a contained-only proponent could ask for it on the circle rows (it also
passes them), but the sampler already separates the forms. The m64 strong-row pass and
the √54 limit are two-point evidence for the convergence claim, not a swept curve.

---
sha256(r1v2-rings-band-constant.md) = 1bdeb5f8ec4528ebe86869740b7596ccde251dc240971a45bdeaac2ce4fbbaae
sha256(predictions.md) = 9d7b696deb386b39e7ab7ba63ddb8aba581ccfc061d8e2ca863c24ffabf0e6cd
sha256(binet_r1v2.py) = 9acc6797ab496a5de59e2ea4958bda346cfe9cf7aa6b51c225cae6688ba24fb6
