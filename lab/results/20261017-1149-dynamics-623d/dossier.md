# Dossier — 20261017-1149-dynamics-623d

## Claim

The shipped dynamics' surprise rate is measured for the first time (principle 3's entropy
side): the belt's chaos floor is ~10⁶× below the certificate stream at 10⁹ bodies — chaos
never binds the belt's event budget — while the fleet's co-orbital regime sits at Lyapunov
time 0.5–3.4 planet periods (6–40 yr), the one shipped regime where the encounters tier's
Diophantine lookahead (a pair's next conjunction from continued fractions, r8) is
chaos-limited: its prediction horizon (6–40 P against a formation's ~10³–10⁴ P synodic
cycle) dies thousands of planet periods before the conjunction it predicts.

## Bottleneck

Board bullet 3's second half ("how many kicks a body really needs per orbit") and the
encounter work at 10⁹: the entropy side of "cost follows change and entropy" had never been
measured on the game's own ensembles (no wiki page holds a Lyapunov number). The gain is a
premise check, not a speedup: it deletes chaos as a candidate justification for finer
cadence anywhere except the fleet, and it names the one tier whose long-horizon predictions
need a chaos guard.

## Evidence

Instrument: Benettin twins on the judge's own reference (`xtask/src/behave/restricted.rs`,
Dormand–Prince, rtol 1e-12), the pair started as the **same orbit rotated about the star**
(a pure phase offset — no semimajor-axis error, so Kepler shear never enters and the μ→0
null is an exact symmetry), monotone to 64 planet periods (759 yr; ~190 local orbits at
2.5 AU), λ = the slope of ln d, saturation at d > 10⁻³ r. Ensembles: the plane's belt birth
range (uniform a ∈ [2,3) AU, e = 0.1 Rayleigh-typical, 4 phases, 164 ICs; the Giant is the
JUPITER scene, μ 10⁻³ at 5.2 AU), the fleet regime (70 corotating tadpole ICs, ±(0–90)°
about L4/L5, ±2.5 Hill radii), and the control (μ 10⁻¹², 12 ICs).

| ensemble | λ per local orbit p50 / p90 / p99 / max | frac > 10⁻² | saturated | stretch max |
|---|---|---|---|---|
| control (μ→0) | ≤ ±4.3×10⁻³ (bounded stretch ≤ 2.0) | 0 | 0/12 | 2.0 |
| belt (164) | 2.9×10⁻⁴ / 5.5×10⁻³ / 1.09×10⁻² / 1.66×10⁻² | 1.8% | 0/164 | 3.8 |
| co-orbital (70) | 0.29 / 0.81 / 1.03 / 1.85 | 96% | 56/70 | 16.2 |

- The belt's top ICs sit **exactly on the 3:1 (a = 2.500 AU) and the 5:2 (2.823 AU)** — the
  Giant's Kirkwood structure, measured on the judge itself; λ·P p50 (2.9×10⁻⁴) is inside the
  control's regression band, i.e. indistinguishable from regular at this horizon.
- **Composition (P5):** even if every one of 10⁹ bodies ran at the belt's p99
  (1.09×10⁻²/orbit, orbit 1.25×10⁸ s), the chaos-driven re-derivation floor is **0.09
  events/game-s** against the certificate stream at 10⁹ (~2.5×10⁵ events/s, from
  birth-stagger ed3a's 25 events/s at 10⁵): **2.9×10⁶× below** — six orders.
- **Lookahead (P6):** prediction horizon ln(10⁵)/λ: belt p99 → 1 052 local orbits (> the 667
  synodic orbits of a Δa/a = 10⁻³ pair — the Diophantine tier survives in the belt);
  co-orbital p50 → **40 planet periods (471 yr)**, max λ → **6 P**: a formation's
  conjunction cycle (~10³–10⁴ P for Δa/a ~ 10⁻⁴) is 25–1000× beyond the horizon — the next
  conjunction of a co-orbital pair cannot be pre-certified; only the current-phase rank
  certificate (coorbital-cert's adopted form, taleb-09b5) is immune.
- λ is flat in tadpole amplitude (medians 0.25–0.33 per P across 0–120° bins): the whole
  tadpole band, not just its edge, is chaotic at this horizon.

Reproduce: `sh lab/results/20261017-1149-dynamics-623d/regen.sh` (~2 min: applies
`work/patch.diff` — the `xtask lyap` probe — builds, runs the three ensembles, prints the
table and compositions). Raw rows: `work/lyap_{control,belt,coorbital}.jsonl`.

## Predictions

`predictions.md` was written before the decisive belt/co-orbital runs. Held: P4's level
(≥30% of tadpoles above 5×10⁻² — 96%, median 0.29), P5 (<0.1 events/game-s — 0.09). Failed:
P1's letter (the null is a bounded stretch with a ±4.3×10⁻³ regression band, not <10⁻⁴),
P2's letter (56% under 10⁻³, not ≥70% — but 90% sit within 2× the null band), P3
(chaotic fraction 1.8%, under the predicted 5–30%; the resonance association held, the
strong slivers are thin at this horizon), P4's amplitude trend (flat, not rising), P6's
inversion for the belt (the belt horizon 1 052 orbits **exceeds** the 667-orbit synodic
lookahead — the Diophantine tier survives in the belt; the inversion holds only in the
co-orbital regime, as reported above).

**Instrument deaths, disclosed (both during calibration, before the decisive runs; both
recorded in the probe's module doc):** (1) restarting only the renormalized twin put the
planet at the wrong phase — the Keplerian control read λ·P ≈ 300; (2) phase-locked
renormalization measured the Kepler monodromy's top singular value (ln σ₁/P ≈ 0.3 — shear,
not chaos). A third bug (velocity rotated about the star's *position*) passed the μ→10⁻¹²
control (the star sits at the origin there) and garbled every real scene — caught because
the belt read λ ≡ 0 with instant saturation. The final instrument's null is exact by
symmetry.

## What would make it wrong

The horizon: 64 planet periods. The real asteroid belt's 3:1 Lyapunov times are
10³–10⁴ yr; mine caps at 759 yr, so the belt's λ are **lower bounds** and the chaotic
fraction (1.8%) can only grow at longer horizons — but P5's margin is 10⁶×, and even λ 100×
larger everywhere leaves the composition 10⁴× under the stream. The co-orbital claim is
robust to horizon (saturated ICs already reached orbit-scale separation). The rotated-pair
construction measures phase-direction divergence only; a full-spectrum Benettin (tangent
integrator) could read a larger λ in eccentricity directions — that would strengthen, not
weaken, both claims. e = 0.1 for all belt ICs (the Rayleigh mode); higher-e tails sample
the resonance overlap more strongly.

Cost of adoption: none (a probe; no engine line touched — outcome-free, the twins run on
the judge only). Fit with PRINCIPLES: "Compute only surprises. Cost follows change and
entropy" — this run prices the entropy term on the game's own scenes; and "a test that
cannot fail is a control": the μ→0 symmetry null and the 3:1/5:2 hotspot structure are the
two-sided controls.

## The lens

The dynamics lens delivered the surprise-rate spectrum, but its blind spot bit once:
long-run behaviour hiding a transient — the first "λ ≈ 0.3 everywhere" reading was the
transient shear of my own instrument, not of the physics; only the exact-symmetry null
separated them. What the lens may still miss: the game-timescale tail (every horizon here
is ≥ 6 yr; nothing is claimed about the player's minute-scale frame), and the belt's
high-eccentricity tail (Rayleigh redraws above 0.4 in the shipped births).
