# Dossier — run 20261020-2158-m2-meso-motion-a877 (lens: mathematical representations, motion and orbits, meso level; second deep pass)

## Claim (one sentence)

A same-(E,L) family — one orbit, phase offsets — is **one integer kick stream**: with the
kick's velocity word at the family's own width (11 fraction bits, the memo code's own
behaviour-passing width) the members' fired kicks are **bit-identical forever** in the root
doll (0 differing firings in 30 synodic periods at separations to 10⁶ root units at 1 AU,
including the full ⅛-orbit ring; 0 to 10³ at the belt), because the per-kick differential
tide h·H·δx sits below the sigma-delta's 2⁻¹⁶·quantum resolution — so a formation rides one
binding and one kick event per epoch — while the shipped 61-significant-bit word splits every
family on **every kick** (first differing firing at kick 0, all cases), which is the exact
mechanism behind 225d's "one kick erases" census; the certificate is the dimensionless number
Ξ = h·H·δx/(2⁻¹¹·v), and above it the fork rate (the family's refinement events) is measured,
not assumed.

## Bottleneck

Board row **"Macro, families and formations (~10² in memory, ~10 in kicks)"** and, through
the mint, the memory row (a fired kick mints ≈2.1 KB, 9edc; every body live at ~1.2 KB after
GPT's cache). What it deletes: for a family of F members, F−1 kick events per epoch, F−1
binding mints per key move, F−1 refits — the members' states are **the same integers**, so
the sharing is exactness-preserving, not an averaging (PRINCIPLES: every body is real; the
member's tube stays its own 16 B; the error vs the continuum is the sigma-delta's bounded
<1-quantum, the law's own error budget, at the family word's width). Expected gain: kicks and
mints ÷ F for compact families (the game births "formation slots on a lattice"), the ring
fleet (a patrol on one orbit) at 1 AU included; at the belt, formations ≤10³ root (1,500 km)
are free and wider spreads fork at the measured rate. This is the open question the board
names verbatim ("a group's reference motion plus each member's small relative state, refined
per member until it deviates... how long a member's certificate lasts against its
separation") — now measured, with the rule that decides it.

## Evidence

One probe, `crates/universe/examples/family.rs` (work/patch.diff), on the shipped law: the
kick's own `force::acceleration` (root doll: Giant μ=2⁻¹⁰ on the plane's circle a=5.263e8
root; Home's doll: the shipped `parent_tide`), and `step.rs::quantize` copied verbatim.
Commands (each ≤ 60 s):

```
cargo run --release -p emergent-universe --example family -- census   # work/census.txt
cargo run --release -p emergent-universe --example family -- growth   # work/growth.txt
cargo run --release -p emergent-universe --example family -- split    # work/split.txt
```

- **Census (the mechanism).** The differential across members is exactly the sources' tidal
  tensor: at 1 AU, |δa|/δx = 2.544e-29 = **2.0×μ_G/d³** radially (the tensor's radial
  eigenvalue), −1× transverse, linear in δx to 10⁶ root; at 2.5 AU, 9.59e-29 = 2×μ_G/d³.
  The origin's fall is x-independent and cancels — the differential has no other source.
- **Growth (the certificate's boundedness).** The carry difference D(t) = ∫δ(a_kick)dt for a
  1-root family, 30 synodic periods, RK4 at 720 steps/orbit: **bounded and flat at every
  radius**, including the exact interior resonances — 1 AU 4.1e-17 (last/mid 1.06×), 2.5 AU
  5.9e-16 (1.00×), 2.82 AU 1.1e-15 (1.30×), res5:2 1.6e-15 (0.96×), **res2:1 1.28e-14
  (0.57×)**: the resonant amplification is ~20× the smooth trend and still bounded — no
  exponential chaos at the plane's μ over these horizons. Kepler repetition holds
  (max|δx| = 1.00–1.03 root: the same-orbit phase-offset construction is the family; a
  position offset at equal velocity is a different orbit and shears at ~n·δx — measured 620
  root from δx0=1 in the first construction — and was never a family).
  - **w61 (the shipped 61-significant-bit word): every kick differs, from kick 0**, at every
  separation ≥ 1 root, both dolls, both cadences (128/orbit and the tide-legal 16/orbit).
    The per-kick differential (belt δx=1 root: h·H·δx ≈ 1.9e-17 c) is ~3.6×10⁵ quanta at
    w61 — the sigma-delta resolves it every time. This is 225d's census derived from the
    law's own arithmetic: no word that fine can share a kick stream.
  - **w11 (family word, 11 fraction bits): bit-identical streams.** 1 AU: **0/4,194 differing
    firings at δx = 10⁶ root and 0/524 at the full ⅛-orbit ring** (δx = 8e7 root). Belt 2.5
    AU: 0/5,763 at δx ≤ 10³ root (the per-kick differential is below the 2⁻¹⁶·quantum
    resolution: identical `inc`, identical carries, forever); at δx = 10⁶: 10/5,763 (first at
    kick 767); ring ⅛: 54/5,763 (0.9%). At 16/orbit the rates halve (4/720, 38/720). The
    forks are the refinement events — each is one member firing one quantum alone — and their
    rate is the per-kick differential in quanta, h·H·δx/(2⁻¹¹v), measured on both sides.
    (Honesty on which rows carry the weight: at 1 AU the whole tide's kick is 0.0016 quanta
    at w11 — the shared stream fires once per ~600 kicks, so the 1 AU zeros are near-trivial;
    the belt rows are the non-trivial proof — the stream there fires 0.0049 quanta/kick at
    128/orbit and 0.0403 at 16/orbit, i.e. a real firing sequence shared bit-identically.)
  - **Home's doll (the plane's fleet region): the family word alone does not certificate it.**
    ρ=10⁵ root (0.001 AU): 591/64,482 differing at δx=10³ (~0.9%/kick); ρ=10⁶ root (0.9 Hill
    radii): the family's own orbit is marginal (B14's edge; the member drifts 371 root) and
    splits from kick ~0 — the Fermi-frame fleet doll (`crates/universe/src/fleet.rs`), which
    already kicks one origin per family, remains the right representation inside planets'
    dolls; the tube-family is the root-doll (and sparse-formation) form.
- **The certificate, one line:** Ξ = h·H·δx/(2⁻¹¹·v) < 2⁻¹⁶ ⇒ bit-identical streams (the
  members are the same integers); Ξ ≪ 1 ⇒ fork rate ≈ Ξ·2¹⁶ per kick (measured 10/5,763 at
  belt δx=10⁶ vs the straddle estimate nkicks·Ξ = 5,763·3.2e-4 ≈ 1.8 — measured 5× it: the
  carry is deterministic, not uniform, so the estimate is a floor); Ξ ≳ 1 ⇒ the ring at the
  belt (0.9%/kick) or the child-doll case (immediate). H is the kick sources' tidal tensor
  (the census: exactly 2μ/d³ radial), h the kick interval, δx the along-arc spread.

## Predictions (predictions.md, written first)

- **P1 (w61 splits everything): held, stronger than written** — differing firings are 100%
  from kick 0, not "within <1% of a synodic period".
- **P2 (w11 restores the certificate): held at 1 AU to the ring (stronger than the predicted
  10⁹-root ceiling — the ring at 8e7 root forks 0 times), and at the belt to 10³ root; the
  predicted 10⁹-root threshold was the D-amplitude bound, but the operative quantity is the
  per-kick differential vs the 2⁻¹⁶ resolution — the certificate is sharper than my
  prediction and the fork rate above it is the honest price.**
- **P3 (member error inside the error model): held by construction** — the sigma-delta bounds
  each member's error below one family quantum (2⁻¹¹·v ≈ 10⁻⁷·v at 1 AU, three decades under
  B2's bar), and D itself is ≤ 10⁻⁹ of that quantum at 1 AU.
- **P4 (chaos sets the long horizon): refuted in the measured regime** — no exponential or
  secular growth anywhere in 30 synodic periods, exact interior resonances included (the
  res2:1 amplification is 20× and bounded); at the plane's μ the horizon is not chaos-limited.
  The child-doll Hill edge (ρ=10⁶ about Home) diverges — correctly, the orbit itself is
  marginal there.
- **P5 (the ring splits immediately at any width): refuted at w11** — the ⅛-orbit ring at
  1 AU fires identically for 30 synodic periods; at the belt it forks at ~1%/kick. It holds
  only at w61 (the control side).

## What would make it wrong, the cost of adoption, PRINCIPLES fit

- **Wrong if** the family word's bounded 2⁻¹¹·v velocity error fails a behaviour gate that
  the 61-bit word passes — the named risk is B13's encounter-phase sensitivity (cell-rebind's
  serving died there on an *accumulating* 2⁻¹¹ period shift; the family's error is bounded,
  a different error type, but the gate must be flown: one named experiment, a w11-family
  variant of the plane against B12/B13/B17/B18). Also wrong if the shipped engine's event
  stream breaks the sharing by cadence or anchor mismatch — same-key members share step size
  and tick anchoring by construction ("steps are powers of two anchored on multiples of the
  step"), but the mint/event side needs the 225d-style census flown on a w11 plane to confirm
  the keys ride together in the engine, not just in the kick arithmetic probed here.
- **Cost:** the velocity word per family (a per-binding width choice the law already makes
  per-doll: `word_for`), the family grouping at birth (the birth program already emits
  "formation slots on a lattice" — the group is free at birth), and the fork handler (a
  member that fires alone rebinds alone — the refit the board calls "refined per member
  until one deviates", at the measured rate). No new state: the shared binding is the intern
  efd4 measured hitting 99.6% at birth; this run shows the kick stream can keep it.
- **PRINCIPLES:** principle 33 verbatim ("a body resolves only the influences that are
  significant at its own scale, and smaller ones enter as an aggregate") — the family word is
  the scale; "one law at every scale" — the same sigma-delta, the same kick, one shared
  evaluation; principle 32 — the symmetry (one orbit = one orbit) was found by representation
  (the phase-free memo key), and the certificate is what it costs to keep it; "compute only
  surprises" — the family's surprise rate is F·(Ξ·2¹⁶) per kick, measured.

## The ranked catalogue (this pass's other candidates, none probed)

1. **The family kick stream (this run).** As above.
2. **The ring's arithmetic sharing (Hansen harmonics of Δv(φ)): dead as a CPU lever** — the
   members' keys fork (correctly, different Δv), so each member still rebinds; the refit
   (~µs) dominates the force evaluation the harmonics would share. Only the *family* form
   (bit-identical streams) deletes the refit, and it deletes the force evaluation too.
3. **The per-body step chooser by dimensionless numbers (the tide class's 16/orbit floor,
   7076): owned by the integrator's cadence job in flight** (`wt/cadence`); this run's Ξ
   composes with it (the family word is per-family what the step is per-body).
4. **The exact pair event at the encounter class (first pass #1): owned by the motion law v2
   design**; 7076's cliff is its certificate case. Not re-run here.
5. **Secular phasors, jets, correctors, resonant normal forms: dead per the record** (the
   belt's conjunctions carry it; one-signed phase error; six runs; r4 v3) — not re-proposed.

## The lens: what it may have made me miss

The meso-math lens reads motion as one orbit at a time and nearly re-derived a D-amplitude
certificate that the integer run corrected (the operative quantity is the per-kick
differential against the sigma-delta's 2⁻¹⁶ resolution). It may miss engine-side facts that
decide adoption: whether the shipped event calendar really fires same-key members at the
same tick under load (the pinned-decision machinery suggests yes, but it is unflown here),
whether the binding mint path can host a family width without a re-freeze (B-gates), and the
game-design question of what formations the player actually flies (F's distribution, which
sizes the win). It also inherits this run's twin's limits: RK4 trajectories between kicks
(not the compiled tube's readout), a circular Giant (the plane's is e=0.05), and no burn arm
(a thrusting member forks its family by construction — the player is the wildcard).
