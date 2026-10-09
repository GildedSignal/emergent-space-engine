# Dossier — 20261009-0621-system-7f97 (system lens)

**Claim.** On the real integer plane, the kick cadence's behaviour frontier is
regime-split by a measured 8× — the resonant bulk holds at 16 kicks per
perturbation period (B17 passes at `step_log2` 4 with e-pump 0.99–1.003) while
deep passages need ≥128 (B13: 60/64 at 7, 62/64 at 8, 41/64 at 6, 3/64 at 4) —
and the plane serves both with one doll-wide constant, so it pays the passage
regime's price everywhere: cutting the bulk's cadence 8× removes ~5× of all kick
events at flat per-kick price, and the knob that must own this split is the
fictitious clock's `Δs`, which today is one constant per doll tied to the
*fastest* secondary (worst case applied to every body, the same shape as
bottleneck 5's position quantum).

**Bottleneck.** Board focus 1 ("fewer kicks per orbit at the same behaviour:
kicks dominate the engine's cost") and 3 (cheaper events). q-cadence's float
replica put the moons' frontier at 4–16/orbit but never validated on the real
law; this run measures the integer plane through its frozen gates and finds the
frontier is not one number but two regimes 8× apart. Nothing here competes with
the queued q-cadence build; it gives it the integer-law numbers and the knob's
true location.

## Evidence

Binary: the shipped `xtask` (two experiment edits, saved in the patch: an
env override `UNIVERSE_STEP_LOG2` on `Config::default`, and an env-gated
`UNIVERSE_STEP_OUTER` regime split in `plan_interval` that turned out to be a
no-op — see Predictions). Linux x86 shared runner, load 1–4; orders of
magnitude only. Default-path bit-identity verified: the bench digest
`21c73edc…` is unchanged with no env set.

```
cargo build --release -p xtask --offline
cargo run --release -q -p xtask -- behave --law plane --gates B13 --plane-step S   # S in 3..8
cargo run --release -q -p xtask -- behave --law plane --gates B17 --plane-step S   # S in 3..6
UNIVERSE_STEP_LOG2=S cargo run --release -q -p xtask -- universe --bench --seed 1 --rtf 30 --seconds 10 --unpaced
UNIVERSE_STEP_LOG2=S cargo run --release -q -p xtask -- universe --kick-bench --seconds 30 --rtf 30 --seed 1
```

**Behaviour vs cadence (the real integer law, frozen gates):**

| S (kicks/period = 2^S) | B13 assists (≥99% of 64 within 1%) | B17 resonance |
|---|---|---|
| 8 (256) | 62/64, worst 1.3e-1 | (>60 s, documented) |
| **7 (128, shipped)** | **60/64, worst 2.1e-2** | (>60 s) |
| 6 (64) | 41/64, worst 8.5e-2 | PASS (pump 0.9995–1.0001, libration 0.998) |
| 5 (32) | 15/64, worst 3.4e-1 | PASS (pump 0.998–1.0003) |
| 4 (16) | 3/64, worst 1.3e0 | PASS (pump 0.990–1.003, libration 0.981) |
| 3 (8) | 1/64, worst 2.9e3 | FAIL (pump 1.31, libration 0.023 — catastrophic) |

The excluded/replaced seed set is identical across all runs (the same 9
oracle-domain draws replaced), so columns compare like for like. Two readings:
(1) the resonant bulk's frontier is 16/orbit — at S=4 B17's pump ratio is still
within 0.4% of 1; (2) the passage regime saturates: even 256/orbit leaves B13 at
62/64, so B13's residual failure is the encounter/changeover representation
(H0214/H0215's finding), not cadence — cadence buys passage accuracy only up to
the saturation, and below 64/orbit it collapses (3/64).

**Cost vs cadence (same window, 1800 frames at rtf 30):** kick samples 630 (S=7)
vs 126 (S=4): 5× fewer kick events; fitting a fixed + cadence-driven split
(F + C, F + C/8) gives ~91% of the S=7 kick stream cadence-driven. Per-kick
price flat (median 88 vs 71 µs; the resolver is the same work), cycle rebinds
611 → 108 (each kick rebinds, so compiles track kicks), events/s 170 → 81
(kicks ≈ half the event stream; the rest — boundaries, opens — is
cadence-independent). The bench is view-dominated (engine share 13%), so the
engine-side ratio is the number that matters, not wall time.

**Where the knob actually lives (the structural finding).** Root-doll ships and
the player are stepped by the motion law v2's fictitious clock
(`on_clock` → `plan_clock`): `Δs = 2^-k · P_D/f'(c)` with `c` the doll-wide sum
of secondary potentials at their Hill radii and `P_D` the *fastest* secondary's
period (`ext::constants`). So the bulk's cadence is one constant per doll, set
by the worst-case secondary, applied to every body in the doll — a tick in
principle 14's sense (work not derived from any per-body validity claim), and
the same "worst case applied everywhere" shape as the position quantum in
bottleneck 5. In-doll ships, planets and moons instead use `plan_interval`
(2^k per *own* period, plus the engaged cascade `RATIO=4 × LEVELS=3` near
secondaries). Two cadence mechanisms already coexist; the split this run
measures says they should be one rule chosen by a dimensionless number (the
body's coupling to its perturbers), not two constants.

**Distinctions are cadence-independent (the negative, P4).** The sigma-delta
carry (`step.rs::quantize`: `out = (carry + inc)/65536`) conserves the total
quanta supplied by the tide, so the velocity-quanta applied per orbit — the
feed of H_live — does not fall with cadence. Measured support: the quantized
(E,L) memo visits the same 45 shapes at S=7 and S=4; only the rebinds per shape
change (611 vs 108). So cadence cuts *work* (events, compiles, encounter
re-setup), not *distinctions*; H_live is physics-fed and stays with b-h-live.

## Predictions (predictions.md, written before any run)

- P1 (B13 holds at S=4): **falsified** — 3/64. The float replica's 4–16/orbit
  moons' frontier does not transfer to deep passages on the integer law.
- P2 (B17 passes 4–6, fails at 3): **held**, including the catastrophic mode
  (libration 0.023 at S=3).
- P3 (≈2× events per unit of S, kicks dominating): **held with a correction** —
  kicks fall 8× but total events only ~2× (a cadence-independent boundary/open
  floor of ~70/s).
- P4 (H_live feed cadence-independent): **held** (carry math + the 45-shape
  invariance).
- P5 (error type): partially answered — B13's degradation with lower S is
  smooth (error size, h²-like: worst 2.1e-2 → 8.5e-2 → 3.4e-1 → 1.3e0 ≈ ×4 per
  halving), while B17's S=3 failure is a regime break (libration crushed 43×),
  not a marginal walk.
- **Disclosed no-op:** my hybrid patch (`UNIVERSE_STEP_OUTER`: coarse in the
  root doll, fine in secondaries' dolls) changed `plan_interval` only; B13/B17
  ships are clock bodies, and PLANE_TRACE confirmed byte-identical event counts.
  The "hybrid = 60/64" runs are the same law as uniform 7 and are NOT evidence
  for the regime split; the sweep is. The clock-path hybrid is the named
  experiment below.

## What would make it wrong

The frontier is measured on two gate families in one weak-field scene each;
a doll whose fastest secondary is also the resonant one couples the two regimes
(the split must then be per body, not per doll). B13's saturation at 62/64
could be cadence-limited after all if S=9–10 recovers the last flybys — one
cheap run I did not spend the window on. The cost split (91% cadence-driven)
is from the bench scene's ship population (mostly fleet leavers in a planet's
doll); a belt scene could differ, and the in-doll (`plan_interval`) path's own
frontier was not swept separately.

## Cost of adoption, fit with PRINCIPLES

The adoptable form: `Δs` per clock body derived from the body's own coupling
(the dimensionless U_P/c at clock start, re-derived on approach — the clock
already carries per-body state), coarse in the bulk (16/orbit, B17-measured)
and fine near Hill shells (≥128, B13-measured); one rule replacing two
constants. It composes with the jet (fewer kicks × cheaper kicks, per
20261008-1719) and with the skin (fewer element changes to absorb). Fit:
"ticks make no sense to me… not compatible with our certificate/compiler idea"
(#14 — a doll-wide Δs tied to the fastest secondary is a tick); "regimes are
chosen by dimensionless numbers" (#4); "an ant cares about a raindrop but the
lion does not" (#33 — the bulk does not pay the passage's resolution); "The
cheapest compute is compute not done" (#1).

## The lens (what the system view made me miss)

I went in expecting the unification "cadence feeds compile, encounters and
H_live alike" and measured the last leg away: the sigma-delta carry already
decouples distinctions from cadence — the store's quantum discipline is ahead
of the scheduler's. What remains unified is narrower and sharper: the tick is
one doll-wide constant read by every body, and the fix belongs to the same
per-body validity budget the jet and the skin read (one certificate, three
consumers: how long the formula holds, how often to kick, what a perturbation
invalidates). The hard case that could break it: a body crossing regimes
mid-clock (a belt body scattered onto a passage) must re-derive Δs at the
crossing — the clock's per-body state makes this legal, but the re-derivation
is exactly where a hidden tick could regrow. My hybrid no-op cost ~15 minutes;
a checker sweeping S=9–10 on B13 and one belt-scene cost run would close the
two open holes above.

Grade suggested: **silver** — real, reproduced frontiers on the frozen gates,
one named experiment from gold (the clock-path regime split, validated by
B12+B13+B17 together and a belt cost run).
