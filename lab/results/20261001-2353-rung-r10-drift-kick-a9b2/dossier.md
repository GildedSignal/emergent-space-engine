# Rung r10 — the compiled drift plus kicks, with a smooth changeover

**Claim.** The smooth-changeover drift+kicks (SyMBA-style, `symba`) does **not** keep the Jacobi
constant bounded: median growth exponent **+0.43** against the 0.2 limit, because every transit
of the changeover window leaves a |ΔC_J/C_J| jump of 1e-6–1e-5 that walks. The Hill-moon classes
(0.988) and apsidal rates (0.925) also miss 0.99. `wh-fixed` fails worse (exponent 1.8, rates 0).
`soi-switch` fails `jacobi` (+0.33) as the negative control must. Resonance libration and cost
pass for everything. **KILL of `symba` and `wh-fixed` as configurations; the rung is valid**
(negative fails, positive passes).

**Bottleneck.** The board's "changeover near a secondary, reversible and integer". This rung is
the cheapest falsifier of the plane's motion law, and it falsified: a C² window at 1.3 R_H with
recursive sub-steps is *not* reversible across the window — the per-transit error, not the deep
encounter, is the blocker (diagnosis below). What it lets us delete: the whole
"window-in-the-separation" family at fixed base step, before the plane commits to it.

**Evidence** (`metrics.json`, `report.txt`, `picture.svg`; cloud x86, orders of magnitude only):

| config | jacobi_exponent | class_match | precession_match | libration_ratio | evals/orbit |
|---|---|---|---|---|---|
| symba | **+0.428** | 0.9882 (252/255) | 0.9245 (49/53) | 0.998 | 102 |
| wh-fixed | **+1.80** | 0.9333 | **0.000** (0/53) | 0.999 | 15 |
| truth | 0 (convention) | 1.0 | 1.0 | 1.0 | 0 (real: ~3,800/orbit) |
| soi-switch | **+0.328** | 0.9882 | 0.9623 | 0.999 | 15 |

- B12: the 16 frozen ships (SplitMix64 seed 20261002, `HANDOFF_KEPT`), 200 periods, 18–40 SOI
  crossings each; reference converged (1e-12 vs 1e-13) on 15/16. Every symba ship's |ΔC_J/C_J|
  sits at 2e-5–5e-5 (within B12's own 1e-4 err cap) but *walks*: ship 0 is flat at ~2e-6 for 190
  periods, then two late transits of the window add 8e-6 — exponent +0.96. wh-fixed's errors run
  to 70 (unit) — close passes destroy it. soi-switch's hard switch gives +0.33.
- B14: 256 moons (50 periods), truth: 155 bound, 100 escape, 1 unconverged, 0 chaotic, 53 with a
  stable apsidal rate (gate floor 32). symba misses 3 classes and 4 rates; wh-fixed misses 17
  classes and *all* rates (a star-centred drift cannot precess a moon's apse); soi-switch misses
  3 classes and 2 rates — its planet-centric interior is nearly as good as symba's at 1/7 the cost.
- B17 resonance (2:1, 3:2, μ = 3e-5…3e-3, three detunings, two phases; 27 librating, 7
  circulating, 1 borderline, 1 not converged): all three candidates hold the libration amplitude
  to 0.998–0.999 of the truth's — they are the *same map* there (the changeover never engages at
  23 body-widths from the planet), so this is a statement about drift+kick at 128 steps/orbit,
  not about the changeover.
- **Diagnosis** (`./r10 diag 1.3 0`): the Jacobi error jumps exactly at ZONE transitions — the
  changeover's outer edge at 1.3 R_H — not in the deep zone. First build kicked at the step
  centre when far and at the edges when inside (a h/2 phasing mismatch at every branch
  alternation, median exponent +0.55); after unifying the skeleton (windowed edge half-kicks
  everywhere) the exponent fell to +0.43. The residual is the window transit itself: the split
  switches content (star-drift vs planet-centric sub-steps) at fixed base step, and each transit
  leaves a systematic O(h²·∇φ) error. Two builds, same failure: this is the configuration, not
  the bug.

**Reproduce** (each ≤ 60 s where possible; the container has 2 vCPU):

```
cd lab/results/20261001-2353-rung-r10-drift-kick-a9b2
gcc -O2 -o r10 r10.c -lm
./r10 selftest                    # 1 s: Kepler round-trip ≤ 3.4e-11; far-field symba == wh-fixed
./r10 truth   &  ./r10 symba &    # ~4 min (the moon reference is 3×256 adaptive runs) / 11 s
./r10 wh      &  ./r10 soi &      # 9 s / 8 s
python3 metrics.py                # metrics.json + report.txt + picture.svg
```

**Predictions** (`predictions.md`, written before the run): held — soi-switch fails `jacobi`
(+0.33, just under the predicted [0.4, 1.0]), symba's class ≥ 0.97 (0.988), the three candidates
identical on resonance, cost in [110, 160] (102). **Failed and reported as held**: symba's
exponent ≤ 0.2 (measured +0.43 — this is the rung's answer, and the pre-registered diagnosis
"the transit injects a systematic sign per crossing" is what the data shows); wh-fixed's class
in [0.4, 0.7] (measured 0.933 — the moon classes are more robust to a wrong drift centre than
expected; its *rates* are not, 0/53); wh-fixed's exponent in [0.3, 0.8] (measured 1.8 —
superlinear tails up to +9.6).

**What would make it wrong.** The exponent floor: the judge's own reference drifts to
max |ΔC_J/C_J| ≈ 1.3e-9 over 200 periods (its err series fits noisy exponents up to +2.9 — this
is the `Drift` planted law of `laws.rs`; hence `truth`'s exponent is 0 by the same convention as
its cost, and its drift is reported here). At symba's 1e-6…1e-5 level the exponent is real, not
noise. Untested: other window shapes/radii, per-level windows tied to the sub-step hierarchy
(DLL98's letter — mine is one window at 1.3 R_H), and smaller base steps (h/2 should cut the
per-transit error 4×, which would pass the exponent but at 2× the cost). The method — drift
about the dominant body with kicks — is not killed (principle 9): the *window at fixed base
step* is.

**Cost of adopting:** nothing to adopt; the falsifying harness (frozen cases, ported samplers,
one-file reproduction) is the deliverable.

**Fit with PRINCIPLES.** "basically we don't want errors that can compound that's the goal"
(#13): the exponent is exactly that metric, and the changeover compounds. "A failed experiment
kills that configuration, never the method" (#9).

**The lens.** The builder's lens: an implementation subtlety of DLL98's exact per-level
changeover could still rescue the configuration — I tested one faithful-in-spirit window, one
radius, one base step, and the negative result is about that configuration, not the family.
Also missed by this lens: the reference's own drift (1e-9) sets the floor of what the exponent
can resolve; a conserving reference (`echo`) would sharpen the gate.
