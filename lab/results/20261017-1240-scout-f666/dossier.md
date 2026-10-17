# Dossier — 20261017-1240-scout-f666 (scout): the doll boundary rule

**Claim:** The doll boundary's chatter is a Zeno problem whose cure is the decision
variable, not the band: deciding once per apsis on the cycle's own radial extent
(r_apo vs the empirical stability radius f(Λ)·R_H, Λ-continuous, margin 0.05) gives
**0 handoffs** where the shipped per-tick predicate chatters at **9.4 per moon-orbit
(180–201/20P, 942/100P — unbounded, linear in time)**, exactly **1 per actual
transition**, is kick-robust (1 handoff where plain two-threshold hysteresis
re-chatters at 76), and misreleases only bodies sitting on the empirical retrograde
edge itself (0.7 R_H retro: released once, still retained at 100P — a dial, not a
failure, and never a re-chatter).

**Bottleneck:** handoff open direction 2 ("rebuild the surface rule"), blocking motion
law v2 step 3 (single-surface handoff; Codex's attempts failed, kept on branches).
Gain: the boundary's event bill drops from ~9.4 rebinds/body/orbit (each a 21–63 µs
rebind plus a one-shot scar ≈ 0.7·(β_c²/2)·|δv| inside light windows, 7ab4 — a
compounding channel at 942/100P) to 0 on stable bodies; deletes the per-tick boundary
check entirely (one integer compare per apsis, on a quantity the compiled cycle
already owns — its radial extent; no new clock, no new state).

## Requirements (numbers, tied to PRINCIPLES)

- Events: a handoff is a rebind (~21–63 µs, a765) — the boundary must cost ~1 event
  per actual ownership change, never per tick (the whole event budget is ≤ 512/orbit,
  board bottleneck 2). #14 (no ticks), #1 (cheapest compute is none).
- Error type, not size: each handoff scars once (7ab4's law); chatter multiplies the
  scar per orbit — errors must not compound (#13). One decision per cycle is one-shot.
- No categories (#4): the criterion is a dimensionless number pair (r_apo/R_H, Λ =
  h_z/r_apo²), thresholds from dynamics, continuous in Λ — "prograde/retrograde" is a
  number, never a class.
- Local (#15) and integer-friendly (#16): f(Λ)·R_H uses only the doll pair's
  constants; r_apo and h_z are cycle-owned quantities (the compiled key already
  carries periapsis; apoapsis at the apsis is the current radius — zero extra
  arithmetic).
- Zeno-free by construction, not by tuning (the rung-writing rule: passable in principle).

## The fields that faced this structure (ranked by fit)

The structure: state-dependent reclassification that chatters at a switching surface
(finitely often per period here, unboundedly in total time — "Zeno of the second kind",
infinite total transitions).

1. **Hybrid systems, Zeno resolution** (Johansson, Egerstedt, Lygeros, Sastry, *On the
   regularization of Zeno hybrid automata*, Systems & Control Letters 39 (1999) 41–50 —
   verified at source): two regularizations exist — hysteresis and time-regularization.
   Fit: exact diagnosis (the 21,403-handoff flight is a chattering execution); the two
   cures map to R1 (band) and R2 (dwell). Known failure mode: hysteresis trades
   chattering for in-band drift; dwell delays true transitions and pays the cap rate
   forever — both measured below.
2. **Celestial mechanics: capture criteria** (temporary-satellite-capture literature;
   Shen & Tremaine 2008, AJ 136, 2453 — verified via abstract: prograde satellites
   survive to ~0.5 R_H, retrograde to ~0.7 R_H; Domingos et al. 2006, MNRAS 373, 1227 —
   empirical stability-boundary expressions, coefficients UNVERIFIED): the boundary is
   *empirical stability radius × sense*, not a metric radius; my replica reproduces
   their table ((0.5,pro) ejects, (0.5,ret) and (0.7,ret) survive). Fit: this is the
   doll question at planetary scale, solved by practitioners; supplies f(Λ) and the
   honesty that it is an empirical dial, not a theorem.
3. **Sliding-mode control** (chattering → boundary layer; Utkin 1977; Slotine & Li
   1991 — standard textbook, UNVERIFIED at source this run): the boundary-layer cure is
   R1; its known cost is steady-state error ∝ band width. Same as (1) in effect.
4. **AMR flagging + buffer zones** (Berger & Oliger 1984 — standard, UNVERIFIED):
   reclassify on an error estimator with a buffer, not on geometry. Fit: supports
   deciding on the *representation's own validity extent* (the cycle's r_apo) rather
   than instantaneous r — the decision-variable half of the rule.
5. **MD Verlet skins** (Verlet 1967 — standard, UNVERIFIED): margin sized by drift
   between rebuilds; the analogue is margin m vs per-cycle apsidal drift. Sizing rule
   adopted (m = 0.05·R_H ≫ the measured quiet-case apsidal drift; not tuned tighter).

Composite candidate (R3): **decide once per apoapsis, on r_apo vs f(Λ)·R_H ± m,
Λ-continuous, E_p<0 retained on capture as a safety** — event-triggered on the cycle's
own apsis (Zeno-free: one decision point per orbit), hysteresis in owner state by
construction (two thresholds), topological (the extent of the tube, not the instant).

## Evidence (regen.sh reproduces every number; ~1 min total)

Replica: planar CR3BP, DOP853 rtol=atol=1e-12, |ΔC_J| ≤ 8.4e-10 on every case (K5
pass); μ ∈ {1e-4, 1e-3, 1e-2}; body born planetocentric-circular at r0·R_H, 8 cases ×
both senses, 20 planet periods (100P for the adjudication), plus a 3% radial kick at
t = 10P. All rules replay the SAME true trajectory — the decision stream is measured,
not trajectory identity (per the r2 criterion-writing rules). Handoffs do not feed
back into the physics (disclosed limitation; the rebind's physics error is priced via
the pages' own scar law, not simulated).

| case (r0/R_H, sense) | truth (100P) | R0 shipped | R1 hysteresis | R2 dwell | R3 per-cycle |
|---|---|---|---|---|---|
| (0.3, pro) / (0.3, ret) | retained | 0 | 0 | 0 | **0** |
| (0.49, ret) 20P | retained | **180** | 0 | 20 | **0** |
| (0.5, ret) 20P / 100P | retained | **201 / 942** | 0 / 0 | 20 / 97 | **0 / 0** |
| (0.5, pro) 20P / 100P | ejected | 5 / 11 | 3 / 9 | 1 / 7 | **1 / 1** |
| (0.7, ret) 20P / 100P | retained | 1 / 1 | 1 / 1 | 1 / 1 | **1 / 1** (edge dial) |
| (0.9, pro) / (0.9, ret) 20P | ejected | 1 / 1 | 1 / 1 | 1 / 1 | **1 / 1** |
| (0.5, ret) + 3% kick at 10P | retained | 179 | **76** | 20 | **1** |
| (0.5, pro) + 3% kick at 10P | ejected | 5 | 3 | 1 | **1** |

- μ-invariance: R0 chatter 179–187 on (0.49–0.5, ret) at μ = 1e-4/1e-3/1e-2 — the flip
  rate is synodic geometry, not the mass ratio.
- The shipped-probe failure class reproduces: the wiki's measured 210 handoffs / 20
  periods at 0.49 R_H retrograde (18d2's checker) vs 180 here, same per-orbit class
  (~9/orbit). The relativistic probe's 21,403 (0.5-retro) and 4,455 (0.9-pro)
  magnitudes were NOT reproduced (different regime/window; UNVERIFIED against that
  probe) — my 0.9-class cases eject promptly with 1 handoff everywhere.
- R0's count is sampling-invariant at 100–200 samples/orbit (R0f control: identical
  counts at every-2nd-sample) — the chatter is the body's own apsidal flip dynamics,
  not an alias of the tick.
- **R3 never exceeds 1 handoff per moon-orbit anywhere** (K3 pass); releases nothing
  deep (moon test, K2 pass); retains nothing forever on true ejections (K4 pass);
  classification errors are exactly the two empirical-edge dials: (0.7,ret) born on
  Shen–Tremaine's retrograde edge (released at its first apoapsis, still within 1.07
  R_H at 100P — conservative, single, never re-chattering), and the kicked (0.5,ret)
  whose pumped apoapsis crosses 0.75 R_H. Both are f/m dial choices, disclosed.

### What would make it wrong

- The replica is Newtonian CR3BP, planar, one perturber, replay-only (no rebind
  feedback, no relativistic shears — the 18d2 probe ran β ≤ 0.9 through nine shears).
  If the relativistic chatter class has a different mechanism (their 21,403), the
  per-cycle rule's event count there must be re-measured on that probe — the Zeno
  argument (one decision point per orbit) is mechanism-independent, the dial is not.
- f(Λ) is empirical (literature values 0.5/0.7), and the Λ-ramp shape is invented;
  eccentric, inclined, multi-perturber and GR domains unprobed — the boundary dial
  must be re-derived where the stability table changes (the wiki's r9 τ-bound is the
  in-engine analogue for the *kick* regime).
- Replay means the rule cannot rescue a trajectory the true dynamics ejects — the
  classification columns are the deliverable, not trajectory quality.
- A body that wanders in the f±m band orbit-to-orbit would still hand off once per
  orbit (bounded, but nonzero); none measured here (max 1 total), but a chaos-driven
  case could sit there. The margin m is the knob, Verlet-skin style.

### Fit with PRINCIPLES

- #4 "no object categories: regimes are chosen by dimensionless numbers" — Λ and
  r_apo/R_H are the numbers; the sense ramp replaces the pro/ret split.
- #13 "errors never compound" — chatter × rebind-scar is the compounding channel;
  1-per-transition makes it one-shot.
- #14/#22 "no ticks … the simulation tells us what's next" — the apsis is the
  simulation's own event point; the per-tick boundary check is deleted.
- #19 "a fix signals the wrong representation" — the refuted predicate decided on the
  instantaneous radius (a per-tick metric); the representation that fixes it is the
  cycle's extent (the tube's own water).

### Cost of adopting

One rule at the apsis site (where the compiled cycle already reads its radial extent):
one compare and, on crossing, one handoff — the payload machinery (tide, keys) is
18d2/ae29's and unchanged. The dial (f-ramp, m) needs one freeze decision. The
checker's six-case table, P5 and the moon test (18d2's instruments) are the adoption
gate; this replica is the rule-class evidence, not the engine test.

### The lens (scout)

What it may have missed: the scout ranks by cross-field fit and reaches for the
literature's dial (0.5/0.7 R_H) — an in-engine derivation from the law's own compiled
frequencies (the r9 τ-family) might place the boundary better than Shen–Tremaine's
giant-planet empirical table, and the relativistic probe's chatter magnitudes were
never re-run here. The replay design also hides any feedback between the rule and the
rebind error — only an engine arm can price that.

## Predictions vs outcome (predictions.md written before the run)

- P1 half-held: R0 chatter ≥ 10 on (0.49,ret) 180 and (0.5,ret) 201 ✓; **failed on
  (0.9,±): 1 each** — those eject promptly in this replica (the 4,455 thrash is the
  relativistic probe's, not reproduced). K1 stands on the 10² class.
- P2 failed as stated: R0f is sampling-invariant at these densities (the flips are
  ~20 samples apart; the count is the physical flip rate, not the tick alias) —
  reported as held in the sense that matters: the chatter is dynamical, not sampling.
- P3 held: R3 = 0 on every retained case except the 0.7-ret edge dial; 1 on all
  ejected; ≤ 1 per moon-orbit everywhere; classification = truth except the edge.
- P4 failed in the quiet regime (R1 = 0 at 20P/100P — hysteresis *does* cure quiet
  chatter) and held in the kicked regime (R1 = 76 vs R3 = 1): the E_p/apsis channel
  is a kick channel, not a quiet channel. The field ranking survives on transitions,
  kicks and persistence (R2 = 20/97), not on quiet chatter.
- P5 held: post-kick R3 ≤ 1 vs R0's 179.
