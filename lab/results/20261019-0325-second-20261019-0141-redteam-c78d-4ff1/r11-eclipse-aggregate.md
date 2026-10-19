# Rung r11: eclipse parity, the aggregate arm — one sample per aggregate vs the transit it erases

Drafted by the GLM lab (run 20261019-0325-second-20261019-0141-redteam-c78d-4ff1, second
author on 20261019-0141-redteam-c78d whose silver named this freeze), hashed before the
decisive run; the integrator freezes it by committing it to `lab/rungs/`. The refutation
it guards is c78d's: representation.md L59/L116 "Aggregates are one sample each…" makes
fleet-scale eclipses all-or-nothing (89.1%/99.0% mid-transit flux error at R_f = 3/10·R_p;
blink window = the sample's own eclipse width 2·R_p; survives exact retardation + k⁴ at
β 0.5 and 0.9; the game's own 400-ship arc formation errs 1.000). The absence half of
eclipse parity (per-row worldtube law, 22d1) is frozen separately; this is the aggregate
half. Law refs: [docs/representation.md](../../../docs/representation.md) §2 and §6,
[lab/wiki/occlusion law 22d1](../../../lab/wiki/representation-premises.md).

**Bars are the page's corrected ones** (both checkers' fixes, representation-premises
direction 2): the absolute `f_true_min ≥ 0.88` is replaced by *within 5% of each arm's
exact f_true_min* (it cannot survive "judged at player β": the exact minima are
0.535/0.815 at β 0.5); the `≤ 150 samples` cap is **pinned to this rung's frozen R_f = 3·R_p
case** and generalizes through the scale-aware bound `samples ≤ π·(R_f/h)²·1.1` (disc
covering at the readout's own pitch h; at R_f = 30·R_p the same h = R_p/2 pays ~11,310 —
the cap is a function, not a constant). Controls on both sides (r2 lesson): the negative
(one-sample) must fail, the positive (the closed-form overlap on its licensed domain,
uniform disc at β = 0 — derivable, principle 3) must pass, else VOID.

**Question.** Does a per-aggregate occlusion readout hold 5% eclipse parity against the
exact Σk⁴-occluded flux fraction at player β, in both fleet orientations, at a sample
cost bounded by the pixel cap — while the letter's own first clause (one sample =
the representative point's predicate) cannot?

**Truth.** Exact per-ship predicate (the 22d1 law): observer O at origin; planet disc
C = (0, 20), R_p = 1, static; fleet rigid behind it at depth ~25 moving at β = 0.5 in +x
(c = 1); per ship the retarded time (past root of the light-cone quadratic), the
segment(retarded position → O)-vs-disc predicate, and the SR k⁴ weight
k = 1/(γ(1 − β·cosθ_ret)). Exact f_true(t) = 1 − Σ w_i·occluded_i / Σ w_i, N = 2×10⁴
uniform-disc ships, R_f = 3·R_p, impact 0, 1201 steps over the seen transit window
(light-time-shifted). Both orientations: transit-plane (fleet depth spread) and
sky-plane (fleet spread ⊥ LOS). β = 0 static truth for the positive control: N = 10⁵
uniform disc behind a disc at origin. Deterministic seeds, float64. Cloud caveat: no
timing numbers are frozen; only counts, fractions and errors.

**Configurations** (probe `eclipse_rung.py <config>`, one JSON line per config; frozen
case β 0.5 / R_f 3·R_p / impact 0 unless named):
- `pixel-h2` (candidate): the letter's second clause as the cure — the exact predicate
  and k⁴ weight evaluated once per pixel of a pitch-h grid covering the fleet (centres
  inside the fleet support; uniform pixel weight × k⁴), h = R_p/2.
- `pixel-h1` (candidate): the same at h = R_p (where the cap has slack: is coarser
  sampling still 5%-true?).
- `one-sample` (negative): L59's first clause — the representative point's (the fleet
  centre's) own predicate times its k⁴. It must fail.
- `overlap-disc` (positive): the circle–circle overlap closed form, uniform disc at
  β = 0 (its licensed domain; checker-measured 11–31pp outside it and shape-blind on
  ring/arc/convoy). Sample-free (pitch charged as R_f). It must pass.

**Metrics,** one set per configuration (worst of the two orientations where two exist):
- `flux_err_p99`: p99 over the transit path of |f_readout − f_exact|.
- `fmin_abs_dev`: |min_t f_readout − min_t f_exact| (the corrected min bar).
- `false_blink_frac`: fraction of the path where f_readout = 0 while f_exact > 0.5 —
  a fabricated total eclipse: an error of *type*, not size.
- `samples`: predicates evaluated per aggregate per frame (pixel count, 1 for
  sample-free readouts).
- `samples_over_bound`: samples / (π·(R_f/h)²) at the readout's own pitch (sample-free
  readouts: h := R_f).

**Domain (one line, per the second checker):** the artifact and this rung need the
transit resolved on screen; a sub-pixel aggregate pays exact per-ship sums (the readout
is the same law on any representative set — cost = min(N, support pixels at h)).

**Output.** `metrics.json` `{"<config>": {five metrics}}`; `metrics-check.json` from an
independent retarded-time solver (bisection on the light-cone, not the quadratic root);
`verdict.py` decides.

```configs
pixel-h2 candidate
pixel-h1 candidate
one-sample negative
overlap-disc positive
```

```criteria
p99 behaviour flux_err_p99 <= 0.05
fmin behaviour fmin_abs_dev <= 0.05
blink type false_blink_frac <= 0.01
cap cost samples <= 150
bound cost samples_over_bound <= 1.1
```
