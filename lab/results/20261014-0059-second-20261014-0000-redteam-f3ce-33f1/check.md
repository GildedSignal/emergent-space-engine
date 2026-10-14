Grade: gold

**Abstract.** Run as specified at the engine's Q = 2²⁰, the parent checker's named gold
experiment refutes the rung's own severity bar at the frozen scene: shipped **passes**
(|Σres|/KE abs-median 7.4×10⁻³ < 1%, worst seed 1.3×10⁻²; verdict VOID), and the
pair-scaled carry fails to flip it in three implemented forms (best 1.4×10⁻²; with the
flag on the candidate also breaks `low_speeds_reduce_to_the_newtonian_bounce`).
Reproduced bit-identically; flag-off bit-identical to the pristine lib; ledgers exact
everywhere. Checker adversarial: the pass is a (β, contrast) window — β 0.85 fails ×40,
β 0.3 passes ×100, 10⁴:1 fails ×280–1600 with γ pinned at 724; 1000 contacts diffuse
(8.6×10⁻³), and γ is now measured directly at engine Q (241–256). Adopt: gate the law's
certificate on mass contrast; re-freeze r5 at 10⁴:1 (separates by >2 orders). Cost:
local predicate.

## Reasons

**1. Reproduction (clean tree, base 33c83f1).** Applied `work/patch.diff` myself,
built, re-ran the decisive cells: all four config×scene cells and the held-out seeds
11–15 are **bit-identical** to the stored logs (shipped per-seed 7.355596e-3 /
−1.271729e-2 / 5.207066e-3 with seeds 1≡3, 2≡4; pair-carry median −1.418911e-2, seed 0
at −5.278862e-1; pairequal 1.430288e-6). `regen.sh` exit 0. Flag-off behaviour verified
bit-identical against the truly pristine lib (stash test). Determinism: double-run
md5 equal. One instrument note, no verdict impact: `metrics.json` takes the abs-per-
seed median (7.36e-3, per the frozen rung text "end |Σ residual| … median over 5
seeds") while the probe's own `METRIC` line prints the signed median (5.21e-3); both
pass. The probe's "worst" label is max(signed), not max |·| (pair-carry prints
"worst=−8.6e-4" while seed 0 sits at −5.3e-1) — the dossier reads per-seed lines
correctly, but the label invites misreading.

**2. Predictions.** `predictions.md` carries full pre-freeze instrument history
(sampler fix, no-op cone bug, fix redesigns) and was honoured as written: P1 failed on
exactly its pre-registered coin-flip branch — the disclosed risk paragraph ("if it
lands under 1% … the verdict is VOID … I report the measured number and the horizon")
is verbatim what happened, so the VOID is a finding, not a surprise; P3 failed (no fix
form clears) — the criterion doing its job on a dead candidate; P2/P4/P5/P6/P7/P9
held (P9's "I will report which test differs" was left unnamed — see missed); P8 was
honestly partial, and my completion supports it: at the frozen scene the momentum
carry grows alongside the energy (Σ|carry| ≈ 1.1×10¹³ ≈ 15% of KE at 1000 contacts),
same quantum; P10 held indirectly and now **directly**: my probe measures the light
body at γ 241–256 at β 0.6 engine Q, pinned at the |k| = Q ceiling (γ 724) in the
harder arms — the Fermi-saturation mechanism the author inferred from step scale is
measured, not inferred.

**3. Adversarial cases (mine; two outside the author's tested domain).**
- **A, 10⁴:1, β 0.6, engine Q** (the author's own named-but-unrun next probe):
  |Σres|/KE abs-median **2.77**, worst **16.2** — the negative fails the 1% bar by
  280–1600×; light body at γ 724 within ~1300 ticks. The severity premise is alive
  one contrast decade up, at the same Q.
- **B, β sweep at 1000:1, engine Q** (β 0.85 is outside even the parent's 0.3–0.7):
  β 0.85 → 0.40 median (fail ×40); β 0.3 → 9.0×10⁻⁵ (pass ×100). The engine-Q pass is
  a **window in (β, contrast)**, not a Q property.
- **C, 1000 contacts** (5× horizon): abs median 8.6×10⁻³, worst 4.3×10⁻² — √N-type
  diffusive growth, no blow-up; the saturation-not-compounding reading holds at this
  scene.
- All arms ledger-exact and subluminal at every step.
These attacks break the headline only if it is read unscoped; the dossier's own domain
statement scopes it, and every attack **confirms the run's disposition** (the
certificate gate on mass contrast; the bar re-frozen where it separates).

**4. Novelty.** The topic page held the parent's 2¹⁶ walk, the missing r5, and the
fix direction. This run supplies what the parent's checker specified as the gold
experiment, and its outcome *contradicts* that checker's severity expectation — a
genuine premise correction, not a repetition. Nothing in docs/HISTORY.md touches
contact energy (B12 judges orbit laws). The dead-fix root causes (score mixes
incommensurate energy/momentum units; on-shell radial shift pays dp/dE ≈ Qγ²/|k|) and
the LCG seed-sampler artifact are new, reusable findings.

**5. The page.** Faithful to the evidence; every number checks. Corrected in place:
scoped "the bar overstates engine-Q severity" to the frozen scene with my β/contrast
numbers; replaced "10⁴:1 untested" with the measured fail; named the flag-on failing
test; extended the domain line with the checker sweeps.

**6. Goal fit.** Deletes a component path (adopt-the-pair-carry is measured dead in
three forms with named causes — principle 19: the bandaids were the wrong
representation speaking), corrects a severity premise with the exact number (principle
10: simplest falsifying run), and hands the integrator a one-step action local to the
law's certificate predicate. Principle 13's "errors never compound" is shown saved at
engine Q only by Q-scaled margins inside a scene window — error *type* named
(saturating γ³ quantum that then diffuses), per principle 2.

**Why gold and not silver.** Reproduced bit-identically; the disjunctive gold test is
met (a premise is shown wrong at the frozen scene with exact numbers; a component path
is deleted; the adoption is one local step). Two predictions failed, but both were
pre-registered branches with their interpretations written in advance, and neither hid
a wrong mechanism — the mechanism prediction is directly confirmed at engine Q by the
checker. Unlike the 1-October silver, nothing was retrofitted and the instrument
history is disclosed to an unusual degree.

## What the author missed

- **The β axis.** A two-point sweep (0.3, 0.85) was one probe flag away and would have
  shown the pass is a window — the one place the dossier's framing ("refutes the
  severity premise") could be over-read. The author's lens section blames the missed
  Q-ladder arithmetic but not the missed β sweep.
- **The 10⁴:1 engine-Q arm** — named "the obvious next probe," ~4 s of compute, not
  run; it is the arm that makes the re-frozen rung separable by >2 orders.
- **Prediction 9 promised to name the differing flag-on test; it was never named.** It
  is `low_speeds_reduce_to_the_newtonian_bounce`: the candidate breaks the Newtonian
  low-speed reduction, a stronger kill than a digest diff (consistent with the
  unit-mismatch diagnosis).
- Minor: the two coexisting median definitions (probe METRIC line vs metrics.json) and
  the misleading "worst" label deserve a line in the rung-rule list alongside the
  sampler lesson; the 3-class seed multiset (disclosed) propagates into every derived
  median, including mine.
