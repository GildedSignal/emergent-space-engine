# Dossier — 20261012-1227-dynamics-bd4e (dynamics lens)

**Claim.** The plane's B12 failure is an instrument artifact, not compounding: on every frozen ship it
answers (6 of 14), the Jacobi error's structure function is flat (median slope β = 0.05, no
increment bias, z = 0.02) — a bounded attractor — while the growth exponent the gate trusts reads
0.39–1.0 on the same traces; and a median-slope statistic separates the P2 control pair
(bounded 0.149 vs compound 0.451 vs drift 0.631, in the right order) that today's exponent cannot.

**Bottleneck.** The instrument (HANDOFF "Risks to attack first": B12 cannot tell bounded from
compounding on chaotic ships; queue item `q-b12-design`). Gain: one statistic replaces the
miscalibrated exponent; it deletes the ambiguity that currently keeps the motion law's stability on
probes instead of a gate, and it adjudicates the plane's standing B12 conviction. No orders of
magnitude: this is the "shows that a premise is wrong" kind of gold.

**Evidence.** Linux x86, 8 vCPU shared, load 3.05/8, 13.3 GB free; run twice, identical numbers.

```
cd <tree> && cargo test --release -p xtask b12_error_type -- --ignored --nocapture   # 41 s + build
```

The probe (an `#[ignore]`d test in `xtask/src/behave/handoff.rs`, in this run's `work/patch.diff`)
types the SIGNED Jacobi error on B12's 16 frozen ships at the gate's own samples (200 periods, 8 per
period): β = slope of ln D(τ) vs ln τ over the top lag decade (bounded → 0, random walk → 1,
drift → 2), z = t-statistic of the mean increment over the second half (|z| > 3 = systematic sign),
against `fit::growth_exponent` on |e|. 14 of 16 ships judged (2 excluded by the gate's own rules).

| law | exponent (median) | β (median) | z (median) | verdict |
|---|---|---|---|---|
| echo | below floor (max 2.3e-15) | ≈ 0.00 | ≤ 0.07 | bounded, at the float floor |
| planted-bounded (P2 control, must PASS) | **0.353** (worst 1.471) | **0.149** | 0.53 | **bounded** (13/14 ships) |
| planted-compound (must FAIL) | 0.416 | 0.451 | 0.93 | diffusive |
| planted-drift (must FAIL) | 1.355 | 0.631 | 1.41 (4/14 ships z > 3) | drift/diffusive |
| **plane** (step 7; 6 answer, 8 no answer) | 0.392 | **0.052** (all six \|β\| ≤ 0.10) | 0.02 | **bounded, max err 3.1e-6** |

- The plane's exponent ranks it with the leaks (0.39 here; 1.03 at the 6 October freeze); its
  structure function ranks it with echo and the bounded control, flat by a factor of ~9 below the
  compound control's. The exponent reads the wandering amplitude of a bounded error — P2's disease,
  now measured on the shipped engine. **The plane does not violate principle 13 on these traces.**
- The plane's real B12 exposure is coverage: 8 of 14 frozen ships get no answer (`NoBoundOrbit`/
  plunge — the `b-plunge-tubes` item), an oracle-domain matter, not an error-type one.
- Echo at 1e-15 is below the 1e-12 floor here, so "echo fails B12 on Linux" does not reproduce on
  these traces (platform difference left to the red-team, not adjudicated).

Data: `data/b12type.csv` (per-ship table), `data/b12traces.csv` (worst ship's signed trace per law).

**Predictions** (`predictions.md`, written before any run). Held: echo bounded; the bounded control
bounded (β 0.149, inside my 0.15–0.6 band). Failed, all reported: compound's β is 0.451, not
0.8–1.15, so my frozen per-ship threshold 0.65 calls it bounded — a leak of 8–42 encounter steps in
200 periods is still in its transient (the asymptote β = 1 needs the leak's own clock, encounters,
or a longer horizon); drift's z > 3 on 4/14 ships, not half; and the plane is bounded (β 0.05), not
the diffusive leak I predicted. The failure that matters is the informative one.

**What would make it wrong.** The 6 answered ships are a tame subset — the ships the plane loses are
the plunging, chaotic ones, so the bounded verdict could fail exactly where it cannot yet be
measured; only plunge tubes can close that. A leak slower than ~σ²/T (10⁻¹²² over 100 periods
here) is invisible to any 200-period trace statistic; β bounds the exponent only within the
measured lag decade. The median-separation (0.149 vs 0.451) was observed, not predicted — a
threshold chosen from it now would be tuned, so the red-team must freeze one blind. **Cost of
adoption:** ~40 lines on the trace B12 already computes; no new oracle work. **PRINCIPLES:** "errors
never compound... divergence is not a joke" (13) — typed, per OC#42 "types of errors and not just
errors"; the typing itself is clock-stability practice ("it's a space clock literally", 28), stolen
from timekeepers with skin in the game (26); gates judge a representation and never size it — β
types the attractor, no magnitude.

**The lens.** The dynamics lens trusted the trace and under-weighted selection: which ships answer
is decided by the law, not the judge, and 8/14 unanswered is the number a gate must confront before
any error typing. Long-run transients (this lens's own blind spot) cap what 200 periods can certify.
