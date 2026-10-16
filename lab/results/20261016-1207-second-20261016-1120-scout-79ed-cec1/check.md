Grade: silver

**Abstract.** Claim: r1v2 executed on the full frozen case set; the refit band-constant
rule wins every differing channel; but capture fails both arms at every m (photon
b̂→√54, matter L̂≈4.23), so adoption waits on a law fix for hyperbolic-band turning.
Reproduction is exact; the rule verdict, the m64 strong-row pass, the 1e-12 repeat bar
(worst 1e-14) and the four harness fixes all reproduce and hold on my adversarial cases
(dense circle grid 351/351 vs 163/351; capture 3/10 also at m64). **But the capture
finding is an instrument bug, not the law's:** the hyperbolic-turn branch records
u_new = up+2√(A·B), wrong when A,B<0 (true turn up−2√(A·B)); orbits teleport past the
horizon. With the one-line fix: capture 0/10 at m∈{8,16,32,64} both arms, b̂→5.1960=3√3,
L̂→3.9995, RK45 turns at u=0.2245 vs GR 0.2247 — H0205's capture-pass vindicated.
Remaining certificate blockers: strong rows (m16 4/6, m32 5/6) and m8's period tail.

## Reasons

**Reproduction.** regen.sh (runner, clean tree, empty patch) matches dossier and
report.json line for line; the three sha256 hashes in the dossier match the files;
mtimes order freeze (12:18:26) → predictions (12:18:51) → run (12:47) → dossier. The
letter-pinned draw, criteria and verdict logic are faithful to the freeze; the negative
control (m8-centre fails prec) and the discrimination clause (centre fails nearcirc at
every m, refit 1.00) both fire as designed.

**Predictions.** Pre-registered, 6/8 held as reported. The two refuted ones were
reported honestly — but P3's refutation was misdiagnosed: the prediction ("0
misclassified; the model's barrier error is ~1e-3 relative at m=16") was in fact
**correct**. The author's own instrument told them otherwise.

**The attack that inverted the headline.** RK45 on the piecewise band ODE (independent
of the walker) turns a b=6 photon at u=0.2245 (GR: 0.2247) and an L=4.12 E=1 particle
at u=0.1901 — the walker absorbs both. Instrumenting the walk: the turn event in a
hyperbolic band fires at the **correct φ** but records u_new = up+2√(A·B), which holds
only for A,B>0 (outgoing dip). For the infalling turn A,B<0 and the true turn is
up−2√(A·B): photon b=6, m16, band k=34 — recorded u_new = 0.648, true 0.2245; the orbit
is teleported above the band and walks to capture. The author's "mechanism"
(up(c)=3c²/(6c−1)>c ⟹ the turn lands above the band) conflates the two sides of up; the
turn is below up and is routinely inside the band. With u_new = up+2·sgn(A)·√(A·B) (one
line, applied to a copy):

- capture **0/10 misclassified** at m ∈ {8,16,32,64}, both arms (was 3/10 at every m);
- photon b̂ = 5.1929 → 5.1954 → 5.1960 → 5.1960 (m8→m64) against 3√3 = 5.1962; matter
  L̂ = 3.9985 → 3.9995 → 3.9995 → 3.9995 against 4 — clean second order, 4× per m
  doubling, same law as every other channel;
- b=6 escapes with deflection rel error 4.9e-4 (m16).

The buggy barriers were the bug's signature: √54 and √18 = 4.2426 are exactly where the
GR turn point crosses u=1/6 into hyperbolic bands — i.e. the boundary between turning
in rotation bands (handled correctly) and turning in hyperbolic bands (teleported). The
m→∞ √54 claim also rested on non-monotone evidence: on the buggy walker my m64 bisection
gives 6.96 with an escape window at b≈7.1–7.25 **inside** the absorbed region (centre
and refit even disagree at b=7.2).

**Contamination sweep (what survives).** No sampler seed's walk, at m16 or m32, either
arm, ever selects a hyperbolic-band turn; circles (u<1/6), light (b≥10), ISCO r=7,
long runs (sampler seeds) are likewise untouched — sampler, nearcirc, defl, shape,
repeat, crossings, isco stand as recorded. Centre-arm strong rows are bit-identical
under the fix (the turn segment's dφ and time are exact; only the next cycle and the
refit's visited-extremes inherit the bad u_end): the strongf failures at m16 (4/6) and
m32 (5/6) are genuine. The refit arm's three hyp-turn rows shift slightly and improve;
verdicts unchanged. The verified extra evidence: m64 passes both failing rows
((8.5,0.9): 6.1e-5/2.2e-4; (6.5,0.1): 5.5e-4/3.2e-4); on my denser circle grid
(±0.999 offsets) refit is 351/351 at ≤2.9e-14 while centre's worst grows to 3.8e-1
(163/351) — the author's grid understates the centre failure, in the run's favour.

**Novelty.** The executed named-rule freeze, the deterministic circles, the strong-row
bars, the 1e-12 repeat bar (first execution anywhere) and the E=1 first-integral fix
(2u/L², verified against the energy equation) are new against the wiki page, fe85 and
79ed. The capture finding is not novel — it is wrong, and H0205 (DISPUTED, 29
September) had capture passing; the corrected reading agrees with H0205.

**Goal fit.** Bottleneck 0 (the representation). The rule verdict (one-law refit wins
every differing channel, no regime branch) is exactly PRINCIPLES 4 and 19 ("a fix
signals the wrong representation" — here the fix was needed in the instrument, not the
law). The run itself quotes H0183's lesson ("a failed expectation is not automatically
a failed method: diagnose which one broke") and then violates it on P3: it diagnosed
four bugs in 79ed's harness (F1–F4, all real — my fixed runs match their frozen-arm
numbers) but stopped at the fifth and attributed the broken channel to the law.

## The one experiment that would make it gold

Apply the one-line hyperbolic-turn fix and re-execute the freeze on the record. My
check already ran its decisive parts (capture rows, barriers, strong rows,
contamination sweep); the corrected run should show capture passing at every m and the
certificate failing only on {strongf m16/m32, m8 period} — which completes the refit
adoption decision without any law change.

## What the author missed

1. The F5 bug itself; their RK45 calibration ran only at u=0.15 (a rotation band, below
   1/6) and never through a hyperbolic-band turn — the one event that decides capture.
2. The √54 limit was argued from two bisection points that are not even monotone in m
   (m64 dips to 6.96 with a non-monotone absorption region on the buggy walker).
3. H0205's record (capture passing at m16/m32) contradicted the new instrument's
   channel and should have triggered a differential test against that channel, not a
   new law claim.
4. Minor: the circle grid understates the centre arm's worst error (their claim of
   grid-insensitivity); the m32 long-run seed cut (16) was disclosed and
   pre-registered, and m16's full 32 seeds show the same 1e-14 drift, so nothing hangs
   on it.
