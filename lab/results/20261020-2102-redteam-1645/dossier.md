# Run 20261020-2102-redteam-1645 — premise red-team: the view at a spinning hole

## Claim

The lopsided shadow is real, player-visible and **unguarded**: a χ-blind (or
|b|-keyed) gather misplaces both shadow edges by 2.7°–28.3° and displaces the
arc centre by up to 33° (retrograde side, worse as χ and depth grow; the
retrograde edge wraps past the tangential direction at r_o ≤ 3.2M), while the
shipped `kerr::deflection` itself matches the exact oracle to the printed
digits — law.md L32's "emerges, none imposed" is true of the geodesics and
seen by no gate.

## Bottleneck

Not a cost bottleneck: a **certificate gap** on the view at rotating holes
(board focus: "the only goal is the engine/compiler to work with GR natively";
Julien: "especially rotating black holes"). It names the wiki's open
direction ("Kerr dolls: B19's compiled Kerr against the same instrument") and
closes its first half. What it deletes: any symmetric-key deflection memo in
the gather, and B19's implicit claim to cover rotating holes (it covers
motion, not the view).

## Evidence

Exact instrument (`kerr_shadow.py`, this folder): Carter's first-order
equatorial Kerr null system, E=1, signed b; flyby bend by r = r_min + u²
Gauss–Legendre quadrature of dφ/dr = Q/√R; shadow edges from Bardeen's photon
circular orbits, validated by winding spirals. All commands ≤ 60 s.

**Controls (must pass, and did):**
- a=0: shadow arc 7.9% / 25.0% / 46.6% of the sky circle at r_o = 20/6/3.2M —
  039d's three published fractions reproduced exactly by the same formula.
- a=0: b_c = ±3√3 = ±5.196152M; near-critical rays spiral (13.42 rad at
  ε=1e-6), and the log-divergence coefficient A = 1.000 (its known exact
  value at Schwarzschild).
- Bend at b=100M = 0.040223 vs series 0.041178: the difference is exactly the
  quadrature's own truncation tail 2b/r_max (r_max = 2×10⁵), b·10⁻⁵ —
  disclosed, and it is what exposes the shipped law's exactness below.

**The lopsidedness (static observer; α from radially-outward, + = spin
sense; χ-blind = the χ=0 law, bit-for-bit per law.md L32):**

| χ | r_o | exact edges [α⁻, α⁺] | χ-blind edges | edge err pro/retro | centre | arc exact/χ-blind |
|---|---|---|---|---|---|---|
| 0.5 | 20M | [−0.295, +0.196] | ±0.249 | −3.1°/−2.7° | −2.9° | 7.8%/7.9% |
| 0.5 | 6M | [−0.989, +0.591] | ±0.785 | −11.1°/−11.7° | −11.4° | 25.1%/25.0% |
| 0.5 | 3.2M | [−π/2, +0.901] wraps | ±1.465 | — | −19.2° | 39.3%/46.6% |
| 0.9 | 20M | [−0.330, +0.135] | ±0.249 | −6.5°/−4.6° | −5.6° | 7.4%/7.9% |
| 0.9 | 6M | [−1.194, +0.398] | ±0.785 | −22.2°/−23.4° | −22.8° | 25.3%/25.0% |
| 0.9 | 3.2M | [−π/2, +0.576] wraps | ±1.465 | — | −28.5° | 34.2%/46.6% |
| 0.998 | 20M | [−0.338, +0.100] | ±0.249 | −8.5°/−5.1° | −6.8° | 7.0%/7.9% |
| 0.998 | 6M | [−1.260, +0.291] | ±0.785 | −28.3°/−27.2° | −27.8° | 24.7%/25.0% |
| 0.998 | 3.2M | [−π/2, +0.416] wraps | ±1.465 | — | −33.1° | 31.6%/46.6% |

The centre displacement is toward the **retrograde** side (the prograde edge
pulls in more than the retrograde edge extends: at χ=0.9, b_c goes
5.196→2.844 prograde but 5.196→6.832 retrograde, so the edge midpoint in b
moves −2.0M). Every near-hole star's bearing is wrong too, not just the
shadow: at |b|=10M, χ=0.9, the bend is 0.5045 prograde / 0.7204 retrograde /
0.5903 χ-blind — sky errors −4.9° and +7.4°, a 12.4° asymmetry.

**The shipped law survives (P5 held):** `kerr::deflection(χ, b)`
(`crates/space/src/kerr.rs:719`) takes a **signed** b, returns capture
exactly between Bardeen's b_c± (χ=0.5: pro escapes from b=4.5 (b_c+=4.096),
retro only from 6.5 (b_c−=−5.93); χ=0.9: retro only from 8.0 (−6.83);
χ=0.998: pro 3.0 escapes with 3.88 rad (b_c+=2.111)), and its bends equal the
float oracle to the printed 9 digits — the residual is *exactly* the oracle's
own 2b/r_max tail (|b|·10⁻⁵), i.e. agreement below 10⁻⁶ relative everywhere
sampled (shipped-defl.txt vs ORACLE lines in instrument-out.txt).

**The rim wall becomes sense-dependent:** winding-image gap δb/b = e^(−2π/A):
Schwarzschild A=1.000 → 1.86×10⁻³ (both sides); χ=0.9: prograde A=2.583 →
8.8×10⁻² (47× coarser, easier), retrograde A=0.784 → 3.3×10⁻⁴ (**5.6×
finer**). The deflection memo's b-key must carry the sense and resolve
~3×10⁻⁴ relative on the retrograde side (≈12 bits), with a per-side wrap
cutoff — 039d's cure clause ("the memo names its wrap cutoff with the
b-resolution it implies") must become two clauses.

## Ranked attacks (the lens deliverable)

1. **The view at a spinning hole — measured above.** Rung that should catch
   it: **none** (r6 = view cost/presence, Schwarzschild; B19's four items are
   motion/clock/fate, no view item; r13 = γ channel). Freeze r15-kerr-shadow
   (criterion below).
2. **The one-sided deflection(b) memo abstraction** (representation.md L57):
   dies as stated — deflection is a two-branch function of signed b at every
   spinning doll; the memo key needs (sense, b). No rung; same freeze.
3. **B19's coverage claim**: passing B19 does not license what the player
   sees at a rotating hole. Cheap fix: one gate item, not new physics.
4. Unmeasured here, named for the next run: the comoving observer at a Kerr
   rim (2fa4's instruments + this geometry); a=0.998 rim (checker's case);
   what the plane's view actually keys on today.

Premises that survive (worth reporting): the shipped tube-with-χ compiles
exact Kerr null paths (this run, on shipped code); the two-body doll and
dense≡sparse untouched.

## Predictions (predictions.md)

P1 held (fractions exact, b_c exact; the bend control's shortfall was the
instrument's own tail — disclosed above). **P2/P3 missed**: predicted centre
displacement +0.076/+0.24 rad toward prograde, measured −0.097/−0.398 toward
retrograde — my hand b_c− had a cos-evaluation slip (5.99 vs 6.83) and I
guessed the midpoint direction wrong; predicted arc 6.7%/22.6% at (0.9,
20/6M), measured 7.4%/25.3%. P4 half-held (sense-dependence real, but
prograde is *coarser*, not finer). P5 held fully. The instrument, not the
hand numbers, decided everything reported above.

## What would make it wrong

The static-frame edge map α = asin(b√(1−2M/r_o)/r_o) uses a static observer
at Boyer–Lindquist r_o; a moving/ZAMO observer changes the angles (2fa4's
instruments). Quadrature tail 2b/r_max biases bends by |b|·10⁻⁵ (disclosed;
it cancels in the shipped comparison). The wrap flag at r_o=3.2M marks
|b_c−|√(1−2/r_o)/r_o > 1 — the arc fraction there is exact given the wrap,
but the *χ-blind* comparison at the wrapped edge is conservative (its error
is at least the tabulated arc-fraction gap).

## Cost of adopting, and fit

One gate (r15, below) + one sense bit and a per-side wrap cutoff in the view
memo key. No new physics code: the geodesics already carry χ exactly.
Principles: "What must be perfect … navigation, knowledge and dynamics"
(#30); "a certificate needs independent, adversarial checks" (Truth); "his
direct influence is bounded and propagates at c" — the view is where the
player feels GR (#30: "I want the player to feel what a human would feel in
space").

**r15-kerr-shadow (freeze-ready):** χ ∈ {0.5, 0.9, 0.998}, static observer at
r_o ∈ {20, 6, 3.2}M: (1) both shadow edge angles within 1% of the exact
table above (positive: the shipped signed-b deflection gather; negative: a
χ-blind or |b|-keyed law, which must misplace edges by ≥ 2.7°); (2) the
retrograde wrap at r_o=3.2M classified exactly (arc fraction within 1 point);
(3) the memo key resolves the retrograde winding gap 3.3×10⁻⁴ (χ=0.9):
successive winding images of one emitter separate, or the key is named too
coarse. Controls: χ=0 must reproduce 7.9/25.0/46.6% (039d's numbers).

## The lens

The premise red-team lens measured the exotic-looking case it was named for
(wiki open direction 2); what it may have missed is the boring half — what
the plane's view path actually keys on today (read-only here; the gather was
not flown end-to-end), and the moving observer at the rim.
