# Dossier — 20261009-0709-second-20261009-0621-system-7f97-1eca (second author on 20261009-0621-system-7f97)

**Claim.** The checker's named gold experiment is done: the clock-path regime split is
built, shipped-code-gated and cost-measured — Δs per clock body from the coupling its
own **orbit** permits (`ext::split_k`: one bit per octave of κ = Σ gm_j/gap_j over c,
anchored at κ = 1 at `Config::step_log2`, floored 3 octaves below), **refining only and
never coarsening within a clock** — and it holds: B13 and the default path are
bit-identical to shipped (60/64, digest `21c73edc…`), B17 PASSES (pump [0.984, 1.001],
libration 0.981, 34/34 regimes, 5/5 controls) where the naive uniform cut fails B13 at
3/64, and a belt of 2,000 clock bodies runs **4.7× (wide belt) to 7.8× (inner belt)
fewer kicks** at the same gates. The run also measured a law-level constraint the
q-cadence build must respect: **a cadence that modulates with the orbit pumps a
resonant libration and destroys it** (two falsifications below), so per-body cadence
may only refine — the ratchet is not an optimisation but a correctness condition.

**Bottleneck.** Board focus 1 (fewer kicks per orbit at the same behaviour). The first
run measured the 8× regime split and named the knob (the doll-wide Δs, a tick in
principle 14's sense); this run turns it into adoptable code and validates it through
the frozen gates, folding the checker's S=9/10 saturation (the claim is bulk-only:
passages keep their shipped resolution, which is the best B13 gets anywhere).

## Evidence

Linux x86 shared runner, load 1–4; orders of magnitude only. Patch:
`work/patch.diff` (crates/universe: ctx.rs `clock_split` config + env
`UNIVERSE_CLOCK_SPLIT`; ext.rs `ds_unit`, `split_k`, `RAMP_LOG2`; step.rs
`coupling_bound`, per-kick re-derivation with the ratchet; examples/belt_bench.rs).
All commands ≤ 60 s unless noted.

```
cargo build --release -p xtask --offline
cargo run --release -q -p xtask -- universe --bench --seed 1 --rtf 30 --seconds 10 --unpaced        # digest control
UNIVERSE_CLOCK_SPLIT=1 cargo run --release -q -p xtask -- behave --law plane --gates B13
UNIVERSE_CLOCK_SPLIT=1 cargo run --release -q -p xtask -- behave --law plane --gates B17            # 36 s
cargo run --release -q -p xtask -- behave --law plane --gates B12                                   # shipped baseline, 38 s
UNIVERSE_CLOCK_SPLIT=1 cargo run --release -q -p xtask -- behave --law plane --gates B12            # 41 s
cargo run --release -q -p emergent-universe --example belt_bench --offline -- 20000 3300 2000 7           # wide belt
UNIVERSE_CLOCK_SPLIT=1 cargo run --release -q -p emergent-universe --example belt_bench --offline -- …    # split
cargo run --release -q -p emergent-universe --example belt_bench --offline -- 20000 3300 2000 7 1.5 2.1 0.12  # inner belt
```

**Gates** (data/*.txt):

| gate | shipped (7) | split (this run) | uniform 4 (first run) |
|---|---|---|---|
| B13 assists | 60/64, worst 2.12e-2 | **identical, trace-identical** | 3/64 |
| B17 resonance | pass (H0215; >60 s) | **PASS** pump [0.984, 1.001], lib 0.981, 34/34, 5/5, 36 s | PASS |
| B12 handoffs | FAIL, median exp ∞, worst ∞ | FAIL, median 0.608, worst ∞ | FAIL, median 0.588 |

B13's identity is structural, not lucky: every judged diver's orbit overlaps the
planet's radial band, so the bound reads full coupling and the clock runs the shipped
k = 7 from the start (PLANE_TRACE byte-identical, `data/trace-*.txt`). B12 fails on
the shipped law itself (it loses judged ships; H0215: "B12 unusable until rebuilt"),
so it cannot validate anything today; the comparison it does support — same 14 judged
ships, same worst — shows the split does not degrade it (median exponent ∞ → 0.608:
fewer lost ships than shipped, slightly more error than the naive cut on those it
keeps).

**Cost** (`data/belt*.txt`; 2,000 clock bodies, star + 3 planets, no fleet; 1.1×10⁶
game-seconds):

| scene | kicks shipped | kicks split | ratio | events | wall |
|---|---|---|---|---|---|
| wide belt (1.8–3.6 AU, e ≤ 0.25) | 78,385 | 16,732 | **4.68×** | 4.68× | 6.1 → 2.4 s |
| inner belt (1.5–2.1 AU, e ≤ 0.12) | 78,094 | 10,032 | **7.79×** | 7.8× | 5.9 → 2.0 s |

No losses, no handoffs, digests differ (the law changed) and reproduce bit for bit on
rerun (`59752da9…` twice). The wide belt's 4.7× is the orbit bound's honesty, not a
weakness of the rule: apoapsis 4.5 AU sits 0.44 AU from Giant's band — 1.4 R_H(Giant)
— so those bodies genuinely can encounter and keep k = 5; the inner belt (gap > 8 R_H
to every planet) takes the full 8× floor. On the shipped **bench** scene the split is
invisible by construction: the 12 root ships' first kick is ~2×10⁵ game-seconds out
(the 170 events/s are all in-doll `plan_interval` bodies), so kick-bench is identical
(630 samples, 611 rebinds, 45 shapes) and the digest moves only through the root
ships' `ext.ds` (`bb81ae6e…`). This also resolves the first run's conflation: its
"5× off the bench" was the *in-doll* path moving with `Config::step_log2`, not the
clock path.

## Predictions (predictions.md, written before any run)

- **P1 (B13 within ±2 of 60/64): held exactly** — and stronger: identical, because the
  split is inert on B13's draws (orbits overlap). The named lag risk never materialised:
  the orbit bound refines *before* the approach, not at it.
- **P2 (B17 bit-identical to uniform-4): falsified, twice, then held after re-deriving
  the rule.** v1 (position-based κ): catastrophic FAIL, libration 0.002, pump
  [0.687, 3.34] — κ crosses the 1/8 shell twice per synodic period, so the cadence
  modulates at the resonance's own frequency. v2 (orbit-based κ, no hold): FAIL,
  libration 0.008, exactly the two 3:2 μ = 3e-3 cases whose *libration* walks κ across
  the k = 6/7 boundary — the modulation moved to the libration frequency and still
  pumped. v3 (the ratchet): PASS. The pre-registered "stop and re-derive" was executed;
  the published rule is the re-derivation, and the two failures are the evidence for it.
- **P3 (B12 no compounding): not decidable today** — the gate fails on the shipped law.
  What it can say: the split is no worse (median ∞ → 0.608, same worst), and the
  compounding channels the falsifications exposed (modulated cadence) are exactly what
  the ratchet removes.
- **P4 (belt ~8×): held for the inner belt (7.79×), missed for the wide belt (4.68×)** —
  the geometry of Giant's Hill radius, quantified above.
- **P5 (bench 126–250 samples): falsified in number (630, unchanged), confirmed in
  substance** — the bench cannot see the clock path at all.
- **P6 (default-path bit-identity): held** — `21c73edc…`, 60/64, every run.

## What would make it wrong

The ratchet leaks: a body scattered outward after one deep encounter keeps its finest
cadence until its clock restarts (a handoff back to the root doll re-derives it). In
scenes with many scatter victims the saving shrinks toward shipped; the encounter skin
(element-change certificates) is the designed partner for resetting it, and that
coupling is untested here. The bound is radial: it ignores phase, so a body whose band
approaches a secondary's within ~8 R_H but never conjuncts still pays k = 5 — the
Binet-cone work (r8) is the honest refinement. B17's PASS is one gate family in three
mass ratios; a doll whose fastest secondary is also the resonant one still couples the
regimes, as the first author noted. And the whole validation is on the plane's
weak-field scenes; the in-doll (`plan_interval`) path keeps its own two constants,
untouched by design.

## Cost of adoption, fit with PRINCIPLES

One rule replaces the doll-wide constant: `split_k` (11 lines) + `coupling_bound` (36
lines) + the ratchet field; `clock_split` defaults off, so the merge is a flag flip
after review. It deletes ~4.7–7.8× of the clock path's kick events on belt-like
populations — the population the billion-body goal is made of — at unchanged gate
behaviour. Fit: "ticks make no sense to me… not compatible with our
certificate/compiler idea" (#14 — the step is now a per-body validity claim over what
the orbit will do); "regimes are chosen by dimensionless numbers" (#4 — κ, one bit per
octave); "an ant cares about a raindrop but the lion does not" (#33); "errors never
compound" (#13 — the ratchet exists because we measured that a modulated cadence
does). For q-cadence (queued): the frontier numbers stand (bulk 16/period, passages
saturated), and this run adds the constraint its build must carry: **cadence changes
only by refinement within a clock, or at handoffs** — a modulating cadence is not a
cheaper integrator, it is a different (worse) law.

## The lens (what the second-author view made me miss)

I inherited the first run's conclusion that the knob's location was the finding, and
spent my first implementation on it (position κ) — the inheritance itself was the
blind spot: the shipped law's "Δs held by the body" was not a compromise but a
correctness condition, and it took two falsified gates to see it. I also nearly
shipped the v1 no-op lesson backwards: my first bit-identity check caught the split
leaking into the default path (`bb81ae6e…`), which is the mirror of the first author's
`UNIVERSE_STEP_OUTER` trap — check the control before reading any result. What I did
not do: sweep the ratchet's interaction with `plan_interval`'s own hysteresis (the
in-doll path keeps `step_log2`), and B12 remains the un-run validation the checker
named, for the reason the checker named it.
