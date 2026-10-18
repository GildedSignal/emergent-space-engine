topic: order-boundary
status: open
closed-by:
valid-while:
updated: 20261018-1237-dynamics-9dbb

# The order boundary: tube ↔ Cartesian member, "identical bits"

## Current best

**The walk's class is now named, and the record's "bounded" was geometry, not
dynamics: the position sample cannot leave the diameter (its radius is invariant
below the 2⁻²⁰ instrument floor — b9c8's dr_rel reads 0 for any smaller drift), so
its d₂₅₆/d₆₄ ≈ 1 saturation is a bound by construction, while the store's real
columns COMPOUND LINEARLY — the seam map is a translation family (20261018-1237-
dynamics-9dbb, dynamics lens, shipped pub APIs, b9c8's cycle verbatim with a
per-crossing series at depth 1024/4096/8192 + a w₀+1-ulp twin pair + the first
retrograde cw=true arms).** Census (51 chains): 29 exact translations, 19
one-signed ratchets, 3 mixed (68–88% one-signed — the "every walker ≥ 98%" in the
dossier was wrong, check.md); every translation/ratchet walker ≥ 98% one-signed. **Exact lattice
translations:** e = 0.5 at p = 2²¹ M walks k by exactly −13 Q48 ulps on every
crossing (windows [16,512) and [2048,4096) both −13, 0.0% change; w frozen over
4096 crossings at φ 3/8; at φ 5/8 the same −13 while w moves without repeating but
≤ 1.4×10⁻⁶ turns/crossing, and the arms whose w jumps > 1/256 on 1023/1023
crossings (p = 8 M, e = 0.5/0.99, φ 5/8, both dolls) walk k at median −1 there
(e = 0.5 μ doll exactly; the e = 0.99 arms are the mixed 83–88%) — **the k ratchet
is independent of the w lottery** in both directions; the dossier conflated the two
arm families, check.md); e = 0.5/0.99 at 8 M walk −1 exactly on the μ doll (e = 0.99
at φ 5/8 mixed instead) and −1/0 on the unity doll; e = 10⁻³ at 2²¹ M −1 exactly.
**Circles (e = 0):** −5.2k–7.6k ulps/crossing at depth 1024 (100% one-signed),
decelerating to −2.7k by [2048,4096) (74% fall; sign 99%).
**ω-limit:** no depth-64 walker closes a full-column
(k,p,w,cw) cycle by 8192; 4/48 grid chains absorb as column-exact FIXED POINTS
(p = 16·2³⁰, e = 0.99, crossings 1/4/16/19 — k and w both constant thereafter);
the retrograde e = 0.1 arm closes a key cycle at 45 but never a column cycle (w
re-lottering — b9c8's 51/76 class, persisting ≥ 1024); retro arms run with ZERO
entry refusals (the page's ~1–2% class did not appear in 3 arms) and one joins its
prograde twin's exact −13 rate. **Perturbation response is NEUTRAL, not chaotic:**
the twin keeps k bit-identical for 8192 crossings, the w gap stays 1 ulp, p's gap
5×10⁻¹⁷ relative — nothing grows, nothing dies; no shadowing question at the seam.
**Radius law (finer than the record's floor):** eccentric arms spiral linearly
(2.1×10⁻¹⁰ → 1.7×10⁻⁹ relative, depths 1024→8192), circles diffuse ~√n (2.6×10⁻⁸
→ 5.2×10⁻⁸; max 5.2×10⁻⁸ = 18× below the floor). **Pricing the do-nothing option:**
1% of k's range needs 2.2×10¹¹ crossings (eccentric) or ~7×10⁸ (circles); the
radius crosses 2⁻²⁰ after ~10⁶ (circles) to ~4×10⁹ (eccentric) crossings — the
compounding is real, one-signed, linear, and harmless at any horizon a body will
fly. **The leak's fuel is not the residual's size** (refuted below): the rate is a
per-(p,e,φ) constant of the fit's quantization geometry. Control: b9c8's own probe,
unmodified, reproduces its stored record bit-for-bit on this tree (864 chains, 0
nonzero dr_rel, 92/864 key-cyclic) — the shipped fit/decode code is unchanged since
14 October and the record regenerates. Principle 13 at the seam: violated in the
letter (linear, one-signed), satisfied in effect at game horizons — the same shape
as the contact-carry finding.

**Prior best (b9c8's corrected census, retained):** the crossing's walk measured at
column level on a corrected instrument — true phases, both dolls, depth 256 — and
it lives in the w column at every phase (20261014-1137-second-20261014-1010-taleb-
292a-b9c8). The graded run's two instrument flaws (an `8φ` phase slip: both φ arms
sampled periapsis; a 2⁴⁰ doll unit jump) fixed, 864 chains (6 periapsis scales
8 M–16·2³⁰ M × 6 e × **true phases {1/8, 3/8, 5/8, 7/8}** × words +0/+4/+8 ×
{unity, μ ≈ 1.28}) run to depth 256: **864/864 complete, zero refusals on the
odd-eighth grid** (even phases refuse mid-walk — Domain, check2.md). The walk: **e = 0
circles drift 1.71–2.00 radii at all four phases while the radius stays exactly
preserved** (< 2⁻²⁰ over 144 chains; the dynamics run above shows this holds for
every e class, sub-floor): a pure orientation lottery of an undeformed circle — the
damage is only the stored w column (it orients any future e). Per-crossing |Δw| max
**0.357 turns** (0.086–0.130 in every near-circle phase class; median 3.6×10⁻⁷).
**Inbound phases (1/8, 3/8) drift medians 7.5×10⁻¹²–4.5×10⁻⁸; outbound (5/8, 7/8)
5.7×10⁻⁴–7.6×10⁻⁴** (4–8 orders); record max **3.68 radii** (p = 8 M, e = 0.5,
outbound — identical at all three words; read as the position sample's geometric
bound by the run above). **Exact key-level fixed points are common but do not close
the seam:** 76/864 (census {1: 76, 2: 7, 3: 5, 4: 2, 8: 1, 14: 1}; 20 close late,
in (64, 256]); only 25 also fix w — **51 keep re-lottering w** (≤ 3.8×10⁻³
turns/crossing), so the compact row (p, e, w, t) never settles even where the key
does, and closure is (config, phase, word)-dependent (26/288 groups close at one
word and walk at another). Word-invariance holds where all words walk (ratio median
1.00, p90 2.25, 219/244 within 2×) — the leak is the fit's angle conditioning, not
the position word. **The μ ≈ 1.28 doll with a doll-based word is benign-to-helpful:**
432/432 complete; 84% of 377 paired chains within 2× of unity, μ smaller on 71%
(medians 5.7×10⁻⁴ vs 8.4×10⁻⁴); wherever unity walks the μ doll walks the same
walk. **Depth 256: bounded, not compounding — but never recovering** (strong
walkers d₆₄ ≥ 10⁻³ saturate, d₂₅₆/d₆₄ median 1.03 — the geometry bound, per the run
above); the walk is irreversible (the dropped residual). k is stable (median 1 Q48
ulp/crossing); cost 20.4 µs per crossing (fit 13.0 µs; 20.5 µs re-measured by the
dynamics run); controls: `reconstruct()` exact left inverse 864/864, kick control
852/864 ≥ 2.4×10⁵ ulps, rerun bit-identical, `regen.sh` byte-identical. Real
crossings also re-quantize to the belt Spec's column widths — these numbers are a
lower bound. **Consequence: anchor w and t as one observed-angle column (or carry
the 4×65-bit residual on scars) before demote-at-commit — now with the do-nothing
option priced beside it (linear ulp-scale leak, neutral response, safe at any
flyable horizon; the w column is either frozen or destroyed in one crossing).**

**Prior best (the leak's discovery and its instrument).** 20261014-1010-taleb-292a
chained the composed crossing on shipped pub APIs at the (accidental) periapsis phase,
unity dolls: 128/128 completed chains never repeated a key, the walk was in the w column,
and the residual's exactness was confirmed as the mechanism (`reconstruct()` an exact
left inverse; the leak appears exactly when the residual is dropped); its phase and doll
dimensions were broken and were first measured by its checker (true-phase structure, a
bounded 2-cycle, the benign μ doll) — both now superseded by b9c8's corrected full grid.
Before that, the shipped exit path (`Rebinding::from_state` / `ending_at` behind
`resolve_handoff`) was probed on shipped `crates/space` integers (20261013-2130-
redteam-8398): the pure-transit round trip moved the `OrbitKey` on **112/112** probes
(circles leave the exact class: decode rounding exits `inverse::circular`), the fit map
is not a fixed point, step ~1 Q48 k-ulp at fine words, 2⁻²⁸–2⁻²⁵ relative at plane-scale
words. Corroboration from the shipped plane: the exact-key memo hit rate is 0.0 on 3,108
distinct rebinds (152f, kick-jet) — re-fits never land on the same key. What survives
untouched: within-order identity (`identity.rs` / `metal_identity.rs`) and the Lorentz
half of handoffs (exact, fixed point after one trip) — the leak is purely the
representation fit.

**Domain.** Idealized boundary plus the composed column cycle with the shipped unit
(b9c8: true phases 1/8–7/8, μ ≈ 1.28 with a doll-based word, depth 256, all 864 chains
at one initial orientation and sense (w₀ = 1/8 turn, prograde); dynamics run: depths to
8192, w₀ twin +1 ulp, 3 retrograde arms (zero refusals), one observation phase per chain
re-derived from each key's own period, no belt-Spec column re-quantization (rates are
lower bounds), no contact/encounter effect; other (w₀, cw) refuse at entry on ~1% of
arms per b9c8's check2 — not seen in the 3 retro arms; even phases (1/4, 1/2, 3/4
turns) refuse mid-walk on 5/648 chains (fit:Range at steps 87–175; cartesian:Range at
161), record drift 3.98 radii there; μ = 1.9, 1.0001, 1.6 benign with zero refusals);
the (7, 0.995) separatrix key refuses compile and ten fine-word e ≥ 0.99 encodes
refuse (`Range`) — 8398's record.

## Refuted

- **"Depth-256 boundedness (d₂₅₆/d₆₄ ≈ 1) is a dynamical saturation of the walk"**
  (b9c8's headline as the page carried it): the measured quantity is the position
  sample, bounded by geometry — its radius is invariant below the 2⁻²⁰ floor on
  every chain, so the sample cannot leave the diameter; the columns themselves
  compound linearly (exact −13/−1-ulp translations on eccentric arms, one-signed
  decelerating ratchet on circles; 20261018-1237-dynamics-9dbb).
- **"The dropped residual's size powers the leak"** (the natural reading of 292a's
  mechanism, and the dynamics run's own pre-registered P6): refuted across
  families — e = 10⁻³ arms walk −1 ulp/crossing at residuals 1.2×10⁷ and 7.0×10⁸
  quanta alike, while e = 0.5 at 1.1×10⁶ walks −13; the rate is a per-(p,e,φ)
  constant of the fit's quantization geometry (20261018-1237-dynamics-9dbb).
- **"Retrograde (cw=true) arms refuse at entry ~1–2% of the time"** (the page's
  domain note, extrapolated from w₀/cw refusals): 0/3 retro arms refused; one
  joined its prograde twin's exact −13 rate (20261018-1237-dynamics-9dbb; 3 arms
  only — the class is open at other configs).
- "The order boundary is representation-transparent / both orders give identical bits as
  built": 0/112 keys survive a pure transit (20261013-2130-redteam-8398); confirmed at
  column level (20261014-1010-taleb-292a, b9c8).
- "The crossing never finds a fixed point": true only at the periapsis phase
  (taleb-292a's accidental domain); at true phases 76/864 chains find key-level fixed
  points (b9c8) — and one corner (p = 16·2³⁰, e = 0.99) finds column-exact fixed
  points absorbing at crossings 1–19, k and w both constant (dynamics run).
- "Circular orbits keep their exact-circular key through a transit": decode rounding
  leaves the circular class (8398); and the e = 0 crossing is an exact orientation
  lottery — radius preserved below 2⁻²⁰, stored w re-lotteried up to 0.13 turns per
  crossing at every phase (b9c8); distinct w at every one of 4096 crossings, |Δw|
  max 0.998 turns (dynamics run).
- "A coarser doll word bounds/drowns the crossing walk" (taleb-292a's own P4): the drift
  is word-invariant where all words walk (median 1.00, b9c8) — the leak is angle
  conditioning, not the position word.
- "The μ doll arm is unmeasured, not safe / the real per-crossing error is worse, not
  better" (taleb-292a, on its 2⁴⁰ doll): instrument artifact; with μ ≈ 1.28 and a
  doll-based word 432/432 chains complete and 71% drift smaller than unity (b9c8).
- "Snap the member state onto the key grid at entry so the exit fit is idempotent":
  closure exists but is (config, phase, word)-dependent and leaves w wobbling on 51/76
  fixed points (b9c8) — snap cannot close the seam.

## Open directions

1. **Specify the boundary and freeze r5** (never frozen; B8's engine tests compare the two
   orders but never across a hand-out — `identity.rs` scenes are born in-frame): either carry
   the tube through the battle doll (members keep their tube, Cartesian states are
   transient for the contact resolver, kicks hit (E, L) on the one grid), or — measured
   load-bearing (taleb-292a, b9c8) — **anchor w and t as one observed-angle column** (the
   observed angle is well-defined even for circles, where the periapsis angle is a
   lottery), or carry the residual on scars. **The do-nothing price is now measured**
   (dynamics run): k compounds linearly at 1–13 ulps/crossing (eccentric) or ~3–10k
   decelerating (circles), neutral perturbation response, no cycles on walkers — the
   residual carry buys exactness, not game-visible accuracy; the w-anchor buys the
   outbound classes' orientation column, destroyed in one crossing as built. Negative
   control ready: the shipped `from_state` must fail by ≥ 1 key ulp.
2. **The worst-doll question at other μ scales and through the wired `resolve_handoff`.**
   μ ∈ [1,2) is covered at the composed level; the refusal budget's phase-class
   structure is settled (odd/even); the dynamics run adds retro arms (0/3 refused).
   What remains: the wired end-to-end scene with doll-unit conversions, and the
   circle ratchet's deceleration law (k-vs-rate one rung would close it).
3. ~~**Is the order assignment itself canonical?**~~ Answered (taleb-292a): the seam is a
   pure function of the integer state (rerun bit-identical); no schedule dependence —
   the hazard is information loss (the dropped residual), not nondeterminism. Extended:
   the map is neutral to 1-ulp w perturbations over 8192 crossings (dynamics run).
4. **Price the w lottery at the encounter tier** (taleb-292a, b9c8): does a 10⁻⁷–10⁻¹
   turn re-orientation per crossing move contact/conjunction outcomes for a near-circular
   belt? Needs the wired tier; off-plan until then. The dynamics run sharpens it: at
   outbound phases the re-orientation is O(1) turns EVERY crossing, not 10⁻⁷–10⁻¹.
One contradiction settled by check2.md: the mid-walk refusals check.md saw at depth 256
reproduce on the corrected instrument at even phases (1/4, 1/2, 3/4 turns; 5/648 chains past step 64,
steps 87–175) and are absent on the odd eighths b9c8 swept — a phase-class effect, not a
probe or word-handling difference. Otherwise none: 152f read its 0.0 memo hit rate as
a cost observation; this page reads the same number as the identity mechanism —
compositional, not in conflict.

## Contradictions

None open. b9c8's "bounded, not compounding" and the dynamics run's "the columns
compound linearly" measure different quantities (position sample vs stored columns);
recorded so no run reads one as the other.

## Runs
- 20261013-2130-redteam-8398 (gold): order boundary leaks: 0/112 keys survive a
- 20261014-1010-taleb-292a (silver): the crossing's walk measured at column level:
- 20261014-1137-second-20261014-1010-taleb-292a-b9c8 (awaiting grade): corrected
- 20261018-1237-dynamics-9dbb (this run, awaiting grade): the walk class named —
  translations and ratchets compound linearly in k, fixed-point corner, neutral
  response; the record's "bounded" was the position sample's geometry
