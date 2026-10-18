# Dossier — 20261018-1237-dynamics-9dbb (dynamics lens): the seam map's walk is a translation family, not a saturating diffusion

## Claim

The order-boundary crossing's "bounded, not compounding" record is re-derived: the
measured saturation is the position sample's **geometric** bound (its radius is an
exact invariant below the 2⁻²⁰ instrument floor, so the sampled point can never
leave the diameter), while the store's real columns **compound linearly**: the shape
column k walks as an **exact lattice translation** (e.g. k ↦ k − 13 Q48 ulps per
crossing, all 8192 crossings, w frozen) on every eccentric arm measured, and as a
one-signed, decelerating ratchet (−10.4×10³ → −2.7×10³ ulps/crossing, 99–100%
one-signed) on exact circles; a column-exact fixed-point corner exists
(p = 16·2³⁰, e = 0.99: absorbed at crossings 1–19, k and w constant forever), and
the map's perturbation response is **neutral, not chaotic** (a 1-ulp w₀ twin keeps
k bit-identical for 8192 crossings and the w gap stays 1 ulp). The leak is real,
one-signed and linear — but priced harmless: 1% of k's range needs 2.2×10¹¹
crossings (eccentric arms) or ~7×10⁸ (circles), and the radius stays sub-2⁻²⁰
through ~10⁶ (circles) to ~4×10⁹ (eccentric) crossings.

## Bottleneck

Not a board top-5 bottleneck; it is order-boundary open direction 1/2's missing
mechanism: the page freezes "bounded, not compounding — but never recovering" on a
quantity (the position sample) whose boundedness is geometric, and prices its fix
(anchor w+t as one observed-angle column, or carry the 4×65-bit residual) without
knowing the leak's class. This run names the leak (linear translation/ratchet,
ulp-scale), the ω-limit structure (no cycles on walkers to depth 8192; one
absorbing corner), and the stability of the response (neutral, not chaotic) — the
inputs the fix's cost/benefit needs, and the fact that "do nothing" is safe at any
horizon a body will ever fly.

## Evidence (all from `regen.sh`, ~30 s once built)

Probe: `crates/universe/examples/seam_walk.rs` (b9c8's cycle verbatim — shipped pub
APIs only: `Orbit::compile`, `state`, `cartesian`, shipped `in_tube_units` mirror,
`Rebinding::from_state`, residual dropped), with per-crossing series (k, p, w, cw,
radius, dropped residual) at depth 1024 (48-chain grid: p ∈ {8 M, 2²¹ M, 16·2³⁰ M} ×
e ∈ {0, 10⁻³, 0.5, 0.99} × φ ∈ {3/8, 5/8} × doll {unity, μ≈1.28}), 4 deep arms at
4096, a w₀ twin pair (w₀ = 1/8 turn vs +1 ulp) at 8192, and 3 retrograde (cw=true)
arms — a class the record never ran.

- **Class census** (`analysis.txt`): 29 translations, 19 ratchets, 3 mixed of 51
  grid+retro chains; every walker ≥ 98% one-signed in k.
- **Exact translations**: e = 0.5 at p = 2²¹ M: dk = −13 on every crossing, windows
  [16,512) vs [2048,4096) both −13 (0.0% change); e = 0.5/0.99 at 8 M and e = 0.001
  at 2²¹ M: −1 exactly; w frozen at φ = 3/8 (dw = 0 over 4096 crossings), while at
  φ = 5/8 the same arms keep k at exactly −13 while w jumps > 1/256 turn on ~every
  crossing (1023/1023) — **the k ratchet is independent of the w lottery**.
- **Circles (e = 0)**: −5.2×10³ to −7.6×10³ ulps/crossing at depth 1024 (100%
  one-signed), decelerating to −2.7×10³ by [2048,4096) (74% fall — the one honest
  P1 miss); w distinct at all 4096 crossings, |Δw| max 0.998 turns.
- **ω-limit**: no depth-64 walker closes a full-column (k,p,w,cw) cycle by 8192;
  4/48 grid chains absorb as column-exact fixed points (p = 16·2³⁰, e = 0.99, at
  crossings 1, 4, 16, 19 — k **and** w constant thereafter); the retrograde e = 0.1
  arm closes a *key* cycle at 45 but never a column cycle (w keeps re-lottering —
  b9c8's 51/76 class, persisting ≥ 1024).
- **Twins (8192)**: k identical; w differs by exactly 1 ulp at every crossing (max
  gap 1); p's significand max gap 505 (~5×10⁻¹⁷ relative), radius max gap 181 quanta
  (~8×10⁻¹⁷) — a perturbation neither grows nor dies: **neutral**, no shadowing
  question at the seam.
- **Radius law** (this probe's finer instrument; b9c8's reads 0 below 2⁻²⁰):
  eccentric arms spiral **linearly** (2.1×10⁻¹⁰ → 8.6×10⁻¹⁰ → 1.7×10⁻⁹ relative at
  depths 1024/4096/8192), circles diffuse ~√n (2.6×10⁻⁸ → 5.2×10⁻⁸); max 5.2×10⁻⁸,
  i.e. 18× below b9c8's floor, everywhere.
- **Control**: b9c8's own `seam_cycle` probe, unmodified, on this tree reproduces
  its stored record exactly — 864 chains, 0 nonzero dr_rel, 92/864 key-cyclic
  (`b9c8-control.json`) — so the shipped fit/decode code is unchanged since
  14 October and the record regenerates; this run's nonzero dr numbers are
  sub-floor, not a code change. Crossing cost 20.5 µs (the record's 20.4).

## Predictions

`predictions.md` was written after smoke (depth ≤ 256), before the decisive run.
Outcome: **P1 holds for every eccentric class (translations exact, rate change
0.0%) and fails only its ±10% clause on circles (deceleration 74%, sign still 99%)**
— the miss is reported above. **P2, P3, P5 hold** (no ω-limit on walkers; radius
sub-floor everywhere; retro arms run with zero refusals — the page's 1–2% entry-
refusal class did not appear — and join the same classes, one at the identical
−13 rate as its prograde twin). **P4 half-holds**: the twins' k is bit-identical
(neutrality confirmed) but w carries the 1-ulp offset forever rather than rounding
it away — reported as the neutral mode, not contraction. **P6 refuted**: the
dropped residual's magnitude does not predict the rate (e = 10⁻³ arms: residual
1.2×10⁷ vs 7.0×10⁸ quanta at the same rate −1; e = 0.5: 1.1×10⁶ residual at −13
while e = 10⁻³'s 7×10⁸ walks −1) — the ratchet rate is a per-(p, e, φ) constant of
the fit's quantization geometry, not a function of the defect's size.

## What would make it wrong

The cycle is idealized (b9c8's domain, inherited): one observation phase per chain
re-derived from each key's own period, no belt-Spec column re-quantization (so the
rates are lower bounds), no contacts, no kicks between crossings, one initial
(w₀ = 1/8 turn, prograde) for the grid (twins and retro arms vary one factor each).
A law change that re-derives `full`/k from orbit constants, or a wired
`resolve_handoff` with doll-unit conversions in flight, could change the rates; the
class structure (translation/ratchet/fixed/neutral) is a property of
`from_state ∘ cartesian`, which the control shows is unchanged since b9c8. The
circle deceleration's cause is unmeasured (k walking away from the near-circular
regime changes the fit bias; one rung of k-vs-rate would close it).

## Cost of adopting / fit with PRINCIPLES

Nothing to adopt in the engine: this prices the **do-nothing** option for demote-
at-commit (the page's open direction 1) at ulp-scale linear leak, neutral response,
no cycles — safe for any body's lifetime (a belt body crossing the seam even 10⁶
times moves k by ≤ 2.7×10⁻⁵ of range; the orientation column is either frozen or
destroyed in one crossing, which the w-anchor fix addresses for free). Principle 13
("errors never compound") is violated **in the letter** at the seam (one-signed,
linear) and satisfied **in effect** at game horizons — the same shape as the
contact-carry finding. Principle 2's "error type over error size": the error type
here is a lattice translation, the friendliest compounding there is.

## The lens

The dynamics lens looked for the attractor and found its absence is the result: a
translation has no ω-limit, and the record's "saturation" was geometry, not
dynamics. What the lens may have missed: the observation-phase structure (one φ per
chain) hides any phase-averaged drift cancellation; and the residual-vs-rate
mechanism (P6) was assumed, not derived — the refutation says the projection of the
decode defect onto k, not its size, sets the rate, but I did not derive that
projection.
