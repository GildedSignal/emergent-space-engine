# Dossier — the fleet doll's interior tide law at the game's own speeds

**Claim.** The fleet doll's interior law — "members feel only the tide x″ = −E(τ)·x with
the Newtonian tensor" (representation.md L23, law.md L50, `crates/engine/src/frame.rs`
L14–19, phase 2 unwritten) — is wrong at the game's own speeds by a measured,
closed-form factor on the radial channel: at a transverse closest approach the true
Fermi-frame tide is **γ²(2+β²)/2 × the Newtonian one radially and exactly 1×
along-motion** (the four-minus-ones cancellation; the null limit is a transverse
plane-wave pulse), so the letter understates the radial tide ×1.100 at the shipped
weak-field cap (β = c/4), ×1.50 at β 0.5, ×7.4 at β 0.9, ×74 at β 0.99, ×750 at
β 0.999 — while the engine's legality rule (`ORBIT_SPEED_DIV = 4`: origin speed ≤ c/4)
makes every faster frame illegal, i.e. B15's own 0.9c fleet stream has no legal fleet
doll, and at the legal cap the letter already errs 30% (radial member) / 115%
(along-track member) per orbit where its own budget line says O(β²) = 6.25%.

## Bottleneck

The dense order's interior law (battles, fleets — the dense half of the engine) sits on
one premise: the parent's tide inside the free-fall frame is the Newtonian tensor. The
measured gain of adopting the corrected law: the tide stays a linear O(1)-coefficient
kick (the same integer-kick structure as `frame.rs`; the coefficients change), and it
deletes the speed ceiling's physics cost — the weak-field rule can then be about
compactness (M/r), not speed. What it deletes: the phase-2 "relativistic tide" as an
open question — the answer is a closed form.

## Evidence (all numbers regenerate: `bash regen.sh`, ~8 s, float64, results.json)

Truth: exact Schwarzschild geodesics (central + member born rigid at ξ = 10⁻³ r₀,
parallel-transported Fermi axes, DOP853 rtol 1e-12, normalization conserved ≤ 6e-8,
linear in ξ: error 0.0907 at ξ/10 vs 0.0901). Instantaneous truth cross-checked two
ways: Riemann contraction R_{acb d}u^c u^d (full, with the t-row and the E_tθ cross
term — load-bearing) and Richardson finite differences of the member geodesics.

**Coefficient (the law's own constant), FD-measured on the truth** (radial channel,
transverse launch; `ratio_radial`/closed in results.json):

| β | measured | closed γ²(2+β²)/2 |
|---|---|---|
| 0.25 (the shipped cap, r = 18 M circular) | 1.0988 | 1.1000 |
| 0.50 (r = 100 M flyby) | 1.5052 | 1.4963 |
| 0.90 (r = 100 M flyby) | ≥ 6.33 (matrix norm; scalar probe reads 8.3, probe-biased) | 7.348 |
| 0.90 (r = 20 M, strong field) | 6.48 (norm) | 7.350 |
| radial infall 0.50 (α = 0, held-out) | **0.9995** | 1.000 (cancellation) |

Along-motion at any β (transverse launch): exactly 1× (derived exactly two ways —
wedge algebra and components-with-cross-terms; the naive γ² is wrong). Out-of-plane
(not the game's 2D): γ²(1+2β²).

**Member separation over the window (exit error of the law vs truth):**

| scene | letter (Newtonian) | cure (contracted E(u)) |
|---|---|---|
| control circle r = 1000 M (β 0.032) | 0.45% / 1.36% ([r]/[th]) | 0.05% / 0.95% |
| cap circle r = 18 M (β = c/4, legal) | **29.8% / 114.9%** | 0.23% / 1.14% |
| flyby r = 100 M β 0.5 | 4.3% / 0.7% | 0.6% / 0.5% |
| flyby r = 100 M β 0.9 | **9.0%** / 1.2% | 2.1% / 5.5% |
| flyby r = 100 M β 0.99 / 0.999 | 24.8% / 79.9% ([r]) | 15.6% / 141% (degrades; see below) |
| strong field r = 20 M β 0.9 | 34.5% / 7.2% | 5.3% / 28.8% |
| radial infall β 0.5 (α = 0) | 0.002% / 0.09% | same (both exact — the cancellation) |

Formation stretch at exit (the player-visible channel): at β 0.9, r = 100 M, a radial
member's offset grows ×1.105 (truth) vs ×1.005 (letter): the letter recovers 5% of the
true growth. Matrix instrument: the truth's tide matrix vs the letter's: relerr 0.0007
(control), 0.088 (cap), 0.43 (β 0.5), 5.6 (β 0.9); vs the cure: 0.0018 / 0.0018 /
0.036 / 0.20.

**The legality collision (shipped code):** `frame.rs` `ORBIT_SPEED_DIV = 4` refuses any
frame whose origin exceeds c/4 about the parent; `law.md` B15 flies "Zipf fleets … the
0.9c stream included … each fleet a free-fall doll" around a central mass; the plane's
own red-line burn is γ ≈ 120 (radial tide there: γ²(2+β²)/2 ≈ 2.2×10⁴). Those scenes
are outside the legal domain of the shipped doll by construction; inside the domain, at
the cap, the per-orbit error is already 30%/115%.

**Instrument defects disclosed:** the scalar FD probe at β ≥ 0.99 is polluted by
offset-axis rotation (reads 325 at β 0.99 vs closed 74 — quoted as bounds only); the
matrix probe's A is ill-conditioned there (cure relerr reads 1.08); the cure's
integrated error degrades at β ≥ 0.99 ([th] 95× at 0.999) — second-order-in-ξ and
probe effects are not separated there, so the cure is licensed to β 0.9 on this
instrument, not beyond. The kill does not rest on those rows: the cap and β ≤ 0.9 rows
are clean, control-anchored, and match the closed form.

## Predictions (predictions.md, written before the decisive run)

3/7 held (P2 exact: 1.0988 vs 1.1000; P6 conservation/linearity; P1 half: [r] 0.45%
< 1%, [th] 1.4% marginal). Four misses, each sharpening the law: **P3/P7 refuted by my
own held-out arms — the amplification is transverse-only** (along-motion and
radial-infall channels are exactly Newtonian at any speed: 0.9995); P4's magnitude was
wrong (the r = 100 M window integrates to 4–25%, not ×2–10 — the compounder is the
per-orbit cap scene, 30%/115%); P5 holds only to β 0.9 (above, the instrument and the
cure degrade together). The biggest discovery came from a failed prediction.

## What would make it wrong

A bug in the geodesic/Fermi instrument (controls: β→0 agreement 0.05–0.95%, mass-shell
conservation ≤ 6e-8, linearity at ξ/10, FD-vs-contraction agreement 0.18% at the
control and cap). The closed form is exact algebra cross-checked against E9's frozen
circular eigenvalue: their w(3γ²−1) with γ² = (1−2M/r)/(1−3M/r) equals my
(2r−3M)/(2(r−3M)) identically. A checker should fly β 0.99 with a fatter offset
instrument (shorter FD window) and the out-of-plane channel.

## Cost of adopting, and fit with PRINCIPLES

The cure is the same kick with corrected coefficients — closed form, O(1) per epoch,
no new mechanism, no new state; it licenses removing the speed term from the
weak-field rule (leaving the compactness term). Principle 2 ("It's a game… error type
over error size"): this is an error of type — the wrong law, not coarse arithmetic.
Principle 7 ("Spacetime, not space plus time… gravity compiled into geometry"): the
contracted E(u) *is* the Fermi geometry law.md L50 already promises ("Fermi normal
coordinates along an exact tube") — the letter says Fermi and ships Newton. Principle
33 ("each scale resolves only what matters"): the cancellation says the along-motion
channel never needed fixing — the cheapest exact law keeps half the Newtonian
coefficients untouched.

## The rung that should have caught it — and the freeze-ready criterion

E9 already freezes the circular GR tide (its planted-defect row *requires* Newtonian
2w to fail at r_p/M = 100 and 10) — but E9's tubes reach only circular/e ≤ 0.6
periapsis speeds (≤ ~0.5c), it currently FAILs 10/21 for phase-1 units reasons, and no
case isolates a player-speed origin. B15 flies the 0.9c stream but judges **cost**
only. r5's frozen scenes are exchanging-contact arms, no tide-vs-GR check. Nothing
judges the doll interior at player speed. Freeze-ready arm (fits E9 as a hyperbolic
row): origin on a transverse-periapsis flyby at r_p = 100 M, β ∈ {0.5, 0.9}; members
at 10⁻³ r_p both axes; PASS iff the radial tide eigenvalue is within 1% of
γ²(2+β²)/2·2GM/r_p³ and exit separation within 5% of the geodesic truth; the
Newtonian tensor is the negative (fails by ×1.5/×7.4 and the 4%/9% exit rows); the
along-motion channel equal to Newtonian within 1% is the cancellation control.

## The lens

The red-team lens overweights the exotic: I almost reported the γ 120 row (×2.2×10⁴) as
the headline; the player-visible kill is the cap (30%/115% per orbit at the legal
boundary, where the letter's own budget line claims 6.25%) and β 0.5–0.9 flybys. The
lens also nearly missed that half the law was already right (the transverse-only
structure) — a premise that survives is worth reporting.
