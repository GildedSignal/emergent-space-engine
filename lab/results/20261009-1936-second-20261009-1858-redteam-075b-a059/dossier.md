# Dossier — 20261009-1936-second-20261009-1858-redteam-075b-a059 (second author on 20261009-1858-redteam-075b)

## Claim

The checker's named experiment is done: the design's **actual** policy — law.md:35's jet,
re-anchored ("error grows as C·drift²; when the accumulated offset reaches √(floor/C) the
cycle is recompiled") — implemented on a separatrix ladder with a clean curvature estimate,
**cannot hold both navigation (≤ 1e-3 rad) and cost (≤ 700 crossing-evals/orbit, the probe-2
fixed-step control) within (p−6−2e)/p ≲ 0.05–0.1, at any floor (1e-6, 1e-3), either trigger
reading, any margin, both seeds** — the original author's central claim, now confirmed on the
design's own mechanism: hot orbits pay the full kick rate in recompiles (saturation: 32
anchors/orbit, 1822–4606 evals/orbit = 2.6–6.6× the control) at the tight floor, and lose
navigation (1.6e-3–5.7e-2 rad) at the loose floor. The skin boundary is measured, not
hedged: robust kill s ≤ 0.05, knife-edge at s = 0.1 (passes on one seed only), robust pass
s ≥ 0.2. The cold bulk survives at a workable operating point the design doc never pins
down (the honest 2D trigger at floor = 1e-3: 87–556 evals/orbit, ≤ 1.5e-4 rad).

## Bottleneck

Board focus line 1 (kicks dominate cost) and §6's "undisturbed orbits ≈ 0". What this run
deletes: the belief that law.md:35's mechanism is uniform in eccentricity/field — it has a
skin, and the skin is where slingshots live. What it adds: the routing number ((p−6−2e)/p ≲
0.1 → dense order) and the r-kick-absorb gate design (seed sweep mandatory). Order of
magnitude at stake: 2.6–6.6× the entire fixed-step control budget per hot orbit, or 2–57×
navigation tolerance.

## Evidence (float64, Linux x86, 8 vCPU shared, every command ≤ 60 s)

Code: `jet_anchor.c` — the author's shipped law/truth machinery verbatim (1PN Binet
u″ = C+3u²−u, RK4 h=1e-3, periapsis element jumps dC=εC₀s, dK=−2u_p·dC), plus the jet:
anchor with exact F, first derivatives and a clean 9-point Hessian; trigger ½|q₂| > floor/margin
→ recompile at the body's state; 32 kicks/orbit (H0190). tmode=1 is law.md's literal 1D
trigger (FCC·dC²); tmode=2 the honest 2D (dᵀHd) — kicks move both C and K. One compile =
one radial cycle = cr crossings, cr = 2·16·log₂((1+e)/(1−e))+8 (B9, m=16): 58.7 (e=0.5),
143.9 (e=0.9). Derivatives not charged (the integer law differentiates the quadrature).

```
gcc -O2 -o jet_anchor jet_anchor.c -lm && gcc -O2 -o kick_absorb kick_absorb.c -lm
./run_ladder.sh          # 452 lines -> ladder.log  (the decisive ladder, ~5 min, -P7)
./extras.sh              # eps-scaling, systematic, fd checks -> extras.log
python3 analyze.py ladder.log   # verdict table
# representative single commands (each <= 60 s):
./jet_anchor 8.21053 0.9 1e-4 0 200 1e-6 1 1    # hot, tight floor: sat, 4566 ev/orbit
./jet_anchor 8.21053 0.9 1e-4 0 200 1e-3 1 1    # hot, loose floor: nav dies (0.017-0.048)
./jet_anchor 15.6   0.9 1e-4 0 300 1e-3 1 1 1e-3 32 2   # cold workable: 87 ev/orbit, 7.1e-5
./jet_anchor 7.87879 0.9 1e-4 0  60 1e-6 1 1 1e-3 32 1 1e-5  # s=0.01: 32.0 anchors/orbit
```

**Verdict table** (frozen rule in predictions.md; max over seeds; full table in
`analyze.py` output; PASS = some jet config ≤ 700 evals ∧ ≤ 1e-3 rad):

| s=(p−6−2e)/p | e=0.5 | e=0.9 |
|---|---|---|
| 0.5 | PASS — t2@1e-3: 42 ev, 1.2e-4; t1@1e-6: 207 ev, 2.1e-5 | PASS — t2@1e-3: 87 ev, 7.1e-5; t1@1e-6: 321 ev, 1.6e-5 |
| 0.3 | PASS — t2@1e-3: 223 ev, 1.5e-4 | PASS — t2@1e-3: 402 ev, 5.6e-5 |
| 0.2 | PASS — t2@1e-3: 556 ev, 1.5e-4 | PASS — t2@1e-3: 313 ev, 4.6e-5 |
| 0.1 | KNIFE-EDGE — t2@1e-3 passes seed 2 only (614 ev, 9.0e-4; seed 1: 649 ev, 2.1e-3); t1@1e-6 saturated: 1822–1857 ev | KNIFE-EDGE — t1@1e-3/m4 passes seed 2 only (408 ev, 5.2e-4; seed 1: 376 ev, 1.07e-3); t1@1e-6 saturated: 4378–4542 ev |
| 0.05 | **KILL** — 1e-6: 1922–1924 ev (sat); 1e-3: 1604 ev/5.7e-2 and 1754 ev/1.7e-2 (cost ∧ nav); hz=22 (plunge) | **KILL** — 1e-6: 4566–4580 ev (sat); 1e-3: 2992 ev/4.8e-2, 3601 ev/1.7e-2 |
| 0.02 | **KILL** — 1e-6: 1877–1878 ev (sat); 1e-3: nav 8.2e-3/1.6e-3 | **KILL** — 1e-6: 4597–4604 ev (sat); 1e-3: nav 4.7e-3/2.1e-3 |
| 0.01 | **KILL** — 1e-6: 1876 ev, 31.95 anchors/orbit (sat; Hmax 1.1e11) | **KILL** — 1e-6: 4601–4606 ev, 32.0/orbit (sat; Hmax 1.6e11) |

Controls held everywhere: exact-per-orbit ≤ 9.2e-10 rad; stale jet ≥ 6.4e-3 rad (49–370 rad
at s ≤ 0.05). Convergence: h=5e-4 vs 1e-3 at the hottest rung — 31.17 vs 31.73 anchors/orbit,
maxerr identical (1.47e-4). Hessian FD step fd ∈ {1e-4, 1e-3}: H stable to 11–28% — no
verdict except the s=0.1 knife-edge sits within that slack, and it is reported as such.

**The two horns, measured** (s ≤ 0.05, both e, both floors fail):
- *Tight floor* 1e-6: anchors/orbit saturates at 30.4–32.8 (recompile every kick) → 1822–4606
  crossing-evals/orbit = 2.6–6.6× the 700 control. Navigation *looks* fine (≤ 1.5e-4) only
  because consumption samples post-trigger states: a single kick landing on a fresh anchor
  costs ½|F″|σ² — 6.1e-3 rad at s=0.05, ~3.4 rad at s=0.01 (envelope from the logged
  Hbase: ½·7.4e7·(1.28e-5)² and ½·4.2e10·(1.28e-5)²) — which the per-kick trigger
  cannot prevent (it fires after landing). law.md:33's mid-interval readers (the view,
  encounters, judges) sample exactly there. maxcons (post-trigger instantaneous error)
  exceeded its own floor by up to 124× at s=0.05 (`conv_h5e4.log`: 1.24e-4 vs floor 1e-6).
- *Loose floor* 1e-3: the walk crosses 1e-3 rad — 1.6e-3 to 5.7e-2 at s ≤ 0.05 (2–57×
  tolerance) — while still paying 1237–3601 ev/orbit at s ≤ 0.1.

**Clean curvature ladder** (replaces the author's contaminated column; checker's four probes
regenerate bit-for-bit in `regenerate_gaps.log`): |F_CC| ≈ 2.5e3 (s=0.65) → 6e3/4.9e4/2.5e5/
4.1e6/7.4e7/2.7e9/4.2e10 (s = 0.5→0.01, e=0.9; e=0.5 within 2× at every rung) — ~18× per
halving of s, flat-ish in e. This is the driver: anchor rate ≈ H·σ²/2floor per kick until it
saturates at 1/kick.

**ε-scaling** (the kill skin's true width): at ε=1e-5, floor=1e-6: s=0.2 passes (60–73 ev,
≤ 6.6e-6); s=0.1 fails cost (784–792 ev, 12% over); s=0.05 fails (3444 ev). 100× smaller
kicks move the skin by **less than one rung** — because H grows ~18× per rung, the boundary
s*(ε) shrinks only logarithmically. The author's hedge ("if real tidal kicks are ≪ 1e-4 the
kill shrinks") is true but weak: the skin barely closes.

**Systematic drift** (sign=1, ε=1e-4): the orbit dies into the separatrix in 8 orbits (s=0.05)
/ 33 (s=0.1) at full recompile-per-kick cost, with Hmax/Hbase = 9.3× / 115× along the walk —
the hot skin is also a death zone, and the anchor's curvature under-triggers as it climbs
(though death arrives before the phase error can walk).

**Cost of the cold bulk, on the design's own number:** at the workable cold config
(t2@1e-3): 0.019 compiles/kick (s=0.5, e=0.9) — law.md:35's "about 0.05 compiles per kick"
confirmed in order of magnitude **where the mechanism survives**. Caveat: its cold walk is
monotone-signed and linear (7.1e-5 over 300 orbits at s=0.5 → ~2.4e-4 at 1000; 1.2e-4 →
4e-4): the certificate must bound residence time at fixed elements or the floor must tighten
with horizon.

## Predictions

`predictions.md` was written before the ladder (frozen kill rule included). Scored: P1 ✓
(controls), P3 ✓ (honest 2D trigger never beats the control: 1679–4580 ev/orbit at floor
1e-6 everywhere), P4 ✓ (two-horned kill at s ≤ 0.05; s=0.1 inside the predicted knife-edge),
P8 ✓ (maxcons up to 106× floor), P9 ✓ (seed spread 2–2.3×; s=0.1 flips on seed). Misses,
reported as misses: **P2 half-wrong** — the literal 1D trigger at floor 1e-6 is above parity
already at s=0.3, e=0.9 (2134 ev); the cold pass comes from floor 1e-3 + the 2D trigger, a
config P2 did not name. **P5 wrong at s ≥ 0.2** — floor 1e-3 holds navigation cold (the
per-orbit error is ~floor²/(Hσ²), not ~floor); it dies only in the skin. **P6 wrong at
s=0.05** — ε=1e-5 still costs 3444 ev/orbit there (the ε² scaling is real but starts from an
uncapped rate ~100× saturation). **P7 wrong in form** — systematic drift kills the orbit in
8–33 orbits; there is no long walk to compare.

## What would make it wrong

The float model idealizes kicks as periapsis element jumps (the law's own bookkeeping, same
as the author); real distributed tidal kicks mid-orbit add first-order phase terms (r4's
lesson) — likely worse for the jet, not better. The Hessian comes from float FD (stable to
~28%); the integer law's differentiated quadrature could differ similarly — only the s=0.1
knife-edge sits inside that slack. Consumption is once per orbit at periapsis: any reader
between kicks sees the ½|F″|σ² landing error, so my navigation numbers are optimistic in
the skin. Horizons are 60–300 orbits, not game residence. If H_live's real kick trains near
a secondary are ≪ 1e-5 relative, the skin thins to s ≲ 0.03–0.05 — still exactly where
slingshots and assists (B13) operate.

## Cost of adopting, and fit with PRINCIPLES

Adoption is one policy line plus one gate, both already half-written: (1) route on the
dimensionless number (p−6−2e)/p ≲ 0.1 to the dense order that law.md already keeps as the
fallback (principle 4: "regimes are chosen by dimensionless numbers"; principle 33: the lion
does not resolve the raindrop — but he does when it is a slingshot); (2) freeze r-kick-absorb
with the seed sweep mandatory (a one-seed gate flips at s=0.1 — the author's bucket-phase
finding generalized to batch-phase and reader-phase). Principle 13 ("we don't want errors
that can compound"): the jet's within-anchor bias is compounding and signed; principle 9:
the configuration (uniform jet policy) dies, not the method — the mechanism survives cold
with the measured operating point (floor 1e-3, 2D trigger, residence-bounded horizon).

## The lens

The second-author lens trusts the checker's framing, and the framing bakes in two choices:
kicks as element jumps, and the frozen 1e-3-rad/700-eval thresholds. Both favour the design
(loose nav, generous cost). What it may have missed: the *time* side — Δt and Δτ per cycle
(law.md:14) share F's curvature structure, so clocks in the skin drift the same way, and I
did not measure them; and the possibility that the dense order itself cannot hold 1e-3 rad
at 700 steps/orbit near the separatrix (probe 2 measured cold orbits only) — if so, the
skin is a representation gap, not a routing decision, and the right fix is a third
representation (the rotating binary doll's sibling at the separatrix), which is a bigger
claim than this run's evidence supports.
